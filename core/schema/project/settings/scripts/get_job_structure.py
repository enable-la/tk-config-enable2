import copy
import os
import re

def getJobStructure(path):
    # Args: path (str): Path to a Nuke script.

    # Returns: Job structure info (dict) containing drive, episode, job, sequence, shot, app, and filepath including filetype.

    job_structure = {}

    script_regex = re.compile(r"(?i)(?P<drive>.*)/(?P<job>\w+)/sequences/(?P<sequence>\w+)/(?P<shot>\w+)/(?P<app>\w+)/(?P<file>.*\w+)$")
    script_match = script_regex.match(path)

    if script_match:
        job_structure = copy.deepcopy(script_match.groupdict())

    return job_structure
