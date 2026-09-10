---
title: "Project LifeOps (Part 3): Core Interactive Modules: Fitness, Library, Cinema, and Professional Kanban Board"
date: 2026-09-15
draft: false
categories: ["Projects", "Web Development"]
tags: ["react", "fastapi", "postgresql", "jsonb", "kanban", "sports", "fitness", "reading", "cinema", "productivity", "frontend"]
image: cover.png
description: "Third installment of the LifeOps series: how I engineered the application's core modules. Dual-view architecture (Cards vs Table), fitness telemetry with pace calculations and PBs, reading and cinema tracking, and an agile Kanban board with progress logs stored in PostgreSQL JSONB."
summary: "We enter the functional engine of LifeOps: exploring dual-view ergonomics (Cards vs Table), workout tracking with dynamic paces and PBs, reading/cinema habits, and a professional Kanban board with chronological progress logging stored in PostgreSQL JSONB. Real code and design decisions inside!"
---

In earlier installments, we engineered the foundational backbone of **LifeOps**: in [Part 1](/en/posts/app-lifeops_part1_arquitectura_backend/) we designed the polymorphic PostgreSQL schema and modular FastAPI backend, and in [Part 2](/en/posts/app-lifeops_part2_frontend_dashboard/) we brought the *Glassmorphism Dark Mode* design system and global 360° Dashboard to life.

Now comes the most defining phase of development: **the day-to-day functional modules**.

A personal operating system fails if it forces users into rigid input forms or scatters daily data across disconnected views. The challenge was articulating three completely disparate life areas under unified design and performance standards:
1. 🏃 **Health & Physical Fitness**: Workout logging across sports with dynamic metrics (distance volume, calories, pace calculations, and Personal Bests).
2. 📚 **Intellectual Culture & Media**: Book tracking with interactive reading progress bars and an entertainment catalog organized by streaming platform.
3. 💼 **Professional Execution**: An agile 4-column Kanban board mapped to projects, equipped with a **chronological progress log powered by PostgreSQL JSONB**.

