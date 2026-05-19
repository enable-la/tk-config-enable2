import os
import re

# This returns the highest version.
def getHighestVersion(path, version_regex=".*_v(?P<version>\d+$)"):
    """
    Search `path` for the highest version of a file that matches the `version_regex`.

    Args:
        path (str): Where the files are.
        version_regex (str): Regular expression with "version" as group key.

    Returns:
        Highest version found (int).
    """
    highest_version = 1
    if not os.path.isdir(path):
        return highest_version

    for basename in os.listdir(path):
        version_match = re.match(version_regex, basename)
        if not version_match:
            continue

        version_number = int(version_match.group("version"))
        if version_number >= highest_version:
            highest_version = version_number + 1

    return highest_version
