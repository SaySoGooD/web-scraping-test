from dataclasses import dataclass
from typing import Any, Dict, List, Optional


@dataclass(frozen=True)
class AuthCredentials:
    """Учетные данные для аутентификации в системе."""
    username: str
    password: str


@dataclass(frozen=True)
class SessionTokens:
    """Токены сессии, полученные после успешной аутентизации."""
    token: str
    nocache: str


@dataclass(frozen=True)
class TableMetadata:
    """Метаинформация о полученной таблице."""
    database: str
    table_name: str
    row_count: int
    sql_query: Optional[str]


@dataclass(frozen=True)
class TableResult:
    """Результат парсинга таблицы с данными и метаинформацией."""
    columns: List[str]
    rows: List[Dict[str, Any]]
    metadata: TableMetadata


@dataclass(frozen=True)
class AppConfig:
    """Конфигурация параметров приложения."""
    debug: bool
    log_to_file: bool
    log_file: str


@dataclass(frozen=True)
class DBConfig:
    """Параметры подключения к базе данных."""
    base_url: str
    database: str
    table: str


@dataclass(frozen=True)
class AuthConfig:
    """Учетные данные из конфигурационного файла."""
    username: str
    password: str


@dataclass(frozen=True)
class Config:
    """Основной класс конфигурации, объединяющий все параметры."""
    app: AppConfig
    db: DBConfig
    auth: AuthConfig
