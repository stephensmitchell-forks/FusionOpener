import adsk.core
import adsk.fusion
import traceback

import time
import os

from .Fusion360Utilities.Fusion360Utilities import AppObjects
from .Fusion360Utilities.Fusion360CommandBase import Fusion360CommandBase

file_name = ''
part_names = []
conversion_max = 500 # multiply times 5 for max seconds to wait
upload_max = 1000
assembly = False


# Class for a Fusion 360 Command
# Place your program logic here
# Delete the line that says "pass" for any method you want to use
class Demo1Command(Fusion360CommandBase):
    # Run whenever a user makes any change to a value or selection in the addin UI
    # Commands in here will be run through the Fusion processor and changes will be reflected in  Fusion graphics area
    def on_preview(self, command: adsk.core.Command, inputs: adsk.core.CommandInputs, args, input_values):
        pass

    # Run after the command is finished.
    # Can be used to launch another command automatically or do other clean up.
    def on_destroy(self, command: adsk.core.Command, inputs: adsk.core.CommandInputs, reason, input_values):
        pass

    # Run when any input is changed.
    # Can be used to check a value and then update the add-in UI accordingly
    def on_input_changed(self, command: adsk.core.Command, inputs: adsk.core.CommandInputs, changed_input, input_values):
        pass

    # Run when the user presses OK
    # This is typically where your main program logic would go
    def on_execute(self, command: adsk.core.Command, inputs: adsk.core.CommandInputs, args, input_values):

        # # Get the values from the user input
        # the_value = input_values['value_input']
        # the_boolean = input_values['bool_input']
        # the_string = input_values['string_input']
        # all_selections = input_values['selection_input']
        #
        # # Selections are returned as a list so lets get the first one and its name
        # the_first_selection = all_selections[0]
        # the_selection_name = the_first_selection.name

        # Get a reference to all relevant application objects in a dictionary


        # converted_value = ao.units_manager.formatInternalValue(the_value, 'in', True)

        # ao.ui.messageBox('The value, in internal units, you entered was:  {} \n'.format(the_value) +
        #                  'The value, in inches, you entered was:  {} \n'.format(converted_value) +
        #                  'The boolean value checked was:  {} \n'.format(the_boolean) +
        #                  'The string you typed was:  {} \n'.format(the_string) +
        #                  'The name of the first object you selected is:  {}'.format(the_selection_name))

        # file_name = '/Users/rainsbp/Library/Application Support/Autodesk/Autodesk Fusion 360/API/AddIns/FusionOpener/Samples/ADSK_BOX.f3d'
        # file_name = '/Users/rainsbp/Library/Application Support/Autodesk/Autodesk Fusion 360/API/AddIns/FusionOpener/Samples/SMD Resistor - 100 ohm.SLDPRT'

        ao = AppObjects()
        active_project = ao.app.data.activeProject
        root_folder = active_project.rootFolder

        # Set styles of progress dialog.
        progress_dialog = ao.ui.createProgressDialog()
        progress_dialog.cancelButtonText = 'Cancel'
        progress_dialog.isBackgroundTranslucent = False
        progress_dialog.isCancelButtonShown = True
        progress_dialog.message = 'Uploading: %v secs'

        if os.path.exists(file_name):

            if assembly:
                data_future = root_folder.uploadAssembly(part_names)
            else:
                data_future = root_folder.uploadFile(file_name)
            test = 0

            adsk.doEvents()
        else:
            ao.ui.messageBox('Something is wrong with the file')
            return

        # Show dialog
        # progress_dialog.show('Progress Dialog', 'Iterations: %v', 0, 100, 0)
        # progress_dialog.hide()

        while data_future.uploadState == adsk.core.UploadStates.UploadProcessing and test <= upload_max:
            # If progress dialog is cancelled, stop drawing.
            if progress_dialog.wasCancelled:
                break
            # Update progress value of progress dialog

            adsk.doEvents()

            progress_dialog.progressValue = test
            time.sleep(1)
            test += 1

            # Hide the progress dialog at the end.




        if data_future.uploadState == adsk.core.UploadStates.UploadFailed:
            ao.ui.messageBox('Failed')
            return

        elif data_future.uploadState == adsk.core.UploadStates.UploadFinished:
            # ao.ui.messageBox('complete in ' + str(test) + ' secs')
            # ao.ui.messageBox(data_future.dataFile.name)

            data_file = data_future.dataFile
            adsk.doEvents()

            time_out = 0
            document = None
            progress_dialog.progressValue = time_out
            progress_dialog.message = 'Converting: %v secs'
            while document is None and time_out <= conversion_max:
                try:

                    # ao.ui.messageBox('complete in '+ str(test) + ' secs and ' + str(time_out) + ' conversion attempts')
                    # ao.ui.messageBox('is ' + str(data_file.hasParentReferences))
                    # ao.ui.messageBox('is ' + str(data_file.isInUse))
                    # ao.ui.messageBox('last ' + str(data_file.lastUpdatedBy))
                    document = ao.app.documents.open(data_file)
                except:
                    pass
                adsk.doEvents()
                progress_dialog.progressValue = time_out

                if progress_dialog.wasCancelled:
                    ao.ui.messageBox('File still uploaded, open from data panel after conversion completes')
                time.sleep(1)
                time_out += 1

            progress_dialog.hide()

        else:
            ao.ui.messageBox('Never Finished in ' + str(test) + ' secs')



        # # ao.ui.messageBox(str(data_future.uploadState))
        # # data_file = data_future.dataFile
        #
        # ao.ui.messageBox('count:  ' + str(root_folder.dataFiles.count))
        # new_file = root_folder.dataFiles.item(root_folder.dataFiles.count-1)
        # ao.ui.messageBox(new_file.name)
        # document = ao.app.documents.open(new_file)

    # Run when the user selects your command icon from the Fusion 360 UI
    # Typically used to create and display a command dialog box
    # The following is a basic sample of a dialog UI
    def on_create(self, command: adsk.core.Command, inputs: adsk.core.CommandInputs):
        global file_name
        global part_names
        global assembly
        assembly = False
        part_names[:] = []
        # Create a default value using a string
        default_value = adsk.core.ValueInput.createByString('1.0 in')
        ao = AppObjects()

        # Create a few inputs in the UI
        # inputs.addValueInput('value_input', '***Sample***Value', ao.units_manager.defaultLengthUnits, default_value)
        # inputs.addBoolValueInput('bool_input', '***Sample***Checked', True)
        # inputs.addStringValueInput('string_input', '***Sample***String Value', 'Default value')
        # inputs.addSelectionInput('selection_input', '***Sample***Selection', 'Select Something')

        fileDlg = ao.ui.createFileDialog()
        fileDlg.isMultiSelectEnabled = False
        fileDlg.title = 'Select a file to import'

        fileDlg.filter = "Supported Files (*.wire;*.dwg;*.f3d;*.f2d;*.cam360;*.iam;*.ipt;*.CATProduct;*.CATPart;*.dxf;*.fbx;*.igs;*.ige;*.iges;*.prt;*.obj;*.x_b;*.x_t;*.prt;*.asm;*.g;*.neu;*.3dm;*.sat;*.smb;*.smt;*.sab;*.asm;*.sldprt;*.sldasm;*.prt;*.step;*.stp;*.ste;*.stl;*.sku);;" \
                        "Alias files (*.wire);;AutoCAD DWG files(*.dwg);;Autodesk Fusion 360 files (*.f3d);;Autodesk Fusion 360 Drawing files (*.f2d);;Autodesk Fusion 360 Toolpath files (*.cam360);;Autodesk Inventor files (*.iam;*.ipt);;Catia V5 files (*.CATProduct;*.CATPart);;DXF files (*.dxf);;FBX files (*.fbx);;IGES files (*.iges;*.ige;*.igs);;NX files (*.prt);;OBJ files (*.obj);;Parasolid Binary files (*.x_b);;Parasolid Text files (*.x_t);;Pro/ENGINEER and Creo Parametric files (*.asm;*.prt);;Pro/ENGINEER Granite files (*.g);;Pro/ENGINEER Neutral files (*.neu);;Rhino files (*.3dm);;SAT/SMT files (*.sab;*.sat;*.smb;*.smt);;SolidWorks files (*.prt;*.asm;*.sldprt;*.sldasm);;STEP files (*.ste;*.step;*.stp);;STL files (*.stl);;SketchUp files (*.sku);;" \
                         "All Files(*.*)"

        directory = os.path.dirname(os.path.realpath(__file__))
        directory = os.path.join(directory, 'Samples')
        fileDlg.initialDirectory = directory
        dlgResult = fileDlg.showOpen()

        if dlgResult == adsk.core.DialogResults.DialogOK:
            file_name = fileDlg.filename
            # ao.ui.messageBox(file_name)
        else:
            ao.ui.terminateActiveCommand()
        # ao.ui.messageBox(os.path.splitext(file_name)[1].lower())
        if os.path.splitext(file_name)[1].lower() in ['.sldasm', '.asm', '.iam']:
            assembly = True
            ao.ui.messageBox('You are trying to open an assembly, now select all its references')
            part_dialog = ao.ui.createFileDialog()
            part_dialog.isMultiSelectEnabled = True
            part_dialog.title = 'Select references'
            part_dialog.filter = "Supported Files (*.iam;*.ipt;*.CATProduct;*.CATPart;*.prt;*.asm;*.sldprt;*.sldasm;)" \
                                 "All Files(*.*)"
            part_dialog.initialDirectory = os.path.dirname(file_name)
            part_result = part_dialog.showOpen()
            if part_result == adsk.core.DialogResults.DialogOK:
                part_names.append(file_name)
                part_names += part_dialog.filenames
                ao.ui.messageBox(str(part_names))