# Content Reorganisation Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Reorganise the portfolio's information architecture so visitors see services and projects before bio, replace skill bars with a tag cloud, inline metrics into the hero, and add CTA buttons.

**Architecture:** Single-page FastAPI portfolio. Content from JSON/Markdown via cached API endpoints. Vanilla JS IIFE renders all sections. CSS uses HSL-based theming with glassmorphic cards. One new API endpoint (`/api/tech-stack`), one new content file (`tech_stack.json`). All other changes are frontend-only reordering and restyling.

**Tech Stack:** FastAPI, Jinja2, vanilla JS (IIFE), CSS custom properties, no build tools.

**Design doc:** `docs/plans/2026-02-27-content-reorganisation-design.md`

---

### Task 1: Create tech stack content file

**Files:**
- Create: `content/tech_stack.json`

**Step 1: Create the content file**

```json
{
  "categories": [
    { "name": "Languages", "tags": ["Python", "SQL", "JavaScript", "HTML/CSS"] },
    { "name": "Data", "tags": ["BigQuery", "Fivetran", "Excel", "Pandas"] },
    { "name": "Cloud & DevOps", "tags": ["AWS", "Docker", "CI/CD", "GitHub Actions"] },
    { "name": "Frameworks & Tools", "tags": ["FastAPI", "Streamlit", "Git", "Hex.Tech"] }
  ]
}
```

**Step 2: Commit**

```bash
git add content/tech_stack.json
git commit -m "feat: add tech stack content file"
```

---

### Task 2: Create tech stack API endpoint

**Files:**
- Create: `app/api/tech_stack.py`
- Modify: `app/main.py:1-38`

**Step 1: Create the endpoint file**

Follow the pattern from `app/api/skills.py`. Create `app/api/tech_stack.py`:

```python
from fastapi import APIRouter
from pydantic import BaseModel

from app.api.content import load_json

router = APIRouter(prefix="/api", tags=["content"])


class TechCategory(BaseModel):
    name: str
    tags: list[str]


class TechStackResponse(BaseModel):
    categories: list[TechCategory]


@router.get("/tech-stack", response_model=TechStackResponse)
async def get_tech_stack():
    return load_json("tech_stack.json")
```

**Step 2: Register in `app/main.py`**

Add import after line 16 (`from app.api.about import router as about_router`):

```python
from app.api.tech_stack import router as tech_stack_router
```

Add registration after line 34 (`app.include_router(about_router)`):

```python
app.include_router(tech_stack_router)
```

**Step 3: Verify the endpoint works**

Run: `cd /Users/rxu/VSCode/personal/website-fastapi && python -c "from app.api.tech_stack import router; print('OK')"`
Expected: `OK`

**Step 4: Commit**

```bash
git add app/api/tech_stack.py app/main.py
git commit -m "feat: add /api/tech-stack endpoint"
```

---

### Task 3: Update HTML — reorder sections, update nav, update footer

**Files:**
- Modify: `templates/index.html`

This is the structural backbone. New section order:
1. Hero (unchanged element, content changed via JS)
2. Services (new standalone section)
3. Projects (moved up)
4. About (slimmed — remove services subheader/grid)
5. Experience (unchanged)
6. Tech Stack (replaces Skills)
7. Contact (unchanged element, content changed via JS)
8. Footer (remove CV download button)

**Step 1: Update nav links (lines 39-44)**

Replace:
```html
            <div class="nav-links">
                <a href="#about" class="nav-link">About</a>
                <a href="#projects" class="nav-link">Projects</a>
                <a href="#experience" class="nav-link">Experience</a>
                <a href="#contact" class="nav-link">Contact</a>
            </div>
```

With:
```html
            <div class="nav-links">
                <a href="#services" class="nav-link">Services</a>
                <a href="#projects" class="nav-link">Projects</a>
                <a href="#about" class="nav-link">About</a>
                <a href="#experience" class="nav-link">Experience</a>
                <a href="#contact" class="nav-link">Contact</a>
            </div>
```

