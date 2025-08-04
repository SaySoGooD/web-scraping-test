import logging
from pathlib import Path
from typing import Optional


class CustomLogger(logging.Logger):
    def success(self, msg, *args, **kwargs):
        if self.isEnabledFor(logging.INFO + 5):
            self._log(logging.INFO + 5, msg, args, **kwargs)


def configure_logging(
        debug: bool = False,
        log_to_file: bool = True,
        log_path: str = "logs/app.log"
) -> None:
    """Настройка логирования с кастомными уровнями"""
    logging.addLevelName(logging.INFO + 5, 'SUCCESS')
    logging.setLoggerClass(CustomLogger)

    level = logging.DEBUG if debug else logging.INFO

    handlers = [logging.StreamHandler()]

    if log_to_file:
        log_path = Path(__file__).parent.parent.parent / "logs/app.log"
        log_path.parent.mkdir(exist_ok=True, parents=True)
        handlers.append(logging.FileHandler(log_path, encoding='utf-8'))

    logging.basicConfig(
        level=level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=handlers,
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    # Настройка логгеров сторонних библиотек
    for lib in ['urllib3', 'requests', 'asyncio']:
        logging.getLogger(lib).setLevel(logging.WARNING)


def get_logger(name: Optional[str] = None) -> logging.Logger:
    """Возвращает настроенный логгер"""
    logger = logging.getLogger(name)
    logger.success = lambda msg, *args, **kwargs: logger._log(logging.INFO + 5, msg, args, **kwargs)
    return logger
