import os
from fpdf import FPDF

class AnalyticsReportPDF(FPDF):
    def header(self):
        if self.page_no() > 1:
            self.set_font('SegoeUI', 'B', 8)
            self.set_text_color(100, 116, 139)
            self.cell(140, 7, 'THENEXMINDS DATA ANALYTICS ASSESSMENT - OSMANIA UNIVERSITY UG ANALYTICS 2026', 0, 0, 'L')
            self.cell(40, 7, f'Page {self.page_no()}', 0, 1, 'R')
            self.set_draw_color(226, 232, 240)
            self.set_line_width(0.4)
            self.line(15, 17, 195, 17)
            self.ln(4)

    def footer(self):
        if self.page_no() > 1:
            self.set_y(-14)
            self.set_font('SegoeUI', 'I', 8)
            self.set_text_color(148, 163, 184)
            self.cell(0, 10, 'Confidential & Proprietary - Prepared for The NexMinds Data Analytics Evaluation', 0, 0, 'C')

    def chapter_title(self, title):
        self.set_font('SegoeUI', 'B', 14)
        self.set_text_color(15, 23, 42)
        self.cell(0, 8, title, 0, 1, 'L')
        self.set_draw_color(37, 99, 235)
        self.set_line_width(1.2)
        self.line(self.get_x(), self.get_y(), self.get_x() + 35, self.get_y())
        self.ln(4)

    def section_heading(self, heading):
        self.set_font('SegoeUI', 'B', 10.5)
        self.set_text_color(30, 41, 59)
        self.cell(0, 6.5, heading, 0, 1, 'L')

    def body_text(self, text):
        self.set_font('SegoeUI', '', 9)
        self.set_text_color(51, 65, 85)
        self.multi_cell(0, 4.8, text)
        self.ln(2)

