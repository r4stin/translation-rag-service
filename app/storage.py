"""
Persistence layer for translation pairs.

This module handles SQLite-based storage, including initialization,
deduplication, and retrieval by language pair.
"""

import sqlite3
from typing import List
from app.schemas import TranslationPair


class TranslationStore:
    """
    SQLite-backed storage for translation pairs.

    Ensures persistence across restarts and prevents duplicate entries
    via a database-level UNIQUE constraint.
    """

    def __init__(self, db_path: str = "data/translations.db"):
        self.db_path = db_path
        self._init_db()

    def _get_connection(self):
        """Create a new database connection."""
        return sqlite3.connect(self.db_path)

    def _init_db(self):
        """Initialize database schema if it does not exist."""
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
        """
        Insert a translation pair into storage.

        Duplicate entries are ignored, making the operation idempotent.

        Args:
            pair (TranslationPair): Translation example to store.
        """
        with self._get_connection() as conn:
            conn.execute(
                """
                INSERT OR IGNORE INTO translation_pairs
                (source_language, target_language, sentence, translation)
                VALUES (?, ?, ?, ?)
                """,
                (pair.source_language, pair.target_language,
                 pair.sentence, pair.translation)
            )
            conn.commit()

    def get_by_language(self, src: str, tgt: str) -> List[TranslationPair]:
        """
        Retrieve all translation pairs for a given language pair.

        Args:
            src (str): Source language code.
            tgt (str): Target language code.

        Returns:
            List[TranslationPair]: Stored translation examples.
        """
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
