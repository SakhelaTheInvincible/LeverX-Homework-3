from pathlib import Path

from mysql.connector import MySQLConnection

from app.db import create_schema, truncate_tables
from app.repositories.rooms_repository import RoomsRepository
from app.repositories.students_repository import StudentsRepository
from app.services.json_loader import load_rooms, load_students


class ImportService:
    def __init__(self, connection: MySQLConnection) -> None:
        self.connection = connection
        self.rooms_repo = RoomsRepository(connection)
        self.students_repo = StudentsRepository(connection)

    def run(self, rooms_path: Path, students_path: Path, recreate: bool = True) -> None:
        create_schema(self.connection)
        if recreate:
            truncate_tables(self.connection)
        rooms = load_rooms(rooms_path)
        if rooms:
            self.rooms_repo.insert_many(rooms)
        for batch in load_students(students_path):
            self.students_repo.insert_many(batch)
