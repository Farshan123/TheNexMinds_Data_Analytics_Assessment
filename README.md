# The NexMinds Data Analytics Assessment
## Osmania University Undergraduate (UG) Colleges Analytics (2026 Admissions Cycle)

**Candidate:** Mohammed Farshan  
**Evaluation:** Data Analyst Assessment  
**Domain:** Higher Education Analytical Modeling, Educational Accessibility & Institutional Capacity  

---

## 1. Executive Summary

This project delivers an end-to-end data analytics and business intelligence solution evaluating undergraduate course offerings across 356 colleges affiliated with Osmania University for the 2026 academic admissions cycle.

The raw dataset contained semi-structured multi-value text declarations with newline and pipe delimiters (`Degree | SubCourse | Medium`). Through an enterprise-grade ETL pipeline, the data was parsed, normalized, harmonized, and architected into a Star Schema data model (`FactCourses` and `DimCollege`) ready for interactive exploration in **Power BI Desktop** and **Python**.

### Key Scorecard Metrics:
- **Total Affiliated Institutions:** 356 colleges (355 offering parsed UG courses; 1 institution without standard delimiters)
- **Total Normalized Course Offerings:** 2,031 atomic courses
- **Top Degree Category:** B.Sc (980 offerings, 48.25% market share)
- **Dominant Instructional Medium:** English (1,576 offerings, 77.60% share)
- **Primary Regional Medium:** Telugu (433 offerings, 21.32% share)
- **Median Courses per College:** 5 offerings (Min: 1, Max: 27)

---

## 2. Directory Structure

```text
TheNexMinds_Data_Analytics_Assessment/
│
├── README.md                                # Comprehensive project documentation
│
├── data/                                    # Raw and processed datasets
│   ├── original_dataset.xlsx                # Source Excel dataset (OU UG Colleges 2026)
│   ├── cleaned_course_data.xlsx             # Normalized Fact table (2,031 rows)
│   ├── fact_courses.xlsx                    # Alternative Fact table naming
│   ├── dim_college.xlsx                     # Institutional Dimension table (356 rows)
│   └── dim_college.csv                      # CSV export for cross-platform interop
│
├── python/                                  # Python analysis & notebooks
│   └── NexMinds_Analysis.ipynb              # Fully executed Jupyter Notebook (Sections 1 to 9)
│
├── powerbi/                                 # Power BI solution & modeling assets
│   ├── NexMinds_UG_Analytics.pbix           # Interactive Power BI report file
│   ├── DAX_Measures.dax                     # Complete catalog of DAX calculated measures
│   ├── DataModel_Guide.md                   # Modeling architecture and dashboard layout guide
│   ├── cleaned_course_data.xlsx             # Linked Fact dataset
│   └── dim_college.xlsx                     # Linked Dimension dataset
│
├── report/                                  # Executive publication deliverables
│   └── NexMinds_Data_Analytics_Report.pdf   # 6-page comprehensive executive PDF report
│
└── images/                                  # High-resolution visual artifacts
    ├── dashboard.png                        # Complete 16:9 Power BI dashboard mockup
    ├── degree_distribution.png              # Course offerings by degree horizontal bar
    ├── medium_distribution.png              # Medium of instruction breakdown
    ├── degree_vs_medium.png                 # 100% stacked bar: Degree vs Medium
    ├── college_coverage.png                 # College availability coverage by degree
    ├── top10_colleges.png                   # Top 10 institutions by academic breadth
    ├── top15_subcourses.png                 # Top 15 subject combinations
    └── course_distribution_histogram.png    # Distribution of offerings per institution
```

---

## 3. Data Architecture & Modeling (Star Schema)

The analytical data model separates institutional metadata from course transaction records:

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

### The 355 vs 356 College Anomaly
During quality auditing, **College Code 1171** (*Road Mystry Degree College*) was found to contain the raw course entry `"BSW\nBSW English"` without pipe delimiters (`|`). Standard 3-token parsing produces no course record for this row.
- **Dimension Table (`DimCollege`):** Retains all **356 colleges** as the source master.
- **Fact Table (`FactCourses`):** Contains **2,031 offerings** spanning **355 course-bearing colleges**.
- Maintaining this separation ensures dashboard KPI cards display `Total Colleges = 356` while correctly distinguishing `Colleges with Courses = 355`.

---

## 4. Power BI Calculated DAX Measures