**Step 2: Update mobile menu links (lines 59-64)**

Replace:
```html
    <div id="mobile-menu" class="mobile-menu">
        <a href="#about" class="mobile-link">About</a>
        <a href="#projects" class="mobile-link">Projects</a>
        <a href="#experience" class="mobile-link">Experience</a>
        <a href="#contact" class="mobile-link">Contact</a>
    </div>
```

With:
```html
    <div id="mobile-menu" class="mobile-menu">
        <a href="#services" class="mobile-link">Services</a>
        <a href="#projects" class="mobile-link">Projects</a>
        <a href="#about" class="mobile-link">About</a>
        <a href="#experience" class="mobile-link">Experience</a>
        <a href="#contact" class="mobile-link">Contact</a>
    </div>
```

**Step 3: Replace everything between hero and footer (lines 76-126)**

Remove the old Metrics, About (with Services sub-section), Projects, Experience, Skills, and Contact sections. Replace with the new order:

```html
    <!-- Services Section -->
    <section id="services" class="section animate-on-scroll">
        <div class="section-content">
            <h2 class="section-title">Services</h2>
            <p class="section-subtitle">What I can do for you</p>
            <div id="services-content" class="services-grid"></div>
        </div>
    </section>

    <!-- Projects Section -->
    <section id="projects" class="section animate-on-scroll">
        <div class="section-content">
            <h2 class="section-title">Projects</h2>
            <p class="section-subtitle">A selection of things I have worked on</p>
            <div id="projects-content" class="projects-grid"></div>
        </div>
    </section>

    <!-- About Section -->
    <section id="about" class="section animate-on-scroll">
        <div class="section-content">
            <h2 class="section-title">About</h2>
            <div id="about-content"></div>
        </div>
    </section>

    <!-- Experience Section -->
    <section id="experience" class="section animate-on-scroll">
        <div class="section-content">
            <h2 class="section-title">Experience</h2>
            <div id="experience-content" class="timeline"></div>
        </div>
    </section>

    <!-- Tech Stack Section -->
    <section id="tech-stack" class="section animate-on-scroll">
        <div class="section-content">
            <h3 class="section-subheader">Tech Stack</h3>
            <div id="tech-stack-content"></div>
        </div>
    </section>

    <!-- Contact Section -->
    <section id="contact" class="section animate-on-scroll">
        <div class="section-content">
            <h2 class="section-title">Get In Touch</h2>
            <p class="section-subtitle">I'd love to hear from you</p>
            <div id="contact-content" class="contact-grid"></div>
        </div>
    </section>
```

Key changes:
- Metrics section removed entirely (will be inlined into hero via JS)
- Services promoted to standalone section with `section-title` h2
- About section slimmed — no `about-grid` class, no services subheader/grid, no `about-col-title` columns
- Skills section replaced by Tech Stack section (ID: `tech-stack`)

**Step 4: Simplify footer (lines 128-134)**

Replace:
```html
    <footer class="footer">
        <img src="/static/images/gold-logo-transparent-bg.PNG" alt="" class="footer-watermark" aria-hidden="true">
        <div class="footer-content">
            <span id="footer-text"></span>
            <a href="/api/download-cv" class="btn btn-accent" download>Download CV</a>
        </div>
    </footer>
```

With:
```html
    <footer class="footer">
        <img src="/static/images/gold-logo-transparent-bg.PNG" alt="" class="footer-watermark" aria-hidden="true">
        <div class="footer-content">
            <span id="footer-text"></span>
        </div>
    </footer>
```

**Step 5: Commit**

```bash
git add templates/index.html
git commit -m "feat: reorder HTML sections for content reorganisation"
```

---

### Task 4: Update JS — Hero enhancements (inline metrics + CTA buttons)

**Files:**
- Modify: `static/js/main.js` — `renderHero` function (lines 450-508)

**Step 1: Update `renderHero` to accept metrics and render stat strip + CTAs**

