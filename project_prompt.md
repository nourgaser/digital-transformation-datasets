Use the dataset-generation prompt we agreed on.

Generate the Python dataset generator for this project:

Company/project:
{{COMPANY_NAME}}

Team:
{{TEAM_MEMBERS}}

Attached:
1. PD1 document
2. Student email/request

Requirements:
- Generate a realistic synthetic dataset based on their actual PD1 and email.
- Main fact table max 3,000 rows.
- Simple star schema.
- Light cleaning issues only.
- Student-facing CSV files + short data dictionary.
- Private instructor notes with expected cleaning tasks, suggested DAX measures, dashboard questions, and model relationships.
- Do not manually generate rows in chat. Generate Python code that creates the files.