---
title: "Project LifeOps (Part 1): Personal Operating System Architecture and FastAPI + Supabase Backend"
date: 2026-09-10
draft: false
categories: ["Projects", "Web Development"]
tags: ["python", "fastapi", "supabase", "react", "postgresql", "backend", "productivity", "data", "cloud", "serverless"]
image: cover.png
description: "First installment of the LifeOps series: how I designed and built my own all-in-one personal & professional operating system at zero cost ($0/month) unifying fitness, books, movies, Kanban tasks and projects with FastAPI and Supabase."
summary: "Tired of juggling 5 different subscription apps for workouts, reading lists, and project management, I built LifeOps: a unified, scalable, and 100% free personal OS powered by FastAPI and Supabase. Here is the architecture breakdown!"
---

How many apps do you use daily to manage your life? If you are anything like me, you probably have one app to track your runs and gym workouts, another to keep tabs on books, a website to rate movies and TV series, and two or three more tools for project management, tasks, and notes.

The result is almost always the same: **scattered data silos, mounting monthly subscription bills, and zero ability to cross-analyze data or generate a consolidated monthly executive review**.

With that problem in mind and true to the Datalaria ethos of "learning by building", I decided to design and engineer **LifeOps**: an **All-in-One Personal & Professional Operating System (OS)** that unifies under a single responsive dashboard:

1. 🏃 **Fitness & Performance**: Track workouts (Running, Cycling, Gym), distance volume, Personal Bests (PB), and calories.
2. 📚 **Reading & Culture**: Book progress tracking, percentage bars, and ratings.
3. 🎬 **Cinema & Entertainment**: Movie, TV series, and documentary catalog organized by platform.
4. 📋 **Professional Portfolio & Tasks**: Interactive Kanban board, budget tracking, and deliverable milestones.
5. 📊 **Reporting & Data Portability**: Streaming Word (`.docx`) executive dossiers, multi-sheet Excel workbooks (`.xlsx`), and raw CSV exports with UTF-8 BOM.

Best of all: **built on top of a rock-solid, production-grade architecture that is 100% Free ($0/month)**.

In this first installment of the series, we dive into the core foundations: **cloud architecture design**, **PostgreSQL relational data modeling**, and building the **high-performance FastAPI backend**. Let's get into it! 🚀

