---
title: "Proyecto LifeOps (Parte 3): Módulos Interactivos: Deporte, Biblioteca, Cine y Tablero Kanban Profesional"
date: 2026-09-15
draft: false
categories: ["Proyectos", "Desarrollo Web"]
tags: ["react", "fastapi", "postgresql", "jsonb", "kanban", "deporte", "fitness", "lectura", "cine", "productivity", "frontend"]
image: cover.png
description: "Tercera entrega de la serie LifeOps: cómo desarrollé los módulos funcionales de la aplicación. Diseño de vistas duales (Tarjetas vs Tabla), telemetría deportiva con cálculo de ritmos y PBs, gestión de lectura y cine, y un tablero Kanban con bitácora de avances en PostgreSQL JSONB."
summary: "Entramos en el corazón funcional de LifeOps: exploramos la arquitectura de vistas duales (Grid vs Tabla), el tracking deportivo con ritmos y PBs, el catálogo de lecturas y cine, y el tablero Kanban profesional con bitácora cronológica almacenada en PostgreSQL JSONB. ¡Código real y decisiones de diseño!"
---

En las entregas anteriores sentamos las bases estructurales de **LifeOps**: en la [Parte 1](/posts/app-lifeops_part1_arquitectura_backend/) modelamos la base de datos relacional en PostgreSQL y la API modular con FastAPI, y en la [Parte 2](/posts/app-lifeops_part2_frontend_dashboard/) dimos vida al sistema de diseño *Glassmorphism Dark Mode* y al cuadro de mandos global 360°.

Ahora llega el momento más determinante del desarrollo: **los módulos funcionales del día a día**. 

Un sistema operativo personal fracasa si obliga al usuario a adaptarse a formularios rígidos o si fragmenta la información en interfaces inconexas. El reto de esta fase consistía en articular tres áreas vitales muy diferentes entre sí bajo una misma coherencia de diseño:
1. 🏃 **Salud & Rendimiento Físico**: Sesiones deportivas con métricas dinámicas (volumen, calorías, ritmos y récords personales).
2. 📚 **Ocio Intelectual & Cultura**: Seguimiento de libros (porcentajes de avance de lectura) y catálogo audiovisual de cine y series por plataforma.
3. 💼 **Productividad Profesional**: Tablero Kanban ágil de cuatro columnas, vinculado a proyectos y dotado de una **bitácora cronológica de avances almacenada en JSONB**.

