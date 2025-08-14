from typing import Iterable, Tuple

from app.repositories.base import BaseRepository


class StudentsRepository(BaseRepository):
    def insert_many(self, students: Iterable[Tuple[int, str, str, str, int]]) -> None:
        sql = "INSERT INTO students (id, name, birthday, sex, room_id) VALUES (%s, %s, %s, %s, %s)"
        with self.connection.cursor() as cur:
            cur.executemany(sql, list(students))
        self.connection.commit()
