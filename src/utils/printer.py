from typing import Optional
from src.models import TableResult


class ResultPrinter:
    """Выводит результаты в консоль"""

    @staticmethod
    def print_table(table: Optional[TableResult], max_rows: int = 5) -> None:
        """Выводит данные таблицы"""
        if not table:
            print("Не удалось получить данные таблицы.")
            return

        print(f"\nСтруктура таблицы [{table.metadata.database}.{table.metadata.table_name}]:")
        print(f"Столбцы: {table.columns}")
        print(f"\nСтрок: {max_rows-1}")

        for idx, row in enumerate(table.rows[:max_rows], 1):
            print(f"{idx}. {row}")
