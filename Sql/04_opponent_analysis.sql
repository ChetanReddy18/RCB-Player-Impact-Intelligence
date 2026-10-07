USE rcb_ipl_analytics;

-- 1. Overall opponent head-to-head
SELECT
    opponent,
    matches,
    wins,
    losses,
    no_results,
    win_percentage
FROM rcb_opponent_master
ORDER BY matches DESC;

-- 2. Opponent performance ranking
WITH ranked_opponents AS (
    SELECT
        opponent,
        matches,
        wins,
        losses,
        win_percentage,
        DENSE_RANK() OVER (
            ORDER BY win_percentage DESC
        ) AS ranking
    FROM rcb_opponent_master
)
SELECT
    ranking,
    opponent,
    matches,
    wins,
    losses,
    win_percentage
FROM ranked_opponents
ORDER BY ranking;

-- 3. Most matches against each opponent
SELECT
    opponent,
    matches,
    wins,
    losses,
    win_percentage
FROM rcb_opponent_master
ORDER BY matches DESC
LIMIT 10;

-- 4. Opponents with highest number of wins
SELECT
    opponent,
    matches,
    wins,
    losses,
    win_percentage
FROM rcb_opponent_master
ORDER BY wins DESC
LIMIT 10;

-- 5. Opponent summary
SELECT
    COUNT(*) AS total_opponents,
    SUM(matches) AS total_matches,
    SUM(wins) AS total_wins,
    SUM(losses) AS total_losses,
    ROUND(AVG(win_percentage), 2) AS average_opponent_win_percentage
FROM rcb_opponent_master;