The function signature changes from `renderHero(profile)` to `renderHero(profile, metrics)`.

Replace the entire `renderHero` function (lines 450-508) with:

```javascript
    function renderHero(profile, metrics) {
        var container = document.getElementById('hero-content');
        if (!container) return;

        // Add glow orb behind hero content
        var heroSection = document.getElementById('hero');
        if (heroSection && !heroSection.querySelector('.hero-glow')) {
            var glow = document.createElement('div');
            glow.className = 'hero-glow';
            heroSection.querySelector('.section-content').appendChild(glow);
        }

        var statusClass = profile.status_available ? 'available' : 'unavailable';
        var fullName = profile.first_name + ' ' + profile.last_name;

        // If the loader brand still exists, render a slot for it to morph into;
        // otherwise (loader skipped / hard refresh) render the title directly.
        var loaderBrand = document.querySelector('.loader-brand');
        var titleHtml = loaderBrand
            ? '<div class="hero-title-slot"></div>'
            : '<div class="hero-title">' +
                  '<img src="/static/images/gold-logo-transparent-bg.PNG" alt="freelanxur" class="logo-img" height="60">' +
                  '<span class="title-text">freelanxur</span>' +
              '</div>';

        // Build inline stat strip from metrics
        var statsHtml = '<div class="hero-stats">';
        metrics.forEach(function (m, i) {
            var parsed = parseMetricValue(m.value);
            if (i > 0) statsHtml += '<span class="hero-stat-divider"></span>';
            statsHtml +=
                '<div class="hero-stat">' +
                    '<span class="hero-stat-value" data-target="' + parsed.target + '" data-suffix="' + escapeHTML(parsed.suffix) + '">0' + escapeHTML(parsed.suffix) + '</span>' +
                    '<span class="hero-stat-label">' + escapeHTML(m.label) + '</span>' +
                '</div>';
        });
        statsHtml += '</div>';

        // CTA buttons
        var ctaHtml =
            '<div class="hero-ctas">' +
                '<a href="#contact" class="btn btn-ghost">Get in touch</a>' +
                '<a href="/api/download-cv" class="btn btn-accent" download>Download CV</a>' +
            '</div>';

        container.innerHTML =
            '<p class="hero-greeting">Hi, I\'m</p>' +
            '<h1 class="hero-name"><span class="typing-text">' + escapeHTML(fullName) + '</span></h1>' +
            titleHtml +
            '<p class="hero-tagline">' + escapeHTML(profile.tagline) + '</p>' +
            '<div class="status-badge ' + statusClass + '">' +
                '<span class="status-dot"></span>' +
                escapeHTML(profile.status) +
            '</div>' +
            statsHtml +
            ctaHtml;

        // Trigger typing animation after a short delay
        requestAnimationFrame(function () {
            var typingEl = container.querySelector('.typing-text');
            if (typingEl) {
                typingEl.style.display = 'inline-block';
                typingEl.style.whiteSpace = 'nowrap';
                var naturalWidth = typingEl.scrollWidth;
                typingEl.style.setProperty('--typing-width', naturalWidth + 'px');
                typingEl.style.overflow = 'hidden';
                typingEl.style.borderRight = '3px solid var(--accent)';
                typingEl.style.width = '0';
                typingEl.style.animation = 'typing 1.8s steps(40, end) forwards, blink 0.75s step-end infinite';
            }
        });

        // Apply staggered entrance to hero children (skip title slot, brand fills it)
        var heroChildren = container.children;
        for (var i = 0; i < heroChildren.length; i++) {
            if (!heroChildren[i].classList.contains('hero-title-slot')) {
                heroChildren[i].classList.add('hero-stagger');
            }
        }

        // Fire hero stat count-ups via IntersectionObserver
        var heroStats = container.querySelectorAll('.hero-stat-value[data-target]');
        if (heroStats.length) {
            var statsObserver = new IntersectionObserver(function (entries) {
                entries.forEach(function (entry) {
                    if (entry.isIntersecting) {
                        heroStats.forEach(function (el) { animateCountUp(el); });
                        statsObserver.disconnect();
                    }
                });
            }, { threshold: 0.3 });
            statsObserver.observe(container.querySelector('.hero-stats'));
        }
    }
```