> [!TIP]
> **Test the live app**: You can explore the production build of LifeOps directly at [https://datalaria.com/apps/lifeops/](https://datalaria.com/apps/lifeops/).

---

### 🗺️ LifeOps Series Roadmap
To understand how every architectural layer fits together, this series spans 5 structured installments:

1. 🟢 **Part 1 (This article)**: Personal Operating System Architecture and FastAPI + Supabase Backend.
2. ⚪ **Part 2**: [React Frontend with Glassmorphism, 360° Dashboard, and Design System](/en/posts/app-lifeops_part2_frontend_dashboard/).
3. ⚪ **Part 3**: [Core Interactive Modules: Fitness, Library, Cinema, and Professional Kanban Board](/en/posts/app-lifeops_part3_modulos_kanban/).
4. ⚪ **Part 4**: [In-Memory Word Dossiers (.docx) & Multi-Sheet Excel Engine (.xlsx)](/en/posts/app-lifeops_part4_informes_word_excel/).
5. ⚪ **Part 5**: [24/7 Zero-Cost Cloud Deployment ($0/month), Mobile UX, and PWA](/en/posts/app-lifeops_part5_deploy_mobile_pwa/).

---

### The $0/Month Architecture: How to Run Free at Scale 💡

When architecting LifeOps, the goal wasn't merely to run on `localhost`, but to deploy a production-grade system with zero recurring hosting costs using the most generous free tiers available:

```
┌─────────────────────────────────────────────────────────────┐
│                       CLIENT BROWSER                        │
│            https://datalaria.com/apps/lifeops               │
└──────────────────────────────┬──────────────────────────────┘
                               │ (Proxy Rewrite 200)
                               ▼
┌─────────────────────────────────────────────────────────────┐
│               FRONTEND: Netlify CDN ($0/month)              │
│           React 18 + Vite 8 + i18n (ES/EN) + CSS Glass      │
└──────────────────────────────┬──────────────────────────────┘
                               │
               JWT Auth Token  │  REST API Calls / Streaming
                               ▼
┌─────────────────────────────────────────────────────────────┐
│               BACKEND: FastAPI + Python 3.13                │
│    • In-Memory Docx Generator (python-docx + io.BytesIO)    │
│    • Multi-Sheet Excel Engine (openpyxl)                    │
│    • Anti-DoS Rate Limiting (slowapi) + Strict CORS         │
└──────────────────────────────┬──────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────┐
│              DATABASE: Supabase Managed Cloud               │
│       • PostgreSQL with isolated `lifeops` schema           │
│       • Row Level Security (RLS) & Supabase Auth            │
└─────────────────────────────────────────────────────────────┘
```

1. **Frontend on Netlify ($0/mo)**: Single Page Application built with Vite and served globally with Gzip compression, route-level code splitting, and transparent proxy rewrite under Datalaria's domain.
2. **Backend on FastAPI ($0/mo)**: Asynchronous Python 3.13 API with strict validation via Pydantic v2, hosted on Render with cold-start resilience.
3. **Database on Supabase ($0/mo)**: Managed PostgreSQL database with 500 MB of storage, JWT authentication, and automated Row Level Security (RLS) policies.

> [!NOTE]
> **Render Cold-Start Handling**: Because the backend runs on Render.com's free tier, the container spins down after 15 minutes of inactivity. In the React frontend (detailed in Part 2), we implemented a preloader screen with automatic exponential-backoff retries, ensuring the user experiences zero abrupt connection drops.

---

### Relational Data Modeling: Clean Polymorphism in PostgreSQL 🗄️

One of the biggest design challenges when combining disparate activities (a 10 km run, a 400-page book, or a Netflix movie) is avoiding monolithic tables cluttered with `NULL` columns.

To solve this, I designed a **master table with specialized child extensions (1-to-1)** inside an isolated `lifeops` schema:

```sql
-- 1. Master Activities Table
CREATE TABLE lifeops.activities (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
    activity_type VARCHAR(30) NOT NULL, -- 'sport', 'book', 'film'
    title VARCHAR(200) NOT NULL,
    date DATE NOT NULL DEFAULT CURRENT_DATE,
    duration_minutes INTEGER,
    rating INTEGER CHECK (rating >= 1 AND rating <= 5),
    description TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- 2. Fitness Extension (Workouts)
CREATE TABLE lifeops.workouts (
    activity_id UUID PRIMARY KEY REFERENCES lifeops.activities(id) ON DELETE CASCADE,
    workout_type VARCHAR(50) NOT NULL, -- 'running', 'cycling', 'gym', etc.
    distance_km NUMERIC(6,2),
    calories INTEGER,
    avg_heart_rate INTEGER,
    elevation_m INTEGER,
    personal_best BOOLEAN DEFAULT FALSE,
    notes TEXT
);

-- 3. Reading Extension (Books)
CREATE TABLE lifeops.books (
    activity_id UUID PRIMARY KEY REFERENCES lifeops.activities(id) ON DELETE CASCADE,
    author VARCHAR(150),
    pages_total INTEGER,
    pages_read INTEGER DEFAULT 0,
    status VARCHAR(30) DEFAULT 'reading', -- 'reading', 'completed', 'wishlist'
    genre VARCHAR(50)
);

-- 4. Cinema Extension (Films)
CREATE TABLE lifeops.films (
    activity_id UUID PRIMARY KEY REFERENCES lifeops.activities(id) ON DELETE CASCADE,
    media_type VARCHAR(30) DEFAULT 'movie', -- 'movie', 'series', 'documentary'
    director VARCHAR(150),
    platform VARCHAR(50), -- 'Cine', 'Netflix', 'HBO Max', 'Prime Video'
    genre VARCHAR(50),
    year INTEGER
);
```

#### Why this architecture shines:
* **Blazing Fast Global Aggregations**: Dashboard queries hit only `lifeops.activities` for KPI counts and calendar activity heatmaps.
* **Cascading Referencial Integrity**: When an activity is removed, PostgreSQL's `ON DELETE CASCADE` automatically purges child tables without orphaned rows.
* **Row-Level Security (RLS)**: Each user can only read and mutate their own data via declarative security policies:
  ```sql
  CREATE POLICY "Users can only view their own activities" 
  ON lifeops.activities FOR SELECT 
  USING (auth.uid() = user_id);
  ```

> [!IMPORTANT]
> **Isolated Schemas & Permissions in Supabase**: When maintaining tables in a dedicated schema like `lifeops` (rather than default `public`), ensure you grant explicit schema access (`GRANT USAGE ON SCHEMA lifeops TO authenticated;`) and table permissions to the `authenticated` role. This isolates the operating system's database domain while honoring multi-tenant security.

---

### The FastAPI Backend: Modular Architecture & Strict Typing ⚡

To organize the API cleanly as business domains expand, we follow FastAPI's **Modular Router pattern**:

```
lifeops-api/
├── main.py                  # Entrypoint, Middlewares, Rate Limiter & CORS
├── config.py                # Centralized environment settings with Pydantic Settings
├── middleware/
│   └── auth.py              # Supabase JWT validation & secure user_id extraction
├── models/
│   ├── activity.py          # Pydantic Schemas (Create, Update, Response)
│   └── project.py           # Schemas for Tasks and Projects
├── routers/
│   ├── activities.py        # CRUD endpoints for Fitness, Books & Cinema
│   ├── projects.py          # Endpoints for Kanban Board and Projects
│   ├── stats.py             # Global KPI aggregations & Dashboard metrics
│   ├── reports.py           # Word (.docx) generator & CSV/Excel streaming
│   └── alerts.py            # Intelligent reminder engine
└── services/
    ├── report_generator.py  # In-memory RAM .docx compilation
    └── data_exporter.py     # CSV (BOM) & multi-sheet Excel generator
```

#### Secure Supabase JWT Authentication
Every endpoint processing user data injects the `get_current_user` dependency:

```python
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import jwt

security = HTTPBearer()

async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> AuthenticatedUser:
    token = credentials.credentials
    try:
        payload = jwt.decode(
            token,
            settings.supabase_jwt_secret,
            algorithms=["HS256"],
            audience="authenticated"
        )
        user_id = payload.get("sub")
        if not user_id:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token missing user identity")
        return AuthenticatedUser(id=user_id, email=payload.get("email"))
    except jwt.PyJWTError as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired token")
```

---

### Production Hardening: Rate Limiting & Anti-Abuse 🛡️

Because LifeOps supports on-the-fly Word report compilation and multi-sheet Excel generation, it was crucial to prevent resource starvation or DoS attacks.

We integrated **Rate Limiting with `slowapi`** directly into the FastAPI application:

```python
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

limiter = Limiter(key_func=get_remote_address, default_limits=["120/minute"])
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# Strict rate limit for CPU/memory-intensive Word generation
@router.post("/generate")
@limiter.limit("10/minute")
def generate_report(request: Request, req: GenerateReportRequest, user = Depends(get_current_user)):
    ...
```

If a client exceeds the threshold, the API responds instantly with an **HTTP 429 Too Many Requests**, protecting compute resources.

---

### Conclusion and What's Next 🎯

With our FastAPI backend hardened, the PostgreSQL relational schema operational on Supabase, and rate limiting active, we have a production-grade foundation running at **$0/month**.

In **Part 2** of this series, we dive straight into the frontend:
* Single Page App development with **React 18/19, Vite, and Glassmorphism design**.
* **Internationalization (i18n)** system for instant Spanish 🇪🇸 / English 🇬🇧 locale toggling.
* The **360° Dashboard** architecture with aggregated KPI widgets and interactive **Recharts** visualizations.
* Authentication context (`AuthContext`) and session synchronization with Supabase.

---

### References & Useful Links 🔗

* 🚀 **Production Application**: Try the live app at [datalaria.com/apps/lifeops](https://datalaria.com/apps/lifeops/).
* 🌐 **Production REST API**: Interactive OpenAPI Swagger documentation at [lifeops-api.onrender.com/docs](https://lifeops-api.onrender.com/docs).
* ⚡ **FastAPI Framework**: Official documentation at [fastapi.tiangolo.com](https://fastapi.tiangolo.com/).
* 🗄️ **Supabase Cloud**: Guide to PostgreSQL and Row Level Security at [supabase.com/docs](https://supabase.com/docs).
* 🛡️ **SlowAPI**: Rate limiting for ASGI/FastAPI at [github.com/laurentS/slowapi](https://github.com/laurentS/slowapi).

See you in the next installment! Feel free to leave a comment below or connect on socials. 👇
