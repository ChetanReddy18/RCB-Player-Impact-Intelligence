USE rcb_ipl_analytics;

-- 1. Season performance
SELECT
    season,
    matches,
    wins,
    losses,
    no_results,
    win_percentage,
    total_runs,
    total_wickets
FROM rcb_season_summary
ORDER BY season;

-- 2. Best seasons by wins
SELECT
    season,
    matches,
    wins,
    losses,
    no_results,
    win_percentage
FROM rcb_season_summary
ORDER BY wins DESC;

-- 3. Highest scoring seasons
SELECT
    season,
    matches,
    total_runs,
    ROUND(total_runs / matches, 2) AS runs_per_match
FROM rcb_season_summary
ORDER BY total_runs DESC;

-- 4. Highest wicket seasons
SELECT
    season,
    matches,
    total_wickets,
    ROUND(total_wickets / matches, 2) AS wickets_per_match
FROM rcb_season_summary
ORDER BY total_wickets DESC;

-- 5. Year-over-year win percentage
SELECT
    season,
    win_percentage,
    LAG(win_percentage) OVER (
        ORDER BY
            CASE season
                WHEN '2007/08' THEN 1
                WHEN '2009' THEN 2
                WHEN '2009/10' THEN 3
                WHEN '2011' THEN 4
                WHEN '2012' THEN 5
                WHEN '2013' THEN 6
                WHEN '2014' THEN 7
                WHEN '2015' THEN 8
                WHEN '2016' THEN 9
                WHEN '2017' THEN 10
                WHEN '2018' THEN 11
                WHEN '2019' THEN 12
                WHEN '2020/21' THEN 13
                WHEN '2021' THEN 14
                WHEN '2022' THEN 15
                WHEN '2023' THEN 16
                WHEN '2024' THEN 17
                WHEN '2025' THEN 18
                WHEN '2026' THEN 19
            END
    ) AS previous_season_win_percentage
FROM rcb_season_summary;

-- 6. Overall season summary
SELECT
    SUM(matches) AS total_matches,
    SUM(wins) AS total_wins,
    SUM(losses) AS total_losses,
    SUM(no_results) AS total_no_results,
    SUM(total_runs) AS total_runs,
    SUM(total_wickets) AS total_wickets
FROM rcb_season_summary;