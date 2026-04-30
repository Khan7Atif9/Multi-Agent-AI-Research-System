"""
ResearchMind AI — Streamlit UI
Deep obsidian dark theme · Playfair Display + IBM Plex Mono
Performance: st.cache_resource caches agents across reruns
Run: streamlit run app.py
"""

import streamlit as st
import time

# ─────────────────────────────────────────────────────────────────────────────
# Page config — must be FIRST streamlit call
# ─────────────────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="ResearchMind AI",
    page_icon="⬡",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ─────────────────────────────────────────────────────────────────────────────
# Cache heavy agent construction — rebuilt only on server restart
# ─────────────────────────────────────────────────────────────────────────────
@st.cache_resource(show_spinner=False)
def get_agents():
    """Load agents once; reuse across all reruns."""
    from agents import build_search_agent, build_reader_agent, writer_chain, critic_chain
    return (
        build_search_agent(),
        build_reader_agent(),
        writer_chain,
        critic_chain,
    )

# ─────────────────────────────────────────────────────────────────────────────
# CSS — deep obsidian, amber/gold accents, serif headlines
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;700;900&family=IBM+Plex+Mono:wght@300;400;500&display=swap');

:root {
    --bg:         #080810;
    --bg1:        #0e0e1a;
    --bg2:        #13131f;
    --bg3:        #1a1a28;
    --border:     rgba(255,255,255,0.07);
    --border-hi:  rgba(255,195,80,0.35);
    --amber:      #ffc350;
    --amber-dim:  rgba(255,195,80,0.12);
    --amber-glow: rgba(255,195,80,0.06);
    --red:        #ff6b6b;
    --green:      #4fffb0;
    --text:       #ddd8cc;
    --text-dim:   #6a6a7a;
    --text-mute:  #2a2a3a;
    --mono:       'IBM Plex Mono', monospace;
    --serif:      'Playfair Display', Georgia, serif;
}

*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

html, body,
[data-testid="stAppViewContainer"],
[data-testid="stAppViewBlockContainer"] {
    background: var(--bg) !important;
    color: var(--text) !important;
    font-family: var(--mono) !important;
}

/* Subtle ambient glow */
[data-testid="stAppViewContainer"]::before {
    content: '';
    position: fixed;
    inset: 0;
    background:
        radial-gradient(700px 500px at 5% 0%,   rgba(255,195,80,0.04) 0%, transparent 65%),
        radial-gradient(500px 700px at 95% 100%, rgba(79,255,176,0.025) 0%, transparent 65%);
    pointer-events: none;
    z-index: 0;
}

/* Star-field dots */
[data-testid="stAppViewContainer"]::after {
    content: '';
    position: fixed;
    inset: 0;
    background-image:
        radial-gradient(1px 1px at 12% 18%, rgba(255,195,80,0.3) 0%, transparent 100%),
        radial-gradient(1px 1px at 68% 7%,  rgba(255,195,80,0.2) 0%, transparent 100%),
        radial-gradient(1px 1px at 85% 52%, rgba(255,195,80,0.25) 0%, transparent 100%),
        radial-gradient(1px 1px at 30% 78%, rgba(255,195,80,0.15) 0%, transparent 100%),
        radial-gradient(1px 1px at 52% 41%, rgba(79,255,176,0.18) 0%, transparent 100%),
        radial-gradient(1px 1px at 94% 30%, rgba(255,195,80,0.12) 0%, transparent 100%);
    pointer-events: none;
    z-index: 0;
}

#MainMenu, footer, header          { visibility: hidden !important; }
[data-testid="stToolbar"]          { display: none !important; }
[data-testid="stDecoration"]       { display: none !important; }

.block-container {
    padding: 0 3.5rem 4rem !important;
    max-width: 1300px !important;
    position: relative;
    z-index: 1;
}

/* ══ HERO ═══════════════════════════════════════════════════════════════════ */
.hero { padding: 3.5rem 0 1.5rem; }

.eyebrow {
    font-size: 0.62rem;
    font-weight: 500;
    letter-spacing: 0.35em;
    color: var(--amber);
    text-transform: uppercase;
    display: flex;
    align-items: center;
    gap: 0.8rem;
    margin-bottom: 1rem;
}
.eyebrow::before, .eyebrow::after {
    content: '';
    height: 1px;
    width: 50px;
    background: linear-gradient(90deg, transparent, var(--amber));
}
.eyebrow::after { background: linear-gradient(90deg, var(--amber), transparent); }

