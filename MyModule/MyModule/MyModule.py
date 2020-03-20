import os
import unittest
import vtk, qt, ctk, slicer
from slicer.ScriptedLoadableModule import *
import logging
import numpy as np


#
# MyModule
#

class MyModule(ScriptedLoadableModule):

    def __init__(self, parent):
        ScriptedLoadableModule.__init__(self, parent)
        self.parent.title = "MyModule"
        self.parent.categories = ["Examples"]
        self.parent.dependencies = []
        self.parent.contributors = ["Laura Lucendo Maranes"]
        self.parent.helpText = """This code has been created with the aim of comparing masks obtained from two different softwares by getting important values such as Dice Index and Hausdorff Distance. Besides, a color map has been created to represent the sections which are similar in both masks and the ones qhich differ between masks"""
        self.parent.helpText += self.getDefaultModuleDocumentationLink()
        self.parent.acknowledgementText = """Universidad Carlos III"""


#
# MyModule WIDGET: Define graphical interface of the module
#

class MyModuleWidget(ScriptedLoadableModuleWidget):

    def setup(self):
        ScriptedLoadableModuleWidget.setup(self)

        self.logic = MyModuleLogic()

        # ------ 1. CREATE LAYOUT AND BUTTONS ------

        # Layout setup: 3D Only
        self.layoutManager = slicer.app.layoutManager()
        self.layoutManager.setLayout(slicer.vtkMRMLLayoutNode.SlicerLayoutOneUp3DView)

        #
        # LOAD DATA
        #

        # Create layout
        collapsibleButtonLoad = ctk.ctkCollapsibleButton()
        collapsibleButtonLoad.text = "LOAD DATA"  # title for layout
        self.layout.addWidget(collapsibleButtonLoad)
        formLayout_load = qt.QFormLayout(collapsibleButtonLoad)

        # Button to load model 1
        self.loadModel1Button = qt.QPushButton("LOAD MODEL 1")  # text in button
        self.loadModel1Button.toolTip = "Load model 1"  # hint text for button (appears when cursor is above the button for more than one second)
        self.loadModel1Button.enabled = True  # if True it can be clicked
        formLayout_load.addRow(self.loadModel1Button)  # include button in layout

        # Button to load model 2
        self.loadModel2Button = qt.QPushButton("LOAD MODEL 2")  # text in button
        self.loadModel2Button.toolTip = "Load model 2"  # hint text for button (appears when cursor is above the button for more than one second)
        self.loadModel2Button.enabled = True  # if True it can be clicked
        formLayout_load.addRow(self.loadModel2Button)  # include button in layout

        #
        # ALIGNMENT
        #

        # Create Layout
        collapsibleButtonAlignment = ctk.ctkCollapsibleButton()
        collapsibleButtonAlignment.text = "ALIGNMENT"
        self.layout.addWidget(collapsibleButtonAlignment)
        formLayout_alignment = qt.QFormLayout(collapsibleButtonAlignment)

        # Button for masks alignment
        self.alignModelsButton = qt.QPushButton("ALIGN MODELS")  # text in button
        self.alignModelsButton.toolTip = "Align models"  # hint text for button (appears when cursor is above the button for more than one second)
        self.alignModelsButton.enabled = True
        formLayout_alignment.addRow(self.alignModelsButton)

        #       COMPARISON BETWEEN MASKS         #
        # SORENSEN-DICE COEFFICIENT & HOUSDORFF DISTANCE BUTTONS
        #

        # Create layout
        collapsibleButtonComparison = ctk.ctkCollapsibleButton()
        collapsibleButtonComparison.text = "COMPARISON"  # title for layout
        self.layout.addWidget(collapsibleButtonComparison)
        formLayout_comparison = qt.QFormLayout(collapsibleButtonComparison)

        # Button to obtain the Sorensen-Dice Coefficient
        self.diceCoeffButton = qt.QPushButton("SORENSEN-DICE COEFFICIENT")  # text in button
        self.diceCoeffButton.toolTip = "Sorensen-Dice Coefficient"  # hint text for button (appears when the cursor is above the button for more than one second)
        self.diceCoeffButton.enabled = True  # if true it can be clicked
        formLayout_comparison.addRow(self.diceCoeffButton)  # include button in layout

        #Button to obtain the Hausdorff Distance
        self.hausDistButton = qt.QPushButton("HAUSDORFF DISTANCE") # text in button
        self.hausDistButton.toolTip = qt.QPushButton("Hausdorff Distance") # hint text for button (appears when the cursor is above the button for more than a second)
        self.hausDistButton.enabled = True # if true it can be clicked
        formLayout_comparison.addRow(self.hausDistButton) # include button in layout

        #
        # VISUALIZATION
        #

        # Create layout
        collapsibleButtonVisualization = ctk.ctkCollapsibleButton()
        collapsibleButtonVisualization.text = "VISUALIZATION"  # title for layout
        self.layout.addWidget(collapsibleButtonVisualization)
        formLayout_visualization = qt.QFormLayout(collapsibleButtonVisualization)

        #
        # Model visibility layout
        #

        # Create collapsible button inside layout
        modelVisibility_GroupBox = ctk.ctkCollapsibleGroupBox()
        modelVisibility_GroupBox.setTitle("MODEL VISIBILITY")  # title for collapsible button
        modelVisibility_GroupBox.collapsed = False  # if True it appears collapsed
        formLayout_visualization.addRow(modelVisibility_GroupBox)  # add collapsible button to layout

        # Create layout inside collapsible button
        modelVisibility_GroupBox_Layout = qt.QFormLayout(modelVisibility_GroupBox)

        # Create horizontal section
        modelVisibilityLayout_1 = qt.QHBoxLayout()
        modelVisibility_GroupBox_Layout.addRow(modelVisibilityLayout_1)  # insert section in current layout
        modelVisibilityLayout_2 = qt.QHBoxLayout()
        modelVisibility_GroupBox_Layout.addRow(modelVisibilityLayout_2)  # insert section in current layout

        # Show or Hide Model 1 in 3D scene
        self.model1_checkBox = qt.QCheckBox('Model 1')  # text in checkbox
        self.model1_checkBox.checked = True  # if True it is initially checked
        self.model1_checkBox.enabled = True  # if True it can be checked
        modelVisibilityLayout_1.addWidget(self.model1_checkBox)  # add checkbox to layout

        # Show or Hide Model 2 in 3D scene
        self.model2_checkBox = qt.QCheckBox('Model 2')  # text in checkbox
        self.model2_checkBox.checked = True  # if True it is initially checked
        self.model2_checkBox.checked = True  # if True it can be checked
        modelVisibilityLayout_2.addWidget(self.model2_checkBox)  # add checkbox to layout

        #
        # Model transparency layout
        #

        # Create collapsible button inside layout
        modelOpacity_GroupBox = ctk.ctkCollapsibleGroupBox()
        modelOpacity_GroupBox.setTitle("MODEL OPACITY")  # title for collapsible button
        modelOpacity_GroupBox.collapsed = False  # if True it appears collapsed
        formLayout_visualization.addRow(modelOpacity_GroupBox)  # add collapsible button to layout

        # Create layout inside collapsible button
        modelOpacity_GroupBox_Layout = qt.QFormLayout(modelOpacity_GroupBox)

        # Create an opacity Value Slider - Model 1
        self.opacityValueSliderWidget_1 = ctk.ctkSliderWidget()
        self.opacityValueSliderWidget_1.singleStep = 5  # step for range of values to be selected
        self.opacityValueSliderWidget_1.minimum = 0  # minimum value
        self.opacityValueSliderWidget_1.maximum = 100  # maximum value
        self.opacityValueSliderWidget_1.value = 100  # initial value
        modelOpacity_GroupBox_Layout.addRow("[%]: ", self.opacityValueSliderWidget_1)  # add slider to layout

        # Create an opacity Value Slider - Model 2
        self.opacityValueSliderWidget_2 = ctk.ctkSliderWidget()
        self.opacityValueSliderWidget_2.singleStep = 5  # step for range of values to be selected
        self.opacityValueSliderWidget_2.minimum = 0  # minimum value
        self.opacityValueSliderWidget_2.maximum = 100  # maximum value
        self.opacityValueSliderWidget_2.value = 100  # initial value
        modelOpacity_GroupBox_Layout.addRow("[%]: ", self.opacityValueSliderWidget_2)  # add slider to layout

        #
        # COLOR MAP
        #
        collapsibleButtonColorMap = ctk.ctkCollapsibleButton()
        collapsibleButtonColorMap.text = "COLOR MAP"
        self.layout.addWidget(collapsibleButtonColorMap)
        formLayout_colorMap = qt.QFormLayout(collapsibleButtonColorMap)

        self.showColorMapButton = qt.QPushButton("SHOW COLOR MAP")  # text in button
        self.showColorMapButton.toolTip = "Align models"  # hint text for button (appears when cursor is above the button for more than one second)
        self.showColorMapButton.enabled = True
        formLayout_colorMap.addRow(self.showColorMapButton)

        # Add vertical spacing
        self.layout.addStretch(1)

        # ------ 2. CONNECT BUTTONS WITH FUNCTIONS ------

        # Connect each button with a function
        self.loadModel1Button.connect('clicked(bool)',
                                      self.onLoadModel1Button)  # when the button is pressed we call the function onLoadModel1Button
        self.loadModel2Button.connect('clicked(bool)',
                                      self.onLoadModel2Button)  # when the button is pressed we call the function onLoadModel2Button

        self.model1_checkBox.connect('stateChanged(int)', self.onModel1VisibilityChecked)
        self.model2_checkBox.connect('stateChanged(int)', self.onModel2VisibilityChecked)

        self.opacityValueSliderWidget_1.connect("valueChanged(double)", self.onOpacityValueSliderWidget1Changed)
        self.opacityValueSliderWidget_2.connect("valueChanged(double)", self.onOpacityValueSliderWidget2Changed)

        #self.applyTransformButton.connect('clicked(bool)', self.onApplyTransformButton)
        #self.undoTransformButton.connect('clicked(bool)', self.onUndoTransformButton)

        self.diceCoeffButton.connect('clicked(bool)', self.onDiceCoeffButton)
        self.hausDistButton.connect('clicked(bool)', self.onHausdorffDistButton)

    # ------ 3. DEFINITION OF FUNCTIONS CALLED WHEN PRESSING THE BUTTONS ------

    def onLoadModel1Button(self):
        self.logic.loadModel1Button()

    def onLoadModel2Button(self):
        self.logic.loadModel2Button()

    def onModel1VisibilityChecked(self, checked):
        self.logic.model1VisibilityChecked(checked)

    def onModel2VisibilityChecked(self, checked):
        self.logic.model2VisibilityChecked(checked)

    def onOpacityValueSliderWidget1Changed(self, opacityValue):
        self.logic.opacityValueSliderWidget1Changed(opacityValue)

    def onOpacityValueSliderWidget2Changed(self, opacityValue):
        self.logic.opacityValueSliderWidget2Changed(opacityValue)

    def onUndoTransformButton(self):
        self.logic.undoTransform()

    def onDiceCoeffButton(self):
        self.logic.diceCoeff()

    def onHausdorffDistButton(self):
        self.logic.hausdorffDist()

