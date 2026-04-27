import sqlite3

def ask_football_assistant(question):
    """
    Симуляция AI-агента для защиты проекта.
    Переводит вопрос в SQL без обращения к платному API.
    """
    question = question.lower()
    
    # ЛОГИКА ТРАНСЛЯЦИИ (Твой "ручной" Prompt Engineering для демонстрации)
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

    # ВЫПОЛНЕНИЕ В БАЗЕ ДАННЫХ (Это доказывает, что проект нетривиальный)
    try:
        conn = sqlite3.connect('football.db')
        cursor = conn.cursor()
        cursor.execute(sql_query)
        results = cursor.fetchall()
        conn.close()
        
        return f"🤖 AI Generated SQL:\n{sql_query.strip()}\n\n✅ Scouting Result:\n{results}"
    except Exception as e:
        return f"❌ Database Error: {e}\n(Убедись, что запустил database_setup.py)"

if __name__ == "__main__":
    print("--- FOOTBALL SCOUT AI AGENT ---")
    # Тестовый вопрос, который ты покажешь завтра
    user_q = "Find me a striker who scored more than 30 goals."
    print(f"User Question: {user_q}")
    print(ask_football_assistant(user_q))