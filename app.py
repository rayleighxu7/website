import csv
import io
import json

import streamlit as st
from pathlib import Path

# ── Load external content ────────────────────────────────────────────────────
import re

CONTENT_PATH = Path(__file__).parent / "content/content.jsonc"
ABOUT_PATH = Path(__file__).parent / "content/about_me.md"

with open(CONTENT_PATH, "r", encoding="utf-8") as f:
    raw_content = f.read()
    # Remove JSONC comments while preserving // inside strings (e.g. URLs)
    raw_content = re.sub(
        r'("(?:[^"\\]|\\.)*")|//.*?$|/\*.*?\*/',
        lambda m: m.group(1) if m.group(1) else '',
        raw_content,
        flags=re.MULTILINE | re.DOTALL,
    )
    _content = json.loads(raw_content)

PROFILE = _content["profile"]
METRICS = _content["metrics"]
SKILLS = _content["skills"]
PROJECTS = _content["projects"]
EXPERIENCE = _content["experience"]
CONTACT = _content["contact"]
ABOUT = ABOUT_PATH.read_text(encoding="utf-8").strip()

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title=PROFILE.get("page_title", "My Portfolio"),
    page_icon=PROFILE.get("page_icon", "🎨"),
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── Theme state ──────────────────────────────────────────────────────────────
if "theme" not in st.session_state:
    st.session_state.theme = "dark"


def _toggle_theme():
    st.session_state.theme = "light" if st.session_state.theme == "dark" else "dark"


is_dark = st.session_state.theme == "dark"