.hero-title {
    font-family: var(--serif);
    font-size: clamp(3rem, 6vw, 6.5rem);
    font-weight: 900;
    line-height: 0.92;
    letter-spacing: -0.02em;
    color: var(--text);
    margin-bottom: 0.8rem;
}
.hero-title em {
    font-style: normal;
    color: transparent;
    -webkit-text-stroke: 1.5px rgba(255,195,80,0.5);
}

.hero-sub {
    font-size: 0.7rem;
    color: var(--text-dim);
    letter-spacing: 0.1em;
}

.hero-rule {
    height: 1px;
    background: linear-gradient(90deg, var(--amber) 0%, rgba(255,195,80,0.25) 35%, transparent 100%);
    margin: 2rem 0;
}

/* ══ INPUT ══════════════════════════════════════════════════════════════════ */
[data-testid="stTextInput"] label {
    font-family: var(--mono) !important;
    font-size: 0.6rem !important;
    font-weight: 500 !important;
    letter-spacing: 0.24em !important;
    text-transform: uppercase !important;
    color: var(--text-dim) !important;
}
[data-testid="stTextInput"] input {
    background: var(--bg2) !important;
    border: 1px solid var(--border) !important;
    border-radius: 3px !important;
    color: var(--text) !important;
    font-family: var(--mono) !important;
    font-size: 1rem !important;
    padding: 0.9rem 1.1rem !important;
    caret-color: var(--amber) !important;
    transition: border-color 0.2s, box-shadow 0.2s !important;
}
[data-testid="stTextInput"] input:focus {
    border-color: rgba(255,195,80,0.6) !important;
    box-shadow: 0 0 0 3px var(--amber-glow) !important;
    outline: none !important;
}
[data-testid="stTextInput"] input::placeholder { color: var(--text-mute) !important; }

/* ══ BUTTONS ════════════════════════════════════════════════════════════════ */
[data-testid="stButton"] button {
    background: transparent !important;
    border: 1px solid var(--amber) !important;
    color: var(--amber) !important;
    font-family: var(--mono) !important;
    font-size: 0.72rem !important;
    font-weight: 500 !important;
    letter-spacing: 0.22em !important;
    text-transform: uppercase !important;
    border-radius: 3px !important;
    padding: 0.88rem 1.6rem !important;
    width: 100% !important;
    cursor: pointer !important;
    transition: background 0.18s, box-shadow 0.18s !important;
}
[data-testid="stButton"] button:hover {
    background: var(--amber-dim) !important;
    box-shadow: 0 0 28px rgba(255,195,80,0.2) !important;
}

