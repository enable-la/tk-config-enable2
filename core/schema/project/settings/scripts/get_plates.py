import nuke # type: ignore
import reads_and_writes

def getPlates():
    try:
        # Grab script path and job structure from standard command
        script_path, job_structure = reads_and_writes.standardCommand('Get Plates')

        # Plates Folder
        plates_folder = "/".join([
            job_structure["drive"],
            job_structure["job"],
            "sequences",
            job_structure["sequence"],
            job_structure["shot"],
            "plates"
        ])

        plates_footage = reads_and_writes.getAllFootage(plates_folder)
        if not plates_footage:
            nuke.message("No footage found in plates folder.")
            return

        # Collect filenames for the dropdown
        file_options = [file_path.split('/')[-1] for file_path in plates_footage.keys()]
        if not file_options:
            nuke.message("No plates found.")
            return
        
        # Create a panel with a dropdown for file selection
        panel = nuke.Panel("Select a Plate")
        panel.addEnumerationPulldown("Plate", " ".join(file_options))  # Space-separated for dropdown
        panel.addButton("Cancel")
        panel.addButton("Select")

        # Show the panel and get the result
        result = panel.show()

        if result == 0:  # If "Cancel" or panel closed
            nuke.message("Panel canceled or closed.")
            return

        # Get the selected file
        selected_file = panel.value("Plate")
        if not selected_file:
            nuke.message("No file selected.")
            return

        # Map the selected filename back to its full path and metadata
        file_path = None
        file_data = None
        for path, data in plates_footage.items():
            if selected_file in path:
                file_path = path
                file_data = data
                break

        if not file_path:
            nuke.message("Selected file path not found.")
            return

        # Find the 'PlatesRead1' node
        plate_read = nuke.toNode('PlatesRead1')
        if not plate_read:
            nuke.message("PlatesRead1 node not found.")
            return

        # Replace the file path and set frame range
        plate_read['file'].fromUserText(file_path)

        # Adjust frame range for proper EXR read
        plate_read['first'].setValue(file_data.get('first', 1))
        plate_read['last'].setValue(file_data.get('last', 1))

        # Set nuke.root frame range
        first_frame = file_data.get('first', 1)
        last_frame = file_data.get('last', 1)

        nuke.root()['first_frame'].setValue(first_frame)
        nuke.root()['last_frame'].setValue(last_frame)

        nuke.message("PlatesRead1 node successfully updated.")

    except Exception as e:
        nuke.message(f"An error occurred: {str(e)}")

#getPlates()
