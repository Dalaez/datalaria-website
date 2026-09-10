---
title: "Proyecto LifeOps (Parte 2): Frontend React con Glassmorphism, Dashboard 360° y Sistema de Diseño Dark Mode"
date: 2026-09-12
draft: false
categories: ["Proyectos", "Desarrollo Web"]
tags: ["react", "vite", "glassmorphism", "css", "recharts", "frontend", "dashboard", "i18n", "ui-ux", "supabase", "javascript"]
image: cover.png
description: "Segunda entrega de la serie LifeOps: cómo diseñé y construí la interfaz web con React 18, Vite, un sistema de diseño Glassmorphism Dark Mode, gráficos dinámicos con Recharts y autenticación reactiva con Supabase."
summary: "Con el backend y la base de datos listos, llega el momento de darle vida al cliente: un frontend React moderno con estética Glassmorphism, un cuadro de mandos 360° con Recharts, i18n ultraligero y gestión inteligente de cold-starts. ¡Te muestro el código paso a paso!"
---

En la [primera parte de esta serie](/posts/app-lifeops_part1_arquitectura_backend/), construimos los cimientos del sistema: una arquitectura cloud a coste cero ($0/mes), el modelo de datos relacional polimórfico en PostgreSQL alojado en Supabase y una API REST modular de alto rendimiento desarrollada con FastAPI.

Tener un backend robusto y una base de datos segura es imprescindible, pero un **Sistema Operativo Personal (LifeOps)** solo tiene éxito si utilizarlo a diario es una experiencia placentera, fluida y visualmente estimulante. Si la interfaz se siente lenta, tosca o parece una plantilla genérica sin personalidad, el hábito de registrar entrenamientos, lecturas o avances profesionales se abandona en cuestión de días.

Para evitarlo, me propuse diseñar una interfaz SPA (*Single Page Application*) que combinase **estética Glassmorphism moderna en Dark Mode**, **tiempos de respuesta instantáneos**, **visualización de datos 360°** y **adaptabilidad total**.

