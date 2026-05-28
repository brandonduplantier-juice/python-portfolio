-- Time-to-First-Purchase Conversion Window
-- Chained CTEs + date arithmetic to bucket days between install and first purchase.
-- Result: 724 same-day | 471 within 1-3 days | 143 within 8-30 days
-- Key insight: 83% of converting users purchase within 3 days of install.

WITH dated_purchases AS (
  SELECT 
    u.udid,
    i.date::date - u.install_date::date AS days_until_purchase
  FROM game_jet.users u
  JOIN game_jet.iaps i ON u.udid = i.udid
),
first_purchase AS (
  SELECT 
    udid,
    MIN(days_until_purchase) AS days_until_first_purchase
  FROM dated_purchases
  GROUP BY udid
)
SELECT 
  CASE
    WHEN days_until_first_purchase = 0 THEN 'Same day'
    WHEN days_until_first_purchase <= 3 THEN '1-3 days'
    WHEN days_until_first_purchase <= 7 THEN '4-7 days'
    WHEN days_until_first_purchase <= 30 THEN '8-30 days'
    ELSE '30+ days'
  END AS conversion_window,
  COUNT(*) AS user_count
FROM first_purchase
GROUP BY conversion_window
ORDER BY user_count DESC;
