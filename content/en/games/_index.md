---
title: "Games"
description: "Arcade games and interactive experiments."
hidemeta: true
---

Welcome to the arcade. Here you will find games developed to experiment with web technologies, game design and AI.

<div>
    <!-- The grid will be populated by the theme's list logic or we can hardcode the cards like in Apps -->
    <!-- For consistency with Apps, we use the HTML structure -->
    <div class="app-grid">
        <div class="app-card">
            <span class="app-icon">🐍</span>
            <h3 class="app-title">Neon Snake</h3>
            <p class="app-desc">Cyberpunk version of the classic Snake with real-time global ranking.</p>
            <div class="app-links" style="display: flex; gap: 10px; justify-content: start; margin-top: 10px;">
                <a href="/games/snake/" class="app-link" target="_blank">Play Now →</a>
                <a href="/posts/game_snake/" class="app-link" style="background: transparent; border: 1px solid var(--primary); color: var(--primary);">Read Post</a>
            </div>
        </div>
    </div>
</div>

<style>
/* Reusing App Grid Styles if they are global, otherwise redefining basic ones just in case */
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
    color: var(--theme); /* Usually white or black depending on theme, but primary text is safer */
    color: white; /* Hardcoded for contrast if primary is dark */
    border-radius: 6px;
    text-decoration: none;
    font-weight: 500;
    font-size: 0.9rem;
}
body.dark .app-link {
    color: black; 
}
</style>
