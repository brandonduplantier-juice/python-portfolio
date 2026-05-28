-- Revenue by Persona
-- 210 whales (9% of paying users) generate $4M — 52% of total revenue.
-- Dolphins generate $2.9M across 615 users. Minnows $733K across 701 users.
-- Key insight: retention efforts should prioritize whale and dolphin tiers.

WITH user_personas AS (
  SELECT 
    u.udid,
    SUM(i.rev) AS total_spent,
    CASE
      WHEN SUM(i.rev) IS NULL THEN 'free player'
      WHEN SUM(i.rev) < 2000 THEN 'minnow'
      WHEN SUM(i.rev) >= 2000 AND SUM(i.rev) < 10000 THEN 'dolphin'
      WHEN SUM(i.rev) >= 10000 THEN 'whale'
    END AS persona
  FROM game_jet.users u
  LEFT JOIN game_jet.iaps i ON u.udid = i.udid
  GROUP BY u.udid
)
SELECT 
  persona,
  COUNT(*) AS user_count,
  ROUND(SUM(total_spent), 2) AS total_revenue,
  ROUND(AVG(total_spent), 2) AS avg_spend_per_user
FROM user_personas
WHERE persona != 'free player'
GROUP BY persona
ORDER BY total_revenue DESC;
