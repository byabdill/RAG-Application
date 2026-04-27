"""
RAG веб интерфейсі — Flask
Іске қосу: python app.py
Браузерде ашу: http://localhost:5000
"""

import os
import sys

sys.stdout.reconfigure(encoding='utf-8')
sys.stderr.reconfigure(encoding='utf-8')

from flask import Flask, request, jsonify, render_template_string
from query import answer, retrieve

app = Flask(__name__)

HTML = """<!DOCTYPE html>
<html lang="kk">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>RAG — Кітаптан сұрақ-жауап</title>
  <style>
    * { box-sizing: border-box; margin: 0; padding: 0; }
    body { font-family: 'Segoe UI', sans-serif; background: #f0f2f5; height: 100vh; display: flex; flex-direction: column; }

    header {
      background: #1a1a2e;
      color: white;
      padding: 16px 24px;
      display: flex;
      align-items: center;
      gap: 12px;
      box-shadow: 0 2px 8px rgba(0,0,0,0.3);
    }
    header h1 { font-size: 18px; font-weight: 600; }
    header span { font-size: 13px; color: #aaa; }
    .badge { background: #16213e; border: 1px solid #0f3460; border-radius: 20px; padding: 4px 12px; font-size: 12px; color: #e94560; }

    #chat {
      flex: 1;
      overflow-y: auto;
      padding: 24px;
      display: flex;
      flex-direction: column;
      gap: 16px;
    }

    .msg { display: flex; gap: 12px; max-width: 820px; }
    .msg.user { align-self: flex-end; flex-direction: row-reverse; }
    .msg.bot  { align-self: flex-start; }

    .avatar {
      width: 36px; height: 36px; border-radius: 50%;
      display: flex; align-items: center; justify-content: center;
      font-size: 16px; flex-shrink: 0;
    }
    .msg.user .avatar { background: #0f3460; }
    .msg.bot  .avatar { background: #e94560; }

    .bubble {
      padding: 12px 16px;
      border-radius: 16px;
      font-size: 14px;
      line-height: 1.6;
      max-width: 680px;
      white-space: pre-wrap;
    }
    .msg.user .bubble { background: #0f3460; color: white; border-bottom-right-radius: 4px; }
    .msg.bot  .bubble { background: white; color: #1a1a2e; border-bottom-left-radius: 4px; box-shadow: 0 1px 4px rgba(0,0,0,0.1); }

    .sources {
      margin-top: 10px;
      padding: 10px 14px;
      background: #f8f9fa;
      border-left: 3px solid #e94560;
      border-radius: 0 8px 8px 0;
      font-size: 12px;
      color: #555;
    }
    .sources b { color: #e94560; }
    .translated { color: #888; font-style: italic; margin-bottom: 6px; }

    .typing { display: flex; gap: 5px; padding: 14px 16px; }
    .typing span { width: 8px; height: 8px; background: #ccc; border-radius: 50%; animation: bounce 1.2s infinite; }
    .typing span:nth-child(2) { animation-delay: 0.2s; }
    .typing span:nth-child(3) { animation-delay: 0.4s; }
    @keyframes bounce { 0%,60%,100%{transform:translateY(0)} 30%{transform:translateY(-8px)} }

    footer {
      background: white;
      padding: 16px 24px;
      box-shadow: 0 -2px 8px rgba(0,0,0,0.08);
    }
    .input-row { display: flex; gap: 10px; max-width: 820px; margin: 0 auto; }
    #q {
      flex: 1;
      border: 1.5px solid #ddd;
      border-radius: 24px;
      padding: 12px 20px;
      font-size: 14px;
      outline: none;
      transition: border 0.2s;
    }
    #q:focus { border-color: #e94560; }
    button {
      background: #e94560;
      color: white;
      border: none;
      border-radius: 24px;
      padding: 12px 24px;
      font-size: 14px;
      cursor: pointer;
      font-weight: 600;
      transition: background 0.2s;
    }
    button:hover { background: #c73652; }
    button:disabled { background: #ccc; cursor: not-allowed; }

    .empty-state {
      margin: auto;
      text-align: center;
      color: #aaa;
    }
    .empty-state .icon { font-size: 48px; margin-bottom: 12px; }
    .empty-state p { font-size: 14px; }

  </style>
</head>
<body>
  <header>
    <div style="font-size:24px">📚</div>
    <div>
      <h1>RAG — Кітаптан сұрақ-жауап</h1>
      <span>Кез келген тілде сұраңыз</span>
    </div>
    <div style="margin-left:auto"><span class="badge">gpt-4o-mini</span></div>
  </header>

  <div id="chat">
    <div class="empty-state" id="empty">
      <div class="icon">🔍</div>
      <p>Кітап туралы кез келген сұрақ қойыңыз</p>
      <p style="margin-top:4px; font-size:12px">Қазақша, орысша немесе ағылшынша сұрауға болады</p>
    </div>
  </div>

  <footer>
    <input id="collection" value="book" type="hidden">
    <div class="input-row">
      <input id="q" placeholder="Сұрағыңызды жазыңыз..." autocomplete="off">
      <button id="send" onclick="sendMsg()">Жіберу</button>
    </div>
  </footer>

<script>
const chat = document.getElementById('chat');
const empty = document.getElementById('empty');
const input = document.getElementById('q');
const btn   = document.getElementById('send');

input.addEventListener('keydown', e => { if (e.key === 'Enter' && !e.shiftKey) { e.preventDefault(); sendMsg(); } });

function addMsg(role, content, meta) {
  if (empty) empty.style.display = 'none';
  const div = document.createElement('div');
  div.className = `msg ${role}`;

  const avatar = document.createElement('div');
  avatar.className = 'avatar';
  avatar.textContent = role === 'user' ? '👤' : '🤖';

  const bubble = document.createElement('div');
  bubble.className = 'bubble';
  bubble.textContent = content;

  div.appendChild(avatar);
  div.appendChild(bubble);


  chat.appendChild(div);
  chat.scrollTop = chat.scrollHeight;
}

function addTyping() {
  const div = document.createElement('div');
  div.className = 'msg bot';
  div.id = 'typing';
  div.innerHTML = '<div class="avatar">🤖</div><div class="bubble"><div class="typing"><span></span><span></span><span></span></div></div>';
  chat.appendChild(div);
  chat.scrollTop = chat.scrollHeight;
}

function removeTyping() {
  const t = document.getElementById('typing');
  if (t) t.remove();
}

async function sendMsg() {
  const q = input.value.trim();
  if (!q) return;
  const col = document.getElementById('collection').value.trim() || 'book';

  addMsg('user', q);
  input.value = '';
  btn.disabled = true;
  addTyping();

  try {
    const res = await fetch('/ask', {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({question: q, collection: col})
    });
    const data = await res.json();
    removeTyping();
    if (data.error) {
      addMsg('bot', '⚠️ Қате: ' + data.error);
    } else {
      addMsg('bot', data.answer, {translated: data.translated, chunks: data.chunks});
    }
  } catch(e) {
    removeTyping();
    addMsg('bot', '⚠️ Сервермен байланыс жоқ.');
  }
  btn.disabled = false;
  input.focus();
}
</script>
</body>
</html>"""


