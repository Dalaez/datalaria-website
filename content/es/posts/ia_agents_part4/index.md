---
title: "La Pesadilla de las APIs: Cómo vencí a la burocracia de LinkedIn para automatizar mi empresa"
date: 2025-12-28
draft: false
categories: ["Backend", "Python", "APIs"]
tags: ["LinkedIn API", "Twitter API", "OAuth", "Automation", "DevOps"]
image: "/images/posts/datalaria-api-victory.jpg"
description: "Cuarto capítulo de Proyecto Autopilot. Lo que iba a ser un script de 10 minutos se convirtió en una guerra de formularios. Narramos cómo desbloqueamos el permiso 'w_organization_social' para publicar como Empresa."
summary: "Conectar una API suele ser fácil... hasta que intentas publicar en una Página de Empresa de LinkedIn. En este post narro la odisea de permisos, verificaciones y formularios de 'Marketing Developer Platform' que tuve que superar para que mi script de Python pudiera hablar oficialmente en nombre de Datalaria."
---

Hasta ahora, todo era divertido. Teníamos agentes de IA con personalidades cínicas ([Post 3]({{< ref "ia_agents_part3" >}})) y un cerebro capaz de analizar texto ([Post 2]({{< ref "ia_agents_part2" >}})). Pero todo vivía en la seguridad de mi terminal, en `localhost`.

Para que **Datalaria Autopilot** fuera real, tenía que salir al mundo.

Aquí es donde el proyecto dejó de ser un problema de ingeniería y se convirtió en una batalla contra la **Burocracia de las APIs**.

![Imagen conceptual del proyecto - La pesadilla de las APIs](autopilot_api_nightmare.png)

## El Objetivo: Publicar como Marca, no como Persona

Mi requisito era claro: No quiero que el bot publique en mi perfil personal de LinkedIn. Quiero que publique en la **Página de Empresa de Datalaria**, con el logo oficial y tono corporativo.

Técnicamente, esto requiere un cambio en el endpoint de la API:
* Perfil Personal: `urn:li:person:12345`
* Página de Empresa: `urn:li:organization:110125695`

Parece un cambio de una línea de código. **Fueron un par de días de espera y gestiones.**

## Batalla 1: Twitter (X) y el Muro Anti-Bots

Primero, Twitter. Conseguir acceso a la API hoy en día requiere pasar un casting. Tuve que solicitar el *Free Tier* y escribir una "carta de motivación" explicando que no soy un bot de spam, sino un técnico aficionado de la IA.

Tras superar el error `403 Forbidden` (olvidé activar los permisos de "Read & Write") y el error `Duplicate Content` (intenté enviar el mismo "Hello World" dos veces), logré la conexión. Twitter/X estaba listo y a priori todo funcionaba de manera sencilla.

![Post publicado automáticamente en twitter](datalaria_twitter_first_publication.png)

## Batalla 2: El Jefe (LinkedIn Company Pages)

El mayor problema ocurrió en LinkedIn.

Diseñé mi script `social_manager.py` para usar un ID de empresa si existía en las variables de entorno:

```python
# Lógica híbrida en Python
if company_id:
    print(f"🏢 Detectado Company ID. Publicando como página...")
    author_urn = f"urn:li:organization:{company_id}"
else:
    print("👤 Publicando como perfil personal...")
```

Al ejecutarlo, la consola me escupió un error rojo sangre:
> `❌ Error posting to LinkedIn: Status 403: ACCESS_DENIED`

### El Permiso Fantasma: `w_organization_social`
Descubrí que el token estándar de LinkedIn solo te da permiso `w_member_social` (publicar como persona). El permiso para empresas (`w_organization_social`) **no existía** en mi panel de desarrollador.

Para desbloquearlo, tuve que completar una *gimkana* administrativa:

1.  **Verificación de Página:** Tuve que generar una URL especial en el Developer Portal y aprobarla con mi cuenta de administrador. Resultado: *Company Verified*. ✅
2.  **Aún así, no funcionaba:** El permiso seguía sin aparecer.
3.  **La Solicitud Oculta:** Tuve que solicitar acceso al producto **"Marketing Developer Platform"**.
4.  **El Formulario:** LinkedIn me hizo rellenar un cuestionario detallando que soy un "Direct Customer", que no soy una agencia de publicidad y que mi uso es estrictamente interno para automatización orgánica.

### La Victoria

Tras unas horas de espera, llegó el correo de aprobación. Volví a generar el token y... ¡ahí estaba!

Con el nuevo "Super Token" cargado en mi `.env`, ejecuté el script una última vez.

```text
--- TESTING SOCIAL MEDIA MANAGER ---
DTO - Posting to Twitter... ✅ Success!
DTO - Posting to LinkedIn...
🏢 Detectado Company ID: 110125695.
✅ LinkedIn Success! Post ID: urn:li:share:741...
```

Y la prueba definitiva en la red social:

![Post publicado automáticamente en la página de Datalaria en Linkedin](datalaria_linkedin_first_publication.png)

## Conclusión y Siguientes Pasos

He logrado lo que parecía imposible: un script de Python que tiene autorización legal para actuar como mi empresa.

Pero hay un problema final: **Este token caduca en 60 días.**

Si no hago nada, en dos meses todo este sistema se romperá. Además, sigo ejecutando el script manualmente desde mi ordenador.

En el **último post** de esta serie, vamos a automatizarlo todo. Usaremos **GitHub Actions** para que el sistema se ejecute solo cada vez que subo un artículo, y (si la API nos deja) implementaremos la renovación automática de tokens.

**Próximamente Post 5: Automatización Total (CI/CD).**

👉 **Código Fuente:** El módulo `social_manager.py` final está disponible en el [repo de GitHub](https://github.com/Dalaez/datalaria-website/tree/main/autopilot).