| Measure Name | DAX Formula | Result | Description |
| :--- | :--- | :--- | :--- |
| **Total Colleges** | `DISTINCTCOUNT(DimCollege[College Code])` | **356** | Total affiliated institutions in universe |
| **Colleges with Courses** | `DISTINCTCOUNT(FactCourses[College Code])` | **355** | Institutions offering parsed UG courses |
| **Total Course Offerings** | `COUNTROWS(FactCourses)` | **2,031** | Total normalized undergraduate course tracks |
| **Total Degrees** | `DISTINCTCOUNT(FactCourses[Degree])` | **4** | B.Sc, B.Com, B.A, BBA |
| **Total SubCourses** | `DISTINCTCOUNT(FactCourses[SubCourse])` | **67** | Distinct curriculum combinations |
| **English Offerings** | `CALCULATE([Total Course Offerings], FactCourses[Medium] = "English")` | **1,576** | Course offerings conducted in English |
| **English Share** | `DIVIDE([English Offerings], [Total Course Offerings], 0)` | **77.6%** | Market share of English-medium courses |
| **Telugu Offerings** | `CALCULATE([Total Course Offerings], FactCourses[Medium] = "Telugu")` | **433** | Course offerings conducted in Telugu |
| **Telugu Share** | `DIVIDE([Telugu Offerings], [Total Course Offerings], 0)` | **21.3%** | Market share of Telugu-medium courses |
| **Top Degree** | `"B.Sc"` | **B.Sc** | Leading degree program by course volume |

---

## 5. The 6 Core Key Insights

1. **Insight 1 — B.Sc Dominates Offerings Volume:**  
   B.Sc accounts for **48.25% (980 of 2,031)** of all course offerings, making it the single largest degree program by curriculum variety.
   
2. **Insight 2 — B.Com Possesses Broadest Institutional Reach:**  
   B.Com is available in **95.2% of colleges (339 of 356)**. Although B.Sc has more specific subject permutations, commerce is the universal standard program across affiliated campuses.

3. **Insight 3 — English is the Prevailing Medium of Higher Education:**  
   English represents **77.6% (1,576 offerings)** of all courses, serving as the default instruction vehicle for science, commerce, and business disciplines.

4. **Insight 4 — B.A Displays a Critical Regional Language Inversion:**  
   Unlike B.Sc (83.6% English) and B.Com (83.9% English), **B.A features 160 Telugu-medium offerings versus 94 English-medium offerings (1.7 : 1 ratio)**. Telugu constitutes **59.9%** of all B.A offerings, underscoring the vital sociolinguistic and public-service role played by vernacular arts education.

5. **Insight 5 — Course Availability is Highly Skewed Across Colleges:**  
   The median affiliated college offers only **5 courses**, whereas premier autonomous colleges offer up to **27 courses** (*St. Ann's Degree College for Women*). Over 75% of institutions offer 7 or fewer courses.

6. **Insight 6 — Computing and General Tracks Form the University Backbone:**  
   `General` (369 offerings) and `Computers` (301 offerings) are the two most prevalent subcourse labels, followed by computational science combinations (Math/Stats/CS: 173, Math/Physics/CS: 165).

---

## 6. Strategic Recommendations

1. **Prioritize Laboratory & Faculty Capacity in B.Sc and B.Com:**  
   Together, B.Sc and B.Com represent **85.3% of all course volume**. Academic governance and resource allocations should focus primarily on infrastructure audits and modernized lab capabilities in these two degree programs.

2. **Protect Regional Language Equity in Humanities:**  
   The strong demand for Telugu B.A programs indicates that humanities courses serve rural and first-generation learners. Universities should avoid unilateral elimination of Telugu tracks while providing bilingual bridge modules to aid English transition.

3. **Establish Academic Consortiums for Rural College Portfolio Broadening:**  
   Because half of colleges offer 5 or fewer course tracks, Osmania University should implement regional hub-and-spoke networks allowing smaller colleges to share faculty for interdisciplinary minors.

4. **Industry Co-Certification of Applied Computing Programs:**  
   With over 700 aggregate computing-oriented courses, the university should partner directly with IT bodies (NASSCOM, TASK) to co-certify curricula in cloud computing, data analysis, and web engineering.

---

## 7. Submission Deliverables Summary

| Deliverable | Location | Details |
| :--- | :--- | :--- |
| **Power BI Model & Report** | `powerbi/NexMinds_UG_Analytics.pbix` | Star Schema data model, 10 DAX measures, 3 slicers, 5 visual charts, 4 KPI cards |
| **Executive PDF Report** | `report/NexMinds_Data_Analytics_Report.pdf` | 6-page comprehensive executive PDF report with embedded charts, tables, and methodology |
| **Jupyter Notebook** | `python/NexMinds_Analysis.ipynb` | Fully executed notebook with 9 markdown sections, complete statistics, and rendered figures |
| **Data Model Assets** | `data/cleaned_course_data.xlsx`, `dim_college.xlsx` | Normalized and standardized data tables |
| **Visual Artifacts** | `images/dashboard.png` + 7 chart figures | High-resolution publication graphics |
