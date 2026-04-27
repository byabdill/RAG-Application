# ⚽ AI Football Scout & Match Predictor

## 🌟 Overview
This project is a non-trivial AI Agent designed for football data analysis. It combines **Machine Learning** for match prediction and **Natural Language Processing (Text-to-SQL)** for scouting players from a relational database.

## 🧠 Project Depth (Criteria: Complexity)
- **Agentic Workflow**: Translates natural language into SQL queries to analyze player stats.
- **Data Science**: Includes a Jupyter Notebook with a **Random Forest** model (Accuracy: 49.8%) for predicting match outcomes.
- **Relational DB**: Uses 3 linked tables (Players, Stats, Market) with JOIN logic.

## 📊 How to Run
1. Install dependencies: `pip install openai`
2. Initialize the database: `python database_setup.py`
3. Run the AI Scout: `python main.py`

## 📈 Technical Details
- Data sourced via Web Scraping (BeautifulSoup, cloudscraper).
- Model: Random Forest Classifier.
- DB: SQLite3.
