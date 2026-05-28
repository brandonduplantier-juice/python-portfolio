-- Environmental Impact by Region and Device Type
-- Window functions calculate each device type's % contribution to regional totals.
-- Demonstrates: JOIN, GROUP BY, ROUND, AVG, and nested SUM OVER PARTITION BY.
-- Result: 6 rows across Asia, Europe, North America by Desktop/Laptop

SELECT
  i.region,
  d.device_type,
  COUNT(*) AS total_devices,
  ROUND(AVG(i.energy_savings_yr), 2) AS avg_energy_savings_kwh,
  ROUND(AVG(i.co2_saved_kg_yr) / 1000.0, 4) AS avg_co2_saved_tons,
  ROUND(SUM(i.energy_savings_yr) * 100.0 / 
    SUM(SUM(i.energy_savings_yr)) OVER (PARTITION BY i.region), 2) AS pct_region_energy_savings,
  ROUND(SUM(i.co2_saved_kg_yr) * 100.0 / 
    SUM(SUM(i.co2_saved_kg_yr)) OVER (PARTITION BY i.region), 2) AS pct_region_co2_saved
FROM intel.device_data d
JOIN intel.impact_data i ON d.device_id = i.device_id
GROUP BY i.region, d.device_type
ORDER BY i.region, d.device_type;