> [!TIP]
> **Test the live app**: You can explore the production build of LifeOps directly at [https://datalaria.com/apps/lifeops/](https://datalaria.com/apps/lifeops/).

---

### 🗺️ LifeOps Series Roadmap
To understand how every architectural layer fits together, this series spans 5 structured installments:

1. 🟢 **Part 1**: [Personal Operating System Architecture and FastAPI + Supabase Backend](/en/posts/app-lifeops_part1_arquitectura_backend/)
2. 🟢 **Part 2**: [React Frontend with Glassmorphism, 360° Dashboard, and Design System](/en/posts/app-lifeops_part2_frontend_dashboard/)
3. 🟢 **Part 3 (This article)**: Core Interactive Modules: Fitness, Library, Cinema, and Professional Kanban Board
4. ⚪ **Part 4**: [In-Memory Word Dossiers (.docx) & Multi-Sheet Excel Engine (.xlsx)](/en/posts/app-lifeops_part4_informes_word_excel/)
5. ⚪ **Part 5**: [24/7 Zero-Cost Cloud Deployment ($0/month), Mobile UX, and PWA](/en/posts/app-lifeops_part5_deploy_mobile_pwa/)

---

### 1. The UX Dilemma: Dual View Mode (Inspiring Cards vs. Synthesized Table) 🎴📊

When building data-intensive dashboards, designers face a classic user experience tradeoff:
* **The Grid / Cards View**: Visually engaging, spacious, and inspiring. It highlights book covers, movie posters, and workout chips at a glance.
* **The Data Table View**: Irreplaceable when auditing timestamps, comparing heart rates, or scanning through an entire month of logs without endless vertical scrolling.

Instead of forcing a single opinionated view, I built a **persistent dual-mode toggle stored in `localStorage`**:

```jsx
const [viewMode, setViewMode] = useState(() => {
  return localStorage.getItem('lifeops_view_sport') || 'grid';
});

const handleViewChange = (mode) => {
  setViewMode(mode);
  localStorage.setItem('lifeops_view_sport', mode);
};
```

In the header of each module, two unobtrusive buttons with `LayoutGrid` and `Table` icons toggle the presentation mode instantly. Thanks to React and Vite's build architecture, view switches execute in sub-milliseconds without triggering redundant server roundtrips.

---

### 2. Fitness & Performance Module (`SportModule.jsx`) 🏃💨

The fitness module caters to multi-sport athletes practicing running, road cycling, gym strength sessions, and swimming.

```
┌────────────────────────────────────────────────────────────────────────┐
│  🏃 Sport & Fitness                    [ + Log Workout ]       [⊞|≡]   │
├─────────────────┬─────────────────┬─────────────────┬──────────────────┤
│ TOTAL DISTANCE  │ ACTIVE TIME     │ CALORIES        │ PERSONAL BESTS   │
│   142.5 km      │   18.4 hours    │   12,450 kcal   │    4 PBs 🏅      │
├─────────────────┴─────────────────┴─────────────────┴──────────────────┤
│                                                                        │
│ ┌───────────────────────────┐         ┌──────────────────────────────┐ │
│ │ 🏃 RUNNING         🏅 PB  │         │ 🚴 CYCLING                   │ │
│ │ Sunday Long Run           │         │ Mountain Pass Century Ride   │ │
│ │ 2026-09-10                │         │ 2026-09-08                   │ │
│ │ [📍 21.1 km] [⏱️ 1h 48m]  │         │ [📍 65.0 km] [⏱️ 2h 45m]     │ │
│ │ [🔥 1,420 kcal] [❤️ 152bpm]│        │ [🔥 1,890 kcal] [⛰️ +950m]    │ │
│ └───────────────────────────┘         └──────────────────────────────┘ │
└────────────────────────────────────────────────────────────────────────┘
```

#### 2.1. Aggregated High-Level KPIs
Before rendering individual activity items, we compute cumulative totals using in-memory array reducers:

```javascript
const totalKm = workouts.reduce((sum, act) => sum + (act.workout?.distance_km || 0), 0);
const totalMinutes = workouts.reduce((sum, act) => sum + (act.duration_minutes || 0), 0);
const totalCalories = workouts.reduce((sum, act) => sum + (act.workout?.calories || 0), 0);
const pbCount = workouts.filter((act) => act.workout?.personal_best).length;
```

#### 2.2. Segregated FastAPI Payload
When an athlete records an exercise, the client dispatches a structured contract that FastAPI parses into the master table `lifeops.activities` and the child table `lifeops.workouts`:

```javascript
const payload = {
  activity: {
    activity_type: 'sport',
    title: formData.title,
    date: formData.date,
    duration_minutes: parseInt(formData.duration_minutes),
    description: formData.notes,
  },
  workout: {
    workout_type: formData.workout_type, // 'running' | 'cycling' | 'gym'
    distance_km: parseFloat(formData.distance_km) || null,
    calories: parseInt(formData.calories) || null,
    avg_heart_rate: parseInt(formData.avg_heart_rate) || null,
    elevation_m: parseInt(formData.elevation_m) || null,
    personal_best: formData.personal_best,
    notes: formData.notes,
  },
};
```

This ensures shared attributes (dates, general durations, notes) remain globally indexable for the 360° Dashboard, while biometric attributes (elevation gain, heart rate, personal bests) reside in their specialized child table with cascading foreign key guarantees.

---

### 3. Culture & Media Tracking: Books & Cinema 📚🎬

For cultural tracking, the goal was leaving behind fragmented mobile notes in favor of an enriched visual library.

#### 3.1. Interactive Reading Progress (`BooksModule.jsx`)
On each book card, we calculate page completion percentages in real time:

```jsx
const percentage = b.pages_total > 0 
  ? Math.min(100, Math.round((b.pages_read / b.pages_total) * 100)) 
  : 0;

<div className="book-progress-wrapper">
  <div className="progress-info">
    <span>{b.pages_read} / {b.pages_total} pages</span>
    <span className="percentage-tag">{percentage}%</span>
  </div>
  <div className="progress-bar-bg">
    <div 
      className="progress-bar-fill" 
      style={{ 
        width: `${percentage}%`,
        background: percentage === 100 ? 'var(--accent-emerald)' : 'var(--grad-primary)'
      }} 
    />
  </div>
</div>
```

A status filter organizes titles into `reading`, `completed`, and `wishlist`, paired with an interactive 5-star rating system using `lucide-react` icons.

#### 3.2. Streaming Media Catalog (`FilmsModule.jsx`)
The cinema module tracks movies, TV series, and documentaries cataloged by streaming provider (*Netflix, HBO Max, Prime Video, Disney+, Cinema*). Each entry logs release year, director, rating, and personal review notes, answering: *"What were the best films I watched this past quarter?"*.

---

### 4. Professional Execution: The Kanban Board (`KanbanBoard.jsx`) 📋

For professional tasks, I implemented a full Kanban board featuring 4 columns reflecting agile task lifecycles:

1. 📝 **To Do (`todo`)**: Backlog tasks queued for upcoming execution.
2. ⚡ **In Progress (`in_progress`)**: Active work during the current sprint.
3. 🔍 **In Review (`review`)**: Tasks pending review, testing, or third-party feedback.
4. ✅ **Done (`done`)**: Completed deliverables.

```
┌──────────────────┬──────────────────┬──────────────────┬──────────────────┐
│ 📝 TO DO (3)     │ ⚡ IN PROGRESS (2)│ 🔍 IN REVIEW (1) │ ✅ DONE (8)      │
├──────────────────┼──────────────────┼──────────────────┼──────────────────┤
│ ┌──────────────┐ │ ┌──────────────┐ │ ┌──────────────┐ │ ┌──────────────┐ │
│ │ Refactor API │ │ │ Frontend UI  │ │ │ E2E Test Run │ │ │ DB Migration │ │
│ │ 🚨 Critical  │ │ │ 🟡 Medium    │ │ │ 🟢 Low       │ │ │ 2026-09-02   │ │
│ │ 📅 Sep 18    │ │ │ 💬 3 notes   │ │ │ 📅 Today     │ │ │ 💬 5 notes   │ │
│ │ [→ Move]     │ │ │ [←]     [→]  │ │ │ [←]     [→]  │ │ │ [← Move]     │ │
│ └──────────────┘ │ └──────────────┘ │ └──────────────┘ │ └──────────────┘ │
└──────────────────┴──────────────────┴──────────────────┴──────────────────┘
```

#### 4.1. Optimistic UI Updates for Tactile Fluidity
When moving a task from `in_progress` to `review`, waiting for the entire roundtrip (browser → Render API → Supabase → response) introduces an undesirable delay of several hundred milliseconds.

To deliver an instantaneous tactile feel, we execute an **optimistic state update** in React:

```javascript
const handleMoveTask = async (taskId, currentStatus, direction) => {
  const statusOrder = ['todo', 'in_progress', 'review', 'done'];
  const currentIndex = statusOrder.indexOf(currentStatus);
  const targetIndex = direction === 'next' ? currentIndex + 1 : currentIndex - 1;

  if (targetIndex < 0 || targetIndex >= statusOrder.length) return;
  const targetStatus = statusOrder[targetIndex];

  // 1. Instantaneous optimistic update in memory
  setTasks((prev) =>
    prev.map((t) => (t.id === taskId ? { ...t, status: targetStatus } : t))
  );

  // 2. Asynchronous persistence in FastAPI
  try {
    await api.updateTask(taskId, { status: targetStatus });
  } catch (err) {
    console.error('State sync failed, rolling back...', err);
    fetchData(); // Rollback upon network error
  }
};
```

Under normal network conditions, transitions happen with 0ms perceived lag. If connection drops occur, the `catch` handler gracefully restores the verified server state.

---

### 5. Progress Logging: The Power of PostgreSQL JSONB 🗄️⚡

One of LifeOps' most impactful design choices is the **Task Progress Timeline**.

In real-world workflows, deliverables span multiple days and encounter road-blocks or discoveries. Traditional project management software typically enforces normalized relational tables (`task_comments`) with foreign keys, join indexes, and cascade migrations.

In LifeOps, we leverage **PostgreSQL JSONB** columns:

```sql
-- Schema migration in Supabase (lifeops schema)
ALTER TABLE lifeops.tasks ADD COLUMN comments JSONB DEFAULT '[]'::jsonb;
```

#### 5.1. Clean FastAPI Endpoint (`routers/projects.py`)
In the backend, recording a progress note is an atomic operation requiring zero SQL joins:

```python
@tasks_router.post(
    "/{task_id}/comments",
    response_model=TaskResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Add progress comment to task",
)
def add_task_comment(
    task_id: str,
    payload: TaskCommentCreate,
    user: AuthenticatedUser = Depends(get_current_user),
):
    # 1. Fetch existing task record
    task = db("tasks").select("*").eq("id", task_id).eq("user_id", user.id).single().execute().data
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    existing_comments = task.get("comments") or []

    # 2. Append new comment with strict UTC timestamp
    new_comment = {
        "id": str(uuid.uuid4()),
        "text": payload.text.strip(),
        "created_at": dt.datetime.now(dt.timezone.utc).isoformat(),
    }
    existing_comments.append(new_comment)

    # 3. Persist into the JSONB column
    result = db("tasks").update({"comments": existing_comments}).eq("id", task_id).execute()
    return result.data[0]
```

#### 5.2. Frontend Timeline Component
Inside the task edit modal, we render a chronological timeline with timestamps and individual removal actions:

```jsx
<div className="task-comments-timeline">
  {editingTask.comments?.map((comment) => (
    <div key={comment.id} className="comment-bubble glass-panel">
      <div className="comment-header">
        <span className="comment-time">
          <Clock size={12} /> {new Date(comment.created_at).toLocaleString()}
        </span>
        <button onClick={() => handleDeleteComment(comment.id)}>
          <Trash2 size={12} />
        </button>
      </div>
      <p className="comment-body">{comment.text}</p>
    </div>
  ))}
</div>
```

> [!NOTE]
> Storing the progress log as structured JSONB within the task row allows our reporting engine (covered in Part 4) to extract the complete project timeline without executing expensive N+1 database queries.

---

### Conclusion & What's Next 🎯

With our interactive Fitness, Reading, Cinema, and Kanban modules operational, LifeOps is fully equipped to ingest and visualize daily telemetry with speed and ergonomic precision.

However, keeping data trapped inside browser tabs defeats the purpose of an enterprise-grade personal operating system. We need to **package, analyze, and export this data beyond the web**.

In **Part 4** of this series, we will unpack the backend's most technically sophisticated subsystem:
* **In-memory RAM Word document generation (`.docx`)** via `python-docx` using executive templates.
* **Multi-sheet Excel export engine (`.xlsx`)** using `openpyxl`, featuring dedicated tabs for workouts, reading logs, cinema catalogs, and projects.
* **CSV backup streaming with UTF-8 Byte Order Mark (BOM)** for seamless plug-and-play analysis in PowerBI and Excel.

---

### References & Useful Links 🔗

* 🚀 **Production Application**: Try the interactive modules at [datalaria.com/apps/lifeops](https://datalaria.com/apps/lifeops/).
* 🌐 **Production Swagger API**: Tasks and comments endpoints at [lifeops-api.onrender.com/docs](https://lifeops-api.onrender.com/docs).
* 🐘 **PostgreSQL JSONB Documentation**: Semistructured data types at [postgresql.org/docs](https://www.postgresql.org/docs/current/datatype-json.html).
* ⚛️ **React Documentation**: State and optimistic updates at [react.dev](https://react.dev/).
* 🎨 **Lucide Icons**: SVG icon system at [lucide.dev](https://lucide.dev/).

See you in Part 4! How do you currently log progress on long-term personal projects? Let me know in the comments below. 👇
