import nuke
import sys
import reads_and_writes

# Define path mappings once
path_mappings = {
    'postvis': 'postvis',
    'color': 'plates',
    'lineup': 'plates',
    'comp': 'comp',
    'paint': 'paint',
    'roto': 'roto'
}

def getWriteExrTask(taskForPass):
    try:
        if taskForPass not in path_mappings:
            raise ValueError(f"Unknown task: {taskForPass}")

        script_path, job_structure = reads_and_writes.standardCommand('Get Write Task')

        exr_folder = "/".join([
            job_structure["drive"], job_structure["job"], 'review',
            f'[date %Y%m%d]', path_mappings[taskForPass]
        ])

        sequence_shot = job_structure["sequence"].upper() + job_structure["shot"]
        task_version = f"{taskForPass}_INH_v0001"
        exr_filename = f"{sequence_shot}_{task_version}"

        write_node = nuke.toNode('write_exr')
        if not write_node:
            print("Write_exr node not found.")
            return
        
        shot_file_path = f"{exr_folder}/{exr_filename}/{exr_filename}/{exr_filename}.%04d.exr"
        write_node.knob('file').setValue(shot_file_path)
        
        print(f"File path of Write_exr node updated to: {shot_file_path}")

    except Exception as e:
        nuke.message(f"An error occurred: {str(e)}")

def getWriteAvidTask(taskForPass):
    try:
        if taskForPass not in path_mappings:
            raise ValueError(f"Unknown task: {taskForPass}")

        script_path, job_structure = reads_and_writes.standardCommand('Get Write Task')

        avid_folder = "/".join([
            job_structure["drive"], job_structure["job"], 'review',
            f'[date %Y%m%d]', path_mappings[taskForPass]
        ])

        sequence_shot = job_structure["sequence"].upper() + job_structure["shot"]
        task_version = f"{taskForPass}_INH_v0001"
        avid_filename = f"{sequence_shot}_{task_version}"

        write_node = nuke.toNode('write_avid')
        if not write_node:
            print("Write_avid node not found.")
            return
        
        shot_file_path = f"{avid_folder}/{avid_filename}/{avid_filename}.mov"
        write_node.knob('file').setValue(shot_file_path)
        
        print(f"File path of Write_avid node updated to: {shot_file_path}")

    except Exception as e:
        nuke.message(f"An error occurred: {str(e)}")

def getWriteVfxTask(taskForPass):
    try:
        if taskForPass not in path_mappings:
            raise ValueError(f"Unknown task: {taskForPass}")

        script_path, job_structure = reads_and_writes.standardCommand('Get Write Task')

        vfx_folder = "/".join([
            job_structure["drive"], job_structure["job"], 'review',
            f'[date %Y%m%d]', path_mappings[taskForPass]
        ])

        sequence_shot = job_structure["sequence"].upper() + job_structure["shot"]
        task_version = f"{taskForPass}_INH_v0001"
        vfx_filename = f"{sequence_shot}_{task_version}"

        write_node = nuke.toNode('write_vfx')
        if not write_node:
            print("Write_vfx node not found.")
            return
        
        shot_file_path = f"{vfx_folder}/{vfx_filename}/{vfx_filename}_vfx/{vfx_filename}_vfx.%04d.jpg"
        write_node.knob('file').setValue(shot_file_path)
        
        print(f"File path of Write_vfx node updated to: {shot_file_path}")

    except Exception as e:
        nuke.message(f"An error occurred: {str(e)}")

def main(task):
    getWriteExrTask(task)
    getWriteAvidTask(task)
    getWriteVfxTask(task)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: script.py <task>")
        sys.exit(1)
    
    task = sys.argv[1]
    main(task)
