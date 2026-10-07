USE rcb_ipl_analytics;

-- 1. Player career summary
SELECT
    player,
    matches,
    runs,
    wickets,
    batting_average,
    strike_rate,
    economy,
    impact_score
FROM rcb_player_master
ORDER BY impact_score DESC;

-- 2. Top 10 players by impact
SELECT
    player,
    matches,
    runs,
    wickets,
    impact_score
FROM rcb_player_master
ORDER BY impact_score DESC
LIMIT 10;

-- 3. Top 10 players by matches
SELECT
    player,
    matches,
    runs,
    wickets,
    impact_score
FROM rcb_player_master
ORDER BY matches DESC
LIMIT 10;

-- 4. Players with strong batting performance
SELECT
    player,
    matches,
    runs,
    batting_average,
    strike_rate,
    impact_score
FROM rcb_player_master
WHERE runs > 0
ORDER BY runs DESC
LIMIT 10;

-- 5. Players with strong bowling performance
SELECT
    player,
    matches,
    wickets,
    economy,
    impact_score
FROM rcb_player_master
WHERE wickets > 0
ORDER BY wickets DESC
LIMIT 10;

-- 6. Player career averages
SELECT
    ROUND(AVG(matches), 2) AS average_matches,
    ROUND(AVG(runs), 2) AS average_runs,
    ROUND(AVG(wickets), 2) AS average_wickets,
    ROUND(AVG(impact_score), 2) AS average_impact_score
FROM rcb_player_master;