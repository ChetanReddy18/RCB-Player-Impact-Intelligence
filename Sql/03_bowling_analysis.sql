USE rcb_ipl_analytics;

-- 1. Top 10 wicket takers
WITH ranked_bowlers AS (
    SELECT
        bowler,
        matches,
        wickets,
        economy,
        bowling_average,
        bowling_strike_rate,
        DENSE_RANK() OVER (
            ORDER BY wickets DESC
        ) AS ranking
    FROM rcb_bowling_master
)
SELECT
    ranking,
    bowler,
    matches,
    wickets,
    economy,
    bowling_average,
    bowling_strike_rate
FROM ranked_bowlers
WHERE ranking <= 10
ORDER BY ranking;

-- 2. Top 10 economy performers
SELECT
    bowler,
    matches,
    balls,
    runs_conceded,
    wickets,
    economy
FROM rcb_bowling_master
WHERE balls >= 500
ORDER BY economy ASC
LIMIT 10;

-- 3. Top dot-ball bowlers
SELECT
    bowler,
    matches,
    balls,
    dot_balls,
    wickets,
    ROUND(dot_balls / balls * 100, 2) AS dot_ball_percentage
FROM rcb_bowling_master
WHERE balls >= 500
ORDER BY dot_balls DESC
LIMIT 10;

-- 4. Top death-over wicket takers
SELECT
    bowler,
    matches,
    wickets,
    death_wickets,
    economy
FROM rcb_bowling_master
ORDER BY death_wickets DESC
LIMIT 10;

-- 5. Top bowling performer in each season
WITH ranked_seasons AS (
    SELECT
        season,
        bowler,
        wickets,
        economy,
        dot_balls,
        death_wickets,
        ROW_NUMBER() OVER (
            PARTITION BY season
            ORDER BY wickets DESC, economy ASC
        ) AS ranking
    FROM rcb_bowling_season_stage
)
SELECT
    season,
    bowler,
    wickets,
    economy,
    dot_balls,
    death_wickets
FROM ranked_seasons
WHERE ranking = 1
ORDER BY season;

-- 6. Bowling career summary
SELECT
    COUNT(DISTINCT bowler) AS total_bowlers,
    SUM(wickets) AS total_wickets,
    SUM(dot_balls) AS total_dot_balls,
    SUM(runs_conceded) AS total_runs_conceded,
    ROUND(AVG(economy), 2) AS average_economy
FROM rcb_bowling_master;