**Step 2: Commit**

```bash
git add static/js/main.js
git commit -m "feat: hero inline metrics stat strip and CTA buttons"
```

---

### Task 5: Update JS — About renderer slimmed to single column

**Files:**
- Modify: `static/js/main.js` — `renderAbout` function (lines 526-533)

**Step 1: Replace `renderAbout` with single-column version**

Replace:
```javascript
    function renderAbout(about) {
        var container = document.getElementById('about-content');
        if (!container) return;

        container.innerHTML =
            '<div class="about-text-col"><h3 class="about-col-title">About Me</h3><div class="about-text">' + about.about_me + '</div></div>' +
            '<div class="about-logo-col"><h3 class="about-col-title">The Logo</h3><div class="about-text">' + about.about_logo + '</div></div>';
    }
```

With:
```javascript
    function renderAbout(about) {
        var container = document.getElementById('about-content');
        if (!container) return;

        container.innerHTML = '<div class="about-text">' + about.about_me + '</div>';
    }
```

**Step 2: Commit**

```bash
git add static/js/main.js
git commit -m "feat: slim about section to single column bio only"
```

---

### Task 6: Update JS — Tech stack renderer (replaces skills)

**Files:**
- Modify: `static/js/main.js` — replace `renderSkills` function (lines 535-554)

**Step 1: Replace `renderSkills` with `renderTechStack`**

Replace the entire `renderSkills` function with:

```javascript
    function renderTechStack(techStack) {
        var container = document.getElementById('tech-stack-content');
        if (!container) return;

        var html = '';
        techStack.categories.forEach(function (cat) {
            html += '<div class="tech-category">';
            html += '<span class="tech-category-label">' + escapeHTML(cat.name) + '</span>';
            html += '<div class="tech-tags">';
            cat.tags.forEach(function (tag) {
                var hue = tagHue(tag);
                html +=
                    '<span class="tech-tag animate-on-scroll" style="' +
                        'background: hsla(' + hue + ', 70%, 50%, var(--tag-bg-alpha)); ' +
                        'color: hsla(' + hue + ', 70%, 70%, var(--tag-text-alpha));">' +
                        escapeHTML(tag) +
                    '</span>';
            });
            html += '</div></div>';
        });
        container.innerHTML = html;
    }
```

**Step 2: Commit**

```bash
git add static/js/main.js
git commit -m "feat: replace renderSkills with renderTechStack tag cloud"
```

---

### Task 7: Update JS — Projects "More on GitHub" card

**Files:**
- Modify: `static/js/main.js` — `renderProjects` function (lines 572-607)

**Step 1: Add "More on GitHub" card after rendering all project cards**

After the `projects.forEach(...)` loop and before `container.innerHTML = html;`, add:

```javascript
        // "More on GitHub" card
        html +=
            '<a class="project-card project-card-github animate-on-scroll" href="https://github.com/rayleighxu7" target="_blank" rel="noopener" style="animation-delay: ' + (projects.length * 0.1) + 's">' +
                '<div class="github-card-inner">' +
                    '<svg class="github-card-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="7" y1="17" x2="17" y2="7"/><polyline points="7 7 17 7 17 17"/></svg>' +
                    '<span class="github-card-text">More on GitHub</span>' +
                '</div>' +
            '</a>';
```

**Step 2: Commit**

```bash
git add static/js/main.js
git commit -m "feat: add 'More on GitHub' card to projects grid"
```

---

### Task 8: Update JS — Contact section with CV download card

**Files:**
- Modify: `static/js/main.js` — `renderContact` function (lines 626-651)

**Step 1: Add a 4th card for CV download**

After the LinkedIn card (ending with the `</a>` before the semicolon), add:

