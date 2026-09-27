import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

# Specify the Excel file path

file_path = "C:\\Users\\MOHAMMED FARSHAN\\OneDrive\\Desktop\\TheNexMinds_Assessment\\data\\TheNexMinds_Data_Analytics_Assessment_Dataset.xlsx"

# Read the Excel file
df = pd.read_excel(
    file_path,
    sheet_name="OU UG Colleges 2026"
)
# Display the first five rows
print(df.head())

# Display the number of rows and columns
print(df.shape)

# Display column names
print(df.columns)

#data quality analysis
print(df.isnull().sum())

df[df.isnull().any(axis=1)]

#duplicate records
print("Duplicate rows:", df.duplicated().sum())

#unique collegs
print("Unique colleges:", df["College Code"].nunique())

#STEP 4 — Transform the course column

course_rows = []

for _, row in df.iterrows():

    college_code = row["College Code"]
    college_name = row["College Name"]

    courses = str(row["Courses | SubCourse | Medium"])

    for course in courses.split("\n"):

        parts = [x.strip() for x in course.split("|")]

        if len(parts) == 3:

            degree = parts[0]
            subcourse = parts[1]
            medium = parts[2]

            course_rows.append({
                "College Code": college_code,
                "College Name": college_name,
                "Degree": degree,
                "SubCourse": subcourse,
                "Medium": medium
            })

courses_df = pd.DataFrame(course_rows)

print(courses_df.head())
print(courses_df.shape)

#STEP 5 — Standardize Degree names

courses_df["Degree"] = (
    courses_df["Degree"]
    .str.strip()
    .str.upper()
)

degree_mapping = {
    "B.SC": "B.Sc",
    "B.COM": "B.Com",
    "B.A.": "B.A"
}

courses_df["Degree"] = courses_df["Degree"].replace(degree_mapping)

#STEP 6 — Clean Medium

courses_df["Medium"] = (
    courses_df["Medium"]
    .str.strip()
    .str.title()
)
print(courses_df["Medium"].value_counts())

# STEP 7 - Save cleaned dataset

import os

os.makedirs("output", exist_ok=True)

courses_df.to_csv(
    "output/cleaned_course_data.csv",
    index=False
)

courses_df.to_excel(
    "output/cleaned_course_data.xlsx",
    index=False
)

print("Cleaned datasets saved successfully!")

#STEP 8 — Basic EDA-Degree distribution

degree_counts = courses_df["Degree"].value_counts()

print(degree_counts)

#Calculate percentages

degree_percentage = (
    courses_df["Degree"]
    .value_counts(normalize=True)
    .mul(100)
    .round(2)
)

print(degree_percentage)

#STEP 9 — Medium analysis

medium_counts = courses_df["Medium"].value_counts()
print(medium_counts)

medium_percentage = (
    courses_df["Medium"]
    .value_counts(normalize=True)
    .mul(100)
    .round(2)
)

print(medium_percentage)

#STEP 10 — Most important analysis: Degree × Medium

degree_medium = pd.crosstab(
    courses_df["Degree"],
    courses_df["Medium"]
)

print(degree_medium)

#STEP 11 — College-level analysis

college_course_count = (
    courses_df
    .groupby(["College Code", "College Name"])
    .size()
    .reset_index(name="Course Count")
)

print(college_course_count.head())

print(college_course_count["Course Count"].describe())

#STEP 12 — Top colleges by course offerings

top_colleges = (
    college_course_count
    .sort_values("Course Count", ascending=False)
    .head(10)
)

print(top_colleges)

#STEP 13 — Top subject combinations

top_subcourses = (
    courses_df["SubCourse"]
    .value_counts()
    .head(15)
)

print(top_subcourses)

#STEP 14 — Degree availability across colleges

degree_college_count = (
    courses_df
    .groupby("Degree")["College Code"]
    .nunique()
    .sort_values(ascending=False)
)

print(degree_college_count)

degree_coverage = (
    courses_df.groupby("Degree")["College Code"]
    .nunique()
    .div(df["College Code"].nunique())
    .mul(100)
    .round(2)
)

print("degree percentage:",degree_coverage)
























