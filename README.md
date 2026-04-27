# RAG — Кітаптан сұрақ-жауап жүйесі

Кітапты жүктеп, сұрақ қойсаңыз — жауап береді. Қазақша, орысша, ағылшынша сұрауға болады.

## Қалай жұмыс жасайды

1. Кітап чанктарға бөлінеді
2. Әр чанктан эмбеддинг жасалады (OpenAI)
3. Сұрақ қойғанда ең ұқсас чанктар табылады
4. GPT-4o-mini жауап береді

## Орнату

**1. Python 3.10+ орнатыңыз**

**2. Виртуалды орта жасаңыз**
```bash
python -m venv venv
venv\Scripts\activate
```

**3. Пакеттерді орнатыңыз**
```bash
pip install openai python-dotenv tiktoken flask numpy pypdf2
```

**4. `.env` файлын жасаңыз**
```
OPENAI_API_KEY=sk-...сіздің кілтіңіз...
EMBED_MODEL=text-embedding-3-small
CHAT_MODEL=gpt-4o-mini
CHUNK_SIZE=500
CHUNK_OVERLAP=50
```

## Қолдану

**Кітапты индекстеу (бір рет)**
```bash
python ingest.py books/kitap.pdf
```

**Веб интерфейсті іске қосу**
```bash
python app.py
```

Браузерде ашыңыз: [http://localhost:5000](http://localhost:5000)

## Технологиялар

- **OpenAI** — эмбеддинг және жауап генерациясы
- **NumPy** — векторлық іздеу
- **Flask** — веб интерфейс
- **PyPDF2** — PDF оқу
- **tiktoken** — мәтінді чанктарға бөлу
