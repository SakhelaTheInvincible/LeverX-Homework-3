from typing import List, Tuple

from app.repositories.base import BaseRepository


class ReportsRepository(BaseRepository):
    def rooms_with_counts(self) -> List[Tuple[int, str, int]]:
        sql = (
            "SELECT r.id, r.name, COUNT(s.id) AS student_count "
            "FROM rooms r LEFT JOIN students s ON s.room_id = r.id "
            "GROUP BY r.id, r.name ORDER BY r.id"
        )
        with self.connection.cursor() as cur:
            cur.execute(sql)
            return list(cur.fetchall())

    def top5_smallest_avg_age(self) -> List[Tuple[int, str, float]]:
        sql = (
            "SELECT r.id, r.name, AVG(TIMESTAMPDIFF(YEAR, s.birthday, CURDATE())) AS avg_age_years "
            "FROM rooms r JOIN students s ON s.room_id = r.id "
            "GROUP BY r.id, r.name HAVING COUNT(s.id) > 0 "
            "ORDER BY avg_age_years ASC, r.id ASC LIMIT 5"
        )
        with self.connection.cursor() as cur:
            cur.execute(sql)
            return list(cur.fetchall())

    def top5_largest_age_gap(self) -> List[Tuple[int, str, int]]:
        sql = (
            "SELECT r.id, r.name, (MAX(TIMESTAMPDIFF(YEAR, s.birthday, CURDATE())) - MIN(TIMESTAMPDIFF(YEAR, s.birthday, CURDATE()))) AS age_gap_years "
            "FROM rooms r JOIN students s ON s.room_id = r.id "
            "GROUP BY r.id, r.name HAVING COUNT(s.id) > 1 "
            "ORDER BY age_gap_years DESC, r.id ASC LIMIT 5"
        )
        with self.connection.cursor() as cur:
            cur.execute(sql)
            return list(cur.fetchall())

    def mixed_sex_rooms(self) -> List[Tuple[int, str]]:
        sql = (
            "SELECT r.id, r.name "
            "FROM rooms r JOIN students s ON s.room_id = r.id "
            "GROUP BY r.id, r.name "
            "HAVING SUM(CASE WHEN s.sex = 'M' THEN 1 ELSE 0 END) > 0 "
            "AND SUM(CASE WHEN s.sex = 'F' THEN 1 ELSE 0 END) > 0 "
            "ORDER BY r.id"
        )
        with self.connection.cursor() as cur:
            cur.execute(sql)
            return list(cur.fetchall())
