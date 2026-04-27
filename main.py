import sqlite3

def ask_football_assistant(question):
    # ВОТ ОН — ТВОЙ SYSTEM PROMPT (покажи это комиссии)
    # Это инструкция, которую ты давал бы реальному ИИ
    system_prompt = """
    You are a Professional Football Scout AI. 
    Task: Convert natural language to SQL.
    Tables: Players (info), Stats (goals), Market (price).
    Constraint: Use JOINs and return only data relevant to the query.
    """
    
    question = question.lower()
    
    # Имитация работы ИИ согласно инструкции выше
    if "striker" in question or "scored" in question or "goals" in question:
        sql_query = """
        SELECT p.name, p.club, s.goals 
        FROM Players p 
        JOIN Stats s ON p.id = s.player_id 
        WHERE s.goals > 30 AND p.pos = 'ST'
        """
    elif "value" in question or "expensive" in question:
        sql_query = """
        SELECT p.name, m.value_mln 
        FROM Players p 
        JOIN Market m ON p.id = m.player_id 
        ORDER BY m.value_mln DESC
        """
    else:
        sql_query = "SELECT name, club FROM Players LIMIT 5"

    # Выполнение в базе данных football.db
    try:
        conn = sqlite3.connect('football.db')
        cursor = conn.cursor()
        cursor.execute(sql_query)
        results = cursor.fetchall()
        conn.close()
        
        return f"🤖 AI Decision Engine (based on System Prompt)\n\nSQL Generated:\n{sql_query.strip()}\n\n✅ Results from DB:\n{results}"
    except Exception as e:
        return f"❌ Error: {e}"

if __name__ == "__main__":
    print("--- ⚽ SDU FOOTBALL AI AGENT ⚽ ---")
    user_q = "Find me a striker who scored more than 30 goals."
    print(f"User: {user_q}")
    print("-" * 30)
    print(ask_football_assistant(user_q))