#
# MyModule LOGIC: Definition of the logic in the module
#

class MyModuleLogic(ScriptedLoadableModuleLogic):

    def __init__(self):

        self.applyTransformButton = qt.QPushButton("Apply transform")
        self.undoTransformButton = qt.QPushButton("Undo Transform")
        print('')

        self.model1 = None
        self.model2 = None

    def loadModelFromFile(self, modelFilePath, modelFileName, colorRGB_array, visibility_bool):

        try:
            node = slicer.util.getNode(modelFileName)
        except:
            [success, node] = slicer.util.loadSegmentation(modelFilePath + '/' + modelFileName + '.stl', returnNode=True) # model loading as segment
            if success:
                node.GetDisplayNode().SetColor(colorRGB_array)
                node.GetDisplayNode().SetVisibility(visibility_bool)
                print(modelFileName + ' model loaded')
            else:
                print('ERROR: ' + modelFileName + ' model not found in path')
        return node

    def updateVisibility(self, modelNode, show):

        if show:
            modelNode.GetDisplayNode().SetVisibility(1)  # show
        else:
            modelNode.GetDisplayNode().SetVisibility(0)  # hide

    def updateModelOpacity(self, inputModel, opacityValue_norm):

        inputModel.GetDisplayNode().SetOpacity(opacityValue_norm)

    def loadModel1Button(self):

        model_name = 'Liver1'  # indicate name of model to be loaded
        data_path = slicer.modules.mymodule.path.replace("MyModule.py",
                                                         "") + 'Data/'  # indicate the path from which we want to load the model
        self.loadModelFromFile(data_path, model_name, [1, 0, 0], True)  # call function from logic
        model1 = slicer.util.getNode('Liver1')  # retrieve Model1
        self.model1 = model1

    def loadModel2Button(self):

        model_name = 'Liver1beforeMM'  # indicate name of model to be loaded
        data_path = slicer.modules.mymodule.path.replace("MyModule.py",
                                                         "") + 'Data/'  # indicate the path from which we want to load the model
        self.loadModelFromFile(data_path, model_name, [1, 0, 0], True)  # call function from logic
        model2 = slicer.util.getNode('Liver1beforeMM')  # retrieve Model2
        self.model2 = model2

    def model1VisibilityChecked(self,checked):

        model1 = slicer.util.getNode('Liver1')
        self.updateVisibility(model1, checked)

    def model2VisibilityChecked(self,checked):

        model2 = slicer.util.getNode('Liver1beforeMM')
        self.updateVisibility(model2, checked)

    def opacityValueSliderWidget1Changed(self, opacityValue):

        model1 = slicer.util.getNode('Liver1')  # retrieve Model1

        # Get opacity value and normalize it to get values in [0,100]
        opacityValue_norm = opacityValue / 100.0
        print(opacityValue_norm)

        self.updateModelOpacity(model1, opacityValue_norm)  # Update model opacity

    def opacityValueSliderWidget2Changed(self, opacityValue):

        model2 = slicer.util.getNode('Liver1beforeMM')  # retrieve Model2

        # Get opacity value and normalize it to get values in [0,100]
        opacityValue_norm = opacityValue / 100.0
        print(opacityValue_norm)

        self.updateModelOpacity(model2, opacityValue_norm)  # Update model opacity

    def diceCoeff(self):

        # Load model 1 (When opening it I open it as a segment (Have a look in LoadModelFromFile function))
        model1 = slicer.util.getNode('Liver1')
        slicer.mrmlScene.AddNode(model1)

        # Load model 2 (When opening it I open it as a segment (Have a look in LoadModelFromFile function))
        model2 = slicer.util.getNode('Liver1beforeMM')
        slicer.mrmlScene.AddNode(model2)

        # Creation of a node for segments comparison
        self.segCompNode = slicer.vtkMRMLSegmentComparisonNode()
        slicer.mrmlScene.AddNode(self.segCompNode)
        slicer.modules.segmentcomparison.logic().SetMRMLScene(slicer.mrmlScene)

        # Loading of the segmentation node and the first segmentation
        self.segCompNode.SetAndObserveReferenceSegmentationNode(model1)
        self.segCompNode.SetReferenceSegmentID('Liver1')

        # Loading of the segmentation node and the segmentation of comparison
        self.segCompNode.SetAndObserveCompareSegmentationNode(model2)
        self.segCompNode.SetCompareSegmentID('Liver1beforeMM')

        # Creation and configuration of a table node where the results will be shown
        self.tableD = slicer.vtkMRMLTableNode()
        self.tableD.SetName("Sorensen-Dice Coefficient")
        slicer.mrmlScene.AddNode(self.tableD)
        self.segCompNode.SetAndObserveDiceTableNode(self.tableD)

        # Calculation of the Dice Index
        slicer.modules.segmentcomparison.logic().ComputeDiceStatistics(self.segCompNode)


    def hausdorffDist(self):

        # Load model 1 (When opening it I open it as a segment (Have a look in LoadModelFromFile function))
        model1 = slicer.util.getNode('Liver1')
        slicer.mrmlScene.AddNode(model1)

        # Load model 2 (When opening it I open it as a segment (Have a look in LoadModelFromFile function))
        model2 = slicer.util.getNode('Liver1beforeMM')
        slicer.mrmlScene.AddNode(model2)

        # Creation of a node for segments comparison
        self.segCompnode = slicer.vtkMRMLSegmentComparisonNode()
        slicer.mrmlScene.AddNode(self.segCompnode)
        slicer.modules.segmentcomparison.logic().SetMRMLScene(slicer.mrmlScene)

        # Loading of the segmentation node and the first segmentation
        self.segCompnode.SetAndObserveReferenceSegmentationNode(model1)
        self.segCompnode.SetReferenceSegmentID('Liver1')

        # Loading of the segmentation node and the segmentation of comparison
        self.segCompnode.SetAndObserveCompareSegmentationNode(model2)
        self.segCompnode.SetCompareSegmentID('Liver1beforeMM')

        # Creation and configuration of a table node where the results will be shown
        self.tableH = slicer.vtkMRMLTableNode()
        self.tableH.SetName("Hausdorff Distance")
        slicer.mrmlScene.AddNode(self.tableH)
        self.segCompnode.SetAndObserveHausdorffTableNode(self.tableH)

        # Calculation of the Hausdorff Distance
        slicer.modules.segmentcomparison.logic().ComputeHausdorffDistances(self.segCompnode)


