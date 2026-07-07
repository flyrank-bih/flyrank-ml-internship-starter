from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np
import pandas as pd

from ml_utils import PROCESSED_DIR, normalize, percentile_rank, write_json


FEATURE_PATH = PROCESSED_DIR / "refresh_feature_vector.csv"
OUTPUT_PATH = PROCESSED_DIR / "baseline_refresh_queue.csv"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build deterministic refresh baseline score.")
    parser.add_argument("--input", default=str(FEATURE_PATH))
    parser.add_argument("--output", default=str(OUTPUT_PATH))
    return parser.parse_args()


def reason_codes(row: pd.Series) -> list[str]:
    reasons: list[str] = []
    if row["days_since_last_update"] >= 180 and row["impressions_90d"] >= 500:
        reasons.append("stale_visible_page")
    if row["trend_direction"].lower() == "down" and row["impressions_90d"] >= 100:
        reasons.append("declining_with_demand")
    if row["word_count"] > 0 and row["word_count"] < 1200 and row["impressions_90d"] >= 250:
        reasons.append("thin_visible_page")
    if row["avg_position"] > 0 and row["avg_position"] <= 10 and row["content_age_days"] >= 180:
        reasons.append("page_one_decay_risk")
    if row["impressions_90d"] >= 500 and 0 < row["avg_position"] <= 20 and row["ctr"] < 0.5:
        reasons.append("low_ctr_visible_page")
    if row["sessions_90d"] >= 30 and (
        (row["engagement_rate"] > 0 and row["engagement_rate"] < 30)
        or (row["scroll_rate"] > 0 and row["scroll_rate"] < 30)
    ):
        reasons.append("low_engagement_visible_page")
    if not reasons:
        reasons.append("general_refresh_review")
    return reasons


def suggested_action(row: pd.Series) -> str:
    reasons = set(str(row["reason_codes"]).split("|"))
    if "thin_visible_page" in reasons:
        return "expand_and_refresh"
    if "low_ctr_visible_page" in reasons:
        return "refresh_and_review_ctr"
    if "stale_visible_page" in reasons or "declining_with_demand" in reasons:
        return "refresh"
    return "monitor"


def main() -> None:
    args = parse_args()
    df = pd.read_csv(args.input)
    if df.empty:
        raise ValueError("Feature vector is empty")

    df["visibility_score"] = percentile_rank(np.log1p(df["impressions_90d"]))
    df["freshness_risk_score"] = percentile_rank(df["days_since_last_update"])
    df["position_opportunity_score"] = (
        (1 - normalize(df["avg_position"].clip(lower=1, upper=50)))
        * df["visibility_score"]
        * (df["avg_position"] > 0).astype(int)
    )
    df["depth_gap_score"] = (1 - percentile_rank(df["word_count"])) * df["visibility_score"]

    df["baseline_refresh_score"] = (
        0.40 * df["visibility_score"]
        + 0.30 * df["freshness_risk_score"]
        + 0.25 * df["position_opportunity_score"]
        + 0.05 * df["depth_gap_score"]
    ).clip(0, 1)

    df["reason_codes"] = df.apply(lambda row: "|".join(reason_codes(row)), axis=1)
    df["suggested_action_baseline"] = df.apply(suggested_action, axis=1)
    df["baseline_rank"] = df["baseline_refresh_score"].rank(method="first", ascending=False).astype(int)

    output_columns = [
        "content_id",
        "client_id",
        "baseline_rank",
        "baseline_refresh_score",
        "visibility_score",
        "freshness_risk_score",
        "position_opportunity_score",
        "depth_gap_score",
        "reason_codes",
        "suggested_action_baseline",
        "is_declining_label",
        "impressions_90d",
        "clicks_90d",
        "sessions_90d",
        "avg_position",
        "ctr",
        "engagement_rate",
        "scroll_rate",
        "content_age_days",
        "days_since_last_update",
        "word_count",
        "trend_direction",
    ]

    out = df[output_columns].sort_values("baseline_rank")
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    out.to_csv(output_path, index=False)

    write_json(PROCESSED_DIR / "baseline_metadata.json", {
        "rows": int(len(out)),
        "top_score": float(out["baseline_refresh_score"].max()),
        "median_score": float(out["baseline_refresh_score"].median()),
        "declining_rate_top_50": float(out.head(50)["is_declining_label"].mean()) if len(out) else 0.0,
        "score_formula": {
            "visibility_score": 0.40,
            "freshness_risk_score": 0.30,
            "position_opportunity_score": 0.25,
            "depth_gap_score": 0.05,
        },
    })

    print(f"Wrote baseline queue: {output_path}")
    print(f"Top-50 declining rate (full data, not the evaluated holdout Precision@50): {out.head(50)['is_declining_label'].mean():.3f}")


if __name__ == "__main__":
    main()