@app.route("/")
def index():
    return render_template_string(HTML)


@app.route("/ask", methods=["POST"])
def ask():
    data = request.get_json()
    question = (data.get("question") or "").strip()
    collection = (data.get("collection") or "book").strip()

    if not question:
        return jsonify({"error": "Сұрақ бос"}), 400

    try:
        chunks = retrieve(question, collection)
        translated = chunks[0].get("translated_query", question)

        context = "\n\n---\n\n".join(
            f"[Чанк {c['chunk_index']}] {c['text']}" for c in chunks
        )
        from openai import OpenAI
        from dotenv import load_dotenv
        load_dotenv()
        cl = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

        resp = cl.chat.completions.create(
            model=os.getenv("CHAT_MODEL", "gpt-4o-mini"),
            messages=[
                {"role": "system", "content": (
                    "Сен кітап мазмұнын талдайтын AI көмекшісің. "
                    "Берілген контекст негізінде сұраққа нақты және толық жауап бер. "
                    "Контекстте жоқ ақпаратты өз бетіңше ойлап таппа. "
                    "Жауапты міндетті түрде сұрақ қойылған тілде бер."
                )},
                {"role": "user", "content": f"Контекст:\n{context}\n\nСұрақ: {question}"},
            ],
            temperature=0.2,
        )
        reply = resp.choices[0].message.content

        return jsonify({
            "answer": reply,
            "translated": translated,
            "chunks": [{"chunk_index": c["chunk_index"], "similarity": c["similarity"]} for c in chunks],
        })

    except ValueError as e:
        return jsonify({"error": str(e)}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    print(f"\nБраузерде ашыңыз: http://localhost:{port}\n")
    app.run(debug=False, port=port, host="0.0.0.0")
