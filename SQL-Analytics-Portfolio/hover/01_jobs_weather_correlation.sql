-- Roofing Jobs vs Weekly Weather Events by State
-- Joins job and weather data on state + week using DATE_TRUNC for time bucketing.
-- Subquery used as the join source before aggregation.
-- Result: 320 state/week rows showing job volume alongside weather event counts.

SELECT
  job_location_region_code AS state,
  job_ts,
  COUNT(*) AS total_jobs,
  SUM(n_weather_events) AS total_weather_events
FROM (
  SELECT
    j.job_deliverable,
    j.job_location_region_code,
    DATE_TRUNC('week', j.job_first_upload_complete_datetime) AS job_ts,
    w.n_weather_events
  FROM hover.jobs j
  INNER JOIN hover.weekly_weather_events w
    ON j.job_location_region_code = w.state
    AND DATE_TRUNC('week', j.job_first_upload_complete_datetime) = w.weather_ts
) AS sub
GROUP BY state, job_ts
ORDER BY state;
