USE rcb_ipl_analytics;

-- 1. Top 10 run scorers
WITH ranked_batters AS (
    SELECT
        batter,
        matches,
        runs,
        strike_rate,
        average,
        ROW_NUMBER() OVER (
            ORDER BY runs DESC
        ) AS ranking
    FROM rcb_batting_master
)
SELECT
    ranking,
    batter,
    matches,
    runs,
    strike_rate,
    average
FROM ranked_batters
WHERE ranking <= 10
ORDER BY ranking;

-- 2. Top 10 strike-rate performers
SELECT
    batter,
    matches,
    runs,
    balls,
    strike_rate
FROM rcb_batting_master
WHERE balls >= 100
ORDER BY strike_rate DESC
LIMIT 10;

-- 3. Top 10 batting averages
SELECT
    batter,
    matches,
    runs,
    innings,
    average
FROM rcb_batting_master
WHERE innings >= 20
ORDER BY average DESC
LIMIT 10;

-- 4. Top boundary hitters
SELECT
    batter,
    runs,
    fours,
    sixes,
    (fours + sixes) AS total_boundaries
FROM rcb_batting_master
ORDER BY total_boundaries DESC
LIMIT 10;

-- 5. Top player-seasons by runs
WITH ranked_seasons AS (
    SELECT
        season,
        batter,
        runs,
        strike_rate,
        average,
        DENSE_RANK() OVER (
            PARTITION BY season
            ORDER BY runs DESC
        ) AS ranking
    FROM rcb_batting_season_master
)
SELECT
    season,
    batter,
    runs,
    strike_rate,
    average
FROM ranked_seasons
WHERE ranking = 1
ORDER BY season;

-- 6. Batting career summary
SELECT
    COUNT(DISTINCT batter) AS total_batters,
    SUM(runs) AS total_runs,
    SUM(fours) AS total_fours,
    SUM(sixes) AS total_sixes,
    ROUND(AVG(strike_rate), 2) AS average_strike_rate
FROM rcb_batting_master;