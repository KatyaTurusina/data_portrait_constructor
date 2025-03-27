import pandas as pd
import csv
from io import StringIO

def detect_separator(source):
    """Определяет разделитель в CSV (запятая, точка с запятой и др.)"""
    try:
        with open(source, 'r', newline='', encoding='utf-8') if isinstance(source, str) else source as f:
            sample = f.read(1024)
            sniffer = csv.Sniffer()
            return sniffer.sniff(sample).delimiter
    except Exception:
        return ','

def load_csv(file_path):
    """Загружает CSV из файла с автоматическим определением разделителя"""
    try:
        separator = detect_separator(file_path)
        return pd.read_csv(file_path, delimiter=separator)
    except Exception:
        return None

def process_text_input(text):
    """Обрабатывает данные, вставленные вручную, с автоопределением разделителя"""
    try:
        separator = detect_separator(StringIO(text))
        return pd.read_csv(StringIO(text), delimiter=separator)
    except Exception:
        return None

class DataHandler:
    def __init__(self):
        self.df = None  # DataFrame с загруженными данными

    def load_csv(self, file_path):
        """Загружает CSV из файла с автоматическим определением разделителя"""
        try:
            separator = detect_separator(file_path)
            self.df = pd.read_csv(file_path, delimiter=separator)
            return True
        except Exception as e:
            print(f"Ошибка загрузки CSV: {e}")
            return False

    def process_text_input(self, text):
        """Обрабатывает данные, вставленные вручную, с автоопределением разделителя"""
        try:
            separator = detect_separator(StringIO(text))
            self.df = pd.read_csv(StringIO(text), delimiter=separator)
            return True
        except Exception as e:
            print(f"Ошибка обработки текста: {e}")
            return False

    def clear_data(self):
        """Очищает данные"""
        self.df = None

    def get_columns(self):
        """Возвращает список столбцов DataFrame"""
        return self.df.columns.tolist() if self.df is not None else []