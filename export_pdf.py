"""Generate a nicely formatted PDF portfolio/resume from content data."""

import io
import re
import unicodedata
from fpdf import FPDF

# Common Unicode → ASCII replacements for characters outside Latin-1
_UNICODE_REPLACEMENTS = {
    "\u2018": "'",   # left single quote
    "\u2019": "'",   # right single quote
    "\u201C": '"',   # left double quote
    "\u201D": '"',   # right double quote
    "\u2013": "-",   # en dash
    "\u2014": "--",  # em dash
    "\u2026": "...", # ellipsis
    "\u00A0": " ",   # non-breaking space
    "\u200B": "",    # zero-width space
    "\u200D": "",    # zero-width joiner
    "\uFEFF": "",    # BOM / zero-width no-break space
}


def _sanitize(text: str) -> str:
    """Make *text* safe for Helvetica (Latin-1) by stripping emoji and
    replacing smart punctuation with ASCII equivalents."""

    # 1. Replace known smart-punctuation / special chars
    for orig, repl in _UNICODE_REPLACEMENTS.items():
        text = text.replace(orig, repl)

    # 2. Strip emoji & miscellaneous symbols
    emoji_pattern = re.compile(
        "["
        "\U0000FE00-\U0000FE0F"  # variation selectors
        "\U00002702-\U000027B0"  # dingbats
        "\U0001F600-\U0001F64F"  # emoticons
        "\U0001F300-\U0001F5FF"  # misc symbols & pictographs
        "\U0001F680-\U0001F6FF"  # transport & map
        "\U0001F700-\U0001F77F"  # alchemical
        "\U0001F780-\U0001F7FF"  # geometric shapes ext
        "\U0001F800-\U0001F8FF"  # supplemental arrows-C
        "\U0001F900-\U0001F9FF"  # supplemental symbols
        "\U0001FA00-\U0001FA6F"  # chess symbols
        "\U0001FA70-\U0001FAFF"  # symbols & pictographs ext-A
        "\U00002600-\U000026FF"  # misc symbols
        "\U0000203C-\U00003299"  # misc technical / enclosed
        "]+",
        flags=re.UNICODE,
    )
    text = emoji_pattern.sub("", text)

    # 3. Last-resort: decompose any remaining non-Latin-1 chars to ASCII
    #    (e.g. accented chars → base letter) and drop anything still outside range
    cleaned = []
    for ch in text:
        try:
            ch.encode("latin-1")
            cleaned.append(ch)
        except UnicodeEncodeError:
            # Try unicode decomposition (é → e, ñ → n, etc.)
            decomposed = unicodedata.normalize("NFD", ch)
            ascii_chars = [c for c in decomposed if ord(c) < 256]
            cleaned.append("".join(ascii_chars) if ascii_chars else "")
    return "".join(cleaned).strip()


class PortfolioPDF(FPDF):
    """Custom PDF with header/footer styling."""

    ACCENT = (79, 140, 255)     # blue accent colour
    DARK = (30, 30, 30)
    MUTED = (120, 120, 120)
    LIGHT_BG = (245, 247, 250)
    WHITE = (255, 255, 255)

    def header(self):
        pass  # drawn manually on first page

    def footer(self):
        self.set_y(-15)
        self.set_font("Helvetica", "I", 8)
        self.set_text_color(*self.MUTED)
        self.cell(0, 10, f"Page {self.page_no()}/{{nb}}", align="C")

    # ── helper drawers ──────────────────────────────────────────────────────

    def _section_title(self, title: str):
        """Draw a coloured section heading with an underline."""
        self.ln(6)
        self.set_font("Helvetica", "B", 14)
        self.set_text_color(*self.ACCENT)
        self.cell(0, 10, title, new_x="LMARGIN", new_y="NEXT")
        # accent underline
        x = self.get_x()
        y = self.get_y()
        self.set_draw_color(*self.ACCENT)
        self.set_line_width(0.6)
        self.line(x, y, x + 60, y)
        self.ln(4)

    def _label_value(self, label: str, value: str):
        self.set_font("Helvetica", "B", 10)
        self.set_text_color(*self.DARK)
        self.cell(40, 6, label + ":", new_x="END")
        self.set_font("Helvetica", "", 10)
        self.set_text_color(*self.MUTED)
        self.multi_cell(0, 6, value, new_x="LMARGIN", new_y="NEXT")

    def _tag_badge(self, text: str):
        """Draw a small rounded-rect tag inline."""
        self.set_font("Helvetica", "", 8)
        w = self.get_string_width(text) + 6
        x = self.get_x()
        y = self.get_y()
        self.set_fill_color(*self.LIGHT_BG)
        self.set_draw_color(200, 200, 200)
        self.rect(x, y, w, 5.5, style="DF", round_corners=True, corner_radius=1.5)
        self.set_text_color(*self.ACCENT)
        self.set_xy(x + 3, y + 0.5)
        self.cell(w - 6, 4.5, text)
        self.set_xy(x + w + 2, y)

    # ── skill bar ───────────────────────────────────────────────────────────

    def _skill_bar(self, skill: str, pct: int):
        bar_w = 100
        bar_h = 4
        x_start = self.get_x() + 45
        y = self.get_y()

        # label
        self.set_font("Helvetica", "", 10)
        self.set_text_color(*self.DARK)
        self.cell(45, 6, skill)

        # background track
        self.set_fill_color(*self.LIGHT_BG)
        self.rect(x_start, y + 1, bar_w, bar_h, style="F", round_corners=True, corner_radius=2)

        # filled portion
        self.set_fill_color(*self.ACCENT)
        self.rect(x_start, y + 1, bar_w * pct / 100, bar_h, style="F", round_corners=True, corner_radius=2)

        # percentage text
        self.set_font("Helvetica", "", 8)
        self.set_text_color(*self.MUTED)
        self.set_xy(x_start + bar_w + 3, y)
        self.cell(15, 6, f"{pct}%")
        self.ln(7)


