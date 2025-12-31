---
title: "Juegos"
description: "Juegos arcade y experimentos interactivos."
hidemeta: true
---

Bienvenido al arcade. Aquí encontrarás juegos desarrollados para experimentar con tecnologías web, diseño de juegos e IA.

<div>
    <div class="app-grid">
        <div class="app-card">
            <span class="app-icon">🐍</span>
            <h3 class="app-title">Neon Snake</h3>
            <p class="app-desc">Versión Cyberpunk del clásico Snake con ranking global en tiempo real.</p>
            <div class="app-links" style="display: flex; gap: 10px; justify-content: start; margin-top: 10px;">
                <a href="/games/snake/" class="app-link" target="_blank">Jugar Ahora →</a>
                <a href="/es/posts/game_snake/" class="app-link" style="background: transparent; border: 1px solid var(--primary); color: var(--primary);">Leer Post</a>
            </div>
        </div>
    </div>
</div>

<style>
.app-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
    gap: 20px;
    margin-top: 2rem;
}
.app-card {
    background: var(--entry);
    border-radius: 12px;
    padding: 20px;
    border: 1px solid var(--border);
    transition: transform 0.2s;
}
.app-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 10px 20px rgba(0,0,0,0.1);
}
.app-icon {
    font-size: 2.5rem;
    display: block;
    margin-bottom: 10px;
}
.app-title {
    margin: 0 0 10px 0;
    font-size: 1.25rem;
}
.app-desc {
    color: var(--secondary);
    font-size: 0.9rem;
    margin-bottom: 15px;
    line-height: 1.5;
}
.app-link {
    display: inline-block;
    padding: 8px 16px;
    background: var(--primary);
    color: white; 
    border-radius: 6px;
    text-decoration: none;
    font-weight: 500;
    font-size: 0.9rem;
}
body.dark .app-link {
    color: black;
}
</style>
