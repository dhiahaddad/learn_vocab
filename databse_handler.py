import numpy as np
import pandas as pd
import sqlite3

from typing import List, Tuple

from word import MAX_LVL, Word


class DatabaseHandler:

    def __init__(self, db_name: str) -> None:
        self._connection = sqlite3.connect(db_name)
        self._cursor = self._connection.cursor()

    def initialize_db_by_df(self, table_name: str, df: pd.DataFrame) -> None:
        self._create_table_from_df(table_name, df)
        self._create_progress_table(table_name)

    def insert_df_into_db(self, table_name: str, df: pd.DataFrame) -> None:
        for row in df.itertuples(index=True):
            self._cursor.execute(
                f"INSERT INTO {table_name} VALUES (?, ?, ?, ?, ?, ?, ?)",
                (row),
            )
            self._cursor.execute(
                f"INSERT INTO {table_name}_progress VALUES (?, ?, ?, ?, ?, ?)",
                (int(row[0]), -1, 0, 0, 0, 0),
            )
        self._connection.commit()

    def reset_progress(self, table_name: str) -> None:
        self._cursor.execute(f"UPDATE {table_name}_progress SET learned_lvl = -1")
        self._cursor.execute(f"UPDATE {table_name}_progress SET correct_translations = 0")
        self._cursor.execute(f"UPDATE {table_name}_progress SET correct_articles = 0")
        self._cursor.execute(f"UPDATE {table_name}_progress SET incorrect_translations = 0")
        self._cursor.execute(f"UPDATE {table_name}_progress SET incorrect_articles = 0")
        self._connection.commit

    def get_random_row(self, table_name: str, words_number: int) -> Tuple:
        MAX_LVL = 5
        query = (
            f"SELECT * FROM {table_name} vocab "
            f"INNER JOIN {table_name}_progress prog ON vocab.id = prog.id "
            "WHERE vocab.id IN "
            f"(SELECT id FROM de_en_vocabulary_progress WHERE learned_lvl < {MAX_LVL} LIMIT {words_number}) "
            "ORDER BY RANDOM() LIMIT 1"
        )
        self._cursor.execute(query)
        return self._cursor.fetchone()

    def get_number_of_rows_in_table(self, table_name: str) -> int:
        self._cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
        return self._cursor.fetchone()[0]

    def get_number_of_studied_words(self, table_name: str) -> int:
        self._cursor.execute(
            f"SELECT COUNT(*) FROM {table_name}_progress "
            "WHERE learned_lvl = -1"
        )
        return self._cursor.fetchone()[0]

    def get_number_of_words_in_lvl(self, table_name: str, lvl: int) -> int:
        self._cursor.execute(
            f"SELECT COUNT(*) FROM {table_name}_progress " f"WHERE learned_lvl = {lvl}"
        )
        return self._cursor.fetchone()[0]

    def update_rows_number(self, table_name: str) -> None:
        self._cursor.execute(f"SELECT COUNT(*) FROM {table_name}")

    def table_exists(self, table_name: str) -> bool:
        self._cursor.execute(
            "SELECT name FROM sqlite_master " "WHERE type='table' AND name=?",
            (table_name,),
        )
        return self._cursor.fetchone() is not None

    def get_table_schema(self, table_name: str) -> List[str]:
        self._cursor.execute(f"PRAGMA table_info({table_name})")
        return self._cursor.fetchall()

    def set_learned_lvl(self, table_name: str, id: int, lvl: int) -> None:
        self._cursor.execute(
            f"UPDATE {table_name}_progress " "SET learned_lvl = ? WHERE id = ?",
            (
                lvl,
                id,
            ),
        )

    def update_progress(
        self, table_name: str, id: int, correct_translation: bool, correct_article: bool
    ) -> None:
        if correct_translation:
            self._cursor.execute(
                f"UPDATE {table_name}_progress "
                "SET correct_translations = correct_translations + 1 WHERE id = ?",
                (id,),
            )
        else:
            self._cursor.execute(
                f"UPDATE {table_name}_progress "
                "SET incorrect_translations = incorrect_translations + 1 WHERE id = ?",
                (id,),
            )

        if correct_article:
            self._cursor.execute(
                f"UPDATE {table_name}_progress "
                "SET correct_articles = correct_articles + 1 WHERE id = ?",
                (id,),
            )
        else:
            self._cursor.execute(
                f"UPDATE {table_name}_progress "
                "SET incorrect_articles = incorrect_articles + 1 WHERE id = ?",
                (id,),
            )

        self._connection.commit()

    def update_learning_lvl(self, table_name: str, word: Word, result: bool) -> None:
        correct = int(word.correct_translations) + int(word.correct_articles) + 2 * int(result)
        incorrect = int(word.incorrect_translations) + int(word.incorrect_articles) + 2 * int(not result)
        lvl = int(MAX_LVL * correct / (correct + incorrect))
        self._cursor.execute(
            f"UPDATE {table_name}_progress " "SET learned_lvl = ? WHERE id = ?",
            (
                lvl,
                word.id,
            ),
        )
        self._connection.commit()

    def close(self):
        self._connection.close()

    def __create_sql_schema_from_df(self, df: pd.DataFrame) -> str:
        schema = ", ".join([f"{col} TEXT" for col in df.columns])
        return schema

    def _create_table_from_df(self, table_name: str, df: pd.DataFrame) -> None:
        self._cursor.execute(f"DROP TABLE IF EXISTS {table_name}")

        df_schema = self.__create_sql_schema_from_df(df)
        schema = f"id INTEGER PRIMARY KEY AUTOINCREMENT,{df_schema}"
        query = f"CREATE TABLE {table_name} ({schema})"
        self._cursor.execute(query)
        self._connection.commit()

    def _create_progress_table(self, table_name: str) -> None:
        self._cursor.execute(f"DROP TABLE IF EXISTS {table_name}_progress")
        schema = """
            id INTEGER PRIMARY KEY,
            learned_lvl TEXT,
            correct_translations INTEGER,
            correct_articles INTEGER,
            incorrect_translations INTEGER,
            incorrect_articles INTEGER
            """
        self._cursor.execute(f"CREATE TABLE {table_name}_progress ({schema})")
        self._connection.commit()
