import nbformat as nbf
import os

nb = nbf.v4.new_notebook()

cells = []

# Title
cells.append(nbf.v4.new_markdown_cell("""# The NexMinds Data Analytics Assessment
### Comprehensive Undergraduate Course Landscape Analysis — Osmania University (2026)
**Author:** Mohammed Farshan  
**Role:** Data Analytics Candidate  
**Tools:** Python (Pandas, NumPy, Matplotlib, Seaborn), Power BI Desktop, Excel  
"""))

# 1. Business Objective
cells.append(nbf.v4.new_markdown_cell("""## 1. Business Objective

The primary objective of this project is to conduct an end-to-end data analysis of undergraduate (UG) course offerings across colleges affiliated with Osmania University for the 2026 academic admissions cycle.

Key goals include:
1. **Data Ingestion & Cleaning:** Parse unstructured, multi-value course strings stored as newline-delimited, pipe-separated records into a normalized fact table.
2. **Quality & Structural Audit:** Detect anomalies, missing attributes, non-delimited rows, and investigate institutional portfolio breadth.
3. **Exploratory Data Analysis (EDA):** Quantify degree market shares, instructional medium distributions, institutional coverage rates, and subject combinations.
4. **Data Modeling:** Design an optimal Star Schema model (`DimCollege` and `FactCourses`) for Power BI analytical reporting.
5. **Strategic Insights & Actionable Recommendations:** Deliver quantified findings and evidence-based proposals for university administrators, academic planners, and higher education policymakers.
"""))

# 2. Dataset Overview
cells.append(nbf.v4.new_markdown_cell("""## 2. Dataset Overview

The source dataset is provided as an Excel spreadsheet titled `TheNexMinds_Data_Analytics_Assessment_Dataset.xlsx` under the sheet `OU UG Colleges 2026`.

Each record represents an affiliated college with institutional identification, contact details, and a semi-structured course text field containing one or more course offerings.
"""))

cells.append(nbf.v4.new_code_cell("""import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Set visual styling
sns.set_theme(style="whitegrid", palette="muted")
plt.rcParams['font.sans-serif'] = 'Segoe UI'
plt.rcParams['figure.dpi'] = 150

# Ingest raw dataset
candidate_paths = [
    os.path.join("..", "data", "original_dataset.xlsx"),
    os.path.join("data", "original_dataset.xlsx"),
    os.path.join("..", "..", "data", "original_dataset.xlsx"),
    os.path.join("data", "TheNexMinds_Data_Analytics_Assessment_Dataset.xlsx"),
    os.path.join("..", "data", "TheNexMinds_Data_Analytics_Assessment_Dataset.xlsx"),
    "C:/Users/MOHAMMED FARSHAN/OneDrive/Desktop/TheNexMinds_Assessment/data/original_dataset.xlsx"
]
raw_file_path = next((p for p in candidate_paths if os.path.exists(p)), "data/original_dataset.xlsx")

df_raw = pd.read_excel(raw_file_path, sheet_name="OU UG Colleges 2026")
print(f"Dataset Dimensions: {df_raw.shape[0]} rows, {df_raw.shape[1]} columns")
print("\\nColumns:", list(df_raw.columns))
df_raw.head()
"""))

# 3. Data Quality Assessment
cells.append(nbf.v4.new_markdown_cell("""## 3. Data Quality Assessment

Before performing transformation, we conduct a data quality audit covering:
- Completeness (missing/null values)
- Uniqueness (duplicate college records or codes)
- Delimiter consistency in the course text field
"""))

cells.append(nbf.v4.new_code_cell("""# 1. Missing Value Audit
print("Missing values per column:")
print(df_raw.isnull().sum())

# 2. Duplicate Checks
print(f"\\nDuplicate rows across all columns: {df_raw.duplicated().sum()}")
print(f"Total College Codes: {len(df_raw['College Code'])}")
print(f"Unique College Codes: {df_raw['College Code'].nunique()}")

# 3. Address column nulls
null_address = df_raw[df_raw['Address / Contact / Website'].isnull()]
print(f"Colleges missing address/contact info: {len(null_address)}")
"""))

