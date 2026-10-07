USE rcb_ipl_analytics;

-- 1. Venue performance
SELECT
    venue,
    matches,
    wins,
    losses,
    no_results,
    win_percentage
FROM rcb_venue_master
ORDER BY matches DESC;

-- 2. Venues with highest win percentage
SELECT
    venue,
    matches,
    wins,
    losses,
    win_percentage
FROM rcb_venue_master
WHERE matches >= 3
ORDER BY win_percentage DESC;

-- 3. Venues with most RCB matches
SELECT
    venue,
    matches,
    wins,
    losses,
    win_percentage
FROM rcb_venue_master
ORDER BY matches DESC
LIMIT 10;

-- 4. Venue win/loss analysis
SELECT
    venue,
    matches,
    wins,
    losses,
    ROUND(wins / matches * 100, 2) AS win_percentage,
    ROUND(losses / matches * 100, 2) AS loss_percentage
FROM rcb_venue_master
WHERE matches > 0
ORDER BY matches DESC;

-- 5. Venue summary
SELECT
    COUNT(*) AS total_venue_records,
    SUM(matches) AS total_matches,
    SUM(wins) AS total_wins,
    SUM(losses) AS total_losses
FROM rcb_venue_master;