> [!TIP]
> **Prueba la aplicación en vivo**: Puedes interactuar con la versión de producción de LifeOps desplegada en [https://datalaria.com/apps/lifeops/](https://datalaria.com/apps/lifeops/).

---

### 🗺️ Hoja de Ruta de la Serie LifeOps
Esta serie documenta el ciclo de vida completo del proyecto a través de 5 entregas estructuradas:

1. 🟢 **Parte 1**: [Arquitectura de un Sistema Operativo Personal y Backend con FastAPI + Supabase](/posts/app-lifeops_part1_arquitectura_backend/)
2. 🟢 **Parte 2**: [Frontend React con Glassmorphism, Dashboard 360° y Sistema de Diseño Dark Mode](/posts/app-lifeops_part2_frontend_dashboard/)
3. 🟢 **Parte 3 (Este artículo)**: Módulos Interactivos: Deporte, Biblioteca, Cine y Tablero Kanban Profesional
4. ⚪ **Parte 4**: [Motor de Informes Ejecutivos en Word (.docx) y Exportación Multi-Hoja en Excel (.xlsx)](/posts/app-lifeops_part4_informes_word_excel/)
5. ⚪ **Parte 5**: [Despliegue 24/7 en la Nube a Coste Cero ($0/mes), Optimización Móvil y PWA](/posts/app-lifeops_part5_deploy_mobile_pwa/)

---

### 1. El Dilema de UX: Modo Dual (Tarjetas Inspiradoras vs. Tabla Sintetizada) 🎴📊

Al diseñar interfaces ricas en datos, surge un compromiso clásico de experiencia de usuario:
* **La vista de Tarjetas (*Grid*)**: Es visualmente atractiva, espaciosa y perfecta para inspirar. Destaca portadas de libros, pósters de cine o resúmenes de carreras con chips de colores.
* **La vista de Tabla (*Data Table*)**: Es insustituible cuando se necesita auditar rápidamente fechas, comparar ritmos cardíacos o revisar de un vistazo el historial completo del mes sin hacer scroll infinito.

En lugar de imponer una sola opción, implementé en todos los módulos personales un **conmutador de vista dual persistente en `localStorage`**:

```jsx
const [viewMode, setViewMode] = useState(() => {
  return localStorage.getItem('lifeops_view_sport') || 'grid';
});

const handleViewChange = (mode) => {
  setViewMode(mode);
  localStorage.setItem('lifeops_view_sport', mode);
};
```

En la cabecera de cada módulo, dos botones discretos con iconos de `LayoutGrid` y `Table` permiten alternar el modo de visualización al instante. Gracias a React y al motor de estilos de Vite, el cambio es sub-milisegundo y no requiere volver a solicitar los datos al servidor.

---

### 2. Módulo de Deporte & Rendimiento Físico (`SportModule.jsx`) 🏃💨

El módulo deportivo está pensado para atletas aficionados que practican varias disciplinas: carreras (*running*), ciclismo (*cycling*), entrenamientos de fuerza (*gym*) o natación.

```
┌────────────────────────────────────────────────────────────────────────┐
│  🏃 Deporte & Fitness                  [ + Registrar Actividad ] [⊞|≡] │
├─────────────────┬─────────────────┬─────────────────┬──────────────────┤
│ DISTANCIA TOTAL │ TIEMPO ACTIVO   │ CALORÍAS        │ RÉCORDS (PB)     │
│   142.5 km      │   18.4 horas    │   12,450 kcal   │    4 PBs 🏅      │
├─────────────────┴─────────────────┴─────────────────┴──────────────────┤
│                                                                        │
│ ┌───────────────────────────┐         ┌──────────────────────────────┐ │
│ │ 🏃 RUNNING         🏅 PB  │         │ 🚴 CICLISMO                  │ │
│ │ Tirada Larga Dominical    │         │ Ruta de Montaña - Puertos    │ │
│ │ 2026-09-10                │         │ 2026-09-08                   │ │
│ │ [📍 21.1 km] [⏱️ 1h 48m]  │         │ [📍 65.0 km] [⏱️ 2h 45m]     │ │
│ │ [🔥 1,420 kcal] [❤️ 152ppm]│         │ [🔥 1,890 kcal] [⛰️ +950m]    │ │
│ └───────────────────────────┘         └──────────────────────────────┘ │
└────────────────────────────────────────────────────────────────────────┘
```

#### 2.1. Métricas de Alto Nivel Agregadas
Antes de renderizar las actividades individuales, calculamos mediante reducers en memoria los totales acumulados para la barra superior:

```javascript
const totalKm = workouts.reduce((sum, act) => sum + (act.workout?.distance_km || 0), 0);
const totalMinutes = workouts.reduce((sum, act) => sum + (act.duration_minutes || 0), 0);
const totalCalories = workouts.reduce((sum, act) => sum + (act.workout?.calories || 0), 0);
const pbCount = workouts.filter((act) => act.workout?.personal_best).length;
```

#### 2.2. Payload Segregado en FastAPI
Cuando el usuario guarda un entrenamiento, el cliente envía un contrato estructurado que FastAPI desglosa en la tabla maestra `lifeops.activities` y en la tabla hija `lifeops.workouts`:

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

Esto garantiza que las métricas comunes (fechas, duración general y notas) queden normalizadas para el Dashboard global, mientras que los atributos de precisión física (desnivel positivo, frecuencia cardíaca y récords) se almacenan en su tabla especializada con integridad referencial estricta.

---

### 3. Cultura y Hábitos Intelectuales: Libros y Cine 📚🎬

Para la parte cultural y de ocio, el objetivo era abandonar las notas sueltas en el móvil y disponer de un catálogo visual enriquecido.

#### 3.1. Biblioteca con Barra de Progreso Dinámica (`BooksModule.jsx`)
En la tarjeta de cada libro, calculamos en tiempo real el porcentaje de páginas leídas respecto al total:

```jsx
const percentage = b.pages_total > 0 
  ? Math.min(100, Math.round((b.pages_read / b.pages_total) * 100)) 
  : 0;

<div className="book-progress-wrapper">
  <div className="progress-info">
    <span>{b.pages_read} / {b.pages_total} págs</span>
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

Además, el selector de estado permite clasificar rápidamente entre `reading` (*Leyendo actualmente*), `completed` (*Leído*) y `wishlist` (*Lista de deseos*), complementado con un componente de puntuación de 1 a 5 estrellas mediante iconos SVG de `lucide-react`.

#### 3.2. Catálogo Audiovisual por Plataforma (`FilmsModule.jsx`)
El módulo de cine organiza películas, series y documentales por plataforma de streaming (*Netflix, HBO Max, Prime Video, Disney+, Cine*). Cada registro incluye título, director, año de estreno, valoración personal y una breve reseña, facilitando responder a la típica pregunta: *"¿Qué películas buenas he visto este último trimestre?"*.

---

### 4. Gestión Profesional: El Tablero Kanban (`KanbanBoard.jsx`) 📋

Para el área profesional, implementé un tablero Kanban completo con 4 columnas que reflejan el ciclo de vida ágil de cualquier tarea:

1. 📝 **Por Hacer (`todo`)**: Tareas planificadas pendientes de inicio.
2. ⚡ **En Progreso (`in_progress`)**: Trabajo activo en la jornada.
3. 🔍 **En Revisión (`review`)**: Tareas a la espera de validación, despliegue o feedback de terceros.
4. ✅ **Completadas (`done`)**: Entregables finalizados.

```
┌──────────────────┬──────────────────┬──────────────────┬──────────────────┐
│ 📝 POR HACER (3) │ ⚡ EN CURSO (2)  │ 🔍 REVISIÓN (1)  │ ✅ HECHO (8)     │
├──────────────────┼──────────────────┼──────────────────┼──────────────────┤
│ ┌──────────────┐ │ ┌──────────────┐ │ ┌──────────────┐ │ ┌──────────────┐ │
│ │ Refactor API │ │ │ Frontend UI  │ │ │ Tests E2E    │ │ │ DB Migration │ │
│ │ 🚨 Urgente   │ │ │ 🟡 Media     │ │ │ 🟢 Baja      │ │ │ 2026-09-02   │ │
│ │ 📅 18 Sep    │ │ │ 💬 3 avances │ │ │ 📅 Hoy       │ │ │ 💬 5 avances │ │
│ │ [→ Mover]    │ │ │ [←]     [→]  │ │ │ [←]     [→]  │ │ │ [← Mover]    │ │
│ └──────────────┘ │ └──────────────┘ │ └──────────────┘ │ └──────────────┘ │
└──────────────────┴──────────────────┴──────────────────┴──────────────────┘
```

#### 4.1. Actualizaciones Optimistas para Transición Instantánea
Cuando el usuario pulsa para avanzar una tarea de `in_progress` a `review`, esperar el viaje de red completo (frontend → Render API → Supabase → respuesta) introduciría un retraso perceptible de varios cientos de milisegundos.

Para lograr una sensación táctil instantánea, aplicamos una **actualización optimista** del estado local en React:

```javascript
const handleMoveTask = async (taskId, currentStatus, direction) => {
  const statusOrder = ['todo', 'in_progress', 'review', 'done'];
  const currentIndex = statusOrder.indexOf(currentStatus);
  const targetIndex = direction === 'next' ? currentIndex + 1 : currentIndex - 1;

  if (targetIndex < 0 || targetIndex >= statusOrder.length) return;
  const targetStatus = statusOrder[targetIndex];

  // 1. Actualización optimista instantánea en memoria
  setTasks((prev) =>
    prev.map((t) => (t.id === taskId ? { ...t, status: targetStatus } : t))
  );

  // 2. Persistencia asíncrona en FastAPI
  try {
    await api.updateTask(taskId, { status: targetStatus });
  } catch (err) {
    console.error('Fallo al persistir estado, revirtiendo...', err);
    fetchData(); // Rollback en caso de error de red
  }
};
```

Si la petición tiene éxito, el usuario no ha percibido la menor latencia; si la red falla, el bloque `catch` recupera el estado auténtico del servidor sin desincronizaciones silenciosas.

---

### 5. La Bitácora de Avances: El Poder de PostgreSQL JSONB 🗄️⚡

Una de las características más potentes y diferenciadoras del tablero Kanban de LifeOps es la **Bitácora de Avances** por tarea.

En proyectos personales y profesionales, una tarea rara vez se resuelve en una sola sesión de trabajo. Habitualmente requiere varios días de investigación, pruebas o bloqueos temporales. El problema habitual de las herramientas de gestión es que los comentarios o notas de evolución suelen forzar la creación de tablas relacionales complejas (`task_comments`) con migraciones, claves foráneas e índices adicionales.

En LifeOps aprovechamos el tipo nativo **`JSONB` de PostgreSQL**:

```sql
-- Definición en Supabase (lifeops schema)
ALTER TABLE lifeops.tasks ADD COLUMN comments JSONB DEFAULT '[]'::jsonb;
```

#### 5.1. El Endpoint en FastAPI (`routers/projects.py`)
En el backend, añadir un comentario es una operación atómica y limpia que no requiere uniones (*JOINs*) complejas:

```python
@tasks_router.post(
    "/{task_id}/comments",
    response_model=TaskResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Añadir comentario de avance a una tarea",
)
def add_task_comment(
    task_id: str,
    payload: TaskCommentCreate,
    user: AuthenticatedUser = Depends(get_current_user),
):
    # 1. Recuperar la tarea existente
    task = db("tasks").select("*").eq("id", task_id).eq("user_id", user.id).single().execute().data
    if not task:
        raise HTTPException(status_code=404, detail="Tarea no encontrada")

    existing_comments = task.get("comments") or []

    # 2. Generar el nuevo registro con timestamp UTC estricto
    new_comment = {
        "id": str(uuid.uuid4()),
        "text": payload.text.strip(),
        "created_at": dt.datetime.now(dt.timezone.utc).isoformat(),
    }
    existing_comments.append(new_comment)

    # 3. Persistir en la columna JSONB
    result = db("tasks").update({"comments": existing_comments}).eq("id", task_id).execute()
    return result.data[0]
```

#### 5.2. Línea Temporal en el Frontend
En el modal de edición de la tarea, renderizamos un *timeline* cronológico con marcas temporales legibles (*hace 2 horas*, *ayer*, fecha formateada) y un botón de eliminación individual:

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
> Gracias a almacenar la bitácora como JSONB estructurado dentro de la propia tarea, el motor de informes de la Parte 4 puede leer la historia completa de cada proyecto sin ejecutar consultas cruzadas N+1.

---

### Conclusión y Próximos Pasos 🎯

Con los módulos interactivos de Deporte, Biblioteca, Cine y el Tablero Kanban plenamente operativos, LifeOps ya es un sistema en el que se puede volcar y consultar toda la actividad diaria con agilidad.

Sin embargo, los datos atrapados en una aplicación web, por bonita que sea, no son suficientes para una gestión profesional de alto nivel. Necesitamos poder **extraer, analizar y presentar estos datos fuera del navegador**.

En la **Parte 4** de esta serie, abordaremos la joya técnica del backend:
* **Generación in-memory en streaming de documentos Word (`.docx`)** con `python-docx` y plantillas de diseño ejecutivo.
* **Exportación de libros multi-hoja en Excel (`.xlsx`)** con `openpyxl`, con pestañas independientes para deporte, lecturas, cine y proyectos.
* **Descarga de backups en CSV con UTF-8 BOM** para compatibilidad nativa e instantánea con PowerBI y Microsoft Excel.

---

### Referencias y Enlaces de Interés 🔗

* 🚀 **Aplicación en Producción**: Prueba los módulos en vivo en [datalaria.com/apps/lifeops](https://datalaria.com/apps/lifeops/).
* 🌐 **API Swagger en Producción**: Endpoints de tareas y comentarios en [lifeops-api.onrender.com/docs](https://lifeops-api.onrender.com/docs).
* 🐘 **PostgreSQL JSONB Documentation**: Guía oficial de tipos semiestructurados en [postgresql.org/docs](https://www.postgresql.org/docs/current/datatype-json.html).
* ⚛️ **React Documentation**: Gestión de estado y efectos en [react.dev](https://react.dev/).
* 🎨 **Lucide Icons**: Iconografía para interfaces web en [lucide.dev](https://lucide.dev/).

¡Nos vemos en la Parte 4! ¿Cómo gestionas tú la bitácora de tus proyectos personales? Cuéntamelo en los comentarios. 👇