```javascript
            '<a class="contact-card glow-card animate-on-scroll" href="/api/download-cv" download style="animation-delay: 0.3s">' +
                '<div class="contact-icon">\uD83D\uDCC4</div>' +
                '<div class="contact-label">Download CV</div>' +
                '<div class="contact-value">One-page PDF</div>' +
            '</a>';
```

Note: `\uD83D\uDCC4` is the 📄 page emoji. Alternatively use a simpler character.

**Step 2: Commit**

```bash
git add static/js/main.js
git commit -m "feat: add CV download as 4th contact card"
```

---

### Task 9: Update JS — Init function (API calls, render order, nav highlighting)

**Files:**
- Modify: `static/js/main.js` — `init` function (lines 863-905), data fetching (lines 911-920), scroll indicator (lines 241-249), nav highlighting (lines 315-354), scroll animations (lines 668-709)

**Step 1: Update `Promise.all` data fetching (lines 911-920)**

Replace:
```javascript
    var dataPromise = Promise.all([
        fetchJSON('/api/profile'),
        fetchJSON('/api/metrics'),
        fetchJSON('/api/about'),
        fetchJSON('/api/skills'),
        fetchJSON('/api/services'),
        fetchJSON('/api/projects'),
        fetchJSON('/api/experience'),
        fetchJSON('/api/contact')
    ]);
```

With:
```javascript
    var dataPromise = Promise.all([
        fetchJSON('/api/profile'),
        fetchJSON('/api/metrics'),
        fetchJSON('/api/about'),
        fetchJSON('/api/tech-stack'),
        fetchJSON('/api/services'),
        fetchJSON('/api/projects'),
        fetchJSON('/api/experience'),
        fetchJSON('/api/contact')
    ]);
```

Note: slot 3 changes from `/api/skills` to `/api/tech-stack`. Variable name in init changes accordingly.

**Step 2: Update `init` function variable assignments and render calls**

Replace the variable assignments and render calls inside `init` (lines 871-896):

```javascript
            var profile    = results[0];
            var metrics    = results[1];
            var about      = results[2];
            var techStack  = results[3];
            var services   = results[4];
            var projects   = results[5];
            var experience = results[6];
            var contact    = results[7];

            renderHero(profile, metrics);
            setupHeroParallax();
            renderServices(services);
            renderProjects(projects);
            renderAbout(about);
            renderExperience(experience);
            renderTechStack(techStack);
            renderContact(contact);

            setupScrollAnimations();
            setupTitleAnimations();
            setupCardGlow();
            setupTimelineAnimations();
            setupMagneticButtons();
            setupBackToTop();
            setupNavHighlighting();
```

Key changes:
- `skills` → `techStack`, `renderSkills(skills)` → `renderTechStack(techStack)`
- `renderHero(profile)` → `renderHero(profile, metrics)`
- `renderMetrics(metrics)` removed (metrics now rendered inside hero)
- Render order follows new section order

**Step 3: Update scroll indicator click target (lines 241-249)**

The scroll indicator currently scrolls to `#metrics`. Change it to scroll to `#services` (the new section after hero).

Replace:
```javascript
            scrollIndicator.addEventListener('click', function () {
                var metricsSection = document.getElementById('metrics');
                if (metricsSection) {
                    metricsSection.scrollIntoView({ behavior: 'smooth' });
                }
            });
```

With:
```javascript
            scrollIndicator.addEventListener('click', function () {
                var servicesSection = document.getElementById('services');
                if (servicesSection) {
                    servicesSection.scrollIntoView({ behavior: 'smooth' });
                }
            });
```

**Step 4: Update nav highlighting section map (lines 322-330)**

Replace:
```javascript
        var sectionToNav = {
            hero: null,
            metrics: null,
            about: '#about',
            projects: '#projects',
            experience: '#experience',
            skills: '#experience',
            contact: '#contact'
        };
```

