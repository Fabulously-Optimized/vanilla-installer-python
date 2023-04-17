# Copyright (C) Fabulously Optimized 2023
# Licensed under the MIT License. The full license text can be found at https://github.com/Fabulously-Optimized/vanilla-installer/blob/main/LICENSE.md.
"""
Starts logging for Vanilla Installer.
"""

import logging
import logging.handlers  # pylance moment
from pathlib import Path
import sys


class LoggerWriter:
    def __init__(self, logfct):
        self.logfct = logfct
        self.buf = []

    def write(self, msg):
        if msg.endswith('\n'):
            self.buf.append(msg.removesuffix('\n'))
            self.logfct(''.join(self.buf))
            self.buf = []
        else:
            self.buf.append(msg)

    def flush(self):
        pass


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logfile_path = Path("./logs").resolve() / "vanilla_installer.log"
if logfile_path.exists() is False:
    Path("./logs").resolve().mkdir(exist_ok=True)
    with logfile_path as file:
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

# To access the original stdout/stderr, use sys.__stdout__/sys.__stderr__
sys.stdout = LoggerWriter(logger.info)
sys.stderr = LoggerWriter(logger.error)

logging.info("Starting Vanilla Installer")
logger = logging.getLogger(__name__)
