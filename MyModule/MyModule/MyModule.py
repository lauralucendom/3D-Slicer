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

        # Model 1 Selector
        self.model1_pathSelector = ctk.ctkPathLineEdit()
        self.model1_pathSelector.enabled = True
        self.model1_pathSelector.setMaximumWidth(400)
        self.model1_pathSelector.currentPath = slicer.modules.mymodule.path.replace("MyModule.py","") + 'Data/Liver1.stl' 
        formLayout_load.addRow("Model 1: ", self.model1_pathSelector)    

        # Model 1 Selector
        self.model2_pathSelector = ctk.ctkPathLineEdit()
        self.model2_pathSelector.enabled = True
        self.model2_pathSelector.setMaximumWidth(400)
        self.model2_pathSelector.currentPath = slicer.modules.mymodule.path.replace("MyModule.py","") + 'Data/Liver1beforeMM.stl' 
        formLayout_load.addRow("Model 2: ", self.model2_pathSelector)    

        # Button to load models
        self.loadModelsButton = qt.QPushButton("LOAD MODELS AS SEGMENTS")  # text in button
        self.loadModelsButton.toolTip = "Load models as segments"  # hint text for button (appears when cursor is above the button for more than one second)
        self.loadModelsButton.enabled = True  # if True it can be clicked
        formLayout_load.addRow(self.loadModelsButton)  # include button in layout

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
        
        # Show or Hide Model 1 in 3D scene
        self.model1_checkBox = qt.QCheckBox('Model 1')  # text in checkbox
        self.model1_checkBox.checked = True  # if True it is initially checked
        self.model1_checkBox.enabled = True  # if True it can be checked
        modelVisibilityLayout_1.addWidget(self.model1_checkBox)  # add checkbox to layout

        # Show or Hide Model 2 in 3D scene
        self.model2_checkBox = qt.QCheckBox('Model 2')  # text in checkbox
        self.model2_checkBox.checked = True  # if True it is initially checked
        self.model2_checkBox.checked = True  # if True it can be checked
        modelVisibilityLayout_1.addWidget(self.model2_checkBox)  # add checkbox to layout

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
        self.loadModelsButton.connect('clicked(bool)',
                                      self.onLoadModelsButton)  # when the button is pressed we call the function onLoadModel1Button

        self.model1_checkBox.connect('stateChanged(int)', self.onModel1VisibilityChecked)
        self.model2_checkBox.connect('stateChanged(int)', self.onModel2VisibilityChecked)

        self.opacityValueSliderWidget_1.connect("valueChanged(double)", self.onOpacityValueSliderWidget1Changed)
        self.opacityValueSliderWidget_2.connect("valueChanged(double)", self.onOpacityValueSliderWidget2Changed)

        self.alignModelsButton.connect('clicked(bool)', self.onAlignModelsButton)

        self.diceCoeffButton.connect('clicked(bool)', self.onDiceCoeffButton)
        self.hausDistButton.connect('clicked(bool)', self.onHausdorffDistButton)

    # ------ 3. DEFINITION OF FUNCTIONS CALLED WHEN PRESSING THE BUTTONS ------

    def onLoadModelsButton(self):

        # Get inputs
        self.logic.model1_path = self.model1_pathSelector.currentPath
        self.logic.model2_path = self.model2_pathSelector.currentPath
            
        # Load models as segments
        success = self.logic.loadModels()

        # Update GUI
        if success: # if models are loaded correctly, then button and selectors are disabled
            self.model1_pathSelector.enabled = False
            self.model2_pathSelector.enabled = False
            self.loadModelsButton.enabled = False

    def onModel1VisibilityChecked(self, checked):
        self.logic.model1VisibilityChecked(checked)

    def onModel2VisibilityChecked(self, checked):
        self.logic.model2VisibilityChecked(checked)

    def onOpacityValueSliderWidget1Changed(self, opacityValue):
        self.logic.opacityValueSliderWidget1Changed(opacityValue)

    def onOpacityValueSliderWidget2Changed(self, opacityValue):
        self.logic.opacityValueSliderWidget2Changed(opacityValue)

    def onAlignModelsButton(self):
        
        # Align models
        self.logic.alignModels()

        # Update GUI
        self.alignModelsButton.enabled = False

    def onDiceCoeffButton(self):
        self.logic.diceCoeff()

    def onHausdorffDistButton(self):
        self.logic.hausdorffDist()

#
# MyModule LOGIC: Definition of the logic in the module
#

class MyModuleLogic(ScriptedLoadableModuleLogic):

    def __init__(self):

        # Model paths
        self.model1_path = ''
        self.model2_path = ''

        self.applyTransformButton = qt.QPushButton("Apply transform")
        self.undoTransformButton = qt.QPushButton("Undo Transform")
        print('')

        self.model1 = None
        self.model2 = None

    def loadModelFromFile(self, modelFilePath, colorRGB_array, visibility_bool):
        
        [success, node] = slicer.util.loadSegmentation(modelFilePath, returnNode=True) # model loading as segment
        if success:
            node.GetDisplayNode().SetColor(colorRGB_array)
            node.GetDisplayNode().SetVisibility(visibility_bool)
            print(node.GetName() + ' model loaded')
        else:
            print('ERROR: model not found in path')
        return (success, node)

    def updateVisibility(self, modelNode, show):

        if show:
            modelNode.GetDisplayNode().SetVisibility(1)  # show
        else:
            modelNode.GetDisplayNode().SetVisibility(0)  # hide

    def updateSegmentOpacity(self, inputModel, opacityValue_norm):

        inputModel.GetDisplayNode().SetOpacity3D(opacityValue_norm)

    def loadModels(self):

        # Model 1
        [success1, self.model1] = self.loadModelFromFile(self.model1_path, [1, 0, 0], True)  # call function from logic
        
        # Model 2
        [success2, self.model2] = self.loadModelFromFile(self.model2_path, [0, 1, 0], True)  # call function from logic

        # Center 3D view
        layoutManager = slicer.app.layoutManager()
        threeDWidget = layoutManager.threeDWidget(0)
        threeDView = threeDWidget.threeDView()
        threeDView.resetFocalPoint() 
        
        return (success1 and success2)

    def alignModels(self):

        # Rotation
        self.alignmentTransform = slicer.vtkMRMLLinearTransformNode()
        self.alignmentTransform.SetName("alignmentTransform")
        slicer.mrmlScene.AddNode(self.alignmentTransform)

        # Create transformation matrix
        rotMatrix = vtk.vtkTransform()
        rotMatrix.RotateZ(-180.0) 
        self.alignmentTransform.SetMatrixTransformToParent(rotMatrix.GetMatrix())

        # Build transform tree
        self.model2.SetAndObserveTransformNodeID(self.alignmentTransform.GetID())

        # Harden transform
        self.model2.HardenTransform()

        # Delete transform from scene
        slicer.mrmlScene.RemoveNode(self.alignmentTransform)
        
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

        self.updateSegmentOpacity(model1, opacityValue_norm)  # Update model opacity

    def opacityValueSliderWidget2Changed(self, opacityValue):

        model2 = slicer.util.getNode('Liver1beforeMM')  # retrieve Model2

        # Get opacity value and normalize it to get values in [0,100]
        opacityValue_norm = opacityValue / 100.0
        print(opacityValue_norm)

        self.updateSegmentOpacity(model2, opacityValue_norm)  # Update model opacity

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


