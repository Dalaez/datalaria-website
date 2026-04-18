---
title: "The Risk Map: Architecting an Obsolescence-Immune Data Foundation"
date: 2026-04-18
draft: false
categories: ["Obsolescence Engineering", "Operations Engineering", "Data Architecture"]
tags: ["Supabase", "PostgreSQL", "BOM Management", "Data Modeling", "IEC 62402", "Supply Chain"]
author: "Datalaria"
description: "How to design a relational database in Supabase to structure an industrial BOM and integrate external market telemetry."
image: "cover.png"
---

## 1. The Flat Table Trap (Excel is Dead)

Managing an industrial *Bill of Materials* (BOM) through spreadsheets is a structural deficiency. Excel provides a two-dimensional environment for a three-dimensional problem. Hardware engineering and manufacturing dependencies operate under a graph logic.

When the procurement department receives an *End of Life* (EOL) alert for a component, calculating the volumetric impact by searching text across multiple static documents introduces operational latency.

The **UNE-EN IEC 62402:2019** standard, in its **Clause 8.10 (Data Acquisition)**, establishes the requirement to maintain "a list of configuration sub items within an item" alongside "the identification of the items and sub items details: manufacturer, part number and specification". Achieving the level of parametric traceability demanded by the standard requires the design of a relational data model.

## 2. Modeling Reality: The Graph Approach (The Internal Environment)

A bill of materials is a dependency tree. To structure the internal manufacturing environment data in PostgreSQL, we define three main indexed tables:

*   **`products`**: Represents the end products. Includes the `gross_margin` parameter, required to correlate component supply risk with the financial impact on the P&L.
*   **`internal_parts`**: A consolidated register of components, raw materials, and sub-assemblies defined by engineering. Uses a global unique identifier (`internal_pn`).
*   **`bom_lines`**: Implements the hierarchical relationship. Defines dependencies through mutually exclusive foreign keys (`parent_product_id` or `parent_assembly_id`) to a child component (`child_pn`), specifying a `quantity`.

**Technical Validation:** Normalizing the data into a graph structure enables the use of recursive algorithms capable of calculating total exposure in milliseconds. If "Equipment A" requires 4 capacitors and "Equipment B" requires 12, a shortage alert on the component node propagates mathematically and automatically up the tree, cross-referencing totals against the order backlog (SLAs).

## 3. The Firewall: The AML Table (Approved Manufacturer List)

A core principle of industrial inventory integrity is to prevent the mixing of internal nomenclature with dynamic global market references. Omitting this separation generates traceability inconsistencies.

The architecture implements the **`aml` (Approved Manufacturer List)** table as an interface between internal hardware design and the supply chain.

This table enables the **Dual-Sourcing** strategy. If the bill of materials specifies the component `CAP-10K` (ERP code), the `aml` table relates this internal node to both a Texas Instruments reference (`preference_level: Primary`) and a validated equivalent from Analog Devices (`preference_level: Secondary`). Upon a supply interruption from the primary source, the relational logic allows switching demand to the secondary source without altering the base BOM.

## 4. The Integrated Radar (The External Environment)

Integration with global commercial dynamics is consolidated in the **`manufacturer_parts`** table.

This entity receives telemetry flows from market aggregators (*SiliconExpert*, *IHS Markit*, *Accuris*) through asynchronous integrations. It maintains an updated record of the manufacturer part numbers (`mpn`), their lifecycle state (`lifecycle_status`), and the estimated obsolescence date (`estimated_eol_date`).

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

    PRODUCTS ||--o{ BOM_LINES : "contains (parent)"
    INTERNAL_PARTS ||--o{ BOM_LINES : "contains (subassembly)"
    INTERNAL_PARTS ||--o{ BOM_LINES : "is consumed as (child)"
    INTERNAL_PARTS ||--|{ AML : "is resolved by"
    AML }o--|| MANUFACTURER_PARTS : "maps external telemetry"
{{< /mermaid >}}

## 5. Data Segmentation and Intellectual Property (RLS in Supabase)

Deploying this model involves managing Intellectual Property (IP) assets. Accidental or unauthorized exposure of the complete product topology is an unacceptable information security risk. Leveraging the Supabase platform allows implementing security architectures at the data layer.

To prevent external generative models (LLMs) or unprivileged users from reconstructing the complete BOM dependencies, we apply **Row Level Security (RLS)** directly in PostgreSQL:

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

The policies restrict any modifications to the `products` and `bom_lines` tables to the "Admin" role. Additionally, the architectural design dictates that the database must parse the mathematical expansion of the tree internally and provide the external AI Agent with only the aggregated risk value, without returning the topological structure.

## 6. Next Steps

The relational database schema for obsolescence management is defined based on modular integrity principles.

> The next step in the data architecture process will focus on integration automation. We will evaluate development in Python, using the Pandas library, to engineer an extraction, transformation, and loading (ETL) pipeline capable of ingesting BOM lists in Excel format and structurally populating them into this Supabase ecosystem. Subscribe to access this operational phase.