With:
```javascript
        var sectionToNav = {
            hero: null,
            services: '#services',
            projects: '#projects',
            about: '#about',
            experience: '#experience',
            'tech-stack': '#experience',
            contact: '#contact'
        };
```

Note: `tech-stack` maps to `#experience` nav link (same grouping as old skills).

**Step 5: Update scroll animations — remove skills-specific observer (lines 691-708)**

Remove the entire skills-specific observer block:
```javascript
        // Skills-specific observer: animate skill bars when the skills section enters view
        var skillsSection = document.getElementById('skills');
        if (skillsSection) {
            var skillsObserver = new IntersectionObserver(function (entries) {
                entries.forEach(function (entry) {
                    if (entry.isIntersecting) {
                        var fills = entry.target.querySelectorAll('.skill-fill');
                        fills.forEach(function (fill) {
                            fill.classList.add('animate');
                            fill.style.width = fill.dataset.width + '%';
                        });
                        skillsObserver.unobserve(entry.target);
                    }
                });
            }, { threshold: 0.1 });

            skillsObserver.observe(skillsSection);
        }
```

This is no longer needed since skill bars are replaced by tags.

**Step 6: Remove `renderMetrics` function (lines 510-524)**

Delete the entire `renderMetrics` function — metrics are now rendered inline in `renderHero`.

**Step 7: Commit**

```bash
git add static/js/main.js
git commit -m "feat: update init, nav highlighting, and remove old metrics/skills code"
```

---

### Task 10: Update CSS — Hero stat strip and CTA button styles

**Files:**
- Modify: `static/css/style.css`

**Step 1: Add hero stat strip styles**

After the `.status-badge.unavailable .status-dot` block (after line 523), add:

```css
/* Hero Stat Strip */
.hero-stats {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 24px;
    margin-top: 28px;
    flex-wrap: wrap;
}

.hero-stat {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 2px;
}

.hero-stat-value {
    font-size: 1.5rem;
    font-weight: 700;
    background: linear-gradient(135deg, var(--accent-dark), var(--accent), var(--accent-light));
    -webkit-background-clip: text;
    background-clip: text;
    -webkit-text-fill-color: transparent;
    line-height: 1.2;
}

.hero-stat-label {
    font-size: 0.75rem;
    color: var(--text-muted);
    text-transform: uppercase;
    letter-spacing: 0.5px;
    font-weight: 500;
}

.hero-stat-divider {
    width: 1px;
    height: 32px;
    background: var(--card-border);
}

/* Hero CTA Buttons */
.hero-ctas {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 16px;
    margin-top: 28px;
    flex-wrap: wrap;
}

.btn-ghost {
    background: transparent;
    color: var(--text);
    border: 1px solid var(--card-border-hover);
    transition: transform 0.2s ease, box-shadow 0.2s ease, border-color 0.2s ease, color 0.2s ease;
}

.btn-ghost:hover {
    transform: translateY(-2px);
    border-color: var(--accent);
    color: var(--accent);
}

.btn-ghost:active {
    transform: translateY(0);
}
```

**Step 2: Add hero stagger delays for new children**

Update the `.hero-stagger:nth-child()` rules (lines 566-570). The hero now has more children (greeting, name, title, tagline, status, stats, ctas = 7 elements). Add two more stagger entries:

```css
.hero-stagger:nth-child(6) { animation-delay: 0.85s; }
.hero-stagger:nth-child(7) { animation-delay: 1.0s; }
```

**Step 3: Add responsive styles for hero stats**

Inside the `@media (max-width: 768px)` block, add:

```css
    .hero-stats {
        gap: 16px;
    }

    .hero-stat-value {
        font-size: 1.25rem;
    }

    .hero-stat-label {
        font-size: 0.7rem;
    }

    .hero-ctas {
        flex-direction: column;
        gap: 12px;
    }

    .hero-ctas .btn {
        width: 100%;
        max-width: 250px;
        justify-content: center;
    }
```

Inside the `@media (max-width: 480px)` block, add:

