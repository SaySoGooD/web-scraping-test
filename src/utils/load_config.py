from configparser import ConfigParser, NoSectionError, NoOptionError
from pathlib import Path
from typing import Optional
import logging

from src.models import AppConfig, AuthConfig, Config, DBConfig

logger = logging.getLogger(__name__)


def load_config(config_path: Optional[str] = None) -> Config:
    """Загружает конфигурацию из config.ini"""
    config = ConfigParser()
    config_path = Path(config_path) if config_path else Path(__file__).parent.parent.parent / "config.ini"

    # Проверка существования файла
    if not config_path.exists():
        error_msg = f"Конфигурационный файл не найден: {config_path.absolute()}"
        logger.critical(error_msg)
        raise FileNotFoundError(error_msg)

    # Чтение конфигурации
    config.read(config_path)

    try:
        return Config(
            app=AppConfig(
                debug=config.getboolean('app', 'debug', fallback=False),
                log_to_file=config.getboolean('app', 'log_to_file', fallback=True),
                log_file=config.get('app', 'log_file', fallback='logs/app.log')
            ),
            db=DBConfig(
                base_url=_get_required(config, 'db', 'base_url'),
                database=_get_required(config, 'db', 'database'),
                table=_get_required(config, 'db', 'table')
            ),
            auth=AuthConfig(
                username=_get_required(config, 'auth', 'username'),
                password=_get_required(config, 'auth', 'password')
            )
        )
    except (NoSectionError, NoOptionError) as e:
        error_msg = f"Ошибка в конфигурационном файле: {str(e)}"
        logger.critical(error_msg)
        raise ValueError(error_msg) from e


def _get_required(config: ConfigParser, section: str, option: str) -> str:
    """Получает обязательный параметр из конфига или вызывает исключение"""
    try:
        return config.get(section, option)
    except (NoSectionError, NoOptionError) as e:
        error_msg = f"Отсутствует обязательный параметр: [{section}] {option}"
        logger.error(error_msg)
        raise ValueError(error_msg) from e
