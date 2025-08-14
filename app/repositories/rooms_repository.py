from typing import Iterable, List, Tuple

from app.repositories.base import BaseRepository


class RoomsRepository(BaseRepository):
    def insert_many(self, rooms: Iterable[Tuple[int, str]]) -> None:
        sql = "INSERT INTO rooms (id, name) VALUES (%s, %s)"
        with self.connection.cursor() as cur:
            cur.executemany(sql, list(rooms))
        self.connection.commit()

    def list_with_student_counts(self) -> List[Tuple[int, str, int]]:
        sql = (
            "SELECT r.id, r.name, COUNT(s.id) AS student_count "
            "FROM rooms r LEFT JOIN students s ON s.room_id = r.id "
            "GROUP BY r.id, r.name ORDER BY r.id"
        )
        with self.connection.cursor() as cur:
            cur.execute(sql)
            return list(cur.fetchall())