# ── Theme palettes ───────────────────────────────────────────────────────────
_PALETTES = {
    "dark": {
        # backgrounds
        "bg":           "#0E1117",
        "bg2":          "#1A1F2B",
        "card":         "#1A1F2B",
        # text
        "text":         "#FAFAFA",
        "text2":        "#D1D5DB",
        "muted":        "#9CA3AF",
        "dim":          "#8B7E5E",
        "dimmer":       "#6B7280",
        "footer":       "#5C5539",
        "subtitle":     "#C9B87A",
        # accent (Psyduck yellow)
        "accent":       "#F5C542",
        "accentL":      "#FBE88A",
        "accentD":      "#E8A317",
        "accentDD":     "#D4A017",
        # hero
        "hero_bg":      "linear-gradient(135deg, #0E1117 0%, #1f1a0e 50%, #0E1117 100%)",
        "hero_border":  "rgba(245,197,66,0.15)",
        "hero_shadow":  "rgba(245,197,66,0.08)",
        # metric
        "metric_bg":    "linear-gradient(135deg, #1A1F2B, #1f1c14)",
        "metric_border": "rgba(245,197,66,0.08)",
        # borders
        "border":       "rgba(255,255,255,0.06)",
        "hover_border": "rgba(245,197,66,0.35)",
        "hover_shadow": "rgba(245,197,66,0.1)",
        "divider":      "rgba(245,197,66,0.1)",
        "timeline_bdr": "rgba(245,197,66,0.3)",
        # badge
        "badge_bg":     "rgba(245,197,66,0.12)",
        "badge_border": "rgba(245,197,66,0.25)",
        # tags
        "tag_bg":       "rgba(245,197,66,0.1)",
        "tag_border":   "rgba(245,197,66,0.18)",
        "tagG_bg":      "rgba(232,163,23,0.1)",
        "tagG_c":       "#E8A317",
        "tagG_border":  "rgba(232,163,23,0.18)",
        "tagP_bg":      "rgba(251,232,138,0.1)",
        "tagP_c":       "#FBE88A",
        "tagP_border":  "rgba(251,232,138,0.18)",
        "tagK_bg":      "rgba(212,160,23,0.1)",
        "tagK_c":       "#D4A017",
        "tagK_border":  "rgba(212,160,23,0.18)",
        # skill bar
        "skillbar_bg":  "rgba(255,255,255,0.06)",
        # nav
        "nav_inactive": "#9CA3AF",
        # gradients
        "hero_grad":    "linear-gradient(135deg, #FBE88A 0%, #F5C542 40%, #E8A317 100%)",
        "brand_grad":   "linear-gradient(135deg, #F5C542, #FBE88A)",
        "metval_grad":  "linear-gradient(135deg, #F5C542, #FBE88A)",
        "skill_grad":   "linear-gradient(90deg, #E8A317, #F5C542, #FBE88A)",
    },
    "light": {
        # backgrounds
        "bg":           "#FAFAF7",
        "bg2":          "#F0EDE5",
        "card":         "#FFFFFF",
        # text
        "text":         "#1A1A2E",
        "text2":        "#333344",
        "muted":        "#555770",
        "dim":          "#7A6F50",
        "dimmer":       "#8B8B8B",
        "footer":       "#8B7E5E",
        "subtitle":     "#7A6F50",
        # accent (richer gold for contrast on light)
        "accent":       "#C88A0A",
        "accentL":      "#E8A317",
        "accentD":      "#B07A09",
        "accentDD":     "#9A6B08",
        # hero
        "hero_bg":      "linear-gradient(135deg, #FAFAF7 0%, #FFF8E1 50%, #FAFAF7 100%)",
        "hero_border":  "rgba(200,138,10,0.18)",
        "hero_shadow":  "rgba(200,138,10,0.06)",
        # metric
        "metric_bg":    "linear-gradient(135deg, #FFFFFF, #FFF8E1)",
        "metric_border": "rgba(200,138,10,0.1)",
        # borders
        "border":       "rgba(0,0,0,0.08)",
        "hover_border": "rgba(200,138,10,0.35)",
        "hover_shadow": "rgba(200,138,10,0.08)",
        "divider":      "rgba(200,138,10,0.15)",
        "timeline_bdr": "rgba(200,138,10,0.3)",
        # badge
        "badge_bg":     "rgba(200,138,10,0.08)",
        "badge_border": "rgba(200,138,10,0.2)",
        # tags
        "tag_bg":       "rgba(200,138,10,0.08)",
        "tag_border":   "rgba(200,138,10,0.2)",
        "tagG_bg":      "rgba(176,122,9,0.08)",
        "tagG_c":       "#9A6B08",
        "tagG_border":  "rgba(176,122,9,0.2)",
        "tagP_bg":      "rgba(200,170,50,0.08)",
        "tagP_c":       "#8B7209",
        "tagP_border":  "rgba(200,170,50,0.2)",
        "tagK_bg":      "rgba(154,107,8,0.08)",
        "tagK_c":       "#856A09",
        "tagK_border":  "rgba(154,107,8,0.18)",
        # skill bar
        "skillbar_bg":  "rgba(0,0,0,0.06)",
        # nav
        "nav_inactive": "#6B7280",
        # gradients (darker for readability on light bg)
        "hero_grad":    "linear-gradient(135deg, #E8A317 0%, #C88A0A 40%, #B07A09 100%)",
        "brand_grad":   "linear-gradient(135deg, #C88A0A, #E8A317)",
        "metval_grad":  "linear-gradient(135deg, #C88A0A, #E8A317)",
        "skill_grad":   "linear-gradient(90deg, #B07A09, #E8A317, #F5C542)",
    },
}

T = _PALETTES[st.session_state.theme]

# ── Load fonts via <link> (more reliable than @import) ───────────────────────
st.markdown(
    '<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">'
    '<link href="https://fonts.googleapis.com/css2?family=Material+Symbols+Rounded:opsz,wght,FILL,GRAD@20..48,100..700,0..1,-50..200" rel="stylesheet">',
    unsafe_allow_html=True,
)

