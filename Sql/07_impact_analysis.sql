USE rcb_ipl_analytics;

-- 1. Top players by overall impact
SELECT
    player,
    matches,
    runs,
    wickets,
    impact_score
FROM rcb_player_master
ORDER BY impact_score DESC
LIMIT 10;


-- 2. Player impact by season
WITH ranked_players AS (
    SELECT
        season,
        player,
        impact_score,
        ROW_NUMBER() OVER (
            PARTITION BY season
            ORDER BY impact_score DESC
        ) AS ranking
    FROM rcb_player_season_master
)
SELECT
    season,
    player,
    impact_score
FROM ranked_players
WHERE ranking = 1
ORDER BY season;


-- 3. Players performing above their career average
WITH career_avg AS (
    SELECT
        player,
        AVG(impact_score) AS career_average
    FROM rcb_player_season_master
    GROUP BY player
)
SELECT
    s.player,
    s.season,
    s.impact_score,
    ROUND(c.career_average, 2) AS career_average
FROM rcb_player_season_master s
JOIN career_avg c
    ON s.player = c.player
WHERE s.impact_score > c.career_average
ORDER BY s.impact_score DESC;


-- 4. Batting impact
SELECT
    player,
    runs,
    strike_rate,
    batting_impact
FROM rcb_player_master
ORDER BY batting_impact DESC
LIMIT 10;


-- 5. Bowling impact
SELECT
    player,
    wickets,
    economy,
    bowling_impact
FROM rcb_player_master
ORDER BY bowling_impact DESC
LIMIT 10;


-- 6. Overall impact summary
SELECT
    COUNT(*) AS total_players,
    ROUND(AVG(impact_score), 2) AS average_impact,
    MAX(impact_score) AS highest_impact,
    MIN(impact_score) AS lowest_impact
FROM rcb_player_master;