from src.http.requests_repository import HttpRequestRepository
from src.http.pma_client import PMAClient

from src.models import AuthCredentials

from src.utils.load_config import load_config
from src.utils.logger import configure_logging
from src.utils.printer import ResultPrinter

from src.utils.logger import get_logger

logger = get_logger(__name__)


def main():
    """Точка входа в программу"""
    try:
        config = load_config()

        configure_logging(
            debug=config.app.debug,
            log_to_file=config.app.log_to_file,
            log_path=config.app.log_file
        )

        logger.info("Запуск приложения")
        logger.debug(f"Загружена конфигурация: {config}")

        client = PMAClient(
            request_handler=HttpRequestRepository(base_url=config.db.base_url),
            credentials=AuthCredentials(
                username=config.auth.username,
                password=config.auth.password
            )
        )

        logger.info("Попытка аутентификации")
        if not client.login():
            print("Аутентификация не удалась. Проверьте учетные данные.")
            return
        logger.info("Аутентификация успешна")

        logger.info(f"Запрос данных таблицы {config.db.table}")
        table_data = client.fetch_table_data(
            database=config.db.database,
            table=config.db.table
        )

        if table_data:
            logger.success(f"Получено {len(table_data.rows)} записей")
            ResultPrinter.print_table(table_data)
        else:
            logger.warning("Данные таблицы не получены")

    except Exception as e:
        logger.critical(f"Критическая ошибка: {str(e)}", exc_info=True)
        raise


if __name__ == "__main__":
    main()