# ── Custom CSS (theme-aware) ─────────────────────────────────────────────────
st.markdown(
    f"""
    <style>
    /* ── App background & base text ────────── */
    .stApp {{
        background-color: {T['bg']} !important;
        color: {T['text']} !important;
    }}

    /* ── Global ─────────────────────────────── */
    html, body, [class*="st-"] {{
        font-family: 'Inter', sans-serif;
    }}
    .block-container {{
        padding-top: 1rem;
        padding-bottom: 2rem;
    }}

    /* ── Streamlit widget overrides ─────────── */
    .stMarkdown {{
        color: {T['text']};
    }}
    .stTextInput label, .stTextArea label {{
        color: {T['text']} !important;
    }}
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea {{
        background-color: {T['card']} !important;
        color: {T['text']} !important;
        border-color: {T['border']} !important;
    }}
    [data-testid="stForm"] {{
        background-color: {T['bg2']} !important;
        border-color: {T['border']} !important;
    }}
    .stFormSubmitButton > button {{
        background-color: {T['accent']} !important;
        color: {T['bg']} !important;
        border: none !important;
        font-weight: 600 !important;
    }}
    .stFormSubmitButton > button:hover {{
        background-color: {T['accentD']} !important;
        color: {T['bg']} !important;
    }}

    /* ── Header navigation ──────────────────── */
    .nav-bar {{
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 0.8rem 1.5rem;
        background: transparent;
        border: none;
        margin-bottom: 2rem;
    }}
    .nav-brand {{
        font-size: 1.15rem;
        font-weight: 700;
        background: {T['brand_grad']};
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-decoration: none;
        letter-spacing: -0.5px;
    }}
    .nav-links {{
        display: flex;
        align-items: center;
        gap: 0.3rem;
    }}
    .nav-link {{
        color: {T['nav_inactive']};
        text-decoration: none;
        font-size: 0.9rem;
        font-weight: 500;
        padding: 0.45rem 1rem;
        border-radius: 8px;
        transition: all 0.2s ease;
        cursor: pointer;
        border: none;
        background: none;
    }}
    .nav-link:hover {{
        color: {T['accent']};
        background: transparent;
    }}
    .nav-link.active {{
        color: {T['accent']};
        background: transparent;
        border: none;
    }}

    /* Strip borders from Streamlit nav buttons */
    div[data-testid="stHorizontalBlock"] button[kind="secondary"],
    div[data-testid="stHorizontalBlock"] button[kind="primary"],
    div[data-testid="stHorizontalBlock"] button[kind="secondaryFormSubmit"],
    div[data-testid="stHorizontalBlock"] button[kind="primaryFormSubmit"] {{
        border: none !important;
        background: transparent !important;
        box-shadow: none !important;
        color: {T['nav_inactive']} !important;
        font-weight: 500 !important;
        font-size: 0.9rem !important;
        font-family: 'Inter', sans-serif !important;
        padding: 0.45rem 1rem !important;
    }}
    div[data-testid="stHorizontalBlock"] button[kind="primary"] {{
        color: {T['accent']} !important;
        font-weight: 600 !important;
        position: relative !important;
    }}
    div[data-testid="stHorizontalBlock"] button[kind="primary"]::after {{
        content: '';
        position: absolute;
        bottom: 4px;
        left: 50%;
        transform: translateX(-50%);
        width: 40%;
        height: 2px;
        background: {T['accent']};
        border-radius: 1px;
    }}
    div[data-testid="stHorizontalBlock"] button:hover {{
        color: {T['accent']} !important;
        background: transparent !important;
        border: none !important;
    }}
    div[data-testid="stHorizontalBlock"] button:focus {{
        box-shadow: none !important;
        border: none !important;
    }}
    div[data-testid="stHorizontalBlock"] button:active {{
        background: transparent !important;
        border: none !important;
    }}

    /* Download button in nav */
    .stDownloadButton > button {{
        border: none !important;
        background: transparent !important;
        box-shadow: none !important;
        color: {T['nav_inactive']} !important;
        font-weight: 500 !important;
        font-size: 0.9rem !important;
        font-family: 'Inter', sans-serif !important;
    }}
    .stDownloadButton > button:hover {{
        color: {T['accent']} !important;
        background: transparent !important;
    }}

    /* ── Hero ────────────────────────────────── */
    .hero-container {{
        text-align: center;
        padding: 4rem 2rem 3rem 2rem;
        background: {T['hero_bg']};
        border-radius: 20px;
        margin-bottom: 2rem;
        border: 1px solid {T['hero_border']};
        box-shadow: 0 8px 32px {T['hero_shadow']};
    }}
    .hero-title {{
        font-size: 3.2rem;
        font-weight: 800;
        background: {T['hero_grad']};
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.5rem;
        letter-spacing: -1px;
    }}
    .hero-subtitle {{
        font-size: 1.35rem;
        color: {T['subtitle']};
        font-weight: 300;
        margin-bottom: 1.5rem;
    }}
    .hero-tagline {{
        font-size: 1rem;
        color: {T['dim']};
        max-width: 600px;
        margin: 0 auto;
        line-height: 1.7;
    }}

    /* ── Status badge ───────────────────────── */
    .status-badge {{
        display: inline-block;
        background: {T['badge_bg']};
        color: {T['accent']};
        padding: 0.35rem 1rem;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: 500;
        margin-bottom: 1.5rem;
        border: 1px solid {T['badge_border']};
    }}

    /* ── Section headers ────────────────────── */
    .section-header {{
        font-size: 1.8rem;
        font-weight: 700;
        color: {T['text']};
        margin-bottom: 0.3rem;
        letter-spacing: -0.5px;
    }}
    .section-subheader {{
        font-size: 1rem;
        color: {T['dim']};
        margin-bottom: 2rem;
    }}

    /* ── Cards ───────────────────────────────── */
    .card-link, .card-link:hover, .card-link:visited {{
        text-decoration: none !important;
        color: inherit !important;
        display: block;
        height: 100%;
    }}
    .card-link *, .card-link:hover * {{
        text-decoration: none !important;
        color: inherit !important;
    }}
    .card {{
        background: {T['card']};
        border-radius: 16px;
        padding: 1.8rem;
        border: 1px solid {T['border']};
        transition: all 0.3s ease;
        height: 100%;
        cursor: pointer;
    }}
    .card:hover {{
        border-color: {T['hover_border']};
        transform: translateY(-2px);
        box-shadow: 0 8px 25px {T['hover_shadow']};
    }}
    .card-title {{
        font-size: 1.15rem;
        font-weight: 600;
        color: {T['text']};
        margin-bottom: 0.5rem;
    }}
    .card-description {{
        font-size: 0.9rem;
        color: {T['muted']};
        line-height: 1.6;
        margin-bottom: 1rem;
    }}

    /* ── Tags ────────────────────────────────── */
    .tag {{
        display: inline-block;
        background: {T['tag_bg']};
        color: {T['accent']};
        padding: 0.25rem 0.65rem;
        border-radius: 6px;
        font-size: 0.75rem;
        font-weight: 500;
        margin-right: 0.4rem;
        margin-bottom: 0.4rem;
        border: 1px solid {T['tag_border']};
    }}
    .tag-green {{
        background: {T['tagG_bg']};
        color: {T['tagG_c']};
        border-color: {T['tagG_border']};
    }}
    .tag-purple {{
        background: {T['tagP_bg']};
        color: {T['tagP_c']};
        border-color: {T['tagP_border']};
    }}
    .tag-pink {{
        background: {T['tagK_bg']};
        color: {T['tagK_c']};
        border-color: {T['tagK_border']};
    }}

    /* ── Skill bars ──────────────────────────── */
    .skill-bar-bg {{
        background: {T['skillbar_bg']};
        border-radius: 8px;
        height: 10px;
        overflow: hidden;
        margin-bottom: 1.2rem;
    }}
    .skill-bar-fill {{
        height: 100%;
        border-radius: 8px;
        background: {T['skill_grad']};
        transition: width 1s ease;
    }}

    /* ── Timeline ────────────────────────────── */
    .timeline-item {{
        border-left: 2px solid {T['timeline_bdr']};
        padding-left: 1.5rem;
        margin-bottom: 2rem;
        position: relative;
    }}
    .timeline-item::before {{
        content: '';
        position: absolute;
        left: -6px;
        top: 4px;
        width: 10px;
        height: 10px;
        border-radius: 50%;
        background: {T['accent']};
    }}
    .timeline-date {{
        font-size: 0.8rem;
        color: {T['accent']};
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 1px;
    }}
    .timeline-title {{
        font-size: 1.1rem;
        font-weight: 600;
        color: {T['text']};
        margin: 0.3rem 0;
    }}
    .timeline-description {{
        font-size: 0.9rem;
        color: {T['muted']};
        line-height: 1.6;
    }}

    /* ── Contact cards ───────────────────────── */
    .contact-card {{
        background: {T['card']};
        border-radius: 12px;
        padding: 1.5rem;
        text-align: center;
        border: 1px solid {T['border']};
        transition: all 0.3s ease;
    }}
    .contact-card:hover {{
        border-color: {T['hover_border']};
    }}
    .contact-icon {{
        font-size: 2rem;
        margin-bottom: 0.5rem;
    }}
    .contact-label {{
        font-size: 0.85rem;
        color: {T['dim']};
        margin-bottom: 0.3rem;
    }}
    .contact-value {{
        font-size: 1rem;
        color: {T['text']};
        font-weight: 500;
    }}

    /* ── Metrics ──────────────────────────────── */
    .metric-card {{
        background: {T['metric_bg']};
        border-radius: 16px;
        padding: 1.5rem;
        text-align: center;
        border: 1px solid {T['metric_border']};
    }}
    .metric-value {{
        font-size: 2.2rem;
        font-weight: 800;
        background: {T['metval_grad']};
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }}
    .metric-label {{
        font-size: 0.85rem;
        color: {T['dim']};
        margin-top: 0.3rem;
    }}

    /* ── Divider ──────────────────────────────── */
    .section-divider {{
        border: none;
        border-top: 1px solid {T['divider']};
        margin: 3rem 0;
    }}

    /* ── Hide sidebar completely ────────────── */
    [data-testid="stSidebar"],
    [data-testid="collapsedControl"],
    [data-testid="stSidebarCollapseButton"] {{
        display: none !important;
    }}

    /* ── Footer ──────────────────────────────── */
    .footer {{
        text-align: center;
        padding: 2rem;
        color: {T['footer']};
        font-size: 0.85rem;
        border-top: 1px solid {T['divider']};
        margin-top: 3rem;
    }}

    /* Hide Streamlit branding */
    #MainMenu {{visibility: hidden;}}
    footer {{visibility: hidden;}}
    header[data-testid="stHeader"] {{
        background: none !important;
        border: none !important;
        height: 0 !important;
        min-height: 0 !important;
        overflow: hidden !important;
    }}

    </style>
    """,
    unsafe_allow_html=True,
)


