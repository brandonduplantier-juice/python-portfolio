-- User Persona Segmentation
-- Classifies players into free, minnow, dolphin, and whale tiers
-- based on total in-app purchase revenue using a LEFT JOIN + CTE + CASE pattern.
-- Result: 21,050 free players | 701 minnows | 615 dolphins | 210 whales

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
  COUNT(*) AS user_count
FROM user_personas
GROUP BY persona
ORDER BY user_count DESC;
