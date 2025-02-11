import logging
import sys


def setup_logger(verbose: bool = False) -> logging.Logger:
    """Set up and configure logger.

    Args:
        verbose: If True, set log level to DEBUG

    Returns:
        Configured logger instance
    """
    logger = logging.getLogger("gcore-api")

    if not logger.handlers:
        handler = logging.StreamHandler(sys.stderr)
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    logger.setLevel(logging.DEBUG if verbose else logging.INFO)
    return logger


logger = setup_logger()