# ═══════════════════════════════════════════════════════════════════════════════
#  CSV EXPORT
# ═══════════════════════════════════════════════════════════════════════════════


def build_portfolio_csv() -> str:
    """Collect all portfolio data into a single, well-structured CSV string."""
    buf = io.StringIO()
    writer = csv.writer(buf)

    # ── Profile ─────────────────────────────────────────────────────────────
    writer.writerow(["Section", "Field", "Value"])
    writer.writerow([])  # blank spacer row
    writer.writerow(["Profile", "Name", PROFILE["name"]])
    writer.writerow(["Profile", "Title", PROFILE["title"]])
    writer.writerow(["Profile", "Tagline", PROFILE["tagline"]])
    writer.writerow(["Profile", "Status", PROFILE["status"]])

    # ── Metrics ─────────────────────────────────────────────────────────────
    writer.writerow([])
    for m in METRICS:
        writer.writerow(["Metrics", m["label"], m["value"]])

    # ── About ───────────────────────────────────────────────────────────────
    writer.writerow([])
    writer.writerow(["About", "Bio", ABOUT.replace("\n", " ")])

    # ── Skills ──────────────────────────────────────────────────────────────
    writer.writerow([])
    for skill, pct in SKILLS.items():
        writer.writerow(["Skills", skill, f"{pct}%"])

    # ── Projects ────────────────────────────────────────────────────────────
    writer.writerow([])
    for proj in PROJECTS:
        writer.writerow([
            "Projects",
            proj["title"],
            proj["description"],
            "; ".join(proj["tags"]),
            proj.get("link", ""),
        ])

    # ── Experience ──────────────────────────────────────────────────────────
    writer.writerow([])
    for exp in EXPERIENCE:
        writer.writerow([
            "Experience",
            exp["date"],
            exp["title"],
            exp["description"],
        ])

    # ── Contact ─────────────────────────────────────────────────────────────
    writer.writerow([])
    for key, val in CONTACT.items():
        writer.writerow(["Contact", key.capitalize(), val])

    return buf.getvalue()


