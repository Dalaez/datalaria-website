---
title: "Project LifeOps (Part 1): Personal Operating System Architecture and FastAPI + Supabase Backend"
date: 2026-09-06
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
2. **Backend on FastAPI ($0/mo)**: Asynchronous Python 3.13 API with strict validation via Pydantic v2.
3. **Database on Supabase ($0/mo)**: Managed PostgreSQL database with 500 MB of storage, JWT authentication, and automated Row Level Security (RLS) policies.

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

In **Part 2** of this series, we will explore the frontend:
* Building the Single Page App with **React 18, Vite, and Glassmorphism design**.
* **Internationalization (i18n)** system for seamless Spanish 🇪🇸 / English 🇬🇧 switching.
* The **Interactive Kanban Board** with inline task editing.
* The **Dual View Mode (Cards vs Synthesized Table)**.

See you in the next post! Feel free to leave a comment below or connect on socials. 👇
