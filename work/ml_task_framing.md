# ML Task Framing

## Lane  
Lane 4: CTR / Engagement Opportunity Scoring

## 1. ML Task Type  
**Scoring / Ranking**

This is a ranking problem, not a classification problem. The goal is not to label pages as "good" or "bad" but to produce a continuous opportunity score that ranks pages from most urgent to least urgent for content review.

## 2. Target / Proxy Label

**Target (ideal, unmeasurable):**  
Whether a page is genuinely under-capturing clicks relative to its true potential given its position and content quality.

**Proxy (measurable):**  
`ctr_gap` : the difference between a page's actual CTR and the average CTR for pages in the same position tier.

A strongly negative ‘ctr_gap’ suggests the page is getting fewer clicks when compared to pages of the same position.

**Proxy limitations:**  
- Low CTR may reflect SERP feature competition, not title quality  
- Low CTR may reflect keyword intent mismatch  
- The proxy assumes position tier is the right grouping variable

## 3. Success Metric  
**Primary: Precision@K (K = 20, K = 50)**

Of the top-K pages ranked by opportunity score, what fraction carry the `is_declining_label = 1` flag? A higher fraction is better.

**Baseline to beat:**  
A random ranking achieves Precision@K equal to the base rate of declining pages in the dataset. The scoring model must exceed this to justify its use.

## 4. Why this is an ML problem and not just a rule:

A fixed rule (like flagging all pages with CTR < 2%) fails because:

1. CTR varies naturally by position. Position 1 pages always have higher CTR than position 8 pages. A flat threshold treats them identically without factoring in positions.

2. A rule produces a binary flag, not a ranked list for prioritization. Content teams need to see which pages to prioritize, not just a binary label.

3. A rule cannot weight by impression volume like an ML model. A page losing clicks at 50,000 impressions is more urgent than the same CTR gap at 500 impressions.

The scoring approach handles all three by computing position-adjusted gaps and combining multiple signals into one weighted score, which is more efficient than fixed hand rules.

## 5. Output and Action

**Output:**  
A ranked list of pages ordered by opportunity score, with reason codes explaining the flag.

**Action a human takes:**  
A content writer reviews the top-ranked pages and rewrites title tags and meta descriptions to better match searchers’ intentions. Pages flagged with `weak_engagement` are sent to a  
content editor to improve on-page structure.
