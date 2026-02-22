# freelanxur

A modern, content-driven portfolio website built with **Streamlit** and **Python**, deployed on **[Railway](https://railway.app)**.

(previously deployed on AWS ECS however migrated off due to saving costs)

🔗 **Live**: [freelanxur.com](https://freelanxur.com)

---

## Features

- **Dynamic theming** — dark / light mode toggle with theme-aware assets
- **Content-driven** — all portfolio data (profile, skills, projects, experience, contact) managed via a single `content/content.jsonc` config file
- **CV PDF export** — one-click download of a professionally styled single-page CV generated with `fpdf2`
- **Responsive navigation** — branded nav bar with the freelanxur logo as the home button
- **Seeded tag colours** — project tags get consistent, visually distinct colours from a preset palette with hash-based fallback

## Tech Stack

| Layer          | Technology                                                        |
| -------------- | ----------------------------------------------------------------- |
| Frontend       | [Streamlit](https://streamlit.io/) with custom HTML/CSS           |
| PDF Generation | [fpdf2](https://py-pdf.github.io/fpdf2/)                         |
| Containerisation | [Docker](https://www.docker.com/) (multi-stage, `python:3.12-slim`) |
| Package Manager | [uv](https://github.com/astral-sh/uv)                           |
| Cloud          | [Railway](https://railway.app) (primary), AWS ECS Fargate (fallback) |

## Project Structure

```
website/
├── app.py                  # Main Streamlit application
├── export_pdf.py           # CV PDF generation module
├── content/
│   ├── content.jsonc       # All portfolio content (JSONC with comments)
│   └── about_me.md         # About Me section (Markdown)
├── images/                 # Logos and icons
├── .streamlit/
│   └── config.toml         # Streamlit server configuration
├── Dockerfile              # Multi-stage Docker build
├── .dockerignore
├── railway.toml            # Railway deployment config
├── infra/
│   └── task-definition.json  # ECS Fargate task definition (fallback)
├── .github/
│   └── workflows/
│       └── deploy.yml      # ECS deploy pipeline (manual trigger only)
├── pyproject.toml          # Python project & dependencies
└── uv.lock                 # Locked dependency versions
```

## Getting Started

### Prerequisites

- Python 3.10+
- [uv](https://github.com/astral-sh/uv) package manager

### Local Development

```bash
# Clone the repo
git clone https://github.com/rayleighxu7/website.git
cd website

# Install dependencies
uv sync

# Run the app
uv run streamlit run app.py
```

The app will be available at `http://localhost:8501`.

### Docker

```bash
# Build the image
docker build -t freelanxur-website .

# Run the container
docker run -p 8501:8501 freelanxur-website
```

## Content Management

All portfolio content lives in `content/content.jsonc`. Edit this file to update:

| Section      | Description                                                              |
| ------------ | ------------------------------------------------------------------------ |
| `profile`    | Name, tagline, status, avatar, page title/icon                           |
| `metrics`    | Key stats displayed on the home page                                     |
| `skills`     | Skill names and proficiency percentages                                  |
| `projects`   | Project cards with title, description, tags, and links                   |
| `experience` | Work history with dates, titles, and `cv_bullets` (PDF-only descriptions)|
| `contact`    | Email, GitHub, and LinkedIn links                                        |

The **About Me** section is written in Markdown in `content/about_me.md`.

> **Note**: The `cv_bullets` field in each experience entry is only rendered in the downloadable PDF — it does not appear on the website.

## Deployment

### Railway (primary)

The site deploys automatically to **Railway** on every push to `main`. Railway builds the Docker image from the `Dockerfile` and runs it.

- Dashboard: [railway.app](https://railway.app)
- Config: `railway.toml` (health check, restart policy)
- Custom domain + SSL handled by Railway

### AWS ECS Fargate (fallback)

The ECS pipeline is kept dormant as a fallback. The GitHub Actions workflow (`deploy.yml`) is set to **manual trigger only** (`workflow_dispatch`).

To activate the fallback:

1. Go to **Actions > Deploy to AWS ECS (fallback)** in GitHub and click **Run workflow**
2. Scale the ECS service back to 1: `aws ecs update-service --cluster freelanxur-cluster --service freelanxur-website-service --desired-count 1`
3. Update Route 53 DNS to point back to the ALB

| Resource            | Details                                              |
| ------------------- | ---------------------------------------------------- |
| ECR Repository      | `freelanxur-website`                                 |
| ECS Cluster         | `freelanxur-cluster`                                 |
| ECS Service         | `freelanxur-website-service`                         |
| Task Definition     | Fargate, 256 CPU / 512 MB                            |
| DNS                 | Route 53 hosted zone for `freelanxur.com`             |
| Region              | `ap-southeast-2` (Sydney)                             |

| Secret         | Description                                         |
| -------------- | --------------------------------------------------- |
| `AWS_ROLE_ARN` | ARN of the IAM role for GitHub Actions OIDC auth    |

## License

© 2026 Rayleigh Xu. All rights reserved.