> [!TIP]
> **Prueba la aplicación en vivo**: Puedes interactuar con la versión de producción de LifeOps desplegada en [https://datalaria.com/apps/lifeops/](https://datalaria.com/apps/lifeops/).

---

### 🗺️ Hoja de Ruta de la Serie LifeOps
Esta serie documenta el ciclo de vida completo del proyecto a través de 5 entregas estructuradas:

1. 🟢 **Parte 1**: [Arquitectura de un Sistema Operativo Personal y Backend con FastAPI + Supabase](/posts/app-lifeops_part1_arquitectura_backend/)
2. 🟢 **Parte 2 (Este artículo)**: Frontend React con Glassmorphism, Dashboard 360° y Sistema de Diseño Dark Mode
3. ⚪ **Parte 3**: [Módulos Core: Deporte, Biblioteca, Cine y Tablero Kanban Profesional](/posts/app-lifeops_part3_modulos_kanban/)
4. ⚪ **Parte 4**: [Motor de Informes Ejecutivos en Word (.docx) y Exportación Multi-Hoja en Excel (.xlsx)](/posts/app-lifeops_part4_informes_word_excel/)
5. ⚪ **Parte 5**: [Despliegue 24/7 en la Nube a Coste Cero ($0/mes), Optimización Móvil y PWA](/posts/app-lifeops_part5_deploy_mobile_pwa/)

---

### 1. El Tooling del Frontend: Velocidad Extrema con Vite y React ⚡

A la hora de configurar el proyecto cliente (`lifeops-app`), la prioridad fue mantener una base de código limpia, modular y libre del exceso de dependencias que suele ralentizar las aplicaciones modernas.

Elegí **React 18/19** junto a **Vite** como empaquetador de nueva generación:

```json
{
  "name": "lifeops-app",
  "private": true,
  "version": "1.0.0",
  "type": "module",
  "scripts": {
    "dev": "vite",
    "build": "vite build",
    "lint": "oxlint",
    "preview": "vite preview"
  },
  "dependencies": {
    "@supabase/supabase-js": "^2.112.2",
    "lucide-react": "^1.31.0",
    "react": "^19.2.8",
    "react-dom": "^19.2.8",
    "react-router-dom": "^7.18.2",
    "recharts": "^3.10.1"
  },
  "devDependencies": {
    "@vitejs/plugin-react": "^6.0.4",
    "vite": "^8.2.0"
  }
}
```

#### ¿Por qué esta combinación técnica?
* **Arranque instantáneo y Hot Module Replacement (HMR)**: Vite utiliza *ES Modules* nativos en el navegador durante el desarrollo, eliminando los molestos tiempos de compilación de herramientas heredadas como Webpack o Create React App.
* **Iconografía consistente con `lucide-react`**: Proporciona iconos vectoriales SVG ultraligeros, con grosor de trazo homogéneo y personalización directa mediante props de React.
* **Visualización declarativa con `recharts`**: Permite componer gráficos responsivos de rendimiento basados en SVG sin pelearnos con manipulaciones imperativas del DOM.
* **Cero librerías de componentes masivas**: Prescindimos de frameworks CSS pesados. Cada componente se estiliza con CSS moderno puro aprovechando variables nativas y efectos de desenfoque por hardware.

---

### 2. El Sistema de Diseño: Glassmorphism Dark Mode Puro 🎨

El diseño visual de LifeOps se basa en el concepto de **Glassmorphism translúcido**: tarjetas que simulan vidrio esmerilado flotando sobre un lienzo oscuro profundo, dejando entrever sutiles resplandores de color esmeralda, cian y púrpura.

En lugar de sobrecargar la aplicación con librerías externas, definimos todos los *design tokens* en `:root` dentro de `src/index.css`:

```css
:root {
  /* Paleta Base — Dark Mode Premium */
  --bg-main: #0b0f17;
  --bg-sidebar: #111827;
  --bg-card: rgba(17, 24, 39, 0.7);
  --bg-card-hover: rgba(31, 41, 55, 0.8);
  --bg-glass: rgba(15, 23, 42, 0.65);
  
  /* Bordes y Desenfoque de Vidrio */
  --border-color: rgba(255, 255, 255, 0.08);
  --border-glow: rgba(59, 130, 246, 0.3);
  --glass-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
  --backdrop-blur: blur(16px);

  /* Acentos Semánticos */
  --accent-emerald: #10b981;
  --accent-emerald-glow: rgba(16, 185, 129, 0.25);
  --accent-cyan: #06b6d4;
  --accent-cyan-glow: rgba(6, 182, 212, 0.25);
  --accent-purple: #8b5cf6;
  --accent-purple-glow: rgba(139, 92, 246, 0.25);
  --accent-amber: #f59e0b;
  --accent-rose: #f43f5e;

  /* Tipografía */
  --font-sans: 'Inter', system-ui, -apple-system, sans-serif;
  --font-heading: 'Outfit', 'Inter', sans-serif;
}
```

#### Las Clases Utilitarias `.glass-panel` y `.glass-card`
Con estos tokens, encapsulamos la apariencia de vidrio en dos clases reutilizables en cualquier componente:

```css
.glass-panel {
  background: var(--bg-card);
  backdrop-filter: var(--backdrop-blur);
  -webkit-backdrop-filter: var(--backdrop-blur);
  border: 1px solid var(--border-color);
  border-radius: 16px;
  box-shadow: var(--glass-shadow);
}

.glass-card {
  background: linear-gradient(145deg, rgba(30, 41, 59, 0.5) 0%, rgba(15, 23, 42, 0.6) 100%);
  backdrop-filter: var(--backdrop-blur);
  -webkit-backdrop-filter: var(--backdrop-blur);
  border: 1px solid var(--border-color);
  border-radius: 16px;
  transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1);
}

.glass-card:hover {
  border-color: rgba(255, 255, 255, 0.18);
  transform: translateY(-2px);
  box-shadow: 0 12px 40px 0 rgba(0, 0, 0, 0.45);
}
```

El truco clave radica en combinar `backdrop-filter: blur(16px)` con un degradado en ángulo (`145deg`) y un borde semitransparente (`rgba(255, 255, 255, 0.08)`). Esto produce un brillo especular en la esquina superior izquierda de cada tarjeta que simula un bisel de cristal físico.

---

### 3. Autenticación Reactiva y Comunicación con FastAPI 🔐

El frontend debe comunicarse de forma transparente con dos servicios en la nube:
1. **Supabase Auth**: Para la gestión de usuarios, inicio de sesión, registro y refresco de tokens.
2. **FastAPI Backend en Render**: Para la lógica de negocio, estadísticas agregadas y generación de informes.

#### `AuthContext.jsx`: Suscripción en Tiempo Real al Estado de Sesión
Creamos un proveedor de contexto que se suscribe al ciclo de vida de autenticación mediante `onAuthStateChange`:

```jsx
import React, { createContext, useContext, useEffect, useState } from 'react';
import { supabase } from '../lib/supabase';

const AuthContext = createContext();

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null);
  const [session, setSession] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // 1. Obtener la sesión activa en el arranque
    supabase.auth.getSession().then(({ data: { session } }) => {
      setSession(session);
      setUser(session?.user ?? null);
      setLoading(false);
    });

    // 2. Escuchar cambios de sesión en tiempo real (login, logout, token refresh)
    const { data: { subscription } } = supabase.auth.onAuthStateChange((_event, session) => {
      setSession(session);
      setUser(session?.user ?? null);
      setLoading(false);
    });

    return () => subscription.unsubscribe();
  }, []);

  const signIn = (email, password) => supabase.auth.signInWithPassword({ email, password });
  const signOut = () => supabase.auth.signOut();

  return (
    <AuthContext.Provider value={{ user, session, loading, signIn, signOut }}>
      {children}
    </AuthContext.Provider>
  );
}

export const useAuth = () => useContext(AuthContext);
```

#### `apiFetch`: Inyección Automática del Token JWT
Para que cualquier petición a la API en FastAPI esté debidamente autenticada, creamos un envoltorio ligero en `src/lib/api.js`:

```javascript
import { supabase } from './supabase';

export const API_BASE_URL = import.meta.env.VITE_API_URL || 'https://lifeops-api.onrender.com';

export async function apiFetch(endpoint, options = {}) {
  // Extrae el token JWT actual de la sesión de Supabase
  const { data: { session } } = await supabase.auth.getSession();
  const token = session?.access_token;

  const headers = {
    'Content-Type': 'application/json',
    ...(token ? { Authorization: `Bearer ${token}` } : {}),
    ...(options.headers || {}),
  };

  const response = await fetch(`${API_BASE_URL}${endpoint}`, { ...options, headers });

  if (!response.ok) {
    const errorData = await response.json().catch(() => ({ detail: response.statusText }));
    throw new Error(errorData.detail || `HTTP Error ${response.status}`);
  }

  return response.status === 204 ? null : response.json();
}
```

Con este patrón, ningún componente tiene que preocuparse por gestionar cabeceras HTTP o refrescar tokens manualmente: si el usuario está autenticado, el token JWT viaja automáticamente al backend.

---

### 4. Construyendo el Dashboard 360° 📊

El **Dashboard Principal** (`DashboardPage.jsx`) es la pantalla que recibe al usuario tras identificarse. Su objetivo es ofrecer una síntesis completa del estado de su vida en menos de 5 segundos.

```
┌────────────────────────────────────────────────────────────────────────┐
│  👋 ¡Bienvenido de nuevo, Diego!                                       │
│  Resumen de actividad personal y estado de proyectos profesionales.    │
├─────────────────┬─────────────────┬─────────────────┬──────────────────┤
│ 🏃 ACTIVIDADES  │ 💼 PROYECTOS    │ 📋 TAREAS       │ 🔥 HÁBITOS       │
│      28         │       5         │      14         │     6 / 7        │
│ Total: 142      │ De 8 totales    │ 2 vencidas      │ Rachas activas   │
├─────────────────┴─────────────────┴─────────────────┴──────────────────┤
│  ⚡ ACCIONES RÁPIDAS: [+ Registrar Deporte] [+ Nuevo Libro] [+ Tarea]   │
├──────────────────────────────────────┬─────────────────────────────────┤
│  📊 DESGLOSE DE ACTIVIDAD (30 DÍAS)  │  📡 CONEXIÓN BACKEND            │
│  [BarChart Recharts con Neon Colors] │  🟢 FastAPI Online (Render.com) │
│  ■ Deporte  ■ Libros  ■ Cine/TV      │  🗄️ Supabase DB (lifeops schema)│
└──────────────────────────────────────┴─────────────────────────────────┘
```

#### 4.1. Grid de Widgets KPI (`StatWidget.jsx`)
Las tarjetas superiores proporcionan las métricas esenciales con un sistema de variantes de color semánticas:

```jsx
export function StatWidget({ title, value, subtitle, icon: Icon, color = 'emerald' }) {
  return (
    <div className={`stat-widget glass-card color-${color}`}>
      <div className="stat-widget-header">
        <span className="stat-title">{title}</span>
        {Icon && (
          <div className="stat-icon-wrapper">
            <Icon size={20} />
          </div>
        )}
      </div>
      <div className="stat-widget-body">
        <span className="stat-value">{value ?? 0}</span>
        {subtitle && <span className="stat-subtitle">{subtitle}</span>}
      </div>
    </div>
  );
}
```

Cada variante de color (`color-emerald`, `color-cyan`, `color-purple`, `color-amber`) tiñe el fondo del icono con un resplandor translúcido al 20% de opacidad (`--accent-emerald-glow`), creando una jerarquía visual inmediata sin estridencias.

#### 4.2. Gráfico de Actividad con Recharts
Para visualizar el volumen de actividad de los últimos 30 días, consumimos el endpoint `/api/v1/stats/breakdown` y alimentamos un gráfico de barras responsivo:

```jsx
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, Cell } from 'recharts';

const chartData = [
  { name: 'Deporte', count: breakdown?.sport || 0, color: '#10b981' },
  { name: 'Libros', count: breakdown?.book || 0, color: '#06b6d4' },
  { name: 'Cine/TV', count: breakdown?.film || 0, color: '#8b5cf6' },
  { name: 'Aprendizaje', count: breakdown?.learning || 0, color: '#f59e0b' },
  { name: 'Journal', count: breakdown?.journal || 0, color: '#ec4899' },
];

<div style={{ width: '100%', height: 220 }}>
  <ResponsiveContainer width="100%" height="100%">
    <BarChart data={chartData} margin={{ top: 10, right: 10, left: -20, bottom: 0 }}>
      <XAxis dataKey="name" stroke="#6b7280" fontSize={12} tickLine={false} />
      <YAxis stroke="#6b7280" fontSize={12} tickLine={false} allowDecimals={false} />
      <Tooltip
        contentStyle={{
          backgroundColor: 'rgba(17, 24, 39, 0.95)',
          borderColor: 'rgba(255, 255, 255, 0.1)',
          borderRadius: '8px',
          color: '#fff',
        }}
      />
      <Bar dataKey="count" radius={[6, 6, 0, 0]}>
        {chartData.map((entry, index) => (
          <Cell key={`cell-${index}`} fill={entry.color} />
        ))}
      </Bar>
    </BarChart>
  </ResponsiveContainer>
</div>
```

---

### 5. Resiliencia Operativa: Monitorización de Cold-Starts (`SystemHealth`) 🛡️

Como vimos en la Parte 1, el backend se ejecuta en el tier gratuito de **Render.com**, el cual hiberna el contenedor tras 15 minutos sin tráfico. 

Si el usuario abre LifeOps tras varias horas, la primera petición tardará entre 20 y 40 segundos en responder mientras el contenedor se despierta. Si el frontend no maneja esta situación, el usuario vería una pantalla congelada o un error genérico.

Para resolverlo de raíz, implementé el componente **`SystemHealth.jsx`**:

```jsx
export function SystemHealth() {
  const [health, setHealth] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [retryCount, setRetryCount] = useState(0);

  const checkHealth = async (isAutoRetry = false) => {
    setLoading(true);
    if (!isAutoRetry) setError(null);

    try {
      const data = await api.getHealth();
      setHealth(data);
      setError(null);
    } catch (err) {
      setError(err.message || 'Error al conectar con la API');
      
      // Auto-reintento hasta 3 veces con 6 segundos de delay mientras Render despierta
      if (retryCount < 3) {
        setTimeout(() => setRetryCount((prev) => prev + 1), 6000);
      }
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    checkHealth(retryCount > 0);
  }, [retryCount]);

  return (
    <div className="system-health-widget glass-panel">
      {/* Indicador visual de estado */}
      {error ? (
        <div className="health-alert error">
          <AlertCircle size={18} />
          <span>La instancia gratuita de Render se está activando (Cold start)... reintentando automáticamente.</span>
        </div>
      ) : (
        <div className="health-alert success">
          <CheckCircle2 size={18} />
          <span>{health?.engine} — Online (Esquema: {health?.schema})</span>
        </div>
      )}
    </div>
  );
}
```

> [!NOTE]
> Esta estrategia de auto-retry transparente transforma lo que normalmente sería un fallo de conexión percibido por el usuario en una transición controlada con telemetría en tiempo real.

---

### 6. Internacionalización Nativa (i18n) Ultraligera 🌐

Muchas aplicaciones web incorporan paquetes pesados de internacionalización con decenas de plugins. Para LifeOps, diseñé una solución en **menos de 80 líneas de código** en `LanguageContext.jsx`:

```jsx
import React, { createContext, useContext, useState, useEffect } from 'react';
import { es } from '../i18n/locales/es';
import { en } from '../i18n/locales/en';

const translations = { es, en };
const LanguageContext = createContext();

export function LanguageProvider({ children }) {
  const [language, setLanguageState] = useState(() => {
    const saved = localStorage.getItem('lifeops_language');
    if (saved === 'es' || saved === 'en') return saved;
    return navigator.language?.toLowerCase().startsWith('es') ? 'es' : 'en';
  });

  const toggleLanguage = () => {
    const next = language === 'es' ? 'en' : 'es';
    setLanguageState(next);
    localStorage.setItem('lifeops_language', next);
    document.documentElement.lang = next;
  };

  // Función traductora con resolución por dot notation e interpolación de variables
  const t = (path, params = {}) => {
    const dict = translations[language] || translations.es;
    let val = path.split('.').reduce((prev, curr) => prev?.[curr], dict) || path;
    if (typeof val === 'string') {
      return Object.keys(params).reduce((str, key) => str.replace(new RegExp(`\\{${key}\\}`, 'g'), params[key]), val);
    }
    return val;
  };

  return (
    <LanguageContext.Provider value={{ language, toggleLanguage, t }}>
      {children}
    </LanguageContext.Provider>
  );
}

export const useLanguage = () => useContext(LanguageContext);
```

#### Ventajas:
1. **Cero dependencias externas**: Reduce el peso del bundle final en más de 100 KB.
2. **Sintaxis familiar**: Permite invocar traducciones como `t('dashboard.welcome')` o `t('sport.stats.distance', { count: 10 })`.
3. **Persistencia y auto-detección**: Recuerda la preferencia del usuario en `localStorage` y detecta el idioma preferido del navegador en la primera visita.

---

### Conclusión y Próximos Pasos 🎯

Con el frontend React estructurado, el sistema de diseño Glassmorphism implementado, la autenticación sincronizada con Supabase y el Dashboard 360° monitorizando la salud del backend, tenemos una aplicación web moderna, rápida y lista para el día a día.

En la **Parte 3** de esta serie, nos adentraremos en el corazón operativo de la aplicación:
* **Módulo Deportivo**: Registro de carreras, gimnasio y ciclismo con cálculo de ritmos medios, marcas personales (PB) y calorías.
* **Módulo de Lecturas & Cine**: Progreso interactivo de páginas, plataformas de streaming y valoraciones.
* **Tablero Kanban Profesional**: Gestión visual de tareas por columnas, proyectos asociados y **bitácora de avances cronológica con marcas temporales almacenadas en JSONB**.

---

### Referencias y Enlaces de Interés 🔗

* 🚀 **Aplicación en Producción**: Prueba la app en vivo en [datalaria.com/apps/lifeops](https://datalaria.com/apps/lifeops/).
* 🌐 **Backend API**: Documentación interactiva Swagger en [lifeops-api.onrender.com/docs](https://lifeops-api.onrender.com/docs).
* ⚛️ **React Documentation**: Guía oficial de React 19 en [react.dev](https://react.dev/).
* ⚡ **Vite**: Empaquetador de frontend de última generación en [vite.dev](https://vite.dev/).
* 📊 **Recharts**: Librería declarativa de gráficos para React en [recharts.org](https://recharts.org/).
* 🎨 **Lucide Icons**: Catálogo de iconos SVG limpios en [lucide.dev](https://lucide.dev/).

¡Nos vemos en la Parte 3! Deja tus impresiones en los comentarios o comparte tus propias soluciones de frontend. 👇
