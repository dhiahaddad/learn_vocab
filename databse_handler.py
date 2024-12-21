import pandas as pd
import sqlite3

from typing import Tuple


class DatabaseHandler:
    def __init__(self, db_name: str) -> None:
        self.connection = sqlite3.connect(db_name)
        self.cursor = self.connection.cursor()

    def initialize_db_by_df(self, table_name: str, df: pd.DataFrame) -> None:
        self.create_table_from_df(table_name, df)

    def create_sql_schema_from_df(self, df: pd.DataFrame) -> str:
        schema = ", ".join([f"{col} TEXT" for col in df.columns])
        return schema

    def create_table_from_df(self, table_name: str, df: pd.DataFrame) -> None:
        schema = self.create_sql_schema_from_df(df)
        self.cursor.execute(f"CREATE TABLE IF NOT EXISTS {table_name} ({schema})")
        self.connection.commit()

    def insert_df_into_db(self, table_name: str, df: pd.DataFrame) -> None:
        df.to_sql(table_name, self.connection, if_exists="replace", index=False)

    def get_random_row(self, table_name: str) -> Tuple:
        self.cursor.execute(f"SELECT * FROM {table_name} ORDER BY RANDOM() LIMIT 1")
        return self.cursor.fetchone()

    def close(self):
        self.connection.close()
