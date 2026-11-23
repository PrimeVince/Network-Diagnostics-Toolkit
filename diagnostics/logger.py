
import logging
from pathlib import Path


def setup_logger():
    logs_directory = Path("logs")
    logs_directory.mkdir(exist_ok=True)

    log_file = logs_directory / "network_toolkit.log"

    logging.basicConfig(
        filename=log_file,
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        encoding="utf-8",
        force=True
    )

    return logging.getLogger("NetworkDiagnostics")
