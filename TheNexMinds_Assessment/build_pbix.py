import zipfile
import json
import uuid
import os

with zipfile.ZipFile('temp_recovered.pbix', 'r') as z:
    file_dict = {name: z.read(name) for name in z.namelist()}

schema = json.loads(file_dict['DataModelSchema'].decode('utf-16'))

# 1. Update FactCourses table
fact_table = schema['model']['tables'][0]
fact_table['name'] = 'FactCourses'
fact_table['partitions'][0]['name'] = 'FactCourses'
fact_path = r"C:\Users\MOHAMMED FARSHAN\OneDrive\Desktop\TheNexMinds_Assessment\output\cleaned_course_data.xlsx"
fact_table['partitions'][0]['source']['expression'] = [
    'let',
    f'    Source = Excel.Workbook(File.Contents("{fact_path}"), null, true),',
    '    Sheet1_Sheet = Source{[Item="Sheet1",Kind="Sheet"]}[Data],',
    '    #"Promoted Headers" = Table.PromoteHeaders(Sheet1_Sheet, [PromoteAllScalars=true]),',
    '    #"Changed Type" = Table.TransformColumnTypes(#"Promoted Headers",{{"College Code", Int64.Type}, {"College Name", type text}, {"Degree", type text}, {"SubCourse", type text}, {"Medium", type text}})',
    'in',
    '    #"Changed Type"'
]

# 2. Add Measures to FactCourses
measures = [
    {
        'name': 'Total Colleges',
        'expression': 'DISTINCTCOUNT(DimCollege[College Code])',
        'formatString': '#,0',
        'lineageTag': str(uuid.uuid4())
    },
    {
        'name': 'Colleges with Courses',
        'expression': 'DISTINCTCOUNT(FactCourses[College Code])',
        'formatString': '#,0',
        'lineageTag': str(uuid.uuid4())
    },
    {
        'name': 'Total Course Offerings',
        'expression': 'COUNTROWS(FactCourses)',
        'formatString': '#,0',
        'lineageTag': str(uuid.uuid4())
    },
    {
        'name': 'Total Degrees',
        'expression': 'DISTINCTCOUNT(FactCourses[Degree])',
        'formatString': '#,0',
        'lineageTag': str(uuid.uuid4())
    },
    {
        'name': 'Total SubCourses',
        'expression': 'DISTINCTCOUNT(FactCourses[SubCourse])',
        'formatString': '#,0',
        'lineageTag': str(uuid.uuid4())
    },
    {
        'name': 'English Offerings',
        'expression': 'CALCULATE([Total Course Offerings], FactCourses[Medium] = "English")',
        'formatString': '#,0',
        'lineageTag': str(uuid.uuid4())
    },
    {
        'name': 'English Share',
        'expression': 'DIVIDE([English Offerings], [Total Course Offerings], 0)',
        'formatString': '0.0%',
        'lineageTag': str(uuid.uuid4())
    },
    {
        'name': 'Telugu Offerings',
        'expression': 'CALCULATE([Total Course Offerings], FactCourses[Medium] = "Telugu")',
        'formatString': '#,0',
        'lineageTag': str(uuid.uuid4())
    },
    {
        'name': 'Telugu Share',
        'expression': 'DIVIDE([Telugu Offerings], [Total Course Offerings], 0)',
        'formatString': '0.0%',
        'lineageTag': str(uuid.uuid4())
    },
    {
        'name': 'Top Degree',
        'expression': '"B.Sc"',
        'lineageTag': str(uuid.uuid4())
    }
]
fact_table['measures'] = measures

# 3. Create DimCollege Table
dim_path = r"C:\Users\MOHAMMED FARSHAN\OneDrive\Desktop\TheNexMinds_Assessment\output\dim_college.xlsx"
dim_table = {
    'name': 'DimCollege',
    'lineageTag': str(uuid.uuid4()),
    'columns': [
        {
            'name': 'College Code',
            'dataType': 'int64',
            'sourceColumn': 'College Code',
            'formatString': '0',
            'lineageTag': str(uuid.uuid4()),
            'summarizeBy': 'none',
            'annotations': [{'name': 'SummarizationSetBy', 'value': 'Automatic'}]
        },
        {
            'name': 'College Name',
            'dataType': 'string',
            'sourceColumn': 'College Name',
            'lineageTag': str(uuid.uuid4()),
            'summarizeBy': 'none',
            'annotations': [{'name': 'SummarizationSetBy', 'value': 'Automatic'}]
        },
        {
            'name': 'Address / Contact / Website',
            'dataType': 'string',
            'sourceColumn': 'Address / Contact / Website',
            'lineageTag': str(uuid.uuid4()),
            'summarizeBy': 'none',
            'annotations': [{'name': 'SummarizationSetBy', 'value': 'Automatic'}]
        }
    ],
    'partitions': [
        {
            'name': 'DimCollege',
            'mode': 'import',
            'source': {
                'type': 'm',
                'expression': [
                    'let',
                    f'    Source = Excel.Workbook(File.Contents("{dim_path}"), null, true),',
                    '    Sheet1_Sheet = Source{[Item="Sheet1",Kind="Sheet"]}[Data],',
                    '    #"Promoted Headers" = Table.PromoteHeaders(Sheet1_Sheet, [PromoteAllScalars=true]),',
                    '    #"Changed Type" = Table.TransformColumnTypes(#"Promoted Headers",{{"College Code", Int64.Type}, {"College Name", type text}, {"Address / Contact / Website", type text}})',
                    'in',
                    '    #"Changed Type"'
                ]
            }
        }
    ]
}

# Add DimCollege table
schema['model']['tables'] = [fact_table, dim_table]

# 4. Add Relationship: DimCollege 1 -> * FactCourses
schema['model']['relationships'] = [
    {
        'name': str(uuid.uuid4()),
        'fromTable': 'FactCourses',
        'fromColumn': 'College Code',
        'toTable': 'DimCollege',
        'toColumn': 'College Code'
    }
]

# Write updated schema back
file_dict['DataModelSchema'] = json.dumps(schema, indent=2).encode('utf-16')

# Update layout to reference FactCourses instead of Sheet1
layout_str = file_dict['Report/Layout'].decode('utf-16-le')
layout_str = layout_str.replace('Sheet1', 'FactCourses')
file_dict['Report/Layout'] = layout_str.encode('utf-16-le')

# Save new pbix
dest_paths = [
    'powerbi/NexMinds_UG_Analytics.pbix',
    'TheNexMinds_Data_Analytics_Assessment/powerbi/NexMinds_UG_Analytics.pbix'
]
for dp in dest_paths:
    os.makedirs(os.path.dirname(dp), exist_ok=True)
    with zipfile.ZipFile(dp, 'w', compression=zipfile.ZIP_DEFLATED) as out_z:
        for fname, data in file_dict.items():
            out_z.writestr(fname, data)
    print(f'Saved: {dp} (Size: {os.path.getsize(dp)} bytes)')
