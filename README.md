# 🎓 SDU AI Smart Assistant (Text-to-SQL)

## 🚀 Overview
This is a non-trivial AI-driven data analysis tool designed for SDU students. It uses an Agentic workflow to translate natural language questions into complex SQL queries to analyze university data.

## 🛠 Features (Criteria: Complexity & Originality)
- **Agentic Workflow**: The LLM acts as a database administrator, generating and executing SQL.
- **Relational Complexity**: Queries data across 3 linked tables using SQL JOINs.
- **Vibe-coded Analysis**: Analyzes student feedback and course difficulty, not just raw facts.

## 📊 Database Schema
1. **Courses**: Main course information.
2. **Schedule**: Instructor names, timing, and locations.
3. **VibeCheck**: Subjective difficulty levels and student comments.

## 💻 How to Run
1. Install requirements: `pip install openai`
2. Initialize DB: Run `python database_setup.py`
3. Launch Assistant: Run `python main.py`
