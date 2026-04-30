# ⬡ ResearchMind AI

> **A multi-agent research pipeline powered by LangGraph & LangChain — with a sleek Streamlit UI.**

ResearchMind AI automates deep research by chaining four specialized AI agents: a **Search Agent** that hunts the web, a **Reader Agent** that scrapes top sources, a **Writer Chain** that drafts a comprehensive report, and a **Critic Chain** that reviews and scores the output — all in a single pipeline run.

---

## ✦ Preview

```
Topic Input  →  Search Agent  →  Reader Agent  →  Writer Chain  →  Critic Chain  →  Final Report
```

The Streamlit UI renders a live pipeline tracker, real-time progress bar, metrics dashboard, and a terminal-style system log — all in a deep obsidian dark theme.

---

## ✦ Features

- **4-Stage Agentic Pipeline** — Search → Scrape → Write → Critique
- **LangGraph Agents** — ReAct-style agents with tool use (Tavily search, web scraper)
- **Live UI Feedback** — per-step pipeline tracker with pulse animation and progress bar
- **Metrics Dashboard** — word count, char counts, and total elapsed time after each run
- **Terminal Log** — timestamped system log for every pipeline event
- **Dual Downloads** — export the report only, or the full pipeline output
- **Performance Caching** — `st.cache_resource` caches agents across reruns for near-instant restarts
- **Dark Theme** — Playfair Display + IBM Plex Mono, obsidian background, amber accents

---

## ✦ Project Structure

```
researchmind/
│
├── app.py              # Streamlit UI (dark theme, live pipeline tracker)
├── pipeline.py         # Core pipeline — run from terminal
├── agents.py           # Agent & chain definitions
├── .env                # API keys (not committed)
├── requirements.txt    # Python dependencies
└── README.md
```

---

## ✦ Quickstart

### 1 — Clone the repo

```bash
git clone https://github.com/Khan7Atif9/Multi-Agent-AI-Research-System.git
cd researchmind-ai
```

### 2 — Create a virtual environment

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS / Linux
source venv/bin/activate
```

### 3 — Install dependencies

```bash
pip install -r requirements.txt
```

### 4 — Set up environment variables

Create a `.env` file in the project root:

```env
OPENAI_API_KEY=sk-...
TAVILY_API_KEY=tvly-...
```

> The search agent uses **Tavily** for web search. Get a free key at [tavily.com](https://tavily.com).

### 5 — Run the Streamlit UI

```bash
streamlit run app.py
```

### 5 (alt) — Run in terminal only

```bash
python pipeline.py
```

---

## ✦ How It Works

| Stage | Agent / Chain | What it does |
|-------|--------------|--------------|
| **1** | `SearchAgent` | Uses Tavily to query the web for recent, reliable sources on the topic |
| **2** | `ReaderAgent` | Picks the most relevant URL from search results and scrapes it for full content |
| **3** | `WriterChain` | Combines search + scraped content and generates a structured research report |
| **4** | `CriticChain` | Reviews the report for accuracy, depth, and quality — returns scored feedback |

All agents and chains are defined in `agents.py` and composed in `pipeline.py`.

---

## ✦ Tech Stack

| Layer | Technology |
|-------|-----------|
| LLM | OpenAI GPT-4o (via `langchain-openai`) |
| Agents | LangGraph `create_react_agent` |
| Search Tool | Tavily Search API |
| Scraping Tool | LangChain Community web loader |
| UI | Streamlit |
| Env Management | `python-dotenv` |
| Data | Pandas, NumPy |

---

## ✦ Requirements

```txt
streamlit
langchain
langchain-community
langchain-openai
langgraph
tavily-python
python-dotenv
```

> Full list in `requirements.txt`

---

## ✦ Environment Variables

| Variable | Description |
|----------|-------------|
| `OPENAI_API_KEY` | Your OpenAI API key |
| `TAVILY_API_KEY` | Your Tavily search API key |
| `GROQ_API_KEY'   | Your Groq API Key |
---

## ✦ Usage Tips

- **First run** is slower — agents are built and cached. Subsequent runs on the same session are significantly faster.
- Topics work best when **specific** — e.g. *"Quantum error correction breakthroughs 2025"* over *"quantum computing"*.
- The **full output download** includes all four pipeline stages in a single `.txt` file — useful for archiving.
- To run headlessly (e.g. in a script or cron job), use `pipeline.py` directly.

---

## ✦ Roadmap

- [ ] PDF export for the final report
- [ ] Support for multiple URLs in the Reader Agent
- [ ] Conversation history / session persistence
- [ ] Swap LLM provider (Anthropic Claude, Gemini) via config
- [ ] Docker support

---

## ✦ Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you'd like to change.

1. Fork the repo
2. Create a feature branch (`git checkout -b feature/your-feature`)
3. Commit your changes (`git commit -m 'Add your feature'`)
4. Push to the branch (`git push origin feature/your-feature`)
5. Open a Pull Request

---

## ✦ License

[MIT](LICENSE)

---

<div align="center">
  <sub>Built with LangGraph · LangChain · Streamlit</sub>
</div>