cells.append(nbf.v4.new_markdown_cell("""### Data Quality Finding: The Delimiter Anomaly (College 1171)
Upon checking the course delimiter structure (`Degree | SubCourse | Medium`), we identify that **College Code 1171** (*Road Mystry Degree College*) contains an entry `"BSW\\nBSW English"` without standard pipe delimiters (`|`). 

This explains why the raw file has **356 colleges**, but only **355 colleges** produce valid 3-part parsed course offerings.
"""))

cells.append(nbf.v4.new_code_cell("""# Inspect College 1171 raw course record
college_1171 = df_raw[df_raw['College Code'] == 1171]
print("Raw Course string for College 1171:")
print(repr(college_1171['Courses | SubCourse | Medium'].values[0]))
"""))

# 4. Data Cleaning
cells.append(nbf.v4.new_markdown_cell("""## 4. Data Cleaning

Data cleaning operations performed:
1. Extraction of distinct institution attributes to create the `DimCollege` dimension table.
2. Parsing and splitting each course record by newline `\\n` and pipe `|`.
3. Standardizing whitespace and trimming leading/trailing characters.
4. Harmonizing casing across Degree and Medium fields.
"""))

cells.append(nbf.v4.new_code_cell("""# Create Dimension Table: DimCollege
dim_college = df_raw[['College Code', 'College Name', 'Address / Contact / Website']].drop_duplicates(subset=['College Code']).copy()
print(f"DimCollege Table: {dim_college.shape[0]} unique colleges")
dim_college.head()
"""))

# 5. Data Transformation
cells.append(nbf.v4.new_markdown_cell("""## 5. Data Transformation

We unpivot and normalize the semi-structured course field into atomic course records.
Each record maps to 5 attributes:
- `College Code`
- `College Name`
- `Degree`
- `SubCourse`
- `Medium`

Standardization mappings applied:
- Degree: `"B.SC"` $\\rightarrow$ `"B.Sc"`, `"B.COM"` $\\rightarrow$ `"B.Com"`, `"B.A."` $\\rightarrow$ `"B.A"`, `"BBA"` $\\rightarrow$ `"BBA"`.
- Medium: Trimmed and converted to Title Case (`"English"`, `"Telugu"`, `"Urdu"`, `"Hindi"`).
"""))

cells.append(nbf.v4.new_code_cell("""course_rows = []

for _, row in df_raw.iterrows():
    c_code = row["College Code"]
    c_name = row["College Name"]
    courses = str(row["Courses | SubCourse | Medium"])

    for course in courses.split("\\n"):
        parts = [x.strip() for x in course.split("|")]
        if len(parts) == 3:
            deg = parts[0].strip().upper()
            deg_map = {
                "B.SC": "B.Sc",
                "B.COM": "B.Com",
                "B.A.": "B.A",
                "BBA": "BBA"
            }
            deg = deg_map.get(deg, deg)
            sub = parts[1].strip()
            med = parts[2].strip().title()

            course_rows.append({
                "College Code": c_code,
                "College Name": c_name,
                "Degree": deg,
                "SubCourse": sub,
                "Medium": med
            })

fact_courses = pd.DataFrame(course_rows)
print(f"Normalized FactCourses Dimensions: {fact_courses.shape[0]} rows, {fact_courses.shape[1]} columns")
print(f"Colleges represented in FactCourses: {fact_courses['College Code'].nunique()} (355 of 356)")
fact_courses.head()
"""))

# 6. Exploratory Data Analysis
cells.append(nbf.v4.new_markdown_cell("""## 6. Exploratory Data Analysis (EDA)

We now conduct detailed exploratory analyses on the normalized course fact table.
"""))

# 6.1 Degree Distribution
cells.append(nbf.v4.new_markdown_cell("""### 6.1 Degree Distribution

Evaluating the volume and market share of courses across undergraduate degree programs.
"""))

