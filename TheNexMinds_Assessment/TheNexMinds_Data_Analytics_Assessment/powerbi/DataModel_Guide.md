# Power BI Data Model & Dashboard Implementation Guide

## 1. Data Model Architecture (Star Schema)

The analytical data model uses a Star Schema design separating the course fact transactions from institutional dimensions:

```
┌───────────────────────────────────────┐
│              DimCollege               │
├───────────────────────────────────────┤
│ • College Code (PK, Int64)            │ ◄─── (1)
│ • College Name (Text)                 │
│ • Address / Contact / Website (Text)  │
└───────────────────────────────────────┘
                    │
                    │ 1-to-Many Relationship
                    │ (DimCollege[College Code] 1 ───► * FactCourses[College Code])
                    ▼
┌───────────────────────────────────────┐
│              FactCourses              │
├───────────────────────────────────────┤
│ • College Code (FK, Int64)            │ ◄─── (*)
│ • College Name (Text)                 │
│ • Degree (Text: B.Sc, B.Com, B.A, BBA)│
│ • SubCourse (Text)                    │
│ • Medium (Text: English, Telugu, etc.)│
└───────────────────────────────────────┘
```

### Table Specifications:
1. **`FactCourses`** (Imported from `cleaned_course_data.xlsx` / `fact_courses.xlsx`):
   - Rows: 2,031 course offerings
   - Columns: `College Code`, `College Name`, `Degree`, `SubCourse`, `Medium`
2. **`DimCollege`** (Imported from `dim_college.xlsx`):
   - Rows: 356 institutions
   - Columns: `College Code`, `College Name`, `Address / Contact / Website`

---

## 2. Key Data Distinctions
- **Total Colleges in Dimension (`DimCollege`)**: **356**
- **Colleges with Parsed Courses (`FactCourses`)**: **355**
- **Non-Parsed Institution**: College Code `1171` (*Road Mystry Degree College*) has raw entry `"BSW\nBSW English"` lacking pipe `|` delimiters, producing no parsed 3-part record.
- By maintaining `DimCollege` as the master dimension, our KPI correctly reflects **356 total institutions** across the university ecosystem.

---

## 3. Power BI Calculated Measures

All DAX formulas are located in `DAX_Measures.dax`:

| Measure Name | DAX Expression | Formatted Value |
| :--- | :--- | :--- |
| **Total Colleges** | `DISTINCTCOUNT(DimCollege[College Code])` | **356** |
| **Colleges with Courses** | `DISTINCTCOUNT(FactCourses[College Code])` | **355** |
| **Total Course Offerings** | `COUNTROWS(FactCourses)` | **2,031** |
| **Total Degrees** | `DISTINCTCOUNT(FactCourses[Degree])` | **4** |
| **Total SubCourses** | `DISTINCTCOUNT(FactCourses[SubCourse])` | **67** |
| **English Offerings** | `CALCULATE([Total Course Offerings], FactCourses[Medium] = "English")` | **1,576** |
| **English Share** | `DIVIDE([English Offerings], [Total Course Offerings], 0)` | **77.6%** |
| **Telugu Offerings** | `CALCULATE([Total Course Offerings], FactCourses[Medium] = "Telugu")` | **433** |
| **Telugu Share** | `DIVIDE([Telugu Offerings], [Total Course Offerings], 0)` | **21.3%** |
| **Top Degree** | `"B.Sc"` | **B.Sc** |

---

## 4. Dashboard Canvas Layout & Visuals

### Canvas Settings:
- Resolution: 16:9 widescreen (1920 × 1080 px)
- Theme: Clean Slate / Executive Fluent

### Top Section:
1. **Header Banner**: Dark Navy `#0F172A` with title:
   - *"OSMANIA UNIVERSITY UG ANALYTICS — 2026"*
2. **Interactive Slicers** (Top Right):
   - `FactCourses[Degree]`
   - `FactCourses[Medium]`
   - `DimCollege[College Name]`
3. **KPI Scorecard Cards**:
   - Card 1: `Total Colleges` = **356**
   - Card 2: `Total Course Offerings` = **2,031**
   - Card 3: `English Share` = **77.6%**
   - Card 4: `Top Degree` = **B.Sc** (980 offerings)

### Visual Body:
1. **Chart 1 — Course Offerings by Degree**:
   - Visual: Clustered Horizontal Bar Chart
   - Y-Axis: `FactCourses[Degree]`
   - X-Axis: `[Total Course Offerings]`
   - Values: B.Sc (980), B.Com (752), B.A (267), BBA (32)
2. **Chart 2 — Medium Distribution**:
   - Visual: Donut Chart
   - Legend: `FactCourses[Medium]`
   - Values: `[Total Course Offerings]`
   - Center Callout: 2,031 Offerings
3. **Chart 3 — Degree vs Medium (Key Insight)**:
   - Visual: 100% Stacked Bar Chart
   - Y-Axis: `FactCourses[Degree]`
   - X-Axis: `[Total Course Offerings]`
   - Legend: `FactCourses[Medium]`
   - *Key Finding*: B.A is 59.9% Telugu (160) vs 35.2% English (94).
4. **Chart 4 — College Coverage by Degree**:
   - Visual: Clustered Column Chart
   - X-Axis: `FactCourses[Degree]`
   - Y-Axis: `Distinct Count of College Code`
   - Values: B.Com (339 / 95.2%), B.Sc (293 / 82.3%), B.A (147 / 41.3%), BBA (32 / 9.0%)
5. **Chart 5 — Top Colleges by Course Offerings**:
   - Visual: Horizontal Bar Chart
   - Y-Axis: `FactCourses[College Name]` (Top N = 10 by `[Total Course Offerings]`)
   - Leader: St. Ann's Degree College for Women (27 offerings)