def build_portfolio_pdf(
    profile: dict,
    metrics: list,
    about: str,
    skills: dict,
    projects: list,
    experience: list,
    contact: dict,
) -> bytes:
    """Return the raw bytes of a styled PDF portfolio document."""

    pdf = PortfolioPDF(orientation="P", unit="mm", format="A4")
    pdf.alias_nb_pages()
    pdf.set_auto_page_break(auto=True, margin=20)
    pdf.add_page()

    # ── Hero / title block ──────────────────────────────────────────────────
    pdf.set_fill_color(*PortfolioPDF.ACCENT)
    pdf.rect(0, 0, 210, 52, style="F")

    pdf.set_xy(15, 10)
    pdf.set_font("Helvetica", "B", 24)
    pdf.set_text_color(*PortfolioPDF.WHITE)
    pdf.cell(0, 10, _sanitize(profile["name"]), new_x="LMARGIN", new_y="NEXT")

    pdf.set_x(15)
    pdf.set_font("Helvetica", "", 12)
    pdf.cell(0, 7, _sanitize(profile["title"]), new_x="LMARGIN", new_y="NEXT")

    pdf.set_x(15)
    pdf.set_font("Helvetica", "I", 10)
    pdf.cell(0, 7, _sanitize(profile["tagline"]), new_x="LMARGIN", new_y="NEXT")

    pdf.set_x(15)
    pdf.set_font("Helvetica", "", 9)
    pdf.cell(0, 6, _sanitize(profile["status"]), new_x="LMARGIN", new_y="NEXT")

    pdf.ln(8)

    # ── Metrics row ─────────────────────────────────────────────────────────
    col_w = (210 - 30) / len(metrics)
    y_top = pdf.get_y()
    for i, m in enumerate(metrics):
        x = 15 + i * col_w
        # card background
        pdf.set_fill_color(*PortfolioPDF.LIGHT_BG)
        pdf.rect(x, y_top, col_w - 4, 16, style="F", round_corners=True, corner_radius=2)
        # value
        pdf.set_xy(x + 2, y_top + 2)
        pdf.set_font("Helvetica", "B", 14)
        pdf.set_text_color(*PortfolioPDF.ACCENT)
        pdf.cell(col_w - 8, 6, _sanitize(str(m["value"])), align="C")
        # label
        pdf.set_xy(x + 2, y_top + 9)
        pdf.set_font("Helvetica", "", 8)
        pdf.set_text_color(*PortfolioPDF.MUTED)
        pdf.cell(col_w - 8, 5, _sanitize(m["label"]), align="C")
    pdf.set_y(y_top + 20)

    # ── About ───────────────────────────────────────────────────────────────
    pdf._section_title("About")
    pdf.set_font("Helvetica", "", 10)
    pdf.set_text_color(*PortfolioPDF.DARK)
    pdf.multi_cell(0, 5.5, _sanitize(about), new_x="LMARGIN", new_y="NEXT")

    # ── Skills ──────────────────────────────────────────────────────────────
    pdf._section_title("Skills")
    for skill, pct in skills.items():
        pdf._skill_bar(skill, pct)

    # ── Experience ──────────────────────────────────────────────────────────
    pdf._section_title("Experience")
    for exp in experience:
        pdf.set_font("Helvetica", "B", 10)
        pdf.set_text_color(*PortfolioPDF.DARK)
        pdf.cell(0, 6, _sanitize(exp["title"]), new_x="LMARGIN", new_y="NEXT")

        pdf.set_font("Helvetica", "I", 9)
        pdf.set_text_color(*PortfolioPDF.ACCENT)
        pdf.cell(0, 5, _sanitize(exp["date"]), new_x="LMARGIN", new_y="NEXT")

        if exp.get("description"):
            pdf.set_font("Helvetica", "", 9)
            pdf.set_text_color(*PortfolioPDF.MUTED)
            pdf.multi_cell(0, 5, _sanitize(exp["description"]), new_x="LMARGIN", new_y="NEXT")
        pdf.ln(3)

    # ── Projects ────────────────────────────────────────────────────────────
    pdf._section_title("Projects")
    for proj in projects:
        # title (strip emoji prefix for cleaner PDF)
        pdf.set_font("Helvetica", "B", 10)
        pdf.set_text_color(*PortfolioPDF.DARK)
        pdf.cell(0, 6, _sanitize(proj["title"]), new_x="LMARGIN", new_y="NEXT")

        # description
        pdf.set_font("Helvetica", "", 9)
        pdf.set_text_color(*PortfolioPDF.MUTED)
        pdf.multi_cell(0, 5, _sanitize(proj["description"]), new_x="LMARGIN", new_y="NEXT")

        # tags row
        pdf.ln(1)
        for tag in proj["tags"]:
            pdf._tag_badge(tag)
        pdf.ln(3)

        # link
        link = proj.get("link", "").strip()
        if link:
            pdf.set_font("Helvetica", "U", 8)
            pdf.set_text_color(*PortfolioPDF.ACCENT)
            pdf.cell(0, 5, link, link=link, new_x="LMARGIN", new_y="NEXT")
        pdf.ln(3)

    # ── Contact ─────────────────────────────────────────────────────────────
    pdf._section_title("Contact")
    for key, val in contact.items():
        pdf._label_value(key.capitalize(), val)

    # ── Output ──────────────────────────────────────────────────────────────
    buf = io.BytesIO()
    pdf.output(buf)
    return buf.getvalue()

