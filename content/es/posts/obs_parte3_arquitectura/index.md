---
title: "El Mapa del Riesgo: Diseñando una Arquitectura de Datos Inmune a la Obsolescencia"
date: 2026-03-29
draft: false
categories: ["Ingeniería de la Obsolescencia", "Operations Engineering", "Data Architecture"]
tags: ["Supabase", "PostgreSQL", "BOM Management", "Data Modeling", "IEC 62402", "Supply Chain"]
author: "Datalaria"
description: "Cómo diseñar una base de datos relacional en Supabase para estructurar un BOM industrial e integrar telemetría de mercado externo."
image: "cover.png"
---

## 1. La Trampa de la Tabla Plana (Excel is Dead)

Gestionar un *Bill of Materials* (BOM) industrial a través de hojas de cálculo es una deficiencia estructural. Excel proporciona un entorno bidimensional para un problema tridimensional. Las dependencias de ingeniería de *hardware* y manufactura operan bajo una lógica de grafos.

Cuando el departamento de compras recibe una alerta de *End of Life* (EOL) de un componente, calcular el impacto volumétrico buscando texto en múltiples documentos estáticos provoca retrasos en la respuesta operativa.

El estándar **UNE-EN IEC 62402:2019**, en su **Cláusula 8.10 (Adquisición de datos)**, establece el requisito de mantener "una lista de subelementos de configuración dentro de un elemento" junto a "la identificación de los detalles del elemento y subelemento: fabricante, número de pieza y especificación". Alcanzar el nivel de trazabilidad paramétrica exigido por la norma requiere el diseño de un modelo de datos relacional.

## 2. Modelando la Realidad: El Enfoque de Grafo (El Entorno Interno)

Una lista de materiales es un árbol de dependencias. Para estructurar los datos del entorno de fabricación interno en PostgreSQL, definimos tres tablas principales indexadas:

*   **`products`**: Representa los productos finales. Incluye el parámetro `gross_margin`, necesario para correlacionar el riesgo de suministro de componentes con el impacto financiero en el P&L.
*   **`internal_parts`**: Un registro consolidado de componentes, materias primas y subensamblajes definidos por ingeniería. Utiliza un identificador único global (`internal_pn`). 
*   **`bom_lines`**: Implementa la relación jerárquica. Define las dependencias mediante claves foráneas excluyentes (`parent_product_id` o `parent_assembly_id`) hacia un componente hijo (`child_pn`) especificando una cantidad (`quantity`).

**Validación Técnica:** Al normalizar los datos en una estructura de grafo, se habilita el uso de algoritmos recursivos capaces de calcular la exposición total en milisegundos. Si el "Equipo A" requiere 4 condensadores y el "Equipo B" requiere 12, una alerta de escasez en el nodo del componente se propaga matemática y automáticamente hacia arriba en el árbol, cruzando los totales contra la cartera de pedidos (SLAs).

## 3. El Cortafuegos: La Tabla AML (Approved Manufacturer List)

Un principio básico de integridad en inventarios industriales es evitar la mezcla de la nomenclatura interna con las referencias dinámicas del mercado global. Omitir esta separación genera inconsistencias en la trazabilidad.

La arquitectura implementa la tabla **`aml` (Approved Manufacturer List)** como interfaz entre el diseño de *hardware* interno y la cadena de suministro.

Esta tabla viabiliza la estrategia de **Dual-Sourcing**. Si la lista de materiales especifica el componente `CAP-10K` (código ERP), la tabla `aml` relaciona este nodo interno tanto con una referencia de Texas Instruments (`preference_level: Primary`) como con una equivalente validada de Analog Devices (`preference_level: Secondary`). Ante una interrupción de suministro de la fuente primaria, la lógica relacional permite conmutar la demanda hacia la fuente secundaria sin alterar el BOM base.

## 4. El Radar Integrado (El Entorno Externo)

La integración con la dinámica comercial global se consolida en la tabla **`manufacturer_parts`**. 

Esta entidad recibe los flujos de telemetría de agregadores de mercado (*SiliconExpert*, *IHS Markit*, *Accuris*) a través de integraciones asíncronas. Mantiene un registro actualizado de los números de parte del fabricante (`mpn`), su estado de ciclo de vida (`lifecycle_status`) y la fecha estimada de obsolescencia (`estimated_eol_date`).

{{< mermaid >}}
erDiagram
    PRODUCTS {
        UUID id PK
        VARCHAR sku
        NUMERIC gross_margin
    }
    INTERNAL_PARTS {
        UUID id PK
        VARCHAR internal_pn
        ENUM part_type
    }
    BOM_LINES {
        UUID id PK
        UUID parent_product_id FK
        UUID parent_assembly_id FK
        UUID child_pn FK
        INTEGER quantity
    }
    AML {
        UUID id PK
        UUID internal_pn FK
        VARCHAR manufacturer_pn
        ENUM preference_level
    }
    MANUFACTURER_PARTS {
        UUID id PK
        VARCHAR mpn
        ENUM lifecycle_status
        DATE estimated_eol_date
    }

    PRODUCTS ||--o{ BOM_LINES : "contiene (padre)"
    INTERNAL_PARTS ||--o{ BOM_LINES : "contiene (subensamblaje)"
    INTERNAL_PARTS ||--o{ BOM_LINES : "es consumido como (hijo)"
    INTERNAL_PARTS ||--|{ AML : "es resuelto por"
    AML }o--|| MANUFACTURER_PARTS : "mapea telemetría externa"
{{< /mermaid >}}

## 5. Segmentación de Datos y Propiedad Intelectual (RLS en Supabase)

Desplegar este modelo implica gestionar activos de Propiedad Intelectual (IP). La exposición accidental o no autorizada de la topología completa de los productos es un riesgo de seguridad de la información inaceptable. El uso de la plataforma Supabase permite implementar arquitecturas de seguridad en la capa de datos.

Para evitar que modelos generativos externos (LLMs) o usuarios sin privilegios reconstruyan las dependencias completas del BOM, aplicamos **Row Level Security (RLS)** directamente en PostgreSQL:

```sql
-- Security: Row Level Security (RLS) policies - IP Protection
ALTER TABLE products ENABLE ROW LEVEL SECURITY;
ALTER TABLE bom_lines ENABLE ROW LEVEL SECURITY;

-- Allow general read access to authenticated logic
CREATE POLICY "Allow read access to authenticated users" 
ON products FOR SELECT TO authenticated USING (true);

-- Restrict mutations (insert/update/delete) on products and BOM lines to Admin role exclusively
CREATE POLICY "Restrict products mutations to admins" 
ON products FOR ALL TO authenticated 
USING ((auth.jwt() ->> 'role') = 'admin');
```

Las políticas restringen cualquier modificación de las tablas `products` y `bom_lines` al rol "Administrador". Adicionalmente, el diseño arquitectónico dicta que la base de datos debe procesar la expansión matemática del árbol de manera interna y proporcionar al Agente IA externo únicamente el valor del riesgo agregado, sin devolver la estructura topológica.

## 6. Siguientes Pasos

El esquema de base de datos relacional para la gestión de la obsolescencia está definido en base a principios de integridad modular. 

> El próximo paso en el proceso de arquitectura de datos se centrará en la automatización de la integración. Evaluaremos el desarrollo en Python, utilizando la librería Pandas, para diseñar un *pipeline* de extracción, transformación y carga (ETL) capaz de ingerir listados BOM en formato Excel y poblarlos estructuralmente en este ecosistema Supabase. Suscríbete para acceder a esta fase operativa.
