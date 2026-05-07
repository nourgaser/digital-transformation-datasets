# Digital Transformation Datasets — Claude Code Context

## What this project is

A repository for generating **synthetic educational datasets** for the Digital Transformation course (BINF 402) at the German International University (GIU), Spring 2026. Each team submits a PD1 document and/or an email describing their company. The task is to read those inputs and produce a Python script that generates a realistic synthetic dataset package for that team.

**Instructor:** Dr. Nourhan Hamdi  
**TAs:** Nour Gaser, Omar Alaa, Menna Khaled, Ibrahim Hisham

## How to run any generator

```bash
source .venv/bin/activate
python generate_<company_slug>.py
```

## Project structure

```
inputs/
  <company_slug>/          # one folder per team
    mail.md or email.md    # student email (always present)
    *.pdf                  # PD1 document (sometimes present)

output/
  <company_slug>/
    student_dataset/       # CSV files — share with students
    data_dictionary.md     # share with students
    private_instructor_notes/
      expected_cleaning_tasks.md
      suggested_dax_measures.md
      dashboard_questions.md
      model_relationships.md

generate_<company_slug>.py   # one generator script per team
generator_template.py        # starter template for new generators
```

## Completed datasets

| Company | Slug | Script |
|---------|------|--------|
| Egyptian National Railways | `enr_t07` | `generate_enr_t07.py` |
| Dar Al Maaref | `dar_al_maaref` | `generate_dar_al_maaref.py` |
| Banque du Caire | `banque_du_caire` | `generate_banque_du_caire.py` |
| Misr Insurance Company | `misr_insurance` | `generate_misr_insurance.py` |
| SODIC | `sodic` | `generate_sodic.py` |
| Talaat Moustafa Group | `tmg` | `generate_tmg.py` |
| Misr Spinning and Weaving | `msw` | `generate_msw.py` |

## Key task when a new team arrives

1. Check `inputs/<slug>/` for their PDF and/or email
2. Read both carefully — base everything on what they actually described
3. Copy `generator_template.py`, rename it `generate_<slug>.py`
4. Fill in company-specific constants, dimensions, fact tables
5. Run it, verify output, confirm validation passes
6. Add entry to the table above

## Full specification

See **`AGENTS.md`** for the complete model-agnostic specification including all conventions, ratios, schema rules, and cleaning issue guidelines.
