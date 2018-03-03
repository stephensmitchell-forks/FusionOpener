import adsk.core
import adsk.fusion
import traceback

import time
import os

from .Fusion360Utilities.Fusion360Utilities import AppObjects
from .Fusion360Utilities.Fusion360CommandBase import Fusion360CommandBase

file_name = ''
conversion_max = 10 # multiply times 5 for max seconds to wait
upload_max = 100


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
        ao = AppObjects()

        # converted_value = ao.units_manager.formatInternalValue(the_value, 'in', True)

        # ao.ui.messageBox('The value, in internal units, you entered was:  {} \n'.format(the_value) +
        #                  'The value, in inches, you entered was:  {} \n'.format(converted_value) +
        #                  'The boolean value checked was:  {} \n'.format(the_boolean) +
        #                  'The string you typed was:  {} \n'.format(the_string) +
        #                  'The name of the first object you selected is:  {}'.format(the_selection_name))

        # file_name = '/Users/rainsbp/Library/Application Support/Autodesk/Autodesk Fusion 360/API/AddIns/FusionOpener/Samples/ADSK_BOX.f3d'
        # file_name = '/Users/rainsbp/Library/Application Support/Autodesk/Autodesk Fusion 360/API/AddIns/FusionOpener/Samples/SMD Resistor - 100 ohm.SLDPRT'

        global file_name

        active_project = ao.app.data.activeProject

        root_folder = active_project.rootFolder

        start_count = root_folder.dataFiles.count
        # ao.ui.messageBox('Start count:  ' + str(root_folder.dataFiles.count))

        data_future = root_folder.uploadFile(file_name)
        test = 0



        # while root_folder.dataFiles.count != start_count+1 and test <= 10:
        #     time.sleep(2)
        #     test += 1

        adsk.doEvents()

        while data_future.uploadState == adsk.core.UploadStates.UploadProcessing and test <= upload_max:
            adsk.doEvents()
            time.sleep(1)
            test += 1

        if data_future.uploadState == adsk.core.UploadStates.UploadFailed:
            ao.ui.messageBox('Failed')
            return

        elif data_future.uploadState == adsk.core.UploadStates.UploadFinished:
            # ao.ui.messageBox('complete in ' + str(test) + ' secs')

            # ao.ui.messageBox(data_future.dataFile.name)
            data_file = data_future.dataFile
            adsk.doEvents()

            time_out = 1
            document = None
            while document is None and time_out <= conversion_max:
                try:
                    document = ao.app.documents.open(data_file)
                    ao.ui.messageBox('complete in '+ str(test) + ' secs and ' + str(time_out) + ' conversion attempts')
                except:
                    time.sleep(5)
                    time_out += 1

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
        fileDlg.title = 'Fusion File Dialog'
        fileDlg.filter = '*.*'
        # fileDlg.filter = "Alias files (*.wire);;AutoCAD DWG files(*.dwg);;Autodesk Fusion 360 files (*.f3d);;Autodesk " \
        #                  "Fusion 360 Drawing files (*.f2d);;Autodesk Fusion 360 Toolpath files (*.cam360);;Autodesk " \
        #                  "Inventor files (*.iam, *.ipt);;Catia V5 files (*.CATProduct, *.CATPart);;DXF files (" \
        #                  "*.dxf);;FBX files (*.fbx);;IGES files (*.iges, *.ige, *.igs);;NX files (*.prt);;OBJ files (" \
        #                  "*.obj);;Parasolid Binary files (*.x_b);;Parasolid Text files (*.x_t);;Pro/ENGINEER and Creo " \
        #                  "Parametric files (*.asm, *.prt);;Pro/ENGINEER Granite files (*.g);;Pro/ENGINEER Neutral " \
        #                  "files (*.neu);;Rhino files (*.3dm);;SAT/SMT files (*.sab, *.sat, *.smb, *.smt);;SolidWorks " \
        #                  "files (*.prt, *.asm, *.sldprt, *.sldasm);;STEP files (*.ste, *.step, *.stp);;STL files (" \
        #                  "*.stl);;SketchUp files (*.sku) "

        # fileDlg.initialDirectory = '/Users/rainsbp/Library/Application Support/Autodesk/Autodesk Fusion 360/API/AddIns/FusionOpener/Samples/'
        directory = os.path.dirname(os.path.realpath(__file__))
        directory = os.path.join(directory, 'Samples')
        fileDlg.initialDirectory = directory
        dlgResult = fileDlg.showOpen()
        if dlgResult == adsk.core.DialogResults.DialogOK:
            file_name = fileDlg.filename
            # ao.ui.messageBox(file_name)
        else:
            return
