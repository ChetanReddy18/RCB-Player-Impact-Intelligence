# 🏏 RCB Player Impact Intelligence

### IPL Analytics Dashboard | 2008–2026

An end-to-end cricket analytics project focused on analyzing Royal Challengers Bengaluru (RCB) performance across 19 IPL seasons using ball-by-ball match data.

The project transforms raw IPL JSON data into structured analytical datasets using **Python**, performs advanced analysis using **MySQL and SQL**, and presents the results through an interactive **Power BI dashboard**.

---

## 📌 Table of Contents

- [Project Overview](#-project-overview)
- [Objectives](#-objectives)
- [Key Questions](#-key-questions)
- [Dataset](#-dataset)
- [Project Statistics](#-project-statistics)
- [Technology Stack](#-technology-stack)
- [Project Architecture](#-project-architecture)
- [Project Workflow](#-project-workflow)
- [Python Analysis](#-python-analysis)
- [SQL Analysis](#-sql-analysis)
- [Power BI Dashboard](#-power-bi-dashboard)
- [Dashboard Pages](#-dashboard-pages)
- [Key Metrics](#-key-metrics)
- [Player Impact Score](#-player-impact-score)
- [Data Model](#-data-model)
- [Project Structure](#-project-structure)
- [Important Data Limitations](#-important-data-limitations)
- [Data Validation](#-data-validation)
- [Future Enhancements](#-future-enhancements)
- [How to Run the Project](#-how-to-run-the-project)
- [Skills Demonstrated](#-skills-demonstrated)
- [Conclusion](#-conclusion)
- [Author](#-author)

---

# 📊 Project Overview

**RCB Player Impact Intelligence** is an IPL analytics project designed to analyze the historical performance of Royal Challengers Bengaluru across multiple seasons.

The project uses detailed ball-by-ball IPL data to analyze:

- Team performance
- Batting performance
- Bowling performance
- Player contribution
- Player impact
- Opponent performance
- Venue performance
- Season-wise trends
- Player-season performance

The project follows a complete data analytics pipeline:

```text
Raw Data
   ↓
Python Data Extraction
   ↓
Data Cleaning
   ↓
Feature Engineering
   ↓
MySQL Database
   ↓
SQL Analysis
   ↓
Power BI Data Model
   ↓
Interactive Dashboard
```

---

# 🎯 Objectives

1. Analyze RCB's historical IPL performance.
2. Identify important batting and bowling contributors.
3. Analyze player performance across different seasons.
4. Measure player impact using a custom analytical metric.
5. Analyze RCB's performance against different opponents.
6. Analyze performance across different venues.
7. Identify season-wise performance trends.
8. Build an interactive Power BI dashboard.
9. Demonstrate an end-to-end data analytics workflow using Python, SQL and Power BI.

---

# ❓ Key Questions

### Team Performance

- How has RCB performed across different seasons?
- What is RCB's season-wise win percentage?
- Which seasons had the highest number of wins?
- How many runs did RCB score in each season?
- How many wickets did RCB take in each season?

### Batting

- Who are RCB's highest run scorers?
- Which players have the highest strike rates?
- Which players have strong batting averages?
- Who scored the most boundaries?
- Which players had the strongest individual seasons?

### Bowling

- Who are RCB's highest wicket takers?
- Which bowlers have the best economy rates?
- Who bowled the most dot balls?
- Which bowlers contributed most in death overs?
- Who were the leading bowlers in each season?

### Players

- Which players have the highest impact scores?
- Which players played the most matches?
- Which players contributed strongly with batting?
- Which players contributed strongly with bowling?

### Opponents

- How has RCB performed against different opponents?
- Which opponents has RCB played most often?
- What are the win and loss records against opponents?

### Venues

- At which venues has RCB played most matches?
- How does RCB's performance vary by venue?
- What are the win and loss percentages at different venues?

---

# 📂 Dataset

The project uses IPL ball-by-ball JSON data from **Cricsheet**.

The raw dataset contains detailed match and delivery-level information including:

- Match ID
- Season
- Teams
- Opponents
- Venue
- City
- Innings
- Over
- Delivery
- Batter
- Bowler
- Runs
- Extras
- Wickets
- Player dismissed
- Match winner

### Dataset Coverage

```text
Seasons: 2008–2026
RCB Matches: 286
RCB Batting Deliveries: 33,572
RCB Bowling Deliveries: 33,827
```

---

# 📈 Project Statistics

| Dataset | Records |
|---|---:|
| RCB Player Master | 180 |
| RCB Batting Master | 163 |
| RCB Bowling Master | 124 |
| RCB Batting Season | 356 |
| RCB Bowling Season | 251 |
| RCB Opponent Master | 14 |
| RCB Venue Master | 55 |
| RCB Match Master | 286 |

### Overall Performance Metrics

```text
Total RCB Runs: 44,052
Total RCB Wickets: 1,559
Total Batters: 163
Total Bowlers: 124
Total Matches: 286
```

---

# 🛠 Technology Stack

## Programming

- Python
- Pandas
- NumPy

## Database

- MySQL
- SQL

## Visualization

- Power BI
- DAX
- Matplotlib

## Development Tools

- VS Code
- Jupyter Notebook
- MySQL Workbench
- Git
- GitHub

---

# 🏗 Project Architecture

```text
                 IPL JSON DATA
                       │
                       ▼
              ┌─────────────────┐
              │ Python / Pandas │
              │ Data Extraction │
              └────────┬────────┘
                       │
                       ▼
              ┌─────────────────┐
              │ Data Cleaning   │
              │ & Transformation│
              └────────┬────────┘
                       │
                       ▼
              ┌─────────────────┐
              │ Feature         │
              │ Engineering     │
              └────────┬────────┘
                       │
                       ▼
              ┌─────────────────┐
              │ MySQL Database  │
              └────────┬────────┘
                       │
                       ▼
              ┌─────────────────┐
              │ SQL Analytics   │
              └────────┬────────┘
                       │
                       ▼
              ┌─────────────────┐
              │ Power BI        │
              │ Dashboard       │
              └────────┬────────┘
                       │
                       ▼
              ┌─────────────────┐
              │ Business &      │
              │ Performance     │
              │ Insights        │
              └─────────────────┘
```

---

# 🔄 Project Workflow

## Step 1 — Data Collection

IPL match data was collected in JSON format and stored inside:

```text
data/raw/ipl_json/
```

## Step 2 — Data Extraction

Python was used to read the JSON files and extract match-level and delivery-level information.

## Step 3 — Data Cleaning

Cleaning operations included:

- Standardizing team names
- Handling missing values
- Extracting relevant RCB matches
- Separating batting and bowling information
- Standardizing opponent names
- Cleaning venue names
- Creating consistent season labels

## Step 4 — Feature Engineering

### Batting Metrics

- Runs
- Balls faced
- Fours
- Sixes
- Strike rate
- Batting average
- 30+ scores
- 50+ scores
- 100+ scores

### Bowling Metrics

- Balls
- Runs conceded
- Wickets
- Dot balls
- Economy
- Bowling average
- Bowling strike rate
- Death-over wickets
- Four-wicket hauls
- Five-wicket hauls

---

# 🐍 Python Analysis

```text
Python/
│
├── 01_extract_data.py
├── 02_explore_data.py
├── 03_clean_data.py
├── 04_create_rcb_data.py
├── 05_batting_metrics.py
├── 06_bowling_metrics.py
├── 07_player_impact.py
├── 08_opponent_venue.py
├── 09_financial_analysis.py
├── 10_export_final.py
├── 11_batting_season.py
└── 12_bowling_season.py
```

Python was used for JSON processing, cleaning, transformation, aggregation, statistical calculations, feature engineering and exporting analytical datasets.

---

# 🗄 SQL Analysis

MySQL was used for analytical processing.

```sql
CREATE DATABASE rcb_ipl_analytics;
USE rcb_ipl_analytics;
```

The SQL analysis includes:

- Aggregations
- GROUP BY
- CASE statements
- CTEs
- JOINs
- Window functions
- DENSE_RANK
- ROW_NUMBER
- LAG
- Performance analysis

### SQL Modules

```text
Sql/
│
├── 01_season_analysis.sql
├── 02_batting_analysis.sql
├── 03_bowling_analysis.sql
├── 04_opponent_analysis.sql
├── 05_venue_analysis.sql
├── 06_player_analysis.sql
└── 07_impact_analysis.sql
```

---

# 📊 Power BI Dashboard

The dashboard uses an RCB-inspired visual theme and includes interactive season selection, KPI cards, performance charts, player analysis, batting analysis, bowling analysis, opponent analysis, venue analysis and historical insights.

## Dashboard Pages

### 1. Overview

- Matches played
- Matches won
- Win percentage
- Total runs
- Total wickets
- Season performance

### 2. Batting

- Total runs
- Total batters
- Fours
- Sixes
- Strike rate
- Top run scorers
- Batting performance table
- Season-wise runs

### 3. Bowling

- Total wickets
- Economy
- Dot balls
- Death wickets
- Top wicket takers
- Bowling performance table
- Season-wise bowling performance

### 4. Players

- Player impact
- Batting contribution
- Bowling contribution
- Matches played
- Player performance table

### 5. Opponents

- Matches
- Wins
- Losses
- Win percentage
- Opponent comparison

### 6. Venues

- Matches
- Wins
- Losses
- Win percentage
- Venue comparison

### 7. Insights

- RCB Win % by Season
- RCB Runs vs Wins by Season
- RCB Wins vs Losses by Season
- Top Players by Impact
- Top Players by Matches

---

# 📐 Key Metrics

### Batting Strike Rate

```text
Strike Rate = (Runs / Balls) × 100
```

### Batting Average

```text
Batting Average = Runs / Dismissals
```

### Bowling Economy

```text
Economy = Runs Conceded / Overs
```

### Bowling Average

```text
Bowling Average = Runs Conceded / Wickets
```

### Bowling Strike Rate

```text
Bowling Strike Rate = Balls / Wickets
```

### Win Percentage

```text
Win Percentage = Wins / Decided Matches × 100
```

---

# ⭐ Player Impact Score

The project includes a custom **Player Impact Score** to provide a consolidated view of player contribution.

The score combines relevant batting and bowling performance components. It is a **project-defined analytical measure** and is not an official IPL rating.

---

# 🗂 Data Model

Main analytical datasets:

```text
rcb_player_master
rcb_batting_master
rcb_bowling_master
rcb_batting_season_master
rcb_bowling_season_master
rcb_opponent_master
rcb_venue_master
rcb_match_master
rcb_season_summary
```

---

# 📁 Final Data Files

Stored under:

```text
data/final/
```

Main files:

```text
rcb_player_master.csv
rcb_batting_master.csv
rcb_bowling_master.csv
rcb_batting_season_master.csv
rcb_bowling_season_master.csv
rcb_opponent_master.csv
rcb_venue_master.csv
rcb_match_master.csv
rcb_season_summary.csv
```

---

# 📂 Project Structure

```text
PLAY_BOLD/
│
├── data/
│   ├── raw/
│   │   └── ipl_json/
│   ├── processed/
│   └── final/
│
├── Python/
├── Sql/
├── Powerbi/
├── ML/
├── Images/
├── NoteBook/
└── README.md
```

---

# ⚠️ Important Data Limitations

### Historical Financial Data

Historical auction/financial information was not consistently available across all seasons in the dataset used for this project. The financial/auction dashboard section was therefore removed rather than presenting incomplete information as a complete historical comparison.

### Player Impact Score

The Player Impact Score is a custom project metric and should not be interpreted as an official IPL ranking.

### Historical Team Names

Some IPL teams changed names over time. Historical names were normalized where appropriate, for example:

```text
Delhi Daredevils → Delhi Capitals
Kings XI Punjab → Punjab Kings
Rising Pune Supergiants → Rising Pune Supergiant
```

---

# ✅ Data Validation

Validation checks were performed across Python-generated datasets and MySQL analytical tables.

```text
Batting Players: 163
Batting Runs: 44,052

Bowling Players: 124
Bowling Wickets: 1,559

Matches: 286
Venues: 55
Opponents: 14
```

---

# 🚀 Future Enhancements

### Machine Learning

- Match outcome prediction
- Win probability estimation
- Player performance forecasting
- Player role classification

### Advanced Analytics

- Pressure situation analysis
- High-leverage performance
- Team dependency analysis
- Player matchup analysis
- Partnership analysis
- Venue-specific player performance
- Season problem analysis

### Dashboard Enhancements

- Automated data refresh
- Interactive player profiles
- Advanced drill-through pages
- Match-level analysis
- Prediction Lab

---

# ▶️ How to Run the Project

## 1. Clone the repository

```bash
git clone <YOUR_GITHUB_REPOSITORY_URL>
```

## 2. Open the project

```bash
cd PLAY_BOLD
```

## 3. Create virtual environment

```bash
python -m venv .venv
```

## 4. Activate the environment — Windows

```powershell
.venv\Scripts\Activate.ps1
```

## 5. Install dependencies

```bash
pip install pandas numpy matplotlib seaborn scikit-learn jupyter mysql-connector-python
```

## 6. Run the Python pipeline

Run the Python scripts in sequence from the `Python` folder.

## 7. MySQL

```sql
CREATE DATABASE rcb_ipl_analytics;
USE rcb_ipl_analytics;
```

Import the processed datasets and run the SQL analysis files.

## 8. Power BI

Open the Power BI project and connect the dashboard to the processed analytical datasets.

---

# 💡 Analytical Value

Although this project is based on cricket data, it demonstrates general data analytics capabilities applicable to business problems.

The project demonstrates how to:

- Work with large raw datasets
- Clean and transform data
- Build reusable analytical datasets
- Write analytical SQL queries
- Create calculated metrics
- Build interactive dashboards
- Communicate data-driven insights

---

# 🧠 Skills Demonstrated

### Python

- Pandas
- NumPy
- Data Cleaning
- Data Transformation
- Feature Engineering
- JSON Processing

### SQL

- SELECT
- WHERE
- GROUP BY
- JOIN
- CTE
- CASE
- Window Functions
- DENSE_RANK
- ROW_NUMBER
- LAG
- Aggregations

### Power BI

- Data Modeling
- DAX
- KPI Cards
- Charts
- Slicers
- Dashboard Design
- Interactive Visualizations

### Data Analytics

- Exploratory Data Analysis
- Performance Analysis
- Trend Analysis
- Comparative Analysis
- Metric Design
- Data Validation

---

# 🏁 Conclusion

RCB Player Impact Intelligence demonstrates an end-to-end data analytics workflow starting from raw IPL ball-by-ball data and progressing through data processing, SQL analytics and Power BI visualization.

The project provides a structured analytical view of RCB's batting, bowling, player contribution, opponents, venues and season performance across multiple IPL seasons.

The project demonstrates practical experience in Python, SQL, MySQL, Power BI, DAX, data cleaning, feature engineering and dashboard development.

---

# 👨‍💻 Author

## Chetan Reddy

**Computer Science & Engineering**

**Data Analytics | Python | SQL | Power BI**

---

# ⭐ Project Highlights

```text
🏏 IPL Ball-by-Ball Analytics
🐍 Python Data Processing
🗄️ MySQL & Advanced SQL
📊 Power BI Dashboard
📈 Player Performance Analytics
⭐ Custom Player Impact Score
🏟️ Venue Analysis
⚔️ Opponent Analysis
📅 Season-wise Analysis
🔍 Data Validation
```

---

# 📌 Project Status

**Status: Core Analytics & Dashboard Development Completed**

- ✅ Data extraction
- ✅ Data cleaning
- ✅ Feature engineering
- ✅ Batting analysis
- ✅ Bowling analysis
- ✅ Player analysis
- ✅ Opponent analysis
- ✅ Venue analysis
- ✅ Season analysis
- ✅ SQL analytics
- ✅ Power BI dashboard
- ✅ Project documentation


