import os
import re
import nuke
import get_job_structure
import get_highest_version

# Used to create facility comp output write node.
def compWrite(command_name, write_type, channels=None, metadata=None, reading=None, checkHashOnRead=None, on_error=None, name=None):
    """
    Defines Nuke standard write command. i.e. Creates a pre-filled
    Nuke Write node according to `write_type`.

    Args:
        command_name (str): Used for error message.
        write_name (str): Used to define file name.
    """
    script_path, job_structure = standardCommand(command_name)
    if not script_path or not job_structure:
        return

    kwargs = dict()
    images_folder = "/".join([job_structure["drive"], job_structure["job"], "sequences",
                              job_structure["sequence"], job_structure["shot"],
                              "renders","comp"])
    version_regex = "_".join([job_structure["shot"], write_type,
                              "v(?P<version>\d+$)"])
    version = get_highest_version.getHighestVersion(images_folder, version_regex)

    # Version string
    version_string = "v{0:0>3}".format(version)

    # Conform naming convention
    file_name = "_".join(job_structure["sequence"], job_structure["shot"], version_string, write_type)

    kwargs['file'] = "{0}/{1}/{1}.%04d.exr".format(images_folder, file_name)

    kwargs['file_type'] = 'exr'
    if channels:
        kwargs['channels'] = channels
    if metadata: 
        kwargs['metadata'] = metadata
    if reading:
        kwargs['reading'] = reading
        kwargs['checkHashOnRead'] = checkHashOnRead
    if on_error:
        kwargs['on_error'] = on_error
    if name:
        kwargs['name'] = name
    write_node = nuke.nodes.Write(**kwargs)
    try:
        write_node.setInput(0, nuke.selectedNode())
    except:
        min_x, min_y, max_x, max_y = getBbox(nuke.allNodes())
        pass

def precompWrite(command_name, write_type, compression=None, channels=None, metadata=None, name=None):
    """
    Defines Nuke standard write command. i.e. Creates a pre-filled
    Nuke Write node according to `write_type`.

    Args:
        command_name (str): Used for error message.
        write_name (str): Used to define file name.
    """
    script_path, job_structure = standardCommand(command_name)
    if not script_path or not job_structure:
        return

    kwargs = dict()
    images_folder = "/".join([job_structure["drive"], job_structure["job"], "sequences",
                              job_structure["sequence"], job_structure["shot"],
                              "renders","precomp"])
    version_regex = "_".join([job_structure["shot"], write_type,
                              "v(?P<version>\d+$)"])
    version = get_highest_version.getHighestVersion(images_folder, version_regex)

    # Version string
    version_string = "v{0:0>3}".format(version)

    file_name = "_".join([job_structure["job"], job_structure["sequence"], job_structure["shot"], write_type, version_string])

    kwargs['file'] = "{0}/{1}/{1}.%04d.exr".format(images_folder, file_name)

    kwargs['file_type'] = 'exr'
    if channels:
        kwargs['channels'] = channels
    if metadata:
        kwargs['metadata'] = metadata
    if name:
        kwargs['name'] = name
    write_node = nuke.nodes.Write(**kwargs)
    try:
        write_node.setInput(0, nuke.selectedNode())
    except:
        min_x, min_y, max_x, max_y = getBbox(nuke.allNodes())
        pass

# Used to gather "standard information" about the current script.
# Returns Script's path and Job Structure.
def standardCommand(command_name):
    """
    Defines Nuke standard command. i.e. Gets the script path, and
    the job structure (dict) of the script path.

    Args:
        command_name (str): Used for error message.

    Returns:
        (tuple) containing `script_path` and `job_structure`.
    """
    script_path = getScriptPath()
    if not script_path:
        message = ("{0} Failed.\n\n"
            "Please save your script prior to running {0}.")
        nuke.critical(message.format(command_name))
        return None, None

    job_structure = get_job_structure.getJobStructure(script_path)
    if not job_structure:
        message = ("{0} Failed.\n\n"
            "Needs job structure.")
        nuke.critical(message.format(command_name))
        return None, None

    return script_path, job_structure

# Returns the path of the current script.
def getScriptPath():
    """
    Avoid RuntimeError while getting script name, so we can give the proper
    error message.

    Returns:
        Script name (str) or None if script is not yet saved.
    """
    try:
        return nuke.scriptName()
    except RuntimeError:
        return None

# Returns size of bbox.
def getBbox(nodes):
    """
    Gets the node graph bounding box of the given `nodes`.

    Returns:
        Bounding box (tuple) `(min_x, min_y, max_x, max_y)`
    """
    min_x = None
    min_y = None
    max_x = None
    max_y = None
    for node in nodes:
        if min_x == None or node.xpos() < min_x:
            min_x = node.xpos()
        if min_y == None or node.ypos() < min_y:
            min_y = node.ypos()
        if max_x == None or node.xpos() > max_x:
            max_x = node.xpos()
        if max_y == None or node.ypos() > max_y:
            max_y = node.ypos()
    return (min_x, min_y, max_x, max_y)


# Returns locations of all footage files in shot directory.
def getAllFootage(footage_folder):
    """
    Recursively gets footage information containing file_path, extension, first
    frame and last frame information.

    Args:
        footage_folder (str): Where the files/subfolders are.

    Returns:
        all_footage (dict).
    """
    file_regex = re.compile("(?P<base>\S+\.(?P<ext>\S+))$")
    sequence_regex = re.compile("(?P<base>(?P<name>\w+)\S*\.(?P<ext>\w+)) "
        "(?P<first>\d+)-(?P<last>\d+)$")
    all_footage = {}
    basenames = nuke.getFileNameList(footage_folder) or []
    for basename in basenames:
        # Subfolder
        fullname = "/".join([footage_folder, basename])
        if os.path.isdir(fullname):
            all_footage.update(getAllFootage(fullname))
            continue

        # Single file
        file_match = file_regex.match(basename)
        if file_match:
            file_path = "/".join([footage_folder, file_match.group("base")])
            all_footage[file_path] = {"ext": file_match.group("ext"),
                                      "first": 1,
                                      "last": 1}
            continue

        # File sequence
        sequence_match = sequence_regex.match(basename)
        if sequence_match:
            file_path = "/".join([footage_folder, sequence_match.group("base")])
            all_footage[file_path] = {"ext": sequence_match.group("ext"),
                                      "first": int(sequence_match.group("first")),
                                      "last": int(sequence_match.group("last"))}
            continue

    if not all_footage:
        pass

    return all_footage
