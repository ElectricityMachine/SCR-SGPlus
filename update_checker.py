import logging
import re
from typing import Optional, Tuple

import colorama
from requests import exceptions as requests_exceptions
from requests import get as requests_get
from semver import Version

from constants import VERSION

# https://python-semver.readthedocs.io/en/latest/advanced/deal-with-invalid-versions.html
BASEVERSION = re.compile(
    r"""[vV]?
        (?P<major>0|[1-9]\d*)
        (\.
        (?P<minor>0|[1-9]\d*)
        (\.
            (?P<patch>0|[1-9]\d*)
        )?
        )?
    """,
    re.VERBOSE,
)


def coerce(version: str) -> Tuple[Version, Optional[str]]:
    """
    Convert an incomplete version string into a semver-compatible Version
    object

    * Tries to detect a "basic" version string (``major.minor.patch``).
    * If not enough components can be found, missing components are
        set to zero to obtain a valid semver version.

    :param str version: the version string to convert
    :return: a tuple with a :class:`Version` instance (or ``None``
        if it's not a version) and the rest of the string which doesn't
        belong to a basic version.
    :rtype: tuple(:class:`Version` | None, str)
    """
    match = BASEVERSION.search(version)
    if not match:
        return (None, version)

    ver = {key: 0 if value is None else value for key, value in match.groupdict().items()}
    ver = Version(**ver)
    rest = match.string[match.end() :]  # noqa:E203
    return ver, rest


def check_for_updates() -> None:
    logging.debug("update_check: called")
    """Fetch the latest release version from the GitHub repo and inform the user if an update is available"""
    URL = "https://api.github.com/repos/ElectricityMachine/SCR-SGPlus/releases/latest"
    try:
        r = requests_get(url=URL, timeout=10)
        data = r.json()
        tag = coerce(data["tag_name"])
        our_tag = coerce(VERSION)
        if our_tag < tag:
            print(f"{colorama.Fore.RED}NOTICE: A new update is available for SG+!")
            print(
                "It is always recommended to update to the latest version. To do so, go to https://github.com/ElectricityMachine/SCR-SGPlus"
            )
            print('and follow the instructions under "Installation"')
            print(colorama.Fore.WHITE)
        else:
            logging.info("No new updates found.")
    except requests_exceptions.RequestException as e:
        logging.error(f"update_check: RequestException occurred: {e}")
        logging.error("Update check failed. Please ensure you have allowed sgplus.exe in your firewall.")
        logging.info("Skipping update check because we errored...")
