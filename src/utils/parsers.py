import re
from typing import Any, Dict, List, Optional, Tuple
from bs4 import BeautifulSoup

from src.models import AuthCredentials, TableMetadata, TableResult
from src.utils.logger import get_logger

logger = get_logger(__name__)


class LoginFormParser:
    """Парсер формы входа phpMyAdmin"""

    @staticmethod
    def parse_form_data(html: str, credentials: AuthCredentials) -> Dict[str, str]:
        """Извлекает данные формы для авторизации"""
        soup = BeautifulSoup(html, 'html.parser')
        hidden_inputs = soup.find_all('input', {'type': 'hidden'})
        form_data = {i['name']: i.get('value', '') for i in hidden_inputs}
        form_data.update({
            'pma_username': credentials.username,
            'pma_password': credentials.password,
            'server': '1'
        })
        logger.debug(f"Получены данные формы для входа: {form_data}")
        return form_data

    @staticmethod
    def get_form_action_url(html: str, base_url: str) -> str:
        """Парсит HTML, находит форму входа и формирует полный URL для POST-запроса."""
        soup = BeautifulSoup(html, 'html.parser')
        form = soup.find('form', {'id': 'login_form'})
        if not form:
            raise ValueError("Форма входа не найдена в HTML")

        action = form.get('action', 'index.php')
        if not action.startswith('http'):
            action = f"{base_url.rstrip('/')}/{action.lstrip('/')}"
        logger.debug(f"Получен URL для авторизации: {action}")
        return action


class SessionTokenExtractor:
    """Извлекает токены сессии из HTML"""

    @staticmethod
    def extract_tokens(html: str) -> Tuple[Optional[str], Optional[str]]:
        """Извлекает токен и nocache из HTML"""
        soup = BeautifulSoup(html, 'html.parser')
        token = SessionTokenExtractor._extract_token(soup)
        nocache = SessionTokenExtractor._extract_nocache(soup)
        return token, nocache

    @staticmethod
    def _extract_token(soup: BeautifulSoup) -> Optional[str]:
        """Извлекает токен сессии"""
        token_input = soup.find('input', {'name': 'token'})
        logger.debug(f"Извлечен токен: {token_input.get('value') if token_input else None}")
        return token_input.get('value') if token_input else None

    @staticmethod
    def _extract_nocache(soup: BeautifulSoup) -> Optional[str]:
        """Извлекает параметр nocache"""
        for link in soup.find_all(['link', 'script']):
            href = link.get('href') or link.get('src') or ''
            if 'nocache=' in href:
                match = re.search(r'nocache=([0-9]+)', href)
                if match:
                    logger.debug(f"Извлечен nocache: {match.group(1)}")
                    return match.group(1)
        logger.debug("Параметр nocache не найден")
        return None


class TableDataParser:
    """Парсер данных таблицы из phpMyAdmin"""

    @staticmethod
    def parse(json_response: Dict) -> Optional[TableResult]:
        """Парсит JSON ответ с данными таблицы"""
        try:
            soup = BeautifulSoup(json_response['message'], 'html.parser')

            columns = TableDataParser._extract_columns(soup)
            rows = TableDataParser._extract_rows(soup, columns)
            metadata = TableDataParser._extract_metadata(json_response, soup, rows)
            return TableResult(
                columns=columns,
                rows=rows,
                metadata=metadata
            )
        except Exception as e:
            logger.error(f"Ошибка при парсинге JSON: {e}")
            return None

    @staticmethod
    def _extract_columns(soup: BeautifulSoup) -> List[str]:
        """Извлекает названия столбцов таблицы"""
        columns = []
        for th in soup.select('thead tr th.draggable'):
            col_name = th.get('data-field') or th.get_text(strip=True).split('\n')[0]
            if col_name and col_name not in columns:
                columns.append(col_name.replace('id1', 'id'))
        logger.debug(f"Извлечены столбцы: {columns}")
        return columns

    @staticmethod
    def _extract_rows(soup: BeautifulSoup, columns: List[str]) -> List[Dict[str, Any]]:
        """Извлекает данные строк таблицы"""
        rows = []
        for row in soup.select('tbody tr'):
            cells = TableDataParser._get_data_cells(row)
            row_data = TableDataParser._process_row_data(cells, columns)
            if row_data:
                rows.append(row_data)
        logger.debug(f'Извлечены строки: {rows}')
        return rows

    @staticmethod
    def _get_data_cells(row) -> List:
        """Получает ячейки с данными из строки таблицы"""
        return row.select('td[data-type], th[data-type]') or [
            td for td in row.find_all('td')
            if 'print_ignore' not in (td.get('class') or [])
        ]

    @staticmethod
    def _process_row_data(cells: List, columns: List[str]) -> Dict[str, Any]:
        """Обрабатывает данные строки"""
        row_data = {}
        for idx, cell in enumerate(cells):
            col_name = columns[idx] if idx < len(columns) else f'col_{idx}'
            cell_text = cell.get_text(' ', strip=True)

            if cell.get('data-type', '') in ['int', 'decimal']:
                cell_text = cell_text.replace(' ', '')

            row_data[col_name] = cell_text
        return row_data

    @staticmethod
    def _extract_metadata(json_response: Dict, soup: BeautifulSoup, rows: List) -> TableMetadata:
        """Извлекает метаданные таблицы"""
        sql_div = soup.find('div', class_='sqlOuter')
        return TableMetadata(
            database=json_response['params']['db'],
            table_name=json_response['params']['table'],
            row_count=len(rows),
            sql_query=sql_div.get_text(strip=True) if sql_div else None
        )
