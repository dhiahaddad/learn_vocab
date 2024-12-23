import numpy as np
import pandas as pd
import sqlite3

from typing import List, Tuple


class DatabaseHandler:

    def __init__(self, db_name: str) -> None:
        self.__connection = sqlite3.connect(db_name)
        self.__cursor = self.__connection.cursor()

    def initialize_db_by_df(self, table_name: str, df: pd.DataFrame) -> None:
        self.__create_table_from_df(table_name, df)
        self.__create_progress_table(table_name)

    def insert_df_into_db(self, table_name: str, df: pd.DataFrame) -> None:
        for row in df.itertuples(index=True):
            self.__cursor.execute(
                f"INSERT INTO {table_name} VALUES (?, ?, ?, ?, ?, ?, ?)",
                (row),
            )
            self.__cursor.execute(
                f"INSERT INTO {table_name}_progress VALUES (?, ?, ?, ?, ?, ?)",
                (int(row[0]), 0, 0, 0, 0, 0),
            )
        self.__connection.commit()

    def get_random_row(self, table_name: str, words_number: int) -> Tuple:
        MAX_LVL = 5
        query = (
            f"SELECT * FROM {table_name} vocab "
            f"INNER JOIN {table_name}_progress prog ON vocab.id = prog.id "
            "WHERE vocab.id IN "
            f"(SELECT id FROM de_en_vocabulary_progress WHERE learned_lvl < {MAX_LVL} LIMIT {words_number}) "
            "ORDER BY RANDOM() LIMIT 1"
        )
        self.__cursor.execute(query)
        return self.__cursor.fetchone()

    def update_rows_number(self, table_name: str) -> None:
        self.__cursor.execute(f"SELECT COUNT(*) FROM {table_name}")

    def table_exists(self, table_name: str) -> bool:
        self.__cursor.execute(
            "SELECT name FROM sqlite_master " "WHERE type='table' AND name=?",
            (table_name,),
        )
        return self.__cursor.fetchone() is not None

    def get_table_schema(self, table_name: str) -> List[str]:
        self.__cursor.execute(f"PRAGMA table_info({table_name})")
        return self.__cursor.fetchall()

    def set_learned_lvl(self, table_name: str, id: int, lvl: int) -> None:
        self.__cursor.execute(
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
            self.__cursor.execute(
                f"UPDATE {table_name}_progress "
                "SET correct_translations = correct_translations + 1 WHERE id = ?",
                (id,),
            )
        else:
            self.__cursor.execute(
                f"UPDATE {table_name}_progress "
                "SET incorrect_translations = incorrect_translations + 1 WHERE id = ?",
                (id,),
            )

        if correct_article:
            self.__cursor.execute(
                f"UPDATE {table_name}_progress "
                "SET correct_articles = correct_articles + 1 WHERE id = ?",
                (id,),
            )
        else:
            self.__cursor.execute(
                f"UPDATE {table_name}_progress "
                "SET incorrect_articles = incorrect_articles + 1 WHERE id = ?",
                (id,),
            )

        self.__connection.commit()

    def close(self):
        self.__connection.close()

    def __create_sql_schema_from_df(self, df: pd.DataFrame) -> str:
        schema = ", ".join([f"{col} TEXT" for col in df.columns])
        return schema

    def __create_table_from_df(self, table_name: str, df: pd.DataFrame) -> None:
        self.__cursor.execute(f"DROP TABLE IF EXISTS {table_name}")

        df_schema = self.__create_sql_schema_from_df(df)
        schema = f"id INTEGER PRIMARY KEY AUTOINCREMENT,{df_schema}"
        query = f"CREATE TABLE {table_name} ({schema})"
        self.__cursor.execute(query)
        self.__connection.commit()

    def __create_progress_table(self, table_name: str) -> None:
        self.__cursor.execute(f"DROP TABLE IF EXISTS {table_name}_progress")
        schema = """
            id INTEGER PRIMARY KEY,
            learned_lvl TEXT,
            correct_translations INTEGER,
            correct_articles INTEGER,
            incorrect_translations INTEGER,
            incorrect_articles INTEGER
            """
        self.__cursor.execute(f"CREATE TABLE {table_name}_progress ({schema})")
        self.__connection.commit()
