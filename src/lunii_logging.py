import logging
from logging import Logger, LogRecord

from tqdm import tqdm

from pkg.api.constants import LUNII_LOGGER


class LuniiPacksLoggingHandler(logging.StreamHandler):
    def emit(self, record: LogRecord) -> None:  # noqa: D401
        """Emit log records through tqdm to avoid clobbering progress bars."""
        try:
            msg = self.format(record)
            tqdm.write(msg)
        except Exception:
            self.handleError(record)


def initialize_logger(log_level: int) -> Logger:
    """Configure and return the shared Lunii logger."""
    logger = logging.getLogger(LUNII_LOGGER)
    logger.addHandler(LuniiPacksLoggingHandler())
    logger.setLevel(log_level)
    return logger