/* ══ PIPELINE ═══════════════════════════════════════════════════════════════ */
.pipe-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 1px;
    background: var(--border);
    border: 1px solid var(--border);
    border-radius: 4px;
    overflow: hidden;
    margin: 1.5rem 0;
}
.step {
    background: var(--bg1);
    padding: 1.4rem 1.2rem 1.2rem;
    position: relative;
    transition: background 0.35s;
    min-height: 140px;
}
.step.active  { background: #111320; }
.step.done    { background: #0c130e; }
.step.waiting { opacity: 0.32; }

.step-n {
    font-family: var(--serif);
    font-size: 2.6rem;
    font-weight: 900;
    color: var(--text-mute);
    line-height: 1;
    margin-bottom: 0.55rem;
    transition: color 0.35s;
}
.step.active .step-n { color: var(--amber); }
.step.done   .step-n { color: rgba(79,255,176,0.18); }

.step-name {
    font-family: var(--mono);
    font-size: 0.73rem;
    font-weight: 500;
    letter-spacing: 0.04em;
    color: var(--text);
    margin-bottom: 0.28rem;
}
.step-desc { font-size: 0.61rem; color: var(--text-dim); line-height: 1.5; }
.step.active .step-desc { color: #7a9a6a; }

.pulse-dot {
    position: absolute;
    top: 0.85rem; right: 0.85rem;
    width: 7px; height: 7px;
    border-radius: 50%;
    background: var(--amber);
    box-shadow: 0 0 10px var(--amber);
    animation: throb 1.3s ease-in-out infinite;
}
.check-mark {
    position: absolute;
    top: 0.85rem; right: 0.85rem;
    color: var(--green);
    font-size: 0.72rem;
}
@keyframes throb {
    0%,100% { opacity:1; transform:scale(1); }
    50%      { opacity:0.25; transform:scale(1.6); }
}

/* ══ PROGRESS ═══════════════════════════════════════════════════════════════ */
[data-testid="stProgress"] > div {
    background: var(--bg3) !important;
    border-radius: 2px !important;
    height: 3px !important;
}
[data-testid="stProgress"] > div > div {
    background: linear-gradient(90deg, var(--amber), rgba(255,195,80,0.55)) !important;
    border-radius: 2px !important;
}

/* ══ METRICS ROW ════════════════════════════════════════════════════════════ */
.metrics-row {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 1px;
    background: var(--border);
    border: 1px solid var(--border);
    border-radius: 4px;
    overflow: hidden;
    margin-bottom: 1.6rem;
}
.m-cell { background: var(--bg1); padding: 1.1rem; text-align: center; }
.m-val  {
    font-family: var(--serif);
    font-size: 1.9rem;
    font-weight: 900;
    color: var(--amber);
    line-height: 1;
}
.m-lbl  {
    font-size: 0.58rem;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    color: var(--text-dim);
    margin-top: 0.3rem;
}

/* ══ RESULT PANELS ══════════════════════════════════════════════════════════ */
.rp {
    border: 1px solid var(--border);
    border-radius: 4px;
    overflow: hidden;
    margin-bottom: 1rem;
    background: var(--bg1);
    transition: border-color 0.2s;
}
.rp:hover { border-color: rgba(255,195,80,0.12); }
.rp-head {
    display: flex;
    align-items: center;
    gap: 0.75rem;
    padding: 0.72rem 1rem;
    border-bottom: 1px solid var(--border);
    background: var(--bg2);
}
.badge {
    font-size: 0.56rem;
    letter-spacing: 0.22em;
    text-transform: uppercase;
    padding: 0.18rem 0.52rem;
    border-radius: 2px;
    font-weight: 500;
}
.b-amber { background:var(--amber-dim); color:var(--amber); border:1px solid rgba(255,195,80,0.22); }
.b-green { background:rgba(79,255,176,0.07); color:var(--green); border:1px solid rgba(79,255,176,0.18); }
.b-red   { background:rgba(255,107,107,0.07); color:var(--red); border:1px solid rgba(255,107,107,0.18); }
.b-mute  { background:rgba(255,255,255,0.03); color:var(--text-dim); border:1px solid var(--border); }

.rp-title { font-size: 0.76rem; font-weight: 500; color: var(--text); }
.rp-body {
    padding: 1.1rem;
    font-size: 0.75rem;
    line-height: 1.88;
    color: var(--text-dim);
    white-space: pre-wrap;
    word-break: break-word;
    max-height: 320px;
    overflow-y: auto;
}
.rp-body.tall { max-height: 600px; color: var(--text); font-size: 0.78rem; }
.rp-body::-webkit-scrollbar { width: 3px; }
.rp-body::-webkit-scrollbar-track { background: transparent; }
.rp-body::-webkit-scrollbar-thumb { background: rgba(255,195,80,0.18); border-radius: 2px; }

/* ══ SECTION HEADERS ════════════════════════════════════════════════════════ */
.sec-hd {
    display: flex;
    align-items: center;
    gap: 1rem;
    margin: 2rem 0 1rem;
}
.sec-title {
    font-family: var(--serif);
    font-size: 1.4rem;
    font-weight: 700;
    color: var(--text);
    white-space: nowrap;
}
.sec-rule {
    flex: 1;
    height: 1px;
    background: linear-gradient(90deg, var(--border), transparent);
}

/* ══ TERMINAL LOG ═══════════════════════════════════════════════════════════ */
.term {
    background: #04040c;
    border: 1px solid rgba(255,195,80,0.09);
    border-left: 2px solid rgba(255,195,80,0.4);
    border-radius: 4px;
    padding: 0.85rem 1rem;
    margin-top: 1.2rem;
    font-size: 0.67rem;
    line-height: 1.8;
    max-height: 190px;
    overflow-y: auto;
}
.term-hdr {
    font-size: 0.58rem;
    letter-spacing: 0.28em;
    color: var(--amber);
    text-transform: uppercase;
    padding-bottom: 0.45rem;
    margin-bottom: 0.45rem;
    border-bottom: 1px solid rgba(255,195,80,0.07);
}
.t-info    { color: #3a5a4a; }
.t-success { color: var(--green); }
.t-warn    { color: var(--amber); }
.t-error   { color: var(--red); }

/* ══ ERROR ══════════════════════════════════════════════════════════════════ */
.err-box {
    background: rgba(255,107,107,0.04);
    border: 1px solid rgba(255,107,107,0.18);
    border-left: 3px solid var(--red);
    border-radius: 4px;
    padding: 1rem 1.2rem;
    color: var(--red);
    font-size: 0.76rem;
    line-height: 1.65;
    white-space: pre-wrap;
    margin-top: 1rem;
}

/* ══ DOWNLOAD BUTTONS ═══════════════════════════════════════════════════════ */
[data-testid="stDownloadButton"] button {
    background: transparent !important;
    border: 1px solid rgba(79,255,176,0.28) !important;
    color: var(--green) !important;
    font-family: var(--mono) !important;
    font-size: 0.68rem !important;
    letter-spacing: 0.16em !important;
    text-transform: uppercase !important;
    border-radius: 3px !important;
    padding: 0.6rem 1.2rem !important;
}
[data-testid="stDownloadButton"] button:hover {
    background: rgba(79,255,176,0.05) !important;
    box-shadow: 0 0 18px rgba(79,255,176,0.1) !important;
}

/* spinner text */
[data-testid="stSpinner"] p {
    color: var(--text-dim) !important;
    font-size: 0.72rem !important;
}
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
# Helpers
# ─────────────────────────────────────────────────────────────────────────────
STEPS = [
    ("I",   "Search Agent",  "Queries the web for latest intelligence"),
    ("II",  "Reader Agent",  "Scrapes top URLs for deep content"),
    ("III", "Writer Chain",  "Synthesises the full research report"),
    ("IV",  "Critic Chain",  "Reviews, scores & improves quality"),
]

def render_pipeline(active: int = -1, done: int = 0):
    cards = ""
    for i, (num, name, desc) in enumerate(STEPS):
        if i < done:
            css  = "step done"
            mark = '<span class="check-mark">✓</span>'
        elif i == active:
            css  = "step active"
            mark = '<div class="pulse-dot"></div>'
        else:
            css  = "step waiting"
            mark = ""
        cards += f"""<div class="{css}">
            {mark}
            <div class="step-n">{num}</div>
            <div class="step-name">{name}</div>
            <div class="step-desc">{desc}</div>
        </div>"""
    st.markdown(f'<div class="pipe-grid">{cards}</div>', unsafe_allow_html=True)


def rp(badge, badge_cls, title, content, body_cls=""):
    safe = content.replace("&","&amp;").replace("<","&lt;").replace(">","&gt;")
    st.markdown(f"""<div class="rp">
        <div class="rp-head">
            <span class="badge {badge_cls}">{badge}</span>
            <span class="rp-title">{title}</span>
        </div>
        <div class="rp-body {body_cls}">{safe}</div>
    </div>""", unsafe_allow_html=True)


def sec(title):
    st.markdown(f"""<div class="sec-hd">
        <span class="sec-title">{title}</span>
        <span class="sec-rule"></span>
    </div>""", unsafe_allow_html=True)


def log(msg: str, level: str = "info"):
    ts = time.strftime("%H:%M:%S")
    st.session_state.logs.append(f'<div class="t-{level}">[{ts}]  {msg}</div>')


def render_logs():
    if st.session_state.logs:
        body = "\n".join(st.session_state.logs)
        st.markdown(f"""<div class="term">
            <div class="term-hdr">⬡ &nbsp;System Log</div>{body}
        </div>""", unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
# Session state bootstrap
# ─────────────────────────────────────────────────────────────────────────────
_defaults = dict(results=None, logs=[], error=None, ran=False, elapsed=0.0, words=0)
for k, v in _defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v


# ─────────────────────────────────────────────────────────────────────────────
# HERO
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
    <div class="eyebrow">Multi-Agent Intelligence System</div>
    <h1 class="hero-title">Research<em>Mind</em></h1>
    <p class="hero-sub">Search &nbsp;→&nbsp; Scrape &nbsp;→&nbsp; Write &nbsp;→&nbsp; Critique &nbsp;·&nbsp; LangGraph + LangChain</p>
    <div class="hero-rule"></div>
</div>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
# INPUT
# ─────────────────────────────────────────────────────────────────────────────
c1, c2 = st.columns([6, 1], gap="small")
with c1:
    topic = st.text_input(
        "Research Topic",
        placeholder="e.g.  Advances in nuclear fusion energy — 2025",
    )
with c2:
    st.markdown("<div style='height:1.95rem'></div>", unsafe_allow_html=True)
    run_btn = st.button("Execute", use_container_width=True)


# ─────────────────────────────────────────────────────────────────────────────
# RUN
# ─────────────────────────────────────────────────────────────────────────────
if run_btn:
    if not topic.strip():
        st.warning("Please enter a research topic to begin.")
    else:
        # reset
        for k, v in _defaults.items():
            st.session_state[k] = v
        st.session_state.ran = True

        t0      = time.time()
        pipe_ph = st.empty()
        prog_ph = st.empty()
        spin_ph = st.empty()

        try:
            # Load agents (cached after first run)
            with spin_ph.container():
                with st.spinner("Loading agents…"):
                    search_agent, reader_agent, w_chain, c_chain = get_agents()
            spin_ph.empty()
            log("Agents ready (cache hit or freshly built)", "info")

            # ── Step 1 : Search
            with pipe_ph.container(): render_pipeline(active=0, done=0)
            with prog_ph.container(): prog = st.progress(5, text="🔍  Search Agent scanning the web…")
            log("Search Agent → invoked", "info")

            search_result  = search_agent.invoke({
                "messages": [("user",
                    f"Find recent, reliable and detailed information about: {topic}"
                )]
            })
            search_results = search_result["messages"][-1].content
            log(f"Search done — {len(search_results):,} chars", "success")

            # ── Step 2 : Reader
            with pipe_ph.container(): render_pipeline(active=1, done=1)
            with prog_ph.container(): prog = st.progress(30, text="📄  Reader Agent scraping top URL…")
            log("Reader Agent → invoked", "info")

            reader_result  = reader_agent.invoke({
                "messages": [("user",
                    f"Based on the following search result about '{topic}', "
                    f"pick the most relevant URL and scrape it for deeper content.\n\n"
                    f"Search Results:\n{search_results[:800]}"
                )]
            })
            scraped_content = reader_result["messages"][-1].content
            log(f"Scraping done — {len(scraped_content):,} chars", "success")

            # ── Step 3 : Writer
            with pipe_ph.container(): render_pipeline(active=2, done=2)
            with prog_ph.container(): prog = st.progress(58, text="✍️  Writer Chain composing the report…")
            log("Writer Chain → invoked", "info")

            research_combined = (
                f"SEARCH RESULTS:\n{search_results}\n\n"
                f"DETAILED SCRAPED CONTENT:\n{scraped_content}"
            )
            report     = w_chain.invoke({"topic": topic, "research": research_combined})
            word_count = len(report.split())
            log(f"Report drafted — {word_count:,} words", "success")

            # ── Step 4 : Critic
            with pipe_ph.container(): render_pipeline(active=3, done=3)
            with prog_ph.container(): prog = st.progress(84, text="🧠  Critic Chain reviewing the report…")
            log("Critic Chain → invoked", "info")

            feedback = c_chain.invoke({"report": report})
            log("Critic review complete", "success")

            # ── Done
            elapsed = round(time.time() - t0, 1)
            with prog_ph.container(): prog = st.progress(100, text="✅  Pipeline complete!")
            time.sleep(0.4)
            prog_ph.empty()
            pipe_ph.empty()
            with pipe_ph.container(): render_pipeline(active=-1, done=4)

            st.session_state.results = dict(
                search_results=search_results,
                scraped_content=scraped_content,
                report=report,
                feedback=feedback,
            )
            st.session_state.elapsed = elapsed
            st.session_state.words   = word_count
            log(f"Pipeline finished in {elapsed}s", "success")

        except ImportError as e:
            st.session_state.error = (
                f"ImportError: {e}\n\n"
                "Ensure agents.py lives in the same directory as app.py "
                "and all dependencies are installed."
            )
            pipe_ph.empty(); prog_ph.empty()
            log(str(e), "error")

        except Exception as e:
            st.session_state.error = f"{type(e).__name__}: {e}"
            pipe_ph.empty(); prog_ph.empty()
            log(str(e), "error")


# ─────────────────────────────────────────────────────────────────────────────
# IDLE pipeline (before first run)
# ─────────────────────────────────────────────────────────────────────────────
if not st.session_state.ran:
    render_pipeline()

# ─────────────────────────────────────────────────────────────────────────────
# ERROR display
# ─────────────────────────────────────────────────────────────────────────────
if st.session_state.error:
    render_pipeline()
    st.markdown(
        f'<div class="err-box">⚠  {st.session_state.error}</div>',
        unsafe_allow_html=True,
    )

# ─────────────────────────────────────────────────────────────────────────────
# RESULTS
# ─────────────────────────────────────────────────────────────────────────────
if st.session_state.results:
    r = st.session_state.results

    # Metrics bar
    st.markdown(f"""
    <div class="metrics-row">
        <div class="m-cell"><div class="m-val">{st.session_state.words:,}</div><div class="m-lbl">Report Words</div></div>
        <div class="m-cell"><div class="m-val">{len(r["search_results"]):,}</div><div class="m-lbl">Search Chars</div></div>
        <div class="m-cell"><div class="m-val">{len(r["scraped_content"]):,}</div><div class="m-lbl">Scraped Chars</div></div>
        <div class="m-cell"><div class="m-val">{st.session_state.elapsed}s</div><div class="m-lbl">Total Time</div></div>
    </div>
    """, unsafe_allow_html=True)

    # Raw intelligence
    sec("Raw Intelligence")
    ca, cb = st.columns(2, gap="small")
    with ca:
        rp("SEARCH", "b-mute",  "Search Agent — Web Results",        r["search_results"])
    with cb:
        rp("SCRAPE", "b-amber", "Reader Agent — Scraped Content",     r["scraped_content"])

    # Final report
    sec("Final Report")
    rp("REPORT",   "b-green", f"Research Report — {topic}",          r["report"],    "tall")

    # Critic
    sec("Critic Review")
    rp("CRITIQUE", "b-red",   "Quality Assessment & Feedback",        r["feedback"])

    # Downloads
    st.markdown("<div style='margin-top:1rem'></div>", unsafe_allow_html=True)
    d1, d2, _ = st.columns([2, 2, 5])
    with d1:
        st.download_button(
            "⬇  Report (.txt)",
            data=r["report"],
            file_name=f"report_{topic[:40].replace(' ','_').lower()}.txt",
            mime="text/plain",
            use_container_width=True,
        )
    with d2:
        full = (
            f"TOPIC: {topic}\n{'='*60}\n\n"
            f"SEARCH RESULTS:\n{r['search_results']}\n\n"
            f"SCRAPED CONTENT:\n{r['scraped_content']}\n\n"
            f"FINAL REPORT:\n{r['report']}\n\n"
            f"CRITIC FEEDBACK:\n{r['feedback']}"
        )
        st.download_button(
            "⬇  Full Output (.txt)",
            data=full,
            file_name=f"full_{topic[:40].replace(' ','_').lower()}.txt",
            mime="text/plain",
            use_container_width=True,
        )

# ─────────────────────────────────────────────────────────────────────────────
# TERMINAL LOG
# ─────────────────────────────────────────────────────────────────────────────
render_logs()

# ─────────────────────────────────────────────────────────────────────────────
# FOOTER
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("""
<div style="
    margin-top:5rem;
    padding-top:1.5rem;
    border-top:1px solid rgba(255,255,255,0.04);
    text-align:center;
    font-size:0.58rem;
    letter-spacing:0.22em;
    color:#1c1c2c;
    text-transform:uppercase;
">
ResearchMind AI &nbsp;·&nbsp; LangGraph + LangChain &nbsp;·&nbsp; Multi-Agent Pipeline
</div>
""", unsafe_allow_html=True)