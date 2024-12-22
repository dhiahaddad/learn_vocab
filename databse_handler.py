import pandas as pd
import sqlite3

from typing import Tuple


class DatabaseHandler:
    def __init__(self, db_name: str) -> None:
        self.connection = sqlite3.connect(db_name)
        self.cursor = self.connection.cursor()

    def initialize_db_by_df(self, table_name: str, df: pd.DataFrame) -> None:
        self.__create_table_from_df(table_name, df)
        self.__create_progress_table(table_name)

    def insert_df_into_db(self, table_name: str, df: pd.DataFrame) -> None:
        for row in df.itertuples(index=True):
            self.cursor.execute(
                f"INSERT INTO {table_name} VALUES (?, ?, ?, ?, ?, ?, ?)",
                (row),
            )
            self.cursor.execute(
                f"INSERT INTO {table_name}_progress VALUES (?, ?, ?, ?, ?, ?)",
                (int(row[0]), None, 0, 0, 0, 0),
            )
        self.connection.commit()

    def get_random_row(self, table_name: str) -> Tuple:
        self.cursor.execute(f"SELECT * FROM {table_name} ORDER BY RANDOM() LIMIT 1")
        return self.cursor.fetchone()

    def close(self):
        self.connection.close()

    def __create_sql_schema_from_df(self, df: pd.DataFrame) -> str:
        schema = ", ".join([f"{col} TEXT" for col in df.columns])
        return schema

    def __create_table_from_df(self, table_name: str, df: pd.DataFrame) -> None:
        self.cursor.execute(f"DROP TABLE IF EXISTS {table_name}")

        df_schema = self.__create_sql_schema_from_df(df)
        schema = f"id INTEGER PRIMARY KEY AUTOINCREMENT,{df_schema}"
        query = f"CREATE TABLE {table_name} ({schema})"
        self.cursor.execute(query)
        self.connection.commit()

    def table_exists(self, table_name: str) -> bool:
        self.cursor.execute(
            "SELECT name FROM sqlite_master "
            "WHERE type='table' AND name=?",
            (table_name,),
        )
        return self.cursor.fetchone() is not None

    def get_table_schema(self, table_name: str) -> str:
        self.cursor.execute(f"PRAGMA table_info({table_name})")
        return self.cursor.fetchall()

    def __create_progress_table(self, table_name: str) -> None:
        self.cursor.execute(f"DROP TABLE IF EXISTS {table_name}_progress")
        schema = """
            id INTEGER PRIMARY KEY,
            learning_lvl TEXT,
            correct_translations INTEGER,
            correct_articles INTEGER,
            incorrect_translations INTEGER,
            incorrect_articles INTEGER
            """
        self.cursor.execute(f"CREATE TABLE {table_name}_progress ({schema})")
        self.connection.commit()

    def update_progress(
        self, table_name: str, id: int, correct_translation: bool, correct_article: bool
    ) -> None:
        if correct_translation:
            self.cursor.execute(
                f"UPDATE {table_name}_progress "
                "SET correct_translations = correct_translations + 1 WHERE id = ?",
                (id,),
            )
        else:
            self.cursor.execute(
                f"UPDATE {table_name}_progress "
                "SET incorrect_translations = incorrect_translations + 1 WHERE id = ?",
                (id,),
            )

        if correct_article:
            self.cursor.execute(
                f"UPDATE {table_name}_progress "
                "SET correct_articles = correct_articles + 1 WHERE id = ?",
                (id,),
            )
        else:
            self.cursor.execute(
                f"UPDATE {table_name}_progress "
                "SET incorrect_articles = incorrect_articles + 1 WHERE id = ?",
                (id,),
            )

        self.connection.commit()
