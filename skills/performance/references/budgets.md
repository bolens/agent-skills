## Starting performance budget

Budgets must reflect the product's target devices, networks, page types, and user journeys. The values below are initial guardrails for a typical content or commerce page, not universal pass/fail criteria. Preserve an existing project budget when one is already defined.

| Resource | Budget | Rationale |
|----------|--------|-----------|
| Total page weight | < 1.5 MB | Bounds transfer time and data cost on constrained target networks; calibrate with representative pages |
| JavaScript (compressed) | < 300 KB | Protect parse and execution cost |
| CSS (compressed) | < 100 KB | Limit render-blocking work |
| Images (above-fold) | < 500 KB | Protect likely LCP resources |
| Fonts | < 100 KB | Limit critical font transfer |
| Third-party | < 200 KB | Bound code outside product control |
