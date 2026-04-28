# Digital Transformation Datasets

Synthetic dataset generators for Digital Transformation course projects. Each Python script creates a small, Power BI-friendly dataset package for a specific student project using a simple star schema and light built-in cleaning issues.

## What This Repo Contains

- `generate_*.py`: standalone dataset generators for different projects
- `inputs/`: source PD1 files and student requests
- `output/`: generated CSV datasets, data dictionaries, and instructor notes
- `main_prompt.md` and `project_prompt.md`: prompt templates used to define the generation requirements

Current generators include:

- `generate_banque_du_caire.py`
- `generate_dar_al_maaref.py`
- `generate_enr_t07.py`
- `generate_misr_insurance.py`
- `generate_sodic.py`

## Output Structure

Each generator writes files under `output/<project_slug>/`:

- `student_dataset/`: student-facing CSV files
- `data_dictionary.md`: short business and column reference
- `private_instructor_notes/`: cleaning tasks, DAX ideas, dashboard questions, and model relationships

## Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Run

Run any generator script directly, for example:

```bash
source .venv/bin/activate
python generate_sodic.py
```

The script will create or overwrite the corresponding folder inside `output/`.
