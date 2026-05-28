-- Customer Issue Rate by Region
-- Conditional aggregation counts orders where rating <= 3 AND issue_reported = 1.
-- Result: NYC 6.59% | SF 6.40% | Chicago 2.29%
-- Key insight: NYC and SF show nearly 3x the issue rate of Chicago.

SELECT 
  region,
  COUNT(*) AS total_orders,
  SUM(CASE WHEN customer_order_rating <= 3 AND issue_reported = 1 THEN 1 ELSE 0 END) AS low_rating_issues,
  ROUND(100.0 * SUM(CASE WHEN customer_order_rating <= 3 
    AND issue_reported = 1 THEN 1 ELSE 0 END) / COUNT(*), 2) AS issue_rate_percent
FROM instacart.data
GROUP BY region
ORDER BY issue_rate_percent DESC;
