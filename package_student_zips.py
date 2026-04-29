"""
Creates one zip per team, containing only student-facing files:
  - student_dataset/*.csv
  - data_dictionary.md

Output: zips/<slug>.zip
Run: python package_student_zips.py [slug ...]
     python package_student_zips.py          # packages all slugs in output/
"""

import os
import sys
import zipfile
from pathlib import Path

OUTPUT_DIR = Path("output")
ZIPS_DIR   = Path("zips")


def package(slug: str) -> Path:
    base = OUTPUT_DIR / slug
    if not base.is_dir():
        raise FileNotFoundError(f"output/{slug}/ not found")

    csv_files  = sorted((base / "student_dataset").glob("*.csv"))
    dict_file  = base / "data_dictionary.md"

    if not csv_files:
        raise FileNotFoundError(f"No CSVs found in output/{slug}/student_dataset/")
    if not dict_file.exists():
        raise FileNotFoundError(f"output/{slug}/data_dictionary.md not found")

    ZIPS_DIR.mkdir(exist_ok=True)
    zip_path = ZIPS_DIR / f"{slug}.zip"

    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
        for csv in csv_files:
            zf.write(csv, arcname=f"{slug}/{csv.name}")
        zf.write(dict_file, arcname=f"{slug}/data_dictionary.md")

    size_kb = zip_path.stat().st_size / 1024
    print(f"  {zip_path}  ({len(csv_files)} CSVs + data_dictionary.md, {size_kb:.1f} KB)")
    return zip_path


def main():
    slugs = sys.argv[1:] or sorted(p.name for p in OUTPUT_DIR.iterdir() if p.is_dir())

    print(f"Packaging {len(slugs)} dataset(s) → zips/\n")
    ok, failed = [], []
    for slug in slugs:
        try:
            package(slug)
            ok.append(slug)
        except Exception as e:
            print(f"  SKIP {slug}: {e}")
            failed.append(slug)

    print(f"\nDone: {len(ok)} zipped" + (f", {len(failed)} skipped" if failed else "") + ".")


if __name__ == "__main__":
    main()
