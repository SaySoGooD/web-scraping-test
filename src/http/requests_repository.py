from typing import Dict, Optional

import requests


class HttpRequestRepository:
    """Обработчик HTTP запросов"""

    def __init__(self, base_url: str):
        self.base_url = base_url
        self.session = requests.Session()
        self._setup_default_headers()

    def _setup_default_headers(self) -> None:
        """Установка стандартных заголовков"""
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        })

    def get(self, endpoint: str = '', params: Optional[Dict] = None,
            headers: Optional[Dict] = None) -> requests.Response:
        """Выполнить GET запрос"""
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        return self.session.get(url, params=params, headers=headers)

    def post(self, endpoint: str = '', data: Optional[Dict] = None,
             headers: Optional[Dict] = None) -> requests.Response:
        """Выполнить POST запрос"""
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        return self.session.post(url, data=data, headers=headers)
