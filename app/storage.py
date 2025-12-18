import sqlite3
from typing import List
from app.schemas import TranslationPair


class TranslationStore:
    def __init__(self, db_path: str = "data/translations.db"):
        self.db_path = db_path
        self._init_db()

    def _get_connection(self):
        return sqlite3.connect(self.db_path)

    def _init_db(self):
        with self._get_connection() as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS translation_pairs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    source_language TEXT NOT NULL,
                    target_language TEXT NOT NULL,
                    sentence TEXT NOT NULL,
                    translation TEXT NOT NULL,
                    UNIQUE(source_language, target_language, sentence, translation)
                )
            """)


            conn.commit()


    def add(self, pair: TranslationPair):
        with self._get_connection() as conn:
            conn.execute(
                """
                INSERT
                OR IGNORE INTO translation_pairs
                (source_language, target_language, sentence, translation)
                VALUES (?, ?, ?, ?)
                """,
                (pair.source_language, pair.target_language,
                 pair.sentence, pair.translation)
            )
            conn.commit()

    def get_by_language(self, src: str, tgt: str) -> List[TranslationPair]:
        with self._get_connection() as conn:
            rows = conn.execute(
                """
                SELECT source_language, target_language, sentence, translation
                FROM translation_pairs
                WHERE source_language = ? AND target_language = ?
                """,
                (src, tgt)
            ).fetchall()

        return [
            TranslationPair(
                source_language=row[0],
                target_language=row[1],
                sentence=row[2],
                translation=row[3]
            )
            for row in rows
        ]