# ═══════════════════════════════════════════════════════════════════════════════
#  HEADER NAVIGATION
# ═══════════════════════════════════════════════════════════════════════════════

NAV_ITEMS = ["Home", "Projects", "CV", "Contact"]

if "page" not in st.session_state:
    st.session_state.page = "Home"


def _nav_click(item: str):
    st.session_state.page = item


# Build nav links HTML-style with columns  (+ theme toggle + CSV download)
nav_cols = st.columns([3] + [1] * len(NAV_ITEMS) + [0.5, 1], gap="small")

with nav_cols[0]:
    st.markdown(
        f'<div class="nav-brand">{PROFILE["page_title"]}</div>',
        unsafe_allow_html=True,
    )

for i, item in enumerate(NAV_ITEMS, start=1):
    with nav_cols[i]:
        active = st.session_state.page == item
        btn_type = "primary" if active else "secondary"
        st.button(
            item,
            key=f"nav_{item}",
            on_click=_nav_click,
            args=(item,),
            type=btn_type,
            use_container_width=True,
        )

with nav_cols[-2]:
    theme_icon = "☀️" if is_dark else "🌙"
    st.button(
        theme_icon,
        key="theme_toggle",
        on_click=_toggle_theme,
        use_container_width=True,
    )

with nav_cols[-1]:
    csv_data = build_portfolio_csv()
    st.download_button(
        label="📥 CSV",
        data=csv_data,
        file_name="portfolio.csv",
        mime="text/csv",
        use_container_width=True,
    )

