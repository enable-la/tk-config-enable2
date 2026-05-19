import nuke
import reads_and_writes

def getRef():
    try:
        # Grab script path and job structure from standard command
        script_path, job_structure = reads_and_writes.standardCommand('Get Ref')

        # Reference Folder
        reference_folder = "/".join([
            job_structure["drive"],
            job_structure["job"],
            "sequences",
            job_structure["sequence"],
            job_structure["shot"],
            "reference"
        ])

        reference_footage = reads_and_writes.getAllFootage(reference_folder)
        if not reference_footage:
            print("No reference footage found.")
            return

        # Find the 'RefRead1' node
        ref_read = nuke.toNode('RefRead1')
        if not ref_read:
            print("RefRead1 node not found.")
            return

        for file_path, file_data in reference_footage.items():
            # Set the file path for the 'RefRead1' node
            ref_read['file'].fromUserText(file_path)
            ref_read['label'].setValue("[value first] - [value last]")

            # Set the "raw" checkbox to True
            ref_read['raw'].setValue(True)

    except Exception as e:
        nuke.message(f"An error occurred: {str(e)}")

#getRef()
