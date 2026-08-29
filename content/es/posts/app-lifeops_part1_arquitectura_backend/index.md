---
title: "Proyecto LifeOps (Parte 1): Arquitectura de un Sistema Operativo Personal y Backend con FastAPI + Supabase"
date: 2026-08-30
draft: false
categories: ["Proyectos", "Desarrollo Web"]
tags: ["python", "fastapi", "supabase", "react", "postgresql", "backend", "productividad", "datos", "cloud", "serverless"]
image: cover.png
description: "Primera entrega de la serie LifeOps: cómo diseñé y construí mi propio sistema operativo personal y profesional a coste cero ($0/mes) unificando deporte, lecturas, cine, tareas Kanban y proyectos con FastAPI y Supabase."
summary: "Cansado de usar 5 aplicaciones distintas de suscripción mensual para registrar entrenamientos, lecturas y proyectos, decidí construir LifeOps: un sistema operativo unificado, escalable y 100% gratuito basado en FastAPI y Supabase. ¡Te cuento la arquitectura!"
---

¿Cuántas aplicaciones utilizas al día para gestionar tu vida? Si eres como yo, probablemente tengas una app para registrar tus carreras y entrenamientos de fuerza, otra para llevar la cuenta de los libros que lees, una web para valorar películas y series, y dos o tres herramientas más para gestionar proyectos, tareas y notas de trabajo. 

El resultado suele ser siempre el mismo: **datos dispersos en silos cerrados, suscripciones mensuales acumuladas y una nula capacidad para cruzar información o generar un informe mensual integrado de tu evolución**.

Con ese reto en mente y fiel al espíritu de Datalaria de "aprender construyendo", decidí diseñar y desarrollar **LifeOps**: un **Sistema Operativo Personal y Profesional (All-in-One OS)** que unifica bajo una sola interfaz reactiva:

1. 🏃 **Salud & Rendimiento Deportivo**: Registro de sesiones (Running, Ciclismo, Gym), cálculo de volumen de kilómetros, marcas personales (PB) y calorías.
2. 📚 **Biblioteca & Hábitos de Lectura**: Seguimiento de páginas leídas, barras de progreso y valoraciones.
3. 🎬 **Cine & Entretenimiento**: Catálogo de películas, series y documentales por plataforma.
4. 📋 **Área Profesional & Proyectos**: Tablero Kanban interactivo, control presupuestario y seguimiento de hitos.
5. 📊 **Motor de Informes y Portabilidad**: Generación en streaming de documentos ejecutivos en Word (`.docx`), libros Excel (`.xlsx`) y backups en CSV con UTF-8 BOM.

Y lo más importante de todo: **diseñado bajo una arquitectura robusta, segura y 100% gratuita ($0/mes)**.

En esta primera entrega de la serie, nos adentraremos en los cimientos del proyecto: el **diseño de la arquitectura cloud**, el **modelo de datos relacional en PostgreSQL** y la construcción del **backend de alto rendimiento con FastAPI**. ¡Vamos a ello! 🚀

---

### La Arquitectura 100% Gratuita: ¿Cómo Operar a Coste Cero? 💡

A la hora de diseñar la infraestructura de LifeOps, el objetivo no era solo que funcionara bien en local, sino que pudiera publicarse y desplegarse en producción sin incurrir en costes mensuales fijos, aprovechando los tiers gratuitos más potentes del ecosistema actual:

```
┌─────────────────────────────────────────────────────────────┐
│                      NAVEGADOR CLIENTE                      │
│            https://datalaria.com/apps/lifeops               │
└──────────────────────────────┬──────────────────────────────┘
                               │ (Proxy Rewrite 200)
                               ▼
┌─────────────────────────────────────────────────────────────┐
│               FRONTEND: Netlify CDN (0 €/mes)               │
│           React 18 + Vite 8 + i18n (ES/EN) + CSS Glass      │
└──────────────────────────────┬──────────────────────────────┘
                               │
               JWT Auth Token  │  REST API Calls / Streaming
                               ▼
┌─────────────────────────────────────────────────────────────┐
│               BACKEND: FastAPI + Python 3.13                │
│    • In-Memory Docx Generator (python-docx + io.BytesIO)    │
│    • Multi-Sheet Excel Engine (openpyxl)                    │
│    • Rate Limiter Anti-DoS (slowapi) + CORS Strict          │
└──────────────────────────────┬──────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────┐
│              BASE DE DATOS: Supabase Cloud                  │
│       • PostgreSQL con esquema aislado `lifeops`            │
│       • Row Level Security (RLS) & Supabase Auth            │
└─────────────────────────────────────────────────────────────┘
```

1. **Frontend en Netlify ($0/mes)**: Aplicación SPA compilada con Vite y servida a través de CDN global con compresión Gzip, *Code Splitting* por ruta y reescritura transparente de URL desde el dominio principal de Datalaria.
2. **Backend en FastAPI ($0/mes)**: API asíncrona en Python, ligera y con tipado estricto gracias a Pydantic v2.
3. **Base de Datos en Supabase ($0/mes)**: PostgreSQL gestionado en la nube con 500 MB de almacenamiento relacional, autenticación segura mediante tokens JWT y políticas de seguridad a nivel de fila (*Row Level Security*).

---

### El Modelo de Datos: Polimorfismo Elegante en PostgreSQL 🗄️

