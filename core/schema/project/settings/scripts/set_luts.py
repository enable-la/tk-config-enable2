import os
import nuke
import reads_and_writes

def setLuts():
    try:
        # Set the path for LUTs folder using standardCommand
        script_path, job_structure = reads_and_writes.standardCommand('Set Lut Folder')

        # Print the returned values for debugging
        # print(f"Script Path: {script_path}")
        # print(f"Job Structure: {job_structure}")

        if not script_path or not job_structure:
            return

        lut_folder = os.path.join(
            job_structure["drive"], job_structure["job"], "sequences",
            job_structure["sequence"], job_structure["shot"], "lut"
        )

        # Normalize the path to avoid mixed slashes and replace backslashes with forward slashes
        lut_folder = os.path.normpath(lut_folder).replace("\\", "/")

        # Print the lut_folder path for debugging
        #print(f"LUT Folder Path: {lut_folder}")

        # Check if the directory exists
        if not os.path.exists(lut_folder):
            #print(f"LUT folder does not exist: {lut_folder}")
            nuke.message(f"LUT folder does not exist: {lut_folder}")
            return

        # List contents of the lut_folder for debugging
        # lut_folder_contents = os.listdir(lut_folder)
        # print(f"Contents of LUT Folder: {lut_folder_contents}")

        # Get all footage files in the lut_folder
        lut_files = reads_and_writes.getAllFootage(lut_folder)

        # Print the LUT files for debugging
        # print(f"LUT Files: {lut_files}")

        # Check if any LUT files were found
        if not lut_files:
            nuke.message(f"No LUT found.")
            return

        # Find the VIEWER_INPUT group
        viewer_input_node = None
        for node in nuke.allNodes('Group'):
            if node.name() == 'VIEWER_INPUT':
                viewer_input_node = node
                break

        if not viewer_input_node:
            #print("VIEWER_INPUT node not found.")
            return

        # Set the file OCIO file paths to the current shot and show LUTs
        # Update here if different than ccc shot / cube show
        for file_path, file_data in lut_files.items():
            # Normalize file paths to avoid mixed slashes and replace backslashes with forward slashes
            file_path = os.path.normpath(file_path).replace("\\", "/")

            if 'ccc' in file_data.get('ext', ''):
                #print(f"Setting VIEWER_INPUT file to: {file_path}")
                viewer_input_node.knob('file').setValue(file_path)
            elif 'cube' in file_data.get('ext', ''):
                #print(f"Setting VIEWER_INPUT file_1 to: {file_path}")
                viewer_input_node.knob('file_1').setValue(file_path)
    except Exception as e:
        nuke.message(f"An error occurred: {str(e)}")


# set_luts.setLuts()
