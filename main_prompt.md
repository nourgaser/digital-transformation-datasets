You are helping generate synthetic educational datasets for Digital Transformation course projects.

Context:
Students submitted a PD1 document describing their product/company/project idea, and they may also provide an email explaining what kind of data they need. Your job is to read the provided PD1 and email carefully, understand the actual business/product story, and generate a realistic synthetic dataset package that fits that project.

Important:
Do not make random assumptions if the PD1/email already specifies the product, target users, processes, KPIs, departments, or business goals. Base the dataset story on the student team's actual description.

The dataset will be used by students in Power BI to:

- clean data,
- transform data types,
- remove or fix simple inconsistencies,
- build a simple star schema,
- create basic DAX measures,
- analyze the business situation,
- create dashboards.

The dataset should NOT be too large. Keep the main fact table around 1,000–3,000 rows maximum. Dimension tables should be much smaller.

Project information:

- Course: Digital Transformation, BINF 402, Business Informatics, Spring 2026
- University: German International University
- Instructor: Dr. Nourhan Hamdi
- Teaching Assistants: Nour Gaser, Omar Alaa, Menna Khaled, Ibrahim Hisham
- Company/project name: {{COMPANY_OR_PROJECT_NAME}}
- Team number/name: {{TEAM_INFO}}
- Attached PD1 document: {{PD1_DOCUMENT_PATH_OR_CONTENT}}
- Student email/request: {{EMAIL_PATH_OR_CONTENT}}

Your task:
Generate Python code that creates the synthetic dataset files. Do not manually type hundreds or thousands of rows. Use Python with pandas, numpy, faker, seeded random generation, distributions, correlations, seasonality, and business rules to generate realistic synthetic data.

The final generated output should include:

1. Student-facing dataset files
   Create a folder:
   output/{{project_slug}}/student_dataset/

Inside it, generate CSV files forming a simple star schema, for example:

- dim_date.csv
- dim_customer.csv or dim_user.csv
- dim_product.csv / dim_service.csv / dim_department.csv depending on the project
- dim_location.csv / dim_branch.csv / dim_channel.csv if relevant
- one or two fact tables, such as:
  - fact_sales.csv
  - fact_orders.csv
  - fact_bookings.csv
  - fact_transactions.csv
  - fact_operations.csv
  - fact_complaints.csv
  - fact_attendance.csv
  - fact_inventory.csv

Choose the tables based on the PD1/project story.

The schema must be simple and suitable for beginner-to-intermediate Power BI modeling:

- dimension tables have primary keys,
- fact tables have foreign keys,
- one-to-many relationships are clear,
- avoid snowflake schemas unless absolutely needed,
- avoid overly complex many-to-many relationships.

2. Student-facing data dictionary
   Create:
   output/{{project_slug}}/data_dictionary.md

This should briefly explain:

- each CSV file,
- each column,
- the intended relationships,
- the general business story.

Keep it short and student-facing. Do not give away a full Power BI solution.

3. Private instructor notes
   Create:
   output/{{project_slug}}/private_instructor_notes/

Include these files:

A. expected_cleaning_tasks.md
List the intended cleaning issues hidden in the raw dataset, such as:

- null values in selected non-critical columns,
- inconsistent casing,
- whitespace issues,
- inconsistent category names,
- wrong data types,
- duplicate rows,
- a few impossible values,
- date columns stored as strings,
- currency/numeric fields stored as text in some rows,
- outliers that should be investigated,
- simple spelling inconsistencies.

The cleaning should be realistic but not too complex. Avoid making the dataset frustrating or broken.

B. suggested_dax_measures.md
Suggest basic DAX measures appropriate for the dataset, such as:

- Total Revenue
- Total Orders
- Average Order Value
- Number of Customers
- Repeat Customer Rate
- Profit Margin
- Occupancy Rate
- Complaint Rate
- On-Time Delivery %
- Monthly Growth %
- YTD Sales
- Average Rating
- Conversion Rate

The exact measures should match the project story.

C. dashboard_questions.md
Suggest analytical questions the students could answer, for example:

- Which products/services generate the most revenue?
- Which branches/locations perform best?
- How does performance change by month?
- Which customer segments are most valuable?
- What causes complaints or cancellations?
- Which operational bottlenecks are visible?
- Which channel performs best?

Also suggest possible dashboard visuals, but only in the private instructor notes, not in the student-facing README.

D. model_relationships.md
Describe the intended star schema relationships:

- fact table column → dimension table column
- relationship cardinality
- filter direction recommendation

4. Python generation code
   Write clean, reusable Python code.

Requirements:

- Use a fixed random seed for reproducibility.
- Use functions for generating each dimension and fact table.
- Keep project-specific constants near the top.
- Create output folders automatically.
- Save CSV files with UTF-8 encoding.
- Validate that all fact foreign keys exist in dimension tables.
- Validate approximate row counts.
- Validate that the dataset contains the intended cleaning issues.
- Print a short summary after generation.

Important data realism requirements:
The data should not be purely random. It should contain realistic patterns, such as:

- seasonality by month,
- different performance by branch/location/channel,
- different prices or demand by product/service,
- customer segments with different behavior,
- occasional cancellations/refunds/complaints,
- realistic correlations between quantity, price, discount, revenue, cost, and profit,
- realistic Egyptian context where appropriate, without using real private data.

Privacy/safety:

- Use only synthetic data.
- Do not use real customer names, real phone numbers, real emails, or real IDs.
- If names are needed, use Faker-generated synthetic names.
- Do not scrape real company data.
- Do not claim that the data is real.
- For real organizations such as banks, clubs, or public authorities, keep the data fictional and educational.

Dataset size:

- Main fact table: 1,000 to 3,000 rows.
- Dimensions: usually 10 to 500 rows depending on the dimension.
- Total package should remain easy to open in Excel and Power BI.

Cleaning issue ratio:
Introduce light-to-moderate dirty data:

- Around 3–8% nulls in selected columns.
- Around 2–5% inconsistent categories.
- Around 1–3% duplicate or near-duplicate records.
- A few invalid values, but not enough to ruin the dataset.
- Some date/numeric columns intentionally saved as strings in raw CSV form.

Do not overdo the dirtiness. The goal is educational cleaning, not advanced data engineering.

Output expectations:
When finished, provide:

1. A short explanation of what was generated.
2. The folder/file list.
3. Any assumptions made because the PD1/email did not specify something.
4. Clear instructions for running the script, for example:

```bash
source .venv/bin/activate
python generate_dataset.py
```
