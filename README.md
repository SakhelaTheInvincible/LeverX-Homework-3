## LeverX Homework 3: MySQL + Raw SQL Reporting

### Setup
1. Python 3.11+
2. MySQL 8+
3. Use uv (fast Python package/deps manager)
```bash
# Install uv (Windows PowerShell)
powershell -Command "iwr https://astral.sh/uv/install.ps1 -UseBasicParsing | iex"
# Or with pipx
pipx install uv
```

Install dependencies:
```bash
uv sync
```

### Configure DB
Create `.env` in project root:
```
MYSQL_HOST=127.0.0.1
MYSQL_PORT=3306
MYSQL_USER=root
MYSQL_PASSWORD=your_password
MYSQL_DATABASE=leverx_homework_3
```

The script auto-creates the database and tables if they do not exist.

### Run
Default paths assume `input/rooms.json` and `input/students.json` exist.
```bash
uv run python main.py
```
Options:
- `--rooms PATH` custom rooms file
- `--students PATH` custom students file
- `--no-import` skip import and only run reports
- `--no-truncate` do not truncate tables before import
- `--reports-dir` output path for reports (default=reports)

### Schema
- `rooms(id PK, name)`
- `students(id PK, name, birthday DATE, sex ENUM('M','F'), room_id FK -> rooms.id)`

Indexes used for optimization:
- `CREATE INDEX idx_students_room ON students(room_id)`
- `CREATE INDEX idx_students_room_sex_bday ON students(room_id, sex, birthday)`

### Reports
- Rooms and student counts
- Top 5 rooms with smallest average age
- Top 5 rooms with largest age gap
- Rooms with mixed sexes

All of them are saved in reports directory
