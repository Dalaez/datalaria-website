---
title: "El Bautismo de Fuego: De Excel Basura a Grafo Relacional con Python y Pandas"
date: 2026-05-02
draft: true
categories: ["Ingeniería de la Obsolescencia", "Operations Engineering", "Data Architecture"]
tags: ["Python", "Pandas", "Supabase", "BOM Management", "Data Engineering", "ETL"]
author: "Datalaria"
description: "Cómo ingerir un BOM corrupto exportado de un ERP heredado, limpiar su entropía con Pandas e inyectarlo en Supabase garantizando la idempotencia."
image: "cover.png"
---

## 1. El Gancho: La Entropía de los Datos Industriales

En la teoría académica, los datos fluyen limpios. En la práctica de la cadena de suministro industrial, los ERPs heredados simplemente escupen basura. 

Recibir un *Bill of Materials* exportado en formato de tabla plana desde un sistema obsoleto implica lidiar habitualmente con una alta entropía de datos: celdas completamente vacías, espacios en blanco anómalos ocultos en los números de pieza (ej. `" SN74LS00N "`), nomenclaturas de fabricantes sin estandarizar (mezclando mayúsculas, minúsculas y acrónimos como "ti" o "Texas Inst."), y un tipado inherentemente mixto donde las cantidades numéricas se solapan con campos de tipo *string*.

Intentar inyectar esta entropía tabular en bruto directamente contra una base de datos relacional provocará inevitablemente un colapso en la integridad referencial y múltiples errores de consistencia. Se necesita una capa de extracción y transformación.

## 2. La Tubería ETL (Extract, Transform, Load)

Para asegurar el ecosistema interno es estrictamente necesario implementar una capa intermedia. **Pandas** actúa en este punto como el "portero de discoteca" de nuestra arquitectura operativa.

Antes de que un solo bloque de datos llegue al motor PostgreSQL, nuestro script de Python fuerza la estandarización. Utilizamos métodos puros de limpieza como `.str.strip()`, `.str.title()` y `.fillna()` para normalizar los números de pieza, formatear los nombres de fabricantes (MPNs) y forzar que los campos nulos categóricos como el *Lifecycle* asuman valores computables antes de invocar la API, resolviendo las inconsistencias de raíz:

```python
def load_and_clean_data(filepath: str) -> pd.DataFrame:
    df = pd.read_csv(filepath)
    
    # 1. Limpieza radical de espacios y estandarización a mayúsculas (Evita hardcoding)
    df['Manufacturer_PN'] = df['Manufacturer_PN'].str.strip().str.upper()
    df['Manufacturer'] = df['Manufacturer'].str.strip().str.upper()
    
    # 2. Tipado de datos forzado (Cantidades numéricas garantizadas)
    df['Quantity_per_Assembly'] = pd.to_numeric(
        df['Quantity_per_Assembly'].astype(str).str.strip(), 
        errors='coerce'
    ).fillna(1).astype(int)
    
    # 3. Contención de valores perdidos
    df['Lifecycle'] = df['Lifecycle'].replace(r'^\s*$', np.nan, regex=True).fillna('Active')
    
    return df
```

## 3. El Desafío del Grafo (Rompiendo la Tabla Plana)

Un *Bill of Materials* nunca es una lista unidimensional; es un árbol jerárquico. 

Para escribir los datos masivos en la tabla conectiva `bom_lines`, la cual soporta la barrera relacional restrictiva (`check_parent_exclusive`) en PostgreSQL que diseñamos previamente, el script divide y reconstruye el *DataFrame* en dos bloques estructurales.

Con este modelo de agrupación segregada, logramos separar e insertar el grafo de forma limpia:

*   **Lazo 1:** Relacionando directa y exclusivamente el Producto Final (`End_Product_SKU`) con su Subensamblaje hijo (`Assembly_PN`).
*   **Lazo 2:** Relacionando internamente cada Subensamblaje (`Assembly_PN`) con sus Componentes Base atómicos correspondientes (`Component_PN`).

Esta segregación del lazo de inserción es el método pragmático e idóneo para respetar la restricción cruzada impuesta por Supabase, mapeando el modelo industrial sin provocar desalineamientos ni rechazos de la base de datos.

## 4. La Regla de Oro: Idempotencia en la Ingesta

La condición predeterminante para un pipeline de datos serio es la **Idempotencia**. El script asume explícitamente que un operador automatizado puede y va a ejecutar el sistema de inyección múltiples veces por error sobre los mismos datos.

Operar a nivel de sentencias `INSERT` planas corrompería la integridad de la base de datos duplicando las aristas del grafo. La solución operativa descansa en exprimir las capacidades de `upsert()` facilitadas por el SDK de Supabase, apoyando el peso arquitectural exclusivamente en las columnas con restricción `UNIQUE` (`sku` en productos terminados, `internal_pn` en el listado base, y `mpn` en la telemetría del fabricante foráneo).

Al ejecutar los cruces lógicos con `upsert()`, la integración actúa escrutando, parcheando y cruzando valores sin duplicados. Esta es exactamente la salida directa de la terminal reportando la consistencia en vivo en segundas pasadas:

```text
--- Ingestando Products (Idempotente) ---
Upserted 3 products.
--- Ingestando Internal Parts (Idempotente) ---
Upserted 18 internal parts (assemblies & components).
--- Ingestando Manufacturer Parts Telemetry (Idempotente) ---
Upserted 16 manufacturer external parts.
--- Ingestando AML (Mapeo Interno -> Externo) ---
No new AML links to insert (Idempotent success).
--- Ingestando BOM Lines (Grafo Bidireccional Segregado) ---
Mapeando relaciones: Producto Final -> Subensamblaje...
Mapeando relaciones: Subensamblaje -> Componente...
El Grafo BOM está completamente sincronizado (Idempotent success).

[OK] Migración a entorno relacional completada al 100%.
```

### El Sandbox: Ejecútalo tú mismo

En Ingeniería de Operaciones, el código vale más que la teoría. He preparado un entorno interactivo y seguro (Zero Friction) para que pruebes esta tubería ETL.

No necesitas instalar nada ni configurar bases de datos. El script levantará un motor SQL en la memoria de tu navegador, ingerirá un archivo CSV corrupto, lo limpiará con Pandas y construirá el árbol relacional en milisegundos demostrando la idempotencia en vivo.

🔗 [Accede al Google Colab Interactivo Aquí](https://colab.research.google.com/drive/1kMLX2RexPSZVHXuXURZ1VnF_w2nRPgxg?usp=sharing)

## 5. Cierre y Próximos Pasos

La arquitectura e inyección operativa están finalizadas. Hemos tomado un conjunto de datos estáticos y fuertemente corruptos de un entorno excel plano, estandarizado sus anomalías por código, e insertado los flujos resultantes en una base de datos relacional de Supabase totalmente normalizada.

> Los cimientos están terminados. Tenemos una base de datos relacional IEC 62402 compliant y un motor de ingesta automatizado operando en frío. En el próximo bloque (Bloque 3), le daremos vida computacional al sistema. Conectaremos infraestructuras modulares de Agentes IA (LangChain / CrewAI) directamente sobre la base de datos PostgreSQL, facultándolas para leer los avisos EOL del mercado y calcular el impacto financiero crítico sobre los nodos lógicos de forma unificada e ininterrumpida. Suscríbete para el despliegue del Radar Agéntico.
