from typing import Optional

from src.http.requests_repository import HttpRequestRepository
from src.models import AuthCredentials, SessionTokens, TableResult
from src.utils.parsers import LoginFormParser, SessionTokenExtractor, TableDataParser

from src.utils.logger import get_logger

logger = get_logger(__name__)


class PMAClient:
    """Сервис для работы с phpMyAdmin API"""

    def __init__(self, request_handler: HttpRequestRepository, credentials: AuthCredentials):
        self.request_handler = request_handler
        self.credentials = credentials
        self.tokens: Optional[SessionTokens] = None

    def login(self) -> bool:
        """Аутентификация в phpMyAdmin"""
        try:
            response = self.request_handler.get(params={'route': '/'})
            response.raise_for_status()

            form_data = LoginFormParser.parse_form_data(response.text, self.credentials)
            form_url = LoginFormParser.get_form_action_url(response.text, self.request_handler.base_url)

            login_response = self.request_handler.post(form_url, data=form_data)
            login_response.raise_for_status()

            token, nocache = SessionTokenExtractor.extract_tokens(login_response.text)
            self.tokens = SessionTokens(token=token, nocache=nocache)
            return True

        except Exception as e:
            logger.error(f"Ошибка аутентификации: {e}")
            return False

    def fetch_table_data(self, database: str, table: str) -> Optional[TableResult]:
        """Получение данных таблицы"""
        if not self.tokens:
            raise RuntimeError("Требуется предварительная аутентификация")

        try:
            response = self.request_handler.get(
                params={
                    'route': '/sql',
                    'db': database,
                    'table': table,
                    'pos': '0',
                    'ajax_request': 'true',
                    'ajax_page_request': 'true',
                    '_nocache': self.tokens.nocache,
                    'token': self.tokens.token
                },
                headers={
                    'X-Requested-With': 'XMLHttpRequest',
                    'Referer': f"{self.request_handler.base_url}/?route=/",
                    'Priority': 'u=0'
                }
            )
            response.raise_for_status()

            json_data = response.json()
            if not json_data.get('success'):
                raise ValueError("Сервер вернул неуспешный статус")

            return TableDataParser.parse(json_data)

        except Exception as e:
            logger.error(f"Ошибка получения данных: {e}")
            return None