```css
    .hero-stats {
        gap: 12px;
    }

    .hero-stat-value {
        font-size: 1.1rem;
    }

    .hero-stat-divider {
        height: 24px;
    }
```

**Step 4: Commit**

```bash
git add static/css/style.css
git commit -m "feat: hero stat strip and CTA button styles"
```

---

### Task 11: Update CSS — Tech stack tag cloud styles

**Files:**
- Modify: `static/css/style.css`

**Step 1: Add tech stack styles**

After the services section styles (after line 777), or replace the old skills section styles (lines 654-720), add:

```css
/* --------------------------------------------------------------------------
   9. TECH STACK (replaces Skills)
   -------------------------------------------------------------------------- */

#tech-stack {
    padding-top: 0;
}

.tech-category {
    margin-bottom: 24px;
}

.tech-category:last-child {
    margin-bottom: 0;
}

.tech-category-label {
    display: block;
    font-size: 0.8rem;
    font-weight: 600;
    color: var(--text-muted);
    text-transform: uppercase;
    letter-spacing: 1px;
    margin-bottom: 10px;
}

.tech-tags {
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
}

.tech-tag {
    padding: 6px 16px;
    border-radius: 20px;
    font-size: 0.85rem;
    font-weight: 500;
    line-height: 1.4;
    transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.tech-tag:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 12px var(--shadow);
}
```

**Step 2: Remove old skill bar styles (lines 654-720)**

Delete the entire skills section:
- `.skill-item` through `.skills-note` (lines 654-720)
- Also remove the `@keyframes skillGrow` (lines 1239-1243) and `@keyframes shimmerSweep` (lines 1245-1252)

**Step 3: Commit**

```bash
git add static/css/style.css
git commit -m "feat: tech stack tag cloud styles, remove skill bar styles"
```

---

### Task 12: Update CSS — Contact grid 4-col, GitHub card, about single-column

**Files:**
- Modify: `static/css/style.css`

**Step 1: Update contact grid to 4 columns (line 991)**

Replace:
```css
.contact-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 24px;
}
```

With:
```css
.contact-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 24px;
}
```

**Step 2: Add tablet responsive for contact grid**

Inside `@media (max-width: 1024px)`, add:
```css
    .contact-grid {
        grid-template-columns: repeat(2, 1fr);
    }
```

The `@media (max-width: 768px)` already has `.contact-grid { grid-template-columns: 1fr; }` which handles mobile.

**Step 3: Add "More on GitHub" project card styles**

After the `.nda-badge` styles (around line 869), add:

```css
.project-card-github {
    background: transparent;
    border: 1px dashed var(--card-border-hover);
    display: flex;
    align-items: center;
    justify-content: center;
    text-decoration: none;
    color: var(--text-secondary);
    min-height: 180px;
    max-height: 180px;
    transition: transform 0.3s ease, border-color 0.3s ease, color 0.3s ease;
}

.project-card-github:hover {
    border-color: var(--accent);
    color: var(--accent);
    transform: translateY(-4px);
    max-height: 180px;
    background: transparent;
    box-shadow: none;
}

.github-card-inner {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 12px;
}

.github-card-icon {
    width: 24px;
    height: 24px;
}

.github-card-text {
    font-size: 1rem;
    font-weight: 600;
}
```

And inside `@media (max-width: 768px)`, add:
```css
    .project-card-github {
        min-height: auto;
        max-height: none;
        padding: 32px;
    }

    .project-card-github:hover {
        max-height: none;
    }
```

**Step 4: Simplify about section styles**

The `.about-grid` 2-column layout (lines 620-625) is no longer needed. The about section is now a single text block. Replace:

```css
.about-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 48px;
    align-items: start;
}
```

With:
```css
.about-grid {
    max-width: 800px;
}
```

Note: We keep the class name for backwards compatibility but simplify it. The `about-content` div no longer has the `about-grid` class in the HTML, but this rule stays harmless.

Also remove the `.about-col-title` styles (lines 642-648) since those column headers are gone:
```css
.about-col-title {
    font-size: 1.2rem;
    font-weight: 600;
    color: var(--accent);
    margin-bottom: 12px;
    margin-top: 0;
}
```

And remove the mobile responsive for `.about-grid` inside `@media (max-width: 768px)`:
```css
    .about-grid {
        grid-template-columns: 1fr;
        gap: 32px;
    }
```

**Step 5: Remove standalone metrics section styles (lines 576-614)**

Since metrics are now inlined in the hero, remove:
- `.metrics-grid` (lines 576-580)
- `.metric-card` through `.metric-label` (lines 582-614)
- The responsive rules for `.metrics-grid` in the three breakpoints
- The `.metric-card` and `.metric-value` responsive overrides

Keep the `[data-theme] .metric-card` glassmorphism box-shadow rules only if you want, or remove those too since metric cards no longer exist.

**Step 6: Update the glassmorphism box-shadow selectors (lines 1051-1063)**

Remove `.metric-card` from both dark and light selectors since metric cards no longer exist.

**Step 7: Update the backdrop-filter fallback (lines 1671-1679)**

Remove `.metric-card` from the fallback selector.

**Step 8: Commit**

```bash
git add static/css/style.css
git commit -m "feat: 4-col contact grid, GitHub card styles, slim about, remove metrics section"
```

---

### Task 13: Visual testing and polish

**Files:**
- All files from previous tasks

**Step 1: Start the dev server**

Run: `cd /Users/rxu/VSCode/personal/website-fastapi && python -m uvicorn app.main:app --reload --port 8000`

**Step 2: Visual checks**

Open `http://localhost:8000` and verify:

1. **Hero**: Name, title, tagline, status badge, stat strip (4 metrics with count-up), two CTA buttons ("Get in touch" ghost, "Download CV" gold)
2. **Services**: Full section with h2 title "Services", subtitle "What I can do for you", 4 glassmorphic cards
3. **Projects**: 5 project cards + 1 "More on GitHub" outline card (6 total in 2-col grid)
4. **About**: Single text block, no logo column, no services sub-section
5. **Experience**: Unchanged timeline
6. **Tech Stack**: Gold h3 "Tech Stack", 4 categories with pill tags, no skill bars
7. **Contact**: 4 cards (Email, GitHub, LinkedIn, Download CV) in a row on desktop
8. **Footer**: Copyright text only, no CV button
9. **Nav**: Services · Projects · About · Experience · Contact
10. **Scroll indicator**: Scrolls to Services section
11. **Nav highlighting**: Services/Projects/About/Experience/Contact highlight correctly; Tech Stack highlights Experience

**Step 3: Mobile testing**

Use browser DevTools responsive mode (375px width):
- Hero stats wrap nicely
- CTA buttons stack vertically
- Services cards single column
- Projects single column, GitHub card adapts
- Contact cards single column
- Nav hamburger menu shows correct links

**Step 4: Fix any visual issues found**

Address spacing, alignment, or overflow issues.

**Step 5: Final commit**

```bash
git add -A
git commit -m "fix: visual polish for content reorganisation"
```

---

## Summary of all files changed

| File | Change |
|------|--------|
| `content/tech_stack.json` | **Created** — categorised tag cloud data |
| `app/api/tech_stack.py` | **Created** — `/api/tech-stack` endpoint |
| `app/main.py` | Import + register `tech_stack_router` |
| `templates/index.html` | Reorder sections, update nav/mobile menu, add services section, slim about, replace skills with tech-stack, simplify footer |
| `static/js/main.js` | `renderHero` takes metrics + renders stat strip/CTAs, `renderAbout` single column, `renderTechStack` replaces `renderSkills`, "More on GitHub" project card, CV contact card, updated init/nav-highlighting/scroll-indicator |
| `static/css/style.css` | Hero stat strip + CTA + ghost button styles, tech stack tag cloud styles, 4-col contact grid, GitHub project card styles, simplified about, removed metrics section/skill bar/shimmer styles |
