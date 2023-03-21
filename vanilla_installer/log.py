# Copyright (C) Fabulously Optimized 2022
# Licensed under the MIT License. The full license text can be found at https://github.com/Fabulously-Optimized/vanilla-installer/blob/main/LICENSE.md.
"""Starts logging for Vanilla Installer."""
import logging
import logging.handlers  # pylance moment
import pathlib

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logfile_path = str(pathlib.Path("./logs").resolve() / "vanilla_installer.log")
try:
    handler = logging.handlers.RotatingFileHandler(
        filename=logfile_path,
        encoding="utf-8",
        maxBytes=32 * 1024 * 1024,  # 32 MiB
        backupCount=5,  # Rotate through 5 files
    )
except FileNotFoundError:
    print("WARNING | Log file not found, creating...")
    pathlib.Path("./logs").mkdir(exist_ok=True)
    with pathlib.Path("./logs").resolve() / "vanilla_installer.log" as file:
        open(file, "x", encoding="utf-8").write("")
    handler = logging.handlers.RotatingFileHandler(
        filename=logfile_path,
        encoding="utf-8",
        maxBytes=32 * 1024 * 1024,  # 32 MiB
        backupCount=5,  # Rotate through 5 files
    )
dt_fmt = "%Y-%m-%d %H:%M:%S"
formatter = logging.Formatter(
    "[{asctime}] [{levelname:<8}] {name}: {message}", dt_fmt, style="{"
)
handler.setFormatter(formatter)
logger.addHandler(handler)

logging.info("Starting Vanilla Installer")
logger = logging.getLogger(__name__)
