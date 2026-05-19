# set_slate.py

import nuke

def set_slate_exr_note(group_name, note_text):
    # Find the group node by name
    group_node = nuke.toNode(group_name)
    if group_node is None:
        print(f"Group node '{group_name}' not found.")
        return

    # Set the note field of the group node
    group_node['note'].setValue(note_text)

def set_slate_edit_note(group_name, note_text):
    # Find the group node by name
    group_node = nuke.toNode(group_name)
    if group_node is None:
        print(f"Group node '{group_name}' not found.")
        return

    # Set the note field of the group node
    group_node['note'].setValue(note_text)

def set_slate_h264_note(group_name, note_text):
    # Find the group node by name
    group_node = nuke.toNode(group_name)
    if group_node is None:
        print(f"Group node '{group_name}' not found.")
        return

    # Set the note field of the group node
    group_node['note'].setValue(note_text)
