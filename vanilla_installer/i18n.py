"""Provides internationalization (i18n) services to the Vanilla Installer."""
import json
import logging
from pathlib import Path

logger = logging.getLogger(__name__)

if Path("vanilla_installer").exists():
    # This is a development environment, being run from the root directory
    lang_file_placeholder = "vanilla_installer/assets/lang/{}.json"
else:
    lang_file_placeholder = "assets/lang/{}.json"


def get_i18n_values(language_code: str = "en_us") -> dict:
    """Get the strings in the language requested.

    Args:
        language (str, optional): The language code to get the strings for. Defaults to en_us, and falls back to en_us if the code given is invalid.

    Returns:
        dict: The dictionary of strings for that language.
    """
    lang_file = Path(lang_file_placeholder.format(language_code)).resolve()
    if lang_file.exists() is False:
        logger.warning("Non-existant i18n code passed, falling back to en_us.")
        lang_file = Path(lang_file_placeholder.format("en_us")).resolve()
    lang_json = json.load(open(lang_file))
    return lang_json
