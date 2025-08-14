import mysql.connector
from mysql.connector import MySQLConnection

from app.config import get_config, MySQLConfig


def _connect(cfg: MySQLConfig, with_database: bool = True) -> MySQLConnection:
    kwargs = {
        "host": cfg.host,
        "port": cfg.port,
        "user": cfg.user,
        "password": cfg.password,
        "connection_timeout": cfg.connect_timeout,
    }
    if with_database:
        kwargs["database"] = cfg.database
    return mysql.connector.connect(**kwargs)


def ensure_database_exists() -> None:
    cfg = get_config().mysql
    admin_conn = _connect(cfg, with_database=False)
    admin_conn.autocommit = True
    try:
        with admin_conn.cursor() as cur:
            cur.execute(f"CREATE DATABASE IF NOT EXISTS `{cfg.database}` CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
    finally:
        admin_conn.close()


def get_connection() -> MySQLConnection:
    ensure_database_exists()
    cfg = get_config().mysql
    return _connect(cfg, with_database=True)


def create_schema(conn: MySQLConnection) -> None:
    table_statements = [
        # Rooms
        """
        CREATE TABLE IF NOT EXISTS rooms (
            id INT PRIMARY KEY,
            name VARCHAR(255) NOT NULL
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE utf8mb4_unicode_ci
        """,
        # Students
        """
        CREATE TABLE IF NOT EXISTS students (
            id INT PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            birthday DATE NOT NULL,
            sex ENUM('M','F') NOT NULL,
            room_id INT NOT NULL,
            CONSTRAINT fk_students_room FOREIGN KEY (room_id)
                REFERENCES rooms(id)
                ON UPDATE CASCADE
                ON DELETE RESTRICT
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE utf8mb4_unicode_ci
        """,
    ]
    conn.autocommit = True
    with conn.cursor() as cur:
        for stmt in table_statements:
            cur.execute(stmt)
    _create_indexes(conn)


def truncate_tables(conn: MySQLConnection) -> None:
    conn.autocommit = True
    with conn.cursor() as cur:
        cur.execute("SET FOREIGN_KEY_CHECKS=0")
        cur.execute("TRUNCATE TABLE students")
        cur.execute("TRUNCATE TABLE rooms")
        cur.execute("SET FOREIGN_KEY_CHECKS=1")


def _create_indexes(conn: MySQLConnection) -> None:
    # in MySQL, IF NOT EXISTS isn't supported for indexes, so ignore duplicate index errors
    index_statements = [
        "CREATE INDEX idx_students_room ON students(room_id)",
        "CREATE INDEX idx_students_room_sex_bday ON students(room_id, sex, birthday)",
    ]
    conn.autocommit = True
    with conn.cursor() as cur:
        for stmt in index_statements:
            try:
                cur.execute(stmt)
            except mysql.connector.Error as exc:
                if getattr(exc, "errno", None) in {1061}:
                    continue
                raise
