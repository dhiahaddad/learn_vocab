import pandas as pd


class CsvReader:
    _required_columns = [
        "Level",
        "Artikel",
        "Deutsch",
        "Plural",
        "Englisch",
        "Beispielsatz",
    ]

    def read_from_url(self, file_path: str) -> pd.DataFrame:
        df = pd.read_csv(file_path, encoding="utf-8")
        filtered_data = df[self._required_columns]
        return filtered_data

    def read_from_file(self, file_path: str) -> pd.DataFrame:
        df = pd.read_csv(file_path, encoding="utf-8")
        filtered_data = df[self._required_columns]
        return filtered_data
