import pandas as pd


class CsvReader:
    required_columns = [
        "Level",
        "Artikel",
        "Deutsch",
        "Plural",
        "Englisch",
        "Beispielsatz",
    ]

    def read_from_url(self, file_path: str) -> pd.DataFrame:
        df = pd.read_csv(file_path, encoding="ISO-8859-1")
        filtered_data = df[self.required_columns]
        return filtered_data

    def read_from_file(self, file_path: str) -> pd.DataFrame:
        df = pd.read_csv(file_path, encoding="ISO-8859-1")
        filtered_data = df[self.required_columns]
        return filtered_data
