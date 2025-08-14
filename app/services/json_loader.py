import json
from pathlib import Path
from typing import Iterator, List, Tuple

import ijson


def load_rooms(json_path: Path) -> List[Tuple[int, str]]:
    with json_path.open("r", encoding="utf-8") as f:
        data = json.load(f)
    return [(int(item["id"]), str(item["name"])) for item in data]


def _iter_students(json_path: Path) -> Iterator[Tuple[int, str, str, str, int]]:
    with json_path.open("r", encoding="utf-8") as f:
        for item in ijson.items(f, "item"):
            yield (
                int(item["id"]),
                str(item["name"]),
                str(item["birthday"]).split("T", 1)[0],
                str(item["sex"]).upper(),
                int(item["room"]),
            )


def load_students(json_path: Path, batch_size: int = 5000) -> Iterator[List[Tuple[int, str, str, str, int]]]:
    batch: List[Tuple[int, str, str, str, int]] = []
    for row in _iter_students(json_path):
        batch.append(row)
        if len(batch) >= batch_size:
            yield batch
            batch = []
    if batch:
        yield batch
