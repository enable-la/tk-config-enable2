# ENABLE.LA
# This opens and saves the template into the new shot
# As well as set's LUT based on template's VIEWER_INPUT
# And then imports relevant plates, reference, and elements.
# Finally, we save the script again.
# Ian Blewitt 2024

import nuke # type: ignore
import sys
import get_plates
import get_ref
import get_write_task
import get_submissions
import set_luts
import afterRender

# Open the script
nuke.scriptOpen(sys.argv[2])

# Save it into the pipeline for variables
nuke.scriptSaveAs(sys.argv[1])

# Update the task specific setup
get_plates.getPlates()

# Sets the shot and show lut
set_luts.setLuts()

# Lock the frame range so the quicktime doesn't reset it
#nuke.root()['lock_range'].setValue(True)

# Finish updating the setup
# Update the ref
get_ref.getRef()

# Update the internal write node
#get_write_task.getWriteTask(sys.argv[3])

# Update the client submission writes
#get_submissions.main(sys.argv[3])

# Unlock the frame range if anyone complains about it being locked
# (leave it locked for safety in my opinion.)
# nuke.root()['lock_range'].setValue(False)

# Callback for write node afterRender
#nuke.addOnScriptSave(afterRender.convert_output_to_edit)
#nuke.addOnScriptSave(afterRender.convert_output_to_vfx)

# Save again now that it's all set up for the task!
nuke.scriptSave(sys.argv[1])