cells.append(nbf.v4.new_code_cell("""deg_counts = fact_courses['Degree'].value_counts()
deg_pct = (deg_counts / len(fact_courses) * 100).round(2)

deg_summary = pd.DataFrame({
    'Course Count': deg_counts,
    'Share (%)': deg_pct
})
print("Degree Distribution Summary:")
print(deg_summary)

# Plot Degree Distribution
plt.figure(figsize=(8, 4.5))
bars = plt.barh(deg_counts.index[::-1], deg_counts.values[::-1], color=['#ef4444', '#10b981', '#f59e0b', '#3b82f6'], height=0.6)
plt.title('UG Course Offerings by Degree (Total: 2,031)', fontsize=13, fontweight='bold', pad=12)
plt.xlabel('Number of Course Offerings', fontsize=11)
plt.ylabel('Degree', fontsize=11)
for bar in bars:
    w = bar.get_width()
    pct = w / len(fact_courses) * 100
    plt.text(w + 12, bar.get_y() + bar.get_height()/2, f'{int(w):,} ({pct:.1f}%)', va='center', fontweight='semibold')
plt.xlim(0, 1150)
plt.tight_layout()
plt.show()
"""))

# 6.2 Medium Distribution
cells.append(nbf.v4.new_markdown_cell("""### 6.2 Medium Distribution

Quantifying language-medium breakdown across all offerings.
"""))

cells.append(nbf.v4.new_code_cell("""med_counts = fact_courses['Medium'].value_counts()
med_pct = (med_counts / len(fact_courses) * 100).round(2)

med_summary = pd.DataFrame({
    'Course Count': med_counts,
    'Share (%)': med_pct
})
print("Medium Distribution Summary:")
print(med_summary)

# Donut Chart for Medium
plt.figure(figsize=(7, 5))
plt.pie(
    med_counts.values,
    labels=[f'{k}: {v:,}' for k, v in zip(med_counts.index, med_counts.values)],
    autopct='%1.1f%%',
    pctdistance=0.75,
    colors=['#2563eb', '#0d9488', '#f59e0b', '#ef4444'],
    startangle=40,
    wedgeprops=dict(width=0.42, edgecolor='white', linewidth=2)
)
plt.title('Course Offerings by Medium of Instruction', fontsize=13, fontweight='bold', pad=15)
plt.tight_layout()
plt.show()
"""))

# 6.3 Degree vs Medium
cells.append(nbf.v4.new_markdown_cell("""### 6.3 Degree vs Medium Analysis

Cross-tabulating degree programs against instructional mediums reveals a profound divergence in language accessibility between professional/science courses and liberal arts.
"""))

cells.append(nbf.v4.new_code_cell("""ct = pd.crosstab(fact_courses['Degree'], fact_courses['Medium'])
ct_pct = ct.div(ct.sum(axis=1), axis=0).mul(100).round(2)

print("Crosstab: Degree × Medium (Absolute Counts):")
print(ct)
print("\\nCrosstab: Degree × Medium (Row Percentages %):")
print(ct_pct)

# 100% Stacked Bar Chart
ax = ct_pct[['English', 'Telugu', 'Urdu', 'Hindi']].plot(
    kind='barh', stacked=True, figsize=(10, 5),
    color=['#1e3a8a', '#0d9488', '#f59e0b', '#ef4444'], width=0.6
)
plt.title('Medium Distribution within Each Degree (100% Stacked)', fontsize=13, fontweight='bold', pad=12)
plt.xlabel('Percentage of Offerings within Degree (%)', fontsize=11)
plt.ylabel('Degree', fontsize=11)
plt.legend(title='Medium', bbox_to_anchor=(1.02, 1), loc='upper left')
plt.xlim(0, 100)
plt.tight_layout()
plt.show()
"""))

# 6.4 College Course Distribution
cells.append(nbf.v4.new_markdown_cell("""### 6.4 College Course Distribution

Assessing how course breadth varies across individual affiliated institutions.
"""))

cells.append(nbf.v4.new_code_cell("""courses_per_college = fact_courses.groupby(['College Code', 'College Name']).size()
print("Descriptive Statistics for Course Count per College:")
print(courses_per_college.describe())

# Histogram of course counts
plt.figure(figsize=(9, 4.5))
sns.histplot(courses_per_college, bins=25, kde=True, color='#0284c7', edgecolor='white')
plt.title('Distribution of Course Offerings per College (Median: 5, Max: 27)', fontsize=13, fontweight='bold', pad=12)
plt.xlabel('Course Offerings per College', fontsize=11)
plt.ylabel('Number of Colleges', fontsize=11)
plt.axvline(courses_per_college.median(), color='red', linestyle='--', linewidth=2, label=f'Median: {int(courses_per_college.median())} courses')
plt.axvline(courses_per_college.mean(), color='orange', linestyle=':', linewidth=2, label=f'Mean: {courses_per_college.mean():.1f} courses')
plt.legend(fontsize=10)
plt.tight_layout()
plt.show()
"""))

# 6.5 Top Colleges
cells.append(nbf.v4.new_markdown_cell("""### 6.5 Top Colleges by Course Offerings

Institutions offering the highest academic diversity and course breadth.
"""))

cells.append(nbf.v4.new_code_cell("""top10_colleges = (
    fact_courses.groupby(['College Code', 'College Name'])
    .size()
    .reset_index(name='Course Count')
    .sort_values('Course Count', ascending=False)
    .head(10)
)
print("Top 10 Colleges by Course Offerings:")
print(top10_colleges.to_string(index=False))

# Plot Top 10 Colleges
plt.figure(figsize=(10, 5))
bars = plt.barh(top10_colleges['College Name'][::-1], top10_colleges['Course Count'][::-1], color='#3b82f6', height=0.6)
plt.title('Top 10 Colleges by UG Course Offerings', fontsize=13, fontweight='bold', pad=12)
plt.xlabel('Number of Course Offerings', fontsize=11)
for bar in bars:
    w = bar.get_width()
    plt.text(w + 0.3, bar.get_y() + bar.get_height()/2, f'{int(w)}', va='center', fontweight='bold')
plt.xlim(0, 30)
plt.tight_layout()
plt.show()
"""))

# 6.6 Top SubCourses
cells.append(nbf.v4.new_markdown_cell("""### 6.6 Top SubCourse Combinations

Evaluating the most prominent subject tracks and vocational combinations across the university.
"""))

cells.append(nbf.v4.new_code_cell("""top15_subcourses = fact_courses['SubCourse'].value_counts().head(15)
print("Top 15 SubCourses:")
print(top15_subcourses)

plt.figure(figsize=(11, 6.5))
bars = plt.barh(top15_subcourses.index[::-1], top15_subcourses.values[::-1], color='#8b5cf6', height=0.6)
plt.title('Top 15 SubCourse Combinations Across All Colleges', fontsize=13, fontweight='bold', pad=12)
plt.xlabel('Number of Offerings', fontsize=11)
for bar in bars:
    w = bar.get_width()
    plt.text(w + 4, bar.get_y() + bar.get_height()/2, f'{int(w)}', va='center', fontweight='semibold', fontsize=9.5)
plt.xlim(0, 410)
plt.tight_layout()
plt.show()
"""))

# 6.7 College Coverage by Degree
cells.append(nbf.v4.new_markdown_cell("""### 6.7 College Coverage by Degree

Examining institutional coverage reveals which degrees form the universal foundation of affiliated colleges.
"""))

cells.append(nbf.v4.new_code_cell("""coverage = fact_courses.groupby('Degree')['College Code'].nunique().sort_values(ascending=False)
total_source_colleges = 356
cov_pct = (coverage / total_source_colleges * 100).round(2)

cov_df = pd.DataFrame({
    'Offering Colleges': coverage,
    'College Coverage (%)': cov_pct
})
print("College Coverage by Degree (Base: 356 Colleges):")
print(cov_df)

plt.figure(figsize=(8, 4.5))
bars = plt.bar(coverage.index, coverage.values, color=['#0284c7', '#10b981', '#f59e0b', '#8b5cf6'], width=0.52)
plt.title('College Coverage by Degree (Base: 356 Colleges)', fontsize=13, fontweight='bold', pad=12)
plt.ylabel('Number of Offering Colleges', fontsize=11)
plt.xlabel('Degree', fontsize=11)
for bar in bars:
    h = bar.get_height()
    pct = h / total_source_colleges * 100
    plt.text(bar.get_x() + bar.get_width()/2, h + 6, f'{int(h)}\\n({pct:.1f}%)', ha='center', va='bottom', fontweight='bold')
plt.ylim(0, 395)
plt.tight_layout()
plt.show()
"""))

# 7. Key Insights
cells.append(nbf.v4.new_markdown_cell("""## 7. Key Insights

Based on the quantitative analysis of 2,031 normalized undergraduate course records across 356 colleges, we identify six primary findings:

1. **Insight 1 — B.Sc Dominates Offerings Volume:**  
   B.Sc accounts for **48.25% (980 offerings)** of all parsed courses, representing nearly half the undergraduate academic volume.
   
2. **Insight 2 — B.Com Possesses Universal College Coverage:**  
   While B.Sc leads in total combinations, **B.Com is offered by 95.2% of colleges (339 of 356)**, making commerce the true universal undergraduate foundation across the university network.

3. **Insight 3 — English is the Dominant Medium:**  
   English represents **77.6% (1,576 offerings)** of all course programs, establishing it as the standard language of instruction across science and commerce disciplines.

4. **Insight 4 — B.A Exhibits an Anomalous Regional Language Inversion:**  
   Unlike B.Com (83.9% English) and B.Sc (83.6% English), **B.A is predominantly Telugu-medium (59.9%, 160 offerings)** versus English (35.2%, 94 offerings). Telugu offerings in B.A outnumber English by a ratio of **1.7 : 1**, reflecting a critical regional demographic link in liberal arts education.

5. **Insight 5 — Institutional Course Breadth is Heavily Skewed:**  
   The median affiliated college offers only **5 courses**, whereas the top institution (*St. Ann's Degree College for Women*) offers **27 courses**. Over 75% of institutions offer 7 or fewer courses, demonstrating concentrated portfolio breadth among a select tier of colleges.

6. **Insight 6 — Computing and General Tracks Form the Academic Backbone:**  
   `General` (369 offerings) and `Computers` (301 offerings) dominate as the single most frequent curricula tracks, complemented heavily by multidisciplinary computational combinations (Math/Stats/CS: 173, Math/Physics/CS: 165).
"""))

# 8. Recommendations
cells.append(nbf.v4.new_markdown_cell("""## 8. Recommendations

Derived directly from the empirical findings, the following four strategic recommendations are proposed:

1. **Recommendation 1 — Modernize B.Sc and B.Com Curricula & Capacity:**  
   Because B.Sc and B.Com jointly comprise **85.3% of all course offerings**, academic governance should focus quality audits, faculty enrichment, and laboratory upgrades on these two core degree programs.

2. **Recommendation 2 — Protect and Support Regional Medium Access in Humanities:**  
   The strong demand for Telugu-medium B.A courses indicates that vernacular education remains essential for first-generation and rural learners. University planners should safeguard Telugu study materials and faculty positions in rural colleges while introducing bilingual transitional modules.

3. **Recommendation 3 — Expand Course Breadth in Specialized Colleges:**  
   With the median college offering just 5 course programs, universities should incentivize colleges to offer cross-disciplinary minors, vocational diplomas, and data-science certifications to broaden rural students' employability.

4. **Recommendation 4 — Institutionalize Applied Computing & Industry Pathways:**  
   With computer-oriented subcourses representing hundreds of offerings across colleges, the university should partner with technology industry bodies to certify computer curricula (cloud, data analysis, web technologies) ensuring strong corporate placement.
"""))

# 9. Conclusion
cells.append(nbf.v4.new_markdown_cell("""## 9. Conclusion

The analysis demonstrates a vibrant but highly concentrated undergraduate course landscape across Osmania University's affiliated network. 

- **Structure:** B.Sc and B.Com drive the vast majority of institutional capacity, while English serves as the operational baseline medium.
- **Equity & Access:** The distinct Telugu-medium concentration in B.A underscores the vital social role played by the university in preserving regional access to higher education.
- **Opportunity:** Substantial variation in course breadth highlights the potential for university leadership to elevate smaller colleges through standardized multidisciplinary offerings aligned with modern industry demands.
"""))

nb.cells = cells

# Save notebook
notebook_paths = [
    os.path.join("python", "NexMinds_Analysis.ipynb"),
    os.path.join("TheNexMinds_Data_Analytics_Assessment", "python", "NexMinds_Analysis.ipynb")
]

for p in notebook_paths:
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, "w", encoding="utf-8") as f:
        nbf.write(nb, f)
    print(f"Jupyter notebook saved to: {p}")
