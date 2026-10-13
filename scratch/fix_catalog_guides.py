import os
import re

def update_file(file_path):
    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        return

    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    orig_len = len(content)

    # 1. Replace static Spanish anchor links (except DAFO)
    # Pattern: <a href="/posts/(?!dafo-cuantitativo-matriz-came)[^"]*" class="btn-kit-info"[^>]*>Gu[íi]a 📖</a>
    content = re.sub(
        r'<a href="/posts/(?!dafo-cuantitativo-matriz-came/)[^"]*" class="btn-kit-info"[^>]*>Gu[íi]a [📖\?\?]+</a>',
        '<span class="btn-kit-info btn-disabled" style="opacity: 0.55; cursor: default; border-style: dashed;" title="Guía metodológica próximamente en el blog">Guía ⏳</span>',
        content
    )

    # 2. Replace static English anchor links (except SWOT)
    content = re.sub(
        r'<a href="/(?:en/)?posts/(?!quantitative-swot-tows-matrix/)[^"]*" class="btn-kit-info"[^>]*>Guide [📖\?\?]+</a>',
        '<span class="btn-kit-info btn-disabled" style="opacity: 0.55; cursor: default; border-style: dashed;" title="Methodological guide coming soon on the blog">Guide ⏳</span>',
        content
    )

    # 3. In KITS_DATA arrays, replace guideUrl with null for all except dafo / swot
    # Match: guideUrl: "/posts/(?!dafo-cuantitativo-matriz-came/)[^"]*"
    content = re.sub(
        r'guideUrl:\s*"/posts/(?!dafo-cuantitativo-matriz-came/)[^"]*"',
        'guideUrl: null',
        content
    )
    # Match: guideUrl: "/en/posts/(?!quantitative-swot-tows-matrix/)[^"]*"
    content = re.sub(
        r'guideUrl:\s*"/en/posts/(?!quantitative-swot-tows-matrix/)[^"]*"',
        'guideUrl: null',
        content
    )

    # 4. In JS render() ES:
    # `${kit.guideUrl ? `<a href="${kit.guideUrl}" class="btn-kit-info" title="Leer guía metodológica">Guía 📖</a>` : ''}`
    content = re.sub(
        r'\$\{kit\.guideUrl \? `<a href="\$\{kit\.guideUrl\}" class="btn-kit-info" title="Leer guía metodológica">Guía 📖</a>` : \'\'\}',
        '${kit.guideUrl ? `<a href="${kit.guideUrl}" class="btn-kit-info" title="Leer guía metodológica">Guía 📖</a>` : `<span class="btn-kit-info" style="opacity: 0.55; cursor: default; border-style: dashed;" title="Guía próximamente">Guía ⏳</span>`}',
        content
    )

    # 5. In JS render() EN:
    # `${kit.guideUrl ? `<a href="${kit.guideUrl}" class="btn-kit-info" title="Read technical guide">Guide 📖</a>` : ''}`
    content = re.sub(
        r'\$\{kit\.guideUrl \? `<a href="\$\{kit\.guideUrl\}" class="btn-kit-info" title="Read technical guide">Guide 📖</a>` : \'\'\}',
        '${kit.guideUrl ? `<a href="${kit.guideUrl}" class="btn-kit-info" title="Read technical guide">Guide 📖</a>` : `<span class="btn-kit-info" style="opacity: 0.55; cursor: default; border-style: dashed;" title="Guide coming soon">Guide ⏳</span>`}',
        content
    )

    # 6. In Modal openModal() ES:
    old_modal_es = """    const guideBtn = document.getElementById('modal-guide-link');
    if (kit.guideUrl) {
      guideBtn.href = kit.guideUrl;
      guideBtn.style.display = 'inline-flex';
    } else {
      guideBtn.style.display = 'none';
    }"""

    new_modal_es = """    const guideBtn = document.getElementById('modal-guide-link');
    if (kit.guideUrl) {
      guideBtn.href = kit.guideUrl;
      guideBtn.innerHTML = 'Leer Guía Gratuita 📖';
      guideBtn.style.display = 'inline-flex';
      guideBtn.style.opacity = '1';
      guideBtn.style.cursor = 'pointer';
      guideBtn.style.borderStyle = 'solid';
    } else {
      guideBtn.removeAttribute('href');
      guideBtn.innerHTML = 'Guía Próximamente ⏳';
      guideBtn.style.display = 'inline-flex';
      guideBtn.style.opacity = '0.55';
      guideBtn.style.cursor = 'default';
      guideBtn.style.borderStyle = 'dashed';
    }"""

    if old_modal_es in content:
        content = content.replace(old_modal_es, new_modal_es)

    # 7. In Modal openModal() EN:
    old_modal_en = """    const guideBtn = document.getElementById('modal-guide-link');
    if (kit.guideUrl) {
      guideBtn.href = kit.guideUrl;
      guideBtn.style.display = 'inline-flex';
    } else {
      guideBtn.style.display = 'none';
    }"""

    # Note: If old_modal_en is identical to old_modal_es, it may have already been replaced or there might be an EN specific version
    old_modal_en_specific = """    const guideBtn = document.getElementById('modal-guide-link');
    if (kit.guideUrl) {
      guideBtn.href = kit.guideUrl;
      guideBtn.style.display = 'inline-flex';
    } else {
      guideBtn.style.display = 'none';
    }"""

    new_modal_en = """    const guideBtn = document.getElementById('modal-guide-link');
    if (kit.guideUrl) {
      guideBtn.href = kit.guideUrl;
      guideBtn.innerHTML = 'Read Free Guide 📖';
      guideBtn.style.display = 'inline-flex';
      guideBtn.style.opacity = '1';
      guideBtn.style.cursor = 'pointer';
      guideBtn.style.borderStyle = 'solid';
    } else {
      guideBtn.removeAttribute('href');
      guideBtn.innerHTML = 'Guide Coming Soon ⏳';
      guideBtn.style.display = 'inline-flex';
      guideBtn.style.opacity = '0.55';
      guideBtn.style.cursor = 'default';
      guideBtn.style.borderStyle = 'dashed';
    }"""

    # Replace second occurrence if present for EN
    if new_modal_es in content:
        # We find if there is another old_modal_es in content
        if old_modal_es in content:
            content = content.replace(old_modal_es, new_modal_en, 1)

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"Updated {file_path}: length {orig_len} -> {len(content)}")

if __name__ == "__main__":
    update_file("scripts/generate_recursos_pages.py")
    update_file("layouts/partials/recursos_catalog.html")
