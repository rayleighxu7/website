"""Theme palettes and CSS builder for the portfolio site."""

PALETTES = {
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


def build_css(theme_name: str, psyduck_b64: str, brand_logo_b64: str) -> str:
    """Return the full <style> block for the given theme."""
    T = PALETTES[theme_name]
    is_dark = theme_name == "dark"
    return f"""
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
    /* Brand button styled as logo */
    button[kind="secondary"][data-testid="stBaseButton-secondary"]:has(+ div),
    div[data-testid="stHorizontalBlock"] > div:first-child button {{
        font-size: 1.5rem !important;
        font-weight: 700 !important;
        background: {T['brand_grad']} !important;
        -webkit-background-clip: text !important;
        -webkit-text-fill-color: transparent !important;
        letter-spacing: -0.5px !important;
        border: none !important;
        box-shadow: none !important;
        padding: 0.45rem 1rem !important;
        cursor: pointer !important;
        text-align: left !important;
        display: inline-flex !important;
        align-items: center !important;
        gap: 0.4rem !important;
    }}
    div[data-testid="stHorizontalBlock"] > div:first-child button::before {{
        content: "";
        display: inline-block;
        width: 1.6rem;
        height: 1.6rem;
        flex-shrink: 0;
        background: url("data:image/png;base64,{brand_logo_b64}") no-repeat center / contain;
        -webkit-text-fill-color: initial;
    }}
    div[data-testid="stHorizontalBlock"] > div:first-child button:hover {{
        background: {T['brand_grad']} !important;
        -webkit-background-clip: text !important;
        -webkit-text-fill-color: transparent !important;
        border: none !important;
        opacity: 0.8;
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

    /* ── Duck theme toggle (desktop) ────────────── */
    div[data-testid="stHorizontalBlock"]:has([data-testid="stPopover"]) > div:last-child button {{
        padding: 0.45rem 0.5rem !important;
        min-height: 0 !important;
        line-height: 1 !important;
        display: inline-flex !important;
        align-items: center !important;
        justify-content: center !important;
        font-size: 0 !important;
        border: none !important;
        background: transparent !important;
        box-shadow: none !important;
    }}
    div[data-testid="stHorizontalBlock"]:has([data-testid="stPopover"]) > div:last-child button::before {{
        content: "";
        display: inline-block;
        width: 1.6rem;
        height: 1.6rem;
        background: url("data:image/png;base64,{psyduck_b64}") no-repeat center / contain;
        -webkit-text-fill-color: initial;
        filter: {"none" if is_dark else "grayscale(100%) brightness(0.7)"};
        transition: filter 0.3s ease;
    }}
    div[data-testid="stHorizontalBlock"]:has([data-testid="stPopover"]) > div:last-child button:hover::before {{
        filter: none;
    }}

    /* ── Responsive nav (hamburger menu) ──────── */
    div[data-testid="stHorizontalBlock"]:has([data-testid="stPopover"]) {{
        flex-wrap: nowrap !important;
        flex-direction: row !important;
        gap: 0.25rem !important;
    }}
    div[data-testid="stHorizontalBlock"]:has([data-testid="stPopover"]) > div {{
        width: auto !important;
        flex: none !important;
        min-width: 0 !important;
    }}
    div[data-testid="stHorizontalBlock"]:has([data-testid="stPopover"]) > div:first-child {{
        flex: 1 1 auto !important;
    }}
    div[data-testid="stHorizontalBlock"]:has([data-testid="stPopover"]) > div:nth-last-child(-n+2) {{
        min-width: 44px !important;
        flex-shrink: 0 !important;
    }}
    div[data-testid="stHorizontalBlock"]:has([data-testid="stPopover"]) button {{
        white-space: nowrap !important;
    }}
    /* Desktop: hide hamburger, show tabs + duck */
    @media (min-width: 1001px) {{
        div[data-testid="stHorizontalBlock"]:has([data-testid="stPopover"]) > div:nth-child(5) {{
            display: none !important;
        }}
    }}
    /* Narrow: hide tabs + duck, show hamburger */
    @media (max-width: 1000px) {{
        div[data-testid="stHorizontalBlock"]:has([data-testid="stPopover"]) > div:nth-child(n+2):nth-last-child(n+3),
        div[data-testid="stHorizontalBlock"]:has([data-testid="stPopover"]) > div:last-child {{
            display: none !important;
        }}
    }}
    /* Hamburger button */
    div[data-testid="stHorizontalBlock"]:has([data-testid="stPopover"]) [data-testid="stPopover"] > div > button,
    div[data-testid="stHorizontalBlock"]:has([data-testid="stPopover"]) .stPopover > div > button {{
        border: none !important;
        background: transparent !important;
        color: {T['accent']} !important;
        -webkit-text-fill-color: {T['accent']} !important;
        font-size: 0 !important;
        padding: 0.55rem !important;
        min-width: 40px !important;
        min-height: 40px !important;
        border-radius: 10px !important;
        transition: background 0.2s ease !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
    }}
    div[data-testid="stHorizontalBlock"]:has([data-testid="stPopover"]) [data-testid="stPopover"] > div > button::after,
    div[data-testid="stHorizontalBlock"]:has([data-testid="stPopover"]) .stPopover > div > button::after {{
        content: "";
        display: block;
        width: 20px;
        height: 2px;
        background: {T['accent']};
        box-shadow: 0 -7px 0 {T['accent']}, 0 7px 0 {T['accent']};
        border-radius: 2px;
    }}
    div[data-testid="stHorizontalBlock"]:has([data-testid="stPopover"]) [data-testid="stPopover"] > div > button:hover,
    div[data-testid="stHorizontalBlock"]:has([data-testid="stPopover"]) .stPopover > div > button:hover {{
        background: {T['card']} !important;
    }}
    [data-testid="stPopover"] > div > button > *,
    .stPopover > div > button > * {{
        display: none !important;
    }}
    /* Popover body */
    [data-testid="stPopoverBody"] {{
        padding: 0.3rem 0 !important;
        background: {T['bg']} !important;
    }}
    [data-testid="stPopoverBody"] > div {{
        background: {T['bg']} !important;
    }}
    [data-testid="stPopoverBody"],
    [data-testid="stPopoverBody"] [data-testid="stVerticalBlockBorderWrapper"],
    [data-testid="stPopoverBody"] [data-testid="stVerticalBlock"] {{
        gap: 0 !important;
        min-height: 0 !important;
    }}
    [data-testid="stPopoverBody"] [data-testid="stVerticalBlock"] > div {{
        padding: 0 !important;
        margin: 0 !important;
    }}
    [data-testid="stPopoverBody"] hr {{
        margin: 0.3rem 0.8rem !important;
    }}
    [data-testid="stPopoverBody"] button {{
        border: none !important;
        background: transparent !important;
        box-shadow: none !important;
        color: {T['text']} !important;
        text-align: left !important;
        padding: 0.6rem 1.2rem !important;
        font-size: 0.95rem !important;
        font-weight: 500 !important;
        width: 100% !important;
        border-radius: 0 !important;
    }}
    [data-testid="stPopoverBody"] button:hover {{
        color: {T['accent']} !important;
        background: {T['card']} !important;
    }}
    [data-testid="stPopoverBody"] button[kind="primary"] {{
        color: {T['accent']} !important;
        font-weight: 600 !important;
    }}
    /* Duck theme toggle inside popover */
    [data-testid="stPopoverBody"] [data-testid="stVerticalBlock"] > div:last-child button {{
        display: inline-flex !important;
        align-items: center !important;
        gap: 0.6rem !important;
    }}
    [data-testid="stPopoverBody"] [data-testid="stVerticalBlock"] > div:last-child button::before {{
        content: "";
        display: inline-block;
        width: 1.3rem;
        height: 1.3rem;
        background: url("data:image/png;base64,{psyduck_b64}") no-repeat center / contain;
        -webkit-text-fill-color: initial;
        flex-shrink: 0;
        filter: {"none" if is_dark else "grayscale(100%) brightness(0.7)"};
        transition: filter 0.3s ease;
    }}
    [data-testid="stPopoverBody"] [data-testid="stVerticalBlock"] > div:last-child button:hover::before {{
        filter: none;
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
    .section-header-sm {{
        font-size: 1.3rem;
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
        transition: all 0.4s ease;
        height: 220px;
        overflow: hidden;
        cursor: pointer;
        position: relative;
        display: flex;
        flex-direction: column;
    }}
    .card-description {{
        flex: 1;
        overflow: hidden;
    }}
    .card-tags {{
        position: absolute;
        bottom: 0;
        left: 0;
        right: 0;
        padding: 0.8rem 1.8rem 1.4rem 1.8rem;
        background: {T['card']};
        z-index: 1;
    }}
    .card:hover {{
        border-color: {T['hover_border']};
        transform: translateY(-2px);
        box-shadow: 0 8px 25px {T['hover_shadow']};
        height: auto;
        max-height: 500px;
    }}
    .card:hover .card-tags {{
        position: relative;
        padding: 0;
        background: none;
    }}
    .card-title {{
        font-size: 1.15rem;
        font-weight: 600;
        color: {T['text']};
        margin-bottom: 0.5rem;
    }}
    .card-description-text {{
        font-size: 0.9rem;
        color: {T['muted']};
        line-height: 1.6;
        margin-bottom: 1rem;
    }}
    .card-icon {{
        width: 36px;
        height: 36px;
        object-fit: contain;
        margin-bottom: 0.8rem;
        border-radius: 6px;
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
        border-radius: 7px;
        height: 10px;
        overflow: hidden;
        margin-bottom: 0.6rem;
        position: relative;
    }}
    .skill-bar-fill {{
        height: 100%;
        border-radius: 10px;
        background: {T['skill_grad']};
        position: relative;
        overflow: hidden;
        animation: skillGrow 1.2s ease-out forwards;
        transform-origin: left;
    }}
    .skill-bar-fill::after {{
        content: "";
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(
            90deg,
            transparent 0%,
            rgba(255,255,255,0.15) 50%,
            transparent 100%
        );
        animation: shimmer 2.5s ease-in-out infinite;
        animation-delay: 1.2s;
    }}
    @keyframes skillGrow {{
        from {{
            transform: scaleX(0);
            opacity: 0.3;
        }}
        to {{
            transform: scaleX(1);
            opacity: 1;
        }}
    }}
    @keyframes shimmer {{
        0% {{ left: -100%; }}
        100% {{ left: 200%; }}
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
    .timeline-header {{
        display: flex;
        align-items: center;
        gap: 0.8rem;
    }}
    .timeline-icon {{
        width: 32px;
        height: 32px;
        object-fit: contain;
        border-radius: 6px;
    }}
    .timeline-date {{
        font-size: 0.8rem;
        color: {T['accent']};
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 1px;
    }}
    .timeline-duration {{
        font-size: 0.7rem;
        color: {T['muted']};
        font-style: italic;
        margin-top: -0.1rem;
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
    @media (max-width: 640px) {{
        .metric-card {{
            margin-bottom: 1rem;
        }}
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

    /* ── Page transition animations ──────────── */
    @keyframes fadeInUp {{
        from {{
            opacity: 0;
            transform: translateY(25px);
        }}
        to {{
            opacity: 1;
            transform: translateY(0);
        }}
    }}
    @keyframes fadeIn {{
        from {{ opacity: 0; }}
        to {{ opacity: 1; }}
    }}
    @keyframes slideInLeft {{
        from {{
            opacity: 0;
            transform: translateX(-30px);
        }}
        to {{
            opacity: 1;
            transform: translateX(0);
        }}
    }}
    @keyframes scaleIn {{
        from {{
            opacity: 0;
            transform: scale(0.95);
        }}
        to {{
            opacity: 1;
            transform: scale(1);
        }}
    }}

    .hero-container {{
        opacity: 0;
        animation: scaleIn 0.6s ease-out forwards;
    }}
    .metric-card {{
        opacity: 0;
        animation: fadeInUp 0.5s ease-out forwards;
    }}
    .section-header, .section-header-sm {{
        opacity: 0;
        animation: slideInLeft 0.4s ease-out forwards;
    }}
    .section-subheader {{
        opacity: 0;
        animation: fadeIn 0.5s ease-out 0.15s forwards;
    }}
    .section-body {{
        opacity: 0;
        animation: fadeIn 0.5s ease-out 0.25s forwards;
    }}
    .section-divider {{
        opacity: 0;
        animation: fadeIn 0.6s ease-out forwards;
    }}
    .card {{
        opacity: 0;
        animation: fadeInUp 0.5s ease-out forwards;
    }}
    .contact-card {{
        opacity: 0;
        animation: fadeInUp 0.5s ease-out forwards;
    }}
    .timeline-item {{
        opacity: 0;
        animation: fadeInUp 0.5s ease-out forwards;
    }}
    .skill-bar-fill {{
        opacity: 0;
        animation: skillGrow 1.2s ease-out forwards;
    }}
    .footer {{
        animation: fadeIn 0.6s ease-out 0.4s forwards;
        opacity: 0 !important;
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
    """