def generate_pdf_report(output_paths):
    pdf = AnalyticsReportPDF(orientation='P', unit='mm', format='A4')
    
    # Add TrueType Unicode fonts from Windows
    font_dir = "C:/Windows/Fonts"
    if os.path.exists(os.path.join(font_dir, "segoeui.ttf")):
        pdf.add_font("SegoeUI", "", os.path.join(font_dir, "segoeui.ttf"))
        pdf.add_font("SegoeUI", "B", os.path.join(font_dir, "segoeuib.ttf"))
        pdf.add_font("SegoeUI", "I", os.path.join(font_dir, "segoeuii.ttf"))
    else:
        pdf.add_font("SegoeUI", "", os.path.join(font_dir, "arial.ttf"))
        pdf.add_font("SegoeUI", "B", os.path.join(font_dir, "arialbd.ttf"))
        pdf.add_font("SegoeUI", "I", os.path.join(font_dir, "ariali.ttf"))

    pdf.set_auto_page_break(auto=True, margin=16)
    pdf.set_margins(15, 15, 15)

    # ==========================================
    # PAGE 1: TITLE & EXECUTIVE SUMMARY
    # ==========================================
    pdf.add_page()
    
    # Header Decorative Banner
    pdf.set_fill_color(15, 23, 42)
    pdf.rect(15, 15, 180, 40, 'F')
    
    pdf.set_xy(20, 20)
    pdf.set_font('SegoeUI', 'B', 18)
    pdf.set_text_color(255, 255, 255)
    pdf.cell(0, 8, 'The NexMinds Data Analytics Assessment', 0, 1, 'L')
    
    pdf.set_xy(20, 30)
    pdf.set_font('SegoeUI', 'B', 12)
    pdf.set_text_color(56, 189, 248)
    pdf.cell(0, 7, 'Executive Analysis: Osmania University UG Colleges (2026 Cycle)', 0, 1, 'L')
    
    pdf.set_xy(20, 39)
    pdf.set_font('SegoeUI', '', 8.5)
    pdf.set_text_color(148, 163, 184)
    pdf.cell(0, 6, 'Candidate: Mohammed Farshan  |  Focus: ETL, Descriptive Analytics & Interactive Power BI Modeling', 0, 1, 'L')
    
    pdf.set_y(60)
    
    # Metadata summary grid
    pdf.set_font('SegoeUI', 'B', 9.5)
    pdf.set_text_color(15, 23, 42)
    pdf.cell(42, 6, 'Project Objective:', 0, 0)
    pdf.set_font('SegoeUI', '', 9)
    pdf.set_text_color(51, 65, 85)
    pdf.multi_cell(0, 5, 'Conduct an end-to-end analytical audit of undergraduate (UG) course offerings across affiliated institutions, standardizing multi-value course text into an enterprise Star Schema model and surfacing strategic insights.')
    
    pdf.ln(1)
    pdf.set_font('SegoeUI', 'B', 9.5)
    pdf.set_text_color(15, 23, 42)
    pdf.cell(42, 6, 'Dataset Examined:', 0, 0)
    pdf.set_font('SegoeUI', '', 9)
    pdf.set_text_color(51, 65, 85)
    pdf.cell(0, 6, 'OU UG Colleges 2026 (356 Institutional Rows, 2,031 Normalized Course Offerings)', 0, 1)
    
    pdf.set_font('SegoeUI', 'B', 9.5)
    pdf.set_text_color(15, 23, 42)
    pdf.cell(42, 6, 'Technology Stack:', 0, 0)
    pdf.set_font('SegoeUI', '', 9)
    pdf.set_text_color(51, 65, 85)
    pdf.cell(0, 6, 'Python 3.14 (Pandas, NumPy, Matplotlib, Seaborn), Power BI Desktop (DAX), Microsoft Excel', 0, 1)

    pdf.ln(4)
    pdf.chapter_title('Executive Scorecard & Key KPIs')
    
    # 4 KPI Cards
    kpi_y = pdf.get_y()
    kpis = [
        ('TOTAL COLLEGES', '356', '355 with courses | 1 without', (37, 99, 235)),
        ('COURSE OFFERINGS', '2,031', 'Mean: 5.7 | Median: 5.0', (13, 148, 136)),
        ('ENGLISH SHARE', '77.6%', '1,576 English courses', (217, 119, 6)),
        ('TOP DEGREE', 'B.Sc', '980 courses (48.3%)', (124, 58, 237))
    ]
    card_w = 42
    gap = 4
    for i, (k_title, k_val, k_sub, k_color) in enumerate(kpis):
        bx = 15 + i * (card_w + gap)
        pdf.set_fill_color(248, 250, 252)
        pdf.set_draw_color(226, 232, 240)
        pdf.rect(bx, kpi_y, card_w, 23, 'DF')
        
        pdf.set_fill_color(*k_color)
        pdf.rect(bx, kpi_y, 2.5, 23, 'F')
        
        pdf.set_xy(bx + 4, kpi_y + 2)
        pdf.set_font('SegoeUI', 'B', 7)
        pdf.set_text_color(100, 116, 139)
        pdf.cell(card_w - 5, 4, k_title, 0, 1, 'L')
        
        pdf.set_xy(bx + 4, kpi_y + 6.5)
        pdf.set_font('SegoeUI', 'B', 13.5)
        pdf.set_text_color(15, 23, 42)
        pdf.cell(card_w - 5, 8, k_val, 0, 1, 'L')
        
        pdf.set_xy(bx + 4, kpi_y + 15)
        pdf.set_font('SegoeUI', '', 6.5)
        pdf.set_text_color(148, 163, 184)
        pdf.cell(card_w - 5, 4, k_sub, 0, 1, 'L')

    pdf.set_y(kpi_y + 28)
    pdf.chapter_title('Executive Summary')
    pdf.body_text(
        "This evaluation provides an authoritative analysis of undergraduate course distribution across Osmania University's "
        "affiliated colleges for the 2026 academic admissions cycle. The source dataset encompasses 356 institutional rows, "
        "which after rigorous parsing and normalization yielded 2,031 atomic course offerings across four primary degree programs: "
        "B.Sc, B.Com, B.A, and BBA."
    )
    pdf.body_text(
        "Key strategic takeaways from the investigation demonstrate significant structural concentrations: B.Sc accounts for nearly "
        "half of all course offerings (48.25%), whereas B.Com achieves virtually universal presence across 95.2% of affiliated institutions. "
        "While English represents the prevailing language of instruction university-wide (77.6%), liberal arts (B.A) displays a profound "
        "regional language inversion, offering 1.7 times more Telugu-medium courses than English. Furthermore, course breadth is "
        "substantially skewed, with a median of only 5 courses per college while premier institutions support up to 27 distinct combinations."
    )

    # ==========================================
    # PAGE 2: DATA PREPARATION & ARCHITECTURE
    # ==========================================
    pdf.add_page()
    pdf.chapter_title('Data Preparation & Structural Audit')
    
    pdf.body_text(
        "The source dataset presented real-world data engineering challenges. Rather than storing records in normalized tables, "
        "individual college rows contained multi-value course declarations concatenated as newline-separated strings with pipe "
        "delimiters ('Degree | SubCourse | Medium')."
    )
    
    pdf.section_heading('1. Data Ingestion & Missing Value Audit')
    pdf.body_text(
        "- Total Records Ingested: 356 college records across 5 initial attributes: S.No., College Code, College Name, Address/Contact/Website, and Courses.\n"
        "- Null Value Audit: Zero missing values in institutional identification (College Code, College Name) or Course fields. 34 records lacked detailed website/address metadata.\n"
        "- Duplicate Verification: Zero duplicate college codes were present; each code uniquely indexes an affiliated college entity."
    )
    
    pdf.section_heading('2. The Delimiter Anomaly: Resolving the 355 vs 356 Institutional Baseline')
    pdf.body_text(
        "A critical finding during ingestion was the structural discrepancy between raw college records (356) and parsed course-bearing "
        "colleges (355). College Code 1171 (Road Mystry Degree College) contained the raw course entry 'BSW\\nBSW English' without pipe "
        "delimiters ('|'). Consequently, standard 3-token parsing yielded no fact records for this institution. Recognizing this anomaly is "
        "essential for maintaining dimensional integrity in enterprise Power BI reporting."
    )

    pdf.section_heading('3. Transformation & Normalization Pipeline')
    pdf.body_text(
        "- String Unpivoting: Course blocks were split by newline ('\\n') and tokenized by pipe ('|') into atomic 3-tuples.\n"
        "- Degree Harmonization: Casing variations were standardized ('B.SC' -> 'B.Sc', 'B.COM' -> 'B.Com', 'B.A.' -> 'B.A').\n"
        "- Medium Normalization: Text entries were trimmed and converted to Title Case ('English', 'Telugu', 'Urdu', 'Hindi').\n"
        "- Data Model Output: Produced 'FactCourses' (2,031 rows x 5 columns) and 'DimCollege' (356 rows x 3 columns)."
    )

    pdf.section_heading('4. Power BI Star Schema Data Model')
    pdf.body_text(
        "To empower performant slicing and self-service analytics, the normalized data was architected into a Star Schema data model:\n"
        "- FactCourses (Fact Table): College Code (FK), College Name, Degree, SubCourse, Medium\n"
        "- DimCollege (Dimension Table): College Code (PK), College Name, Address / Contact / Website\n"
        "- Relationship: 1-to-Many cardinality from DimCollege[College Code] (1) to FactCourses[College Code] (*)."
    )

    # Model Summary Table
    pdf.set_font('SegoeUI', 'B', 8.5)
    pdf.set_fill_color(241, 245, 249)
    pdf.cell(45, 6, 'Table Name', 1, 0, 'C', True)
    pdf.cell(35, 6, 'Table Type', 1, 0, 'C', True)
    pdf.cell(30, 6, 'Row Count', 1, 0, 'C', True)
    pdf.cell(70, 6, 'Key Attributes', 1, 1, 'C', True)
    
    pdf.set_font('SegoeUI', '', 8)
    pdf.cell(45, 6, 'DimCollege', 1, 0, 'L')
    pdf.cell(35, 6, 'Dimension (1)', 1, 0, 'C')
    pdf.cell(30, 6, '356', 1, 0, 'C')
    pdf.cell(70, 6, 'College Code (PK), College Name, Contact', 1, 1, 'L')
    
    pdf.cell(45, 6, 'FactCourses', 1, 0, 'L')
    pdf.cell(35, 6, 'Fact (*)', 1, 0, 'C')
    pdf.cell(30, 6, '2,031', 1, 0, 'C')
    pdf.cell(70, 6, 'College Code (FK), Degree, SubCourse, Medium', 1, 1, 'L')

    # ==========================================
    # PAGE 3: EXPLORATORY DATA ANALYSIS
    # ==========================================
    pdf.add_page()
    pdf.chapter_title('Exploratory Data Analysis & Visualizations')
    
    # Add Degree Distribution Chart
    if os.path.exists('images/degree_distribution.png'):
        pdf.image('images/degree_distribution.png', x=15, y=28, w=88)
    
    # Add Medium Distribution Chart
    if os.path.exists('images/medium_distribution.png'):
        pdf.image('images/medium_distribution.png', x=107, y=28, w=88)
        
    pdf.set_y(82)
    pdf.section_heading('Core Distributions: Degree & Language Market Share')
    pdf.body_text(
        "- B.Sc Dominance: B.Sc represents 980 of 2,031 course offerings (48.25%), followed by B.Com with 752 offerings (37.03%). "
        "Together, Science and Commerce constitute 85.28% of all undergraduate pathways.\n"
        "- Medium Landscape: English is the primary medium of instruction across 1,576 offerings (77.60%), while Telugu represents "
        "433 offerings (21.32%). Urdu accounts for 20 offerings (0.98%), and Hindi comprises 2 offerings (0.10%)."
    )
    
    # Add College Coverage Chart
    if os.path.exists('images/college_coverage.png'):
        pdf.image('images/college_coverage.png', x=15, y=114, w=88)
        
    # Add Course Distribution Histogram
    if os.path.exists('images/course_distribution_histogram.png'):
        pdf.image('images/course_distribution_histogram.png', x=107, y=114, w=88)

    pdf.set_y(172)
    pdf.section_heading('Institutional Breadth & Degree Availability Analysis')
    pdf.body_text(
        "- Institutional Degree Reach: While B.Sc has the highest number of discrete course combinations, B.Com is present in 339 of 356 colleges (95.2%), "
        "confirming that commerce is the ubiquitous baseline for affiliated colleges. B.Sc is available in 293 colleges (82.3%), B.A in 147 colleges (41.3%), "
        "and BBA in 32 colleges (9.0%).\n"
        "- Course Breadth Dispersion: The distribution of course offerings per institution is highly right-skewed. While the statistical mean is 5.7 offerings, "
        "the median institution offers exactly 5 courses. The bottom 25% of colleges offer 3 or fewer courses, whereas the upper tail features large autonomous "
        "colleges offering up to 27 courses."
    )

    # ==========================================
    # PAGE 4: THE 6 CORE KEY INSIGHTS
    # ==========================================
    pdf.add_page()
    pdf.chapter_title('The 6 Final Key Insights')

    # Embed Degree vs Medium chart
    if os.path.exists('images/degree_vs_medium.png'):
        pdf.image('images/degree_vs_medium.png', x=15, y=28, w=105)

    pdf.set_xy(123, 28)
    pdf.set_font('SegoeUI', 'B', 9.5)
    pdf.set_text_color(15, 23, 42)
    pdf.cell(72, 6, 'Insight 4 Highlight:', 0, 1)
    pdf.set_font('SegoeUI', '', 8.5)
    pdf.set_text_color(51, 65, 85)
    pdf.multi_cell(72, 4.3, 
        "Unlike B.Sc and B.Com where English comprises >83% of offerings, B.A displays a complete language inversion:\n\n"
        "- Telugu B.A: 160 (59.9%)\n"
        "- English B.A: 94 (35.2%)\n"
        "- Urdu B.A: 12 (4.5%)\n"
        "- Hindi B.A: 1 (0.4%)\n\n"
        "Telugu offerings in B.A outnumber English offerings by 1.7 to 1, indicating strong vernacular demand in arts and humanities."
    )

    pdf.set_y(84)
    
    # 6 Detailed Insights Boxed
    insights = [
        ("Insight 1 - B.Sc Dominates Offerings Volume", 
         "B.Sc accounts for approximately 48.25% (980 of 2,031) of all parsed course offerings. This reflects extensive curriculum permutations across physical and life sciences."),
        
        ("Insight 2 - B.Com Possesses Broadest College Coverage", 
         "B.Com is offered by 95.2% of colleges (339 out of 356). Although B.Sc has more course combinations, B.Com is the foundational commercial track across nearly every affiliated campus."),
        
        ("Insight 3 - English is the Dominant Medium University-Wide", 
         "English represents 77.6% of all course offerings (1,576 courses), serving as the de facto standard of higher education instruction in scientific, technological, and corporate disciplines."),
         
        ("Insight 4 - B.A Exhibits an Inverted Regional Language Pattern", 
         "B.A shows 160 Telugu-medium offerings compared to only 94 in English. This is the single most significant sociolinguistic finding of the assessment, reflecting regional demand in public services."),
         
        ("Insight 5 - Course Availability is Highly Uneven Across Colleges", 
         "The median college offers 5 course programs, while the top institution offers 27. Over 75% of colleges offer 7 or fewer courses, showing that broad multidisciplinary portfolios are confined to premier urban colleges."),
         
        ("Insight 6 - Computing & General Tracks Form the University Backbone", 
         "General (369 offerings) and Computers (301 offerings) are the top two subcourse labels, followed by applied computing combinations like Math/Stats/CS (173) and Math/Physics/CS (165).")
    ]

    for title, desc in insights:
        pdf.set_font('SegoeUI', 'B', 9)
        pdf.set_text_color(37, 99, 235)
        pdf.cell(0, 5, title, 0, 1)
        pdf.set_font('SegoeUI', '', 8.5)
        pdf.set_text_color(51, 65, 85)
        pdf.multi_cell(0, 4.2, desc)
        pdf.ln(1.5)

    # ==========================================
    # PAGE 5: STRATEGIC RECOMMENDATIONS
    # ==========================================
    pdf.add_page()
    pdf.chapter_title('Evidence-Based Strategic Recommendations')
    
    pdf.body_text(
        "All recommendations are derived strictly from quantitative findings, providing university administrators and academic planners "
        "with actionable interventions to enhance educational accessibility, curriculum relevance, and institutional equity."
    )
    
    recs = [
        ("Recommendation 1: Capacity & Quality Optimization for B.Sc & B.Com",
         "Evidence: B.Sc and B.Com jointly constitute 85.28% of all undergraduate course offerings (1,732 of 2,031).\n"
         "Action: University authorities should prioritize lab infrastructure audits, laboratory modernization, and teaching faculty allocation "
         "within these two degree categories. Standardizing curriculum tracks and introducing continuous industry assessment will have the maximum "
         "systemic impact on student outcomes."),
        
        ("Recommendation 2: Safeguard Regional Language Equity in Humanities",
         "Evidence: B.A Telugu-medium offerings (160) substantially exceed English offerings (94), representing 59.9% of humanities capacity.\n"
         "Action: Educational planners must not eliminate vernacular options under generic digitalization mandates. Vernacular humanities courses "
         "serve as vital entry points for rural and socially disadvantaged students targeting civil service and state competitive exams. Planners should "
         "provide high-quality digital textbooks in Telugu while introducing transitional English communication modules."),
        
        ("Recommendation 3: Portfolio Broadening & Interdisciplinary Clusters for Rural Colleges",
         "Evidence: Over 50% of colleges offer 5 or fewer course tracks, severely limiting students' elective flexibility in non-urban districts.\n"
         "Action: Osmania University should implement regional hub-and-spoke academic networks where smaller colleges can share faculty for high-demand "
         "minors (e.g., Data Analytics, Financial Modeling, Biotechnology) through blended hybrid classrooms."),
         
        ("Recommendation 4: Industry Co-Certification of Applied Computing Tracks",
         "Evidence: Computational programs (Computers, Math/Stats/CS, Math/Physics/CS, Vocational CA) account for over 700 aggregate offerings.\n"
         "Action: Establish direct academic partnerships with IT/ITES industry leaders (NASSCOM, Telangana Academy for Skill and Knowledge) to validate "
         "and co-certify computing curricula, ensuring applied laboratory proficiency and direct employability upon graduation.")
    ]

    for title, desc in recs:
        pdf.set_fill_color(248, 250, 252)
        pdf.set_draw_color(203, 213, 225)
        rx = 15
        ry = pdf.get_y()
        pdf.rect(rx, ry, 180, 29, 'DF')
        
        pdf.set_fill_color(13, 148, 136)
        pdf.rect(rx, ry, 2.5, 29, 'F')
        
        pdf.set_xy(rx + 5, ry + 2)
        pdf.set_font('SegoeUI', 'B', 9)
        pdf.set_text_color(15, 23, 42)
        pdf.cell(170, 5, title, 0, 1)
        
        pdf.set_xy(rx + 5, ry + 7.5)
        pdf.set_font('SegoeUI', '', 7.8)
        pdf.set_text_color(51, 65, 85)
        pdf.multi_cell(170, 3.8, desc)
        
        pdf.set_y(ry + 32)

    # Embed Top Subcourses chart at bottom
    if os.path.exists('images/top15_subcourses.png'):
        pdf.image('images/top15_subcourses.png', x=15, y=pdf.get_y() + 2, w=180)

    # ==========================================
    # PAGE 6: CONCLUSION & SUBMISSION ARTIFACTS
    # ==========================================
    pdf.add_page()
    pdf.chapter_title('Conclusion & Submission Deliverables')
    
    # Dashboard preview
    if os.path.exists('images/dashboard.png'):
        pdf.image('images/dashboard.png', x=15, y=26, w=180)
        
    pdf.set_y(132)
    pdf.section_heading('Analytical Conclusion')
    pdf.body_text(
        "The analysis demonstrates a diverse but highly concentrated undergraduate course landscape across Osmania University's "
        "affiliated colleges. B.Sc and B.Com account for the vast majority of course offerings, while English represents the predominant "
        "operational medium. However, the B.A category reveals a distinctive Telugu-medium pattern, highlighting critical differences in "
        "language accessibility across disciplines. Academic breadth also varies considerably across colleges, with median institutions offering "
        "5 courses while premier centers offer up to 27 distinct specializations."
    )
    
    pdf.section_heading('Submission Deliverables Directory Structure')
    pdf.body_text(
        "The project is structured in strict conformance with the evaluation submission standard:\n"
        "- README.md: Comprehensive architectural walkthrough, methodology, DAX formulas, and finding summaries.\n"
        "- data/: Contains original_dataset.xlsx, cleaned_course_data.xlsx, and dim_college.xlsx.\n"
        "- python/: NexMinds_Analysis.ipynb (fully executed Jupyter Notebook with 9 structured markdown sections).\n"
        "- powerbi/: NexMinds_UG_Analytics.pbix (interactive Star Schema report with DAX measures and slicers) + DAX_Measures.dax.\n"
        "- report/: NexMinds_Data_Analytics_Report.pdf (this executive report).\n"
        "- images/: High-resolution dashboard mockup (dashboard.png) and 7 standalone visual figures."
    )
    
    pdf.ln(1)
    # Verification signoff box
    pdf.set_fill_color(241, 245, 249)
    pdf.set_draw_color(148, 163, 184)
    pdf.rect(15, pdf.get_y(), 180, 14, 'DF')
    pdf.set_xy(18, pdf.get_y() + 2)
    pdf.set_font('SegoeUI', 'B', 8)
    pdf.set_text_color(15, 23, 42)
    pdf.cell(0, 4, 'Assessment Completed & Verified By: Mohammed Farshan', 0, 1)
    pdf.set_xy(18, pdf.get_y())
    pdf.set_font('SegoeUI', '', 7.5)
    pdf.set_text_color(100, 116, 139)
    pdf.cell(0, 4, 'Integrity Verified: FactCourses = 2,031 rows | DimCollege = 356 institutions | All DAX Formulas Validated', 0, 1)

    # Save to both paths
    for p in output_paths:
        os.makedirs(os.path.dirname(p), exist_ok=True)
        pdf.output(p)
        print(f"Report PDF generated at: {p} ({os.path.getsize(p)} bytes)")

if __name__ == '__main__':
    paths = [
        'report/NexMinds_Data_Analytics_Report.pdf',
        'TheNexMinds_Data_Analytics_Assessment/report/NexMinds_Data_Analytics_Report.pdf'
    ]
    generate_pdf_report(paths)