Uno de los principales desafíos al unificar actividades tan dispares (un entrenamiento de 10 km, un libro de 400 páginas o una película de Netflix) es evitar tablas sobredimensionadas llenas de campos nulos (`NULL`).

Para resolver esto, implementé un **patrón de tabla maestra con extensiones hijas especializadas (1 a 1)** dentro del esquema dedicado `lifeops`:

```sql
-- 1. Tabla Maestra de Actividades Generales
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

-- 2. Extensión Deportiva (Workouts)
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

-- 3. Extensión Lecturas (Books)
CREATE TABLE lifeops.books (
    activity_id UUID PRIMARY KEY REFERENCES lifeops.activities(id) ON DELETE CASCADE,
    author VARCHAR(150),
    pages_total INTEGER,
    pages_read INTEGER DEFAULT 0,
    status VARCHAR(30) DEFAULT 'reading', -- 'reading', 'completed', 'wishlist'
    genre VARCHAR(50)
);

-- 4. Extensión Cine & Series (Films)
CREATE TABLE lifeops.films (
    activity_id UUID PRIMARY KEY REFERENCES lifeops.activities(id) ON DELETE CASCADE,
    media_type VARCHAR(30) DEFAULT 'movie', -- 'movie', 'series', 'documentary'
    director VARCHAR(150),
    platform VARCHAR(50), -- 'Cine', 'Netflix', 'HBO Max', 'Prime Video'
    genre VARCHAR(50),
    year INTEGER
);
```

#### ¿Por qué este diseño es superior?
* **Consultas globales ultrarrápidas**: El Dashboard y los motores de alertas consultan únicamente `lifeops.activities` para calcular totales y frecuencias.
* **Integridad referencial total**: Si se elimina una actividad, la cláusula `ON DELETE CASCADE` limpia automáticamente los registros hijos en PostgreSQL sin dejar basura huérfana.
* **Seguridad Multi-inquilino (RLS)**: Cada usuario sólo puede leer y escribir sus propios registros mediante políticas como:
  ```sql
  CREATE POLICY "Users can only view their own activities" 
  ON lifeops.activities FOR SELECT 
  USING (auth.uid() = user_id);
  ```

---

### El Backend con FastAPI: Modularidad y Tipado Estricto ⚡

Para estructurar la API, organizamos el código siguiendo el patrón de **Routers Modulares** de FastAPI:

```
lifeops-api/
├── main.py                  # Punto de entrada, Middlewares, Rate Limiter y CORS
├── config.py                # Configuración centralizada con Pydantic Settings
├── middleware/
│   └── auth.py              # Validación de JWT y extracción segura del user_id
├── models/
│   ├── activity.py          # Schemas Pydantic (Create, Update, Response)
│   └── project.py           # Schemas para Tareas y Proyectos
├── routers/
│   ├── activities.py        # Endpoints CRUD para Deporte, Libros y Cine
│   ├── projects.py          # Endpoints para Tablero Kanban y Proyectos
│   ├── stats.py             # Agregaciones y métricas del Dashboard
│   ├── reports.py           # Generador de Word y exportaciones CSV/Excel
│   └── alerts.py            # Motor de alertas inteligentes
└── services/
    ├── report_generator.py  # Creación de .docx en memoria RAM
    └── data_exporter.py     # Generador de CSV (BOM) y Excel multi-hoja
```

#### Autenticación Segura con Supabase JWT
Cualquier endpoint que manipule datos privados inyecta la dependencia `get_current_user`:

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
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token sin identificador de usuario")
        return AuthenticatedUser(id=user_id, email=payload.get("email"))
    except jwt.PyJWTError as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token inválido o expirado")
```

---

### Blindaje para Producción: Rate Limiting y Protección Anti-Abuso 🛡️

Dado que LifeOps permite descargar informes completos en Word y libros de cálculo multi-hoja en Excel, era indispensable evitar que un bot o usuario malintencionado saturase la memoria del servidor generando cientos de documentos por segundo.

Para ello, integramos **Rate Limiting con `slowapi`** a nivel de endpoint:

```python
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

limiter = Limiter(key_func=get_remote_address, default_limits=["120/minute"])
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# Límite estricto para generación pesada de informes Word (.docx)
@router.post("/generate")
@limiter.limit("10/minute")
def generate_report(request: Request, req: GenerateReportRequest, user = Depends(get_current_user)):
    ...
```

Si un cliente excede el límite permitido, la API responde inmediatamente con un **HTTP 429 Too Many Requests**, protegiendo los recursos sin consumir ciclos de CPU innecesarios.

---

### Conclusión y Próximos Pasos 🎯

Con el backend en FastAPI blindado, el esquema relacional en PostgreSQL funcionando en Supabase y las políticas de seguridad activas, tenemos una base sólida como una roca y con un coste operativo de **0 € al mes**.

En la **Parte 2** de esta serie, nos sumergiremos en el frontend:
* Construcción de la interfaz SPA con **React 18, Vite y diseño Glassmorphism**.
* Sistema de **Internacionalización (i18n)** para alternar entre Español 🇪🇸 e Inglés 🇬🇧 al instante.
* El **Tablero Kanban interactivo** con edición en vivo.
* El **modo dual de visualización (Tarjetas vs Tabla Sintetizada)**.

¡Nos vemos en la siguiente entrega! Si tienes cualquier duda sobre la arquitectura o quieres compartir tu experiencia montando proyectos similares, déjame un comentario abajo o en redes. 👇