st.markdown("")  # spacer
page = st.session_state.page

# ═══════════════════════════════════════════════════════════════════════════════
#  PAGES
# ═══════════════════════════════════════════════════════════════════════════════


def render_home():
    """Hero + About + Skills + quick metrics."""

    # ── Hero ────────────────────────────────────────────────────────────────
    st.markdown(
        f"""
        <div class="hero-container">
            <div class="status-badge">{PROFILE['status']}</div>
            <div class="hero-title">{PROFILE['name']}</div>
            <div class="hero-subtitle">{PROFILE['title']}</div>
            <div class="hero-tagline">{PROFILE['tagline']}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # ── Metrics ─────────────────────────────────────────────────────────────
    cols = st.columns(len(METRICS))
    for col, m in zip(cols, METRICS):
        with col:
            st.markdown(
                f"""
                <div class="metric-card">
                    <div class="metric-value">{m['value']}</div>
                    <div class="metric-label">{m['label']}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    st.markdown('<hr class="section-divider">', unsafe_allow_html=True)

    # ── About ───────────────────────────────────────────────────────────────
    left, right = st.columns([3, 2])

    with left:
        st.markdown(
            '<div class="section-header">About Me</div>',
            unsafe_allow_html=True,
        )
        st.markdown(ABOUT)

    # ── Skills ──────────────────────────────────────────────────────────────
    with right:
        st.markdown(
            '<div class="section-header">Skills</div>',
            unsafe_allow_html=True,
        )
        for skill, pct in SKILLS.items():
            st.markdown(
                f"""
                <div style="display:flex; justify-content:space-between; margin-bottom:0.3rem;">
                    <span style="font-size:0.9rem; color:{T['text2']};">{skill}</span>
                    <span style="font-size:0.8rem; color:{T['dimmer']};">{pct}%</span>
                </div>
                <div class="skill-bar-bg">
                    <div class="skill-bar-fill" style="width:{pct}%"></div>
                </div>
                """,
                unsafe_allow_html=True,
            )
        st.markdown(
            f'<div class="section-subheader" style="margin-top:1rem; font-style:italic; color:{T["dimmer"]}; font-size:0.75rem;">p.s I will never set any skill to 100% - there is always something new to learn</div>',
            unsafe_allow_html=True,
        )


def render_projects():
    """Project showcase grid."""

    st.markdown(
        '<div class="section-header">Projects</div>'
        '<div class="section-subheader">A selection of things I\'ve built</div>',
        unsafe_allow_html=True,
    )

    rows = [PROJECTS[i : i + 2] for i in range(0, len(PROJECTS), 2)]
    for row in rows:
        cols = st.columns(2)
        for col, proj in zip(cols, row):
            tags_html = "".join(
                f'<span class="tag">{tag}</span>'
                for tag in proj["tags"]
            )
            with col:
                link = proj.get("link", "").strip()
                card_inner = f"""
                            <div class="card">
                                <div class="card-title">{proj['title']}</div>
                                <div class="card-description">{proj['description']}</div>
                                <div>{tags_html}</div>
                            </div>"""
                if link:
                    card_html = f'<a href="{link}" target="_blank" class="card-link">{card_inner}</a>'
                else:
                    card_html = f'<div class="card-link" style="cursor: default;">{card_inner}</div>'
                st.markdown(card_html, unsafe_allow_html=True)
                st.write("")  # spacing


def render_experience():
    """Experience timeline."""

    st.markdown(
        '<div class="section-header">Experience</div>'
        '<div class="section-subheader">My professional journey</div>',
        unsafe_allow_html=True,
    )

    for exp in EXPERIENCE:
        st.markdown(
            f"""
            <div class="timeline-item">
                <div class="timeline-date">{exp['date']}</div>
                <div class="timeline-title">{exp['title']}</div>
                <div class="timeline-description">{exp['description']}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )


def render_contact():
    """Contact info + form."""

    st.markdown(
        '<div class="section-header">Get In Touch</div>'
        '<div class="section-subheader">I\'d love to hear from you</div>',
        unsafe_allow_html=True,
    )

    c1, c2, c3, c4 = st.columns(4)
    items = [
        ("📧", "Email", CONTACT["email"]),
        ("📍", "Location", CONTACT["location"]),
        ("🐙", "GitHub", CONTACT["github"]),
        ("💼", "LinkedIn", CONTACT["linkedin"]),
    ]
    for col, (icon, label, value) in zip([c1, c2, c3, c4], items):
        with col:
            st.markdown(
                f"""
                <div class="contact-card">
                    <div class="contact-icon">{icon}</div>
                    <div class="contact-label">{label}</div>
                    <div class="contact-value">{value}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    st.markdown('<hr class="section-divider">', unsafe_allow_html=True)

    st.markdown(
        '<div class="section-header">Send a Message</div>',
        unsafe_allow_html=True,
    )

    with st.form("contact_form", clear_on_submit=True):
        col_a, col_b = st.columns(2)
        with col_a:
            name = st.text_input("Name")
        with col_b:
            email = st.text_input("Email")
        message = st.text_area("Message", height=150)
        submitted = st.form_submit_button("Send Message ✉️", use_container_width=True)
        if submitted:
            if name and email and message:
                st.success("Thanks for reaching out! I'll get back to you soon. 🎉")
            else:
                st.warning("Please fill in all fields.")


# ── Router ──────────────────────────────────────────────────────────────────

if page == "Home":
    render_home()
elif page == "Projects":
    render_projects()
elif page == "CV":
    render_experience()
elif page == "Contact":
    render_contact()

# ── Footer ──────────────────────────────────────────────────────────────────
st.markdown(
    f'<div class="footer">{PROFILE.get("footer", "© 2026")}</div>',
    unsafe_allow_html=True,
)
