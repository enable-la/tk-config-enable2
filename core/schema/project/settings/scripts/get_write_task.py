import nuke
import sys
import reads_and_writes

def getWriteTask(taskForPass):
    try:
        # Define path mappings for each task
        path_mappings = {
            'postvis': 'renders/postvis',
            'color': 'plates',
            'lineup': 'plates',
            'comp': 'renders/comp',
            'paint': 'renders/paint',
            'roto': 'renders/roto'
        }
                
        # Check if the provided task is valid
        if taskForPass not in path_mappings:
            raise ValueError(f"Unknown task: {taskForPass}")

        # Grab script path and job structure from standard command
        script_path, job_structure = reads_and_writes.standardCommand('Get Write Task')
        task = taskForPass
        
        # task folder
        task_folder = "/".join([
            job_structure["drive"], job_structure["job"], 'sequences',
            job_structure["sequence"], job_structure["shot"], path_mappings[task]
        ])

        # task filename
        task_filename = "_".join([
            job_structure["job"], job_structure["sequence"], job_structure["shot"], task, 'v0001'
        ])

        # Find the Write node
        write_node = nuke.toNode('write_task')
        if not write_node:
            print("Write_task node not found.")
            return
        
        # shot file path
        shot_file_path = f"{task_folder}/{task_filename}/{task_filename}.%04d.exr"
        
        # Modify the file path of the write node
        write_node.knob('file').setValue(shot_file_path)
        write_node.knob('name').setValue(f'write_{task}')
        
        print(f"File path of Write_task node updated to: {shot_file_path}")

    except Exception as e:
        nuke.message(f"An error occurred: {str(e)}")

# Example usage
#getWriteTask('postvis')
#getWriteTask('color')
#getWriteTask('lineup')
#getWriteTask('comp')
