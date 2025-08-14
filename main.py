import argparse
from pathlib import Path
from typing import Any

from app.db import get_connection
from app.repositories.reports_repository import ReportsRepository
from app.services.import_service import ImportService


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Load students and rooms into MySQL and run reports")
    parser.add_argument("--rooms", type=Path, default=Path("input/rooms.json"), help="Path to rooms.json")
    parser.add_argument("--students", type=Path, default=Path("input/students.json"), help="Path to students.json")
    parser.add_argument("--no-import", action="store_true", help="Skip import and only run reports")
    parser.add_argument("--no-truncate", action="store_true", help="Do not truncate tables before import")
    parser.add_argument("--reports-dir", type=Path, default=Path("reports"), help="Directory to write text reports to")
    return parser.parse_args()


def format_table(headers: list[str], rows: list[tuple[Any, ...]]) -> str:
    widths = [len(h) for h in headers]
    for row in rows:
        for i, cell in enumerate(row):
            widths[i] = max(widths[i], len(str(cell)))
    def fmt_row(values: list[Any]) -> str:
        return " | ".join(str(v).ljust(widths[i]) for i, v in enumerate(values))
    lines: list[str] = []
    lines.append(fmt_row(headers))
    lines.append("-+-".join("-" * w for w in widths))
    for row in rows:
        lines.append(fmt_row(list(row)))
    return "\n".join(lines)


def print_and_save(table_title: str, headers: list[str], rows: list[tuple[Any, ...]], out_path: Path) -> None:
    print(f"\n{table_title}")
    rendered = format_table(headers, rows)
    print(rendered)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(rendered + "\n", encoding="utf-8")


def main() -> None:
    args = parse_args()
    conn = get_connection()
    try:
        if not args.no_import:
            importer = ImportService(conn)
            importer.run(args.rooms, args.students, recreate=not args.no_truncate)
        reports = ReportsRepository(conn)

        reports_dir: Path = args.reports_dir

        # 1. List of rooms and the number of students in each
        rooms_counts = reports.rooms_with_counts()
        print_and_save(
            "Rooms and student counts:",
            ["room_id", "room_name", "student_count"],
            rooms_counts,
            reports_dir / "rooms_student_counts.txt",
        )

        # 2. Top 5 rooms with the smallest average student age
        smallest_avg_age = reports.top5_smallest_avg_age()
        print_and_save(
            "Top 5 rooms with smallest average age:",
            ["room_id", "room_name", "avg_age_years"],
            smallest_avg_age,
            reports_dir / "top5_smallest_avg_age.txt",
        )

        # 3. Top 5 rooms with the largest age difference among students
        largest_age_gap = reports.top5_largest_age_gap()
        print_and_save(
            "Top 5 rooms with largest age gap:",
            ["room_id", "room_name", "age_gap_years"],
            largest_age_gap,
            reports_dir / "top5_largest_age_gap.txt",
        )

        # 4. Rooms where students of different sexes live together
        mixed_sex = reports.mixed_sex_rooms()
        print_and_save(
            "Rooms with mixed sexes:",
            ["room_id", "room_name"],
            mixed_sex,
            reports_dir / "mixed_sex_rooms.txt",
        )
    finally:
        conn.close()


if __name__ == "__main__":
    main()
