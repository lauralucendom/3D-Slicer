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

        # Segment 1 Selector
        self.segment1_pathSelector = ctk.ctkPathLineEdit()
        self.segment1_pathSelector.enabled = True
        self.segment1_pathSelector.setMaximumWidth(400)
        self.segment1_pathSelector.currentPath = slicer.modules.mymodule.path.replace("MyModule.py","") + 'Data/Liver1.stl' 
        formLayout_load.addRow("Segment 1: ", self.segment1_pathSelector)    

        # Segment 1 Selector
        self.segment2_pathSelector = ctk.ctkPathLineEdit()
        self.segment2_pathSelector.enabled = True
        self.segment2_pathSelector.setMaximumWidth(400)
        self.segment2_pathSelector.currentPath = slicer.modules.mymodule.path.replace("MyModule.py","") + 'Data/Liver1beforeMM.stl' 
        formLayout_load.addRow("Segment 2: ", self.segment2_pathSelector)    

        # Button to load segments
        self.loadSegmentsButton = qt.QPushButton("LOAD MODELS AS SEGMENTS")  # text in button
        self.loadSegmentsButton.toolTip = "Load segments as segments"  # hint text for button (appears when cursor is above the button for more than one second)
        self.loadSegmentsButton.enabled = True  # if True it can be clicked
        formLayout_load.addRow(self.loadSegmentsButton)  # include button in layout

        #
        # ALIGNMENT
        #

        # Create Layout
        collapsibleButtonAlignment = ctk.ctkCollapsibleButton()
        collapsibleButtonAlignment.text = "ALIGNMENT"
        self.layout.addWidget(collapsibleButtonAlignment)
        formLayout_alignment = qt.QFormLayout(collapsibleButtonAlignment)

        # Button for masks alignment
        self.alignSegmentsButton = qt.QPushButton("ALIGN MODELS")  # text in button
        self.alignSegmentsButton.toolTip = "Align segments"  # hint text for button (appears when cursor is above the button for more than one second)
        self.alignSegmentsButton.enabled = True
        formLayout_alignment.addRow(self.alignSegmentsButton)

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
        # Segment visibility layout
        #

        # Create collapsible button inside layout
        segmentVisibility_GroupBox = ctk.ctkCollapsibleGroupBox()
        segmentVisibility_GroupBox.setTitle("MODEL VISIBILITY")  # title for collapsible button
        segmentVisibility_GroupBox.collapsed = False  # if True it appears collapsed
        formLayout_visualization.addRow(segmentVisibility_GroupBox)  # add collapsible button to layout

        # Create layout inside collapsible button
        segmentVisibility_GroupBox_Layout = qt.QFormLayout(segmentVisibility_GroupBox)

        # Create horizontal section
        segmentVisibilityLayout_1 = qt.QHBoxLayout()
        segmentVisibility_GroupBox_Layout.addRow(segmentVisibilityLayout_1)  # insert section in current layout
        
        # Show or Hide Segment 1 in 3D scene
        self.segment1_checkBox = qt.QCheckBox('Segment 1')  # text in checkbox
        self.segment1_checkBox.checked = True  # if True it is initially checked
        self.segment1_checkBox.enabled = True  # if True it can be checked
        segmentVisibilityLayout_1.addWidget(self.segment1_checkBox)  # add checkbox to layout

        # Show or Hide Segment 2 in 3D scene
        self.segment2_checkBox = qt.QCheckBox('Segment 2')  # text in checkbox
        self.segment2_checkBox.checked = True  # if True it is initially checked
        self.segment2_checkBox.checked = True  # if True it can be checked
        segmentVisibilityLayout_1.addWidget(self.segment2_checkBox)  # add checkbox to layout

        #
        # Segment transparency layout
        #

        # Create collapsible button inside layout
        segmentOpacity_GroupBox = ctk.ctkCollapsibleGroupBox()
        segmentOpacity_GroupBox.setTitle("MODEL OPACITY")  # title for collapsible button
        segmentOpacity_GroupBox.collapsed = False  # if True it appears collapsed
        formLayout_visualization.addRow(segmentOpacity_GroupBox)  # add collapsible button to layout

        # Create layout inside collapsible button
        segmentOpacity_GroupBox_Layout = qt.QFormLayout(segmentOpacity_GroupBox)

        # Create an opacity Value Slider - Segment 1
        self.opacityValueSliderWidget_1 = ctk.ctkSliderWidget()
        self.opacityValueSliderWidget_1.singleStep = 5  # step for range of values to be selected
        self.opacityValueSliderWidget_1.minimum = 0  # minimum value
        self.opacityValueSliderWidget_1.maximum = 100  # maximum value
        self.opacityValueSliderWidget_1.value = 100  # initial value
        segmentOpacity_GroupBox_Layout.addRow("[%]: ", self.opacityValueSliderWidget_1)  # add slider to layout

        # Create an opacity Value Slider - Segment 2
        self.opacityValueSliderWidget_2 = ctk.ctkSliderWidget()
        self.opacityValueSliderWidget_2.singleStep = 5  # step for range of values to be selected
        self.opacityValueSliderWidget_2.minimum = 0  # minimum value
        self.opacityValueSliderWidget_2.maximum = 100  # maximum value
        self.opacityValueSliderWidget_2.value = 100  # initial value
        segmentOpacity_GroupBox_Layout.addRow("[%]: ", self.opacityValueSliderWidget_2)  # add slider to layout

        #
        # COLOR MAP
        #
        collapsibleButtonColorMap = ctk.ctkCollapsibleButton()
        collapsibleButtonColorMap.text = "COLOR MAP"
        self.layout.addWidget(collapsibleButtonColorMap)
        formLayout_colorMap = qt.QFormLayout(collapsibleButtonColorMap)

        self.showColorMapButton = qt.QPushButton("SHOW COLOR MAP")  # text in button
        self.showColorMapButton.toolTip = "Align segments"  # hint text for button (appears when cursor is above the button for more than one second)
        self.showColorMapButton.enabled = True
        formLayout_colorMap.addRow(self.showColorMapButton)

        # Add vertical spacing
        self.layout.addStretch(1)

        # ------ 2. CONNECT BUTTONS WITH FUNCTIONS ------

        # Connect each button with a function
        self.loadSegmentsButton.connect('clicked(bool)',
                                      self.onloadSegmentsButton)  # when the button is pressed we call the function onLoadSegment1Button

        self.segment1_checkBox.connect('stateChanged(int)', self.onupdateSegment1Visibility)
        self.segment2_checkBox.connect('stateChanged(int)', self.onupdateSegment2Visibility)

        self.opacityValueSliderWidget_1.connect("valueChanged(double)", self.onupdateSegment1Opacity)
        self.opacityValueSliderWidget_2.connect("valueChanged(double)", self.onupdateSegment2Opacity)

        self.alignSegmentsButton.connect('clicked(bool)', self.onAlignSegmentsButton)

        self.diceCoeffButton.connect('clicked(bool)', self.onDiceCoeffButton)
        self.hausDistButton.connect('clicked(bool)', self.onHausdorffDistButton)

    # ------ 3. DEFINITION OF FUNCTIONS CALLED WHEN PRESSING THE BUTTONS ------

    def onloadSegmentsButton(self):

        # Get inputs
        self.logic.segment1_path = self.segment1_pathSelector.currentPath
        self.logic.segment2_path = self.segment2_pathSelector.currentPath
            
        # Load segments as segments
        success = self.logic.loadSegments()

        # Update GUI
        if success: # if segments are loaded correctly, then button and selectors are disabled
            self.segment1_pathSelector.enabled = False
            self.segment2_pathSelector.enabled = False
            self.loadSegmentsButton.enabled = False

    def onupdateSegment1Visibility(self, checked):
        self.logic.updateSegment1Visibility(checked)

    def onupdateSegment2Visibility(self, checked):
        self.logic.updateSegment2Visibility(checked)

    def onupdateSegment1Opacity(self, opacityValue):
        self.logic.updateSegment1Opacity(opacityValue)

    def onupdateSegment2Opacity(self, opacityValue):
        self.logic.updateSegment2Opacity(opacityValue)

    def onAlignSegmentsButton(self):
        
        # Align segments
        self.logic.alignSegments()

        # Update GUI
        self.alignSegmentsButton.enabled = False

    def onDiceCoeffButton(self):
        self.logic.diceCoeff()

    def onHausdorffDistButton(self):
        self.logic.hausdorffDist()

#
# MyModule LOGIC: Definition of the logic in the module
#

class MyModuleLogic(ScriptedLoadableModuleLogic):

    def __init__(self):

        # Segment paths
        self.segment1_path = ''
        self.segment2_path = ''

        # Segments
        self.segment1 = None
        self.segment2 = None

    def loadSegmentFromFile(self, segmentFilePath, colorRGB_array, visibility_bool):
        
        [success, node] = slicer.util.loadSegmentation(segmentFilePath, returnNode=True) # segment loading as segment
        if success:
            node.GetDisplayNode().SetColor(colorRGB_array)
            node.GetDisplayNode().SetVisibility(visibility_bool)
            print(node.GetName() + ' segment loaded')
        else:
            print('ERROR: segment not found in path')
        return (success, node)

    def updateVisibility(self, segmentNode, show):

        if show:
            segmentNode.GetDisplayNode().SetVisibility(1)  # show
        else:
            segmentNode.GetDisplayNode().SetVisibility(0)  # hide

    def updateSegmentOpacity(self, inputSegment, opacityValue_norm):

        inputSegment.GetDisplayNode().SetOpacity3D(opacityValue_norm)

    def loadSegments(self):

        # Segment 1
        [success1, self.segment1] = self.loadSegmentFromFile(self.segment1_path, [1, 0, 0], True)  # call function from logic
        
        # Segment 2
        [success2, self.segment2] = self.loadSegmentFromFile(self.segment2_path, [0, 1, 0], True)  # call function from logic

        # Center 3D view
        layoutManager = slicer.app.layoutManager()
        threeDWidget = layoutManager.threeDWidget(0)
        threeDView = threeDWidget.threeDView()
        threeDView.resetFocalPoint() 
        
        return (success1 and success2)

    def alignSegments(self):

        # Rotation
        self.alignmentTransform = slicer.vtkMRMLLinearTransformNode()
        self.alignmentTransform.SetName("alignmentTransform")
        slicer.mrmlScene.AddNode(self.alignmentTransform)

        # Create transformation matrix
        rotMatrix = vtk.vtkTransform()
        rotMatrix.RotateZ(-180.0) 
        self.alignmentTransform.SetMatrixTransformToParent(rotMatrix.GetMatrix())

        # Build transform tree
        self.segment2.SetAndObserveTransformNodeID(self.alignmentTransform.GetID())

        # Harden transform
        self.segment2.HardenTransform()

        # Delete transform from scene
        slicer.mrmlScene.RemoveNode(self.alignmentTransform)
        
    def updateSegment1Visibility(self,checked):

        self.updateVisibility(self.segment1, checked)

    def updateSegment2Visibility(self,checked):

        self.updateVisibility(self.segment2, checked)

    def updateSegment1Opacity(self, opacityValue):

        # Get opacity value and normalize it to get values in [0,100]
        opacityValue_norm = opacityValue / 100.0
        print(opacityValue_norm)

        self.updateSegmentOpacity(self.segment1, opacityValue_norm)  # Update segment opacity

    def updateSegment2Opacity(self, opacityValue):

        # Get opacity value and normalize it to get values in [0,100]
        opacityValue_norm = opacityValue / 100.0
        print(opacityValue_norm)

        self.updateSegmentOpacity(self.segment2, opacityValue_norm)  # Update segment opacity

    def diceCoeff(self):

        # Creation of a node for segments comparison
        self.segCompNode = slicer.vtkMRMLSegmentComparisonNode()
        slicer.mrmlScene.AddNode(self.segCompNode)
        slicer.modules.segmentcomparison.logic().SetMRMLScene(slicer.mrmlScene)

        # Loading of the segmentation node and the first segmentation
        self.segCompNode.SetAndObserveReferenceSegmentationNode(self.segment1)
        self.segCompNode.SetReferenceSegmentID(self.segment1.GetName())

        # Loading of the segmentation node and the segmentation of comparison
        self.segCompNode.SetAndObserveCompareSegmentationNode(self.segment2)
        self.segCompNode.SetCompareSegmentID(self.segment2.GetName())

        # Creation and configuration of a table node where the results will be shown
        self.tableD = slicer.vtkMRMLTableNode()
        self.tableD.SetName("Sorensen-Dice Coefficient")
        slicer.mrmlScene.AddNode(self.tableD)
        self.segCompNode.SetAndObserveDiceTableNode(self.tableD)
        
        # Display Dice Coefficient Table (3D Table View)
        slicer.app.layoutManager().setLayout(slicer.vtkMRMLLayoutNode.SlicerLayout3DTableView)
        slicer.app.applicationLogic().GetSelectionNode().SetReferenceActiveTableID(self.tableD.GetID())
        slicer.app.applicationLogic().PropagateTableSelection()

        # Calculation of the Dice Index
        slicer.modules.segmentcomparison.logic().ComputeDiceStatistics(self.segCompNode)
        
        # Save table in a CSV file
        storagenode = self.tableD.CreateDefaultStorageNode()
        storagenode.SetFileName("dice.csv")
        storagenode.WriteData(self.tableD)



    def hausdorffDist(self):

        # Creation of a node for segments comparison
        self.segCompnode = slicer.vtkMRMLSegmentComparisonNode()
        slicer.mrmlScene.AddNode(self.segCompnode)
        slicer.modules.segmentcomparison.logic().SetMRMLScene(slicer.mrmlScene)

        # Loading of the segmentation node and the first segmentation
        self.segCompnode.SetAndObserveReferenceSegmentationNode(self.segment1)
        self.segCompnode.SetReferenceSegmentID(self.segment1.GetName())

        # Loading of the segmentation node and the segmentation of comparison
        self.segCompnode.SetAndObserveCompareSegmentationNode(self.segment2)
        self.segCompnode.SetCompareSegmentID(self.segment2.GetName())

        # Creation and configuration of a table node where the results will be shown
        self.tableH = slicer.vtkMRMLTableNode()
        self.tableH.SetName("Hausdorff Distance")
        slicer.mrmlScene.AddNode(self.tableH)
        self.segCompnode.SetAndObserveHausdorffTableNode(self.tableH)
        
        # Display Hausdorff Distance Table (3D Table View)
        slicer.app.layoutManager().setLayout(slicer.vtkMRMLLayoutNode.SlicerLayout3DTableView)
        slicer.app.applicationLogic().GetSelectionNode().SetReferenceActiveTableID(self.tableH.GetID())
        slicer.app.applicationLogic().PropagateTableSelection()

        # Calculation of the Hausdorff Distance
        slicer.modules.segmentcomparison.logic().ComputeHausdorffDistances(self.segCompnode)
        
        # Save table in a CSV file
        storagenode = self.tableH.CreateDefaultStorageNode()
        storagenode.SetFileName("hausdorff.csv")
        storagenode.WriteData(self.tableH)
      
    def showColorMap(self):
    
        # Get PolyData from Segment 1
        self.segment1.CreateClosedSurfaceRepresentation();
        ss1 = self.segment1.GetSegmentation();
        str1 = ss1.GetNthSegmentID(0);
        pl1 = vtk.vtkPolyData()
        pl1 = self.segment1.GetClosedSurfaceRepresentation(str1)

        # Get PolyData from Segment 2
        self.segment2.CreateClosedSurfaceRepresentation();
        ss2 = self.segment2.GetSegmentation();
        str2 = ss2.GetNthSegmentID(0);
        pl2 = vtk.vtkPolyData()
        pl2 = self.segment2.GetClosedSurfaceRepresentation(str2)

        # Compute distance
        distanceFilter = vtk.vtkDistancePolyDataFilter()
        distanceFilter.SetInputData(0, pl1)
        distanceFilter.SetInputData(1, pl2)
        distanceFilter.SignedDistanceOff()
        distanceFilter.Update()

        # Center 3D view
        slicer.app.layoutManager().tableWidget(0).setVisible(False)
        layoutManager = slicer.app.layoutManager()
        threeDWidget = layoutManager.threeDWidget(0)
        threeDView = threeDWidget.threeDView()
        threeDView.resetFocalPoint()

        #Output model
        model = slicer.vtkMRMLModelNode()
        slicer.mrmlScene.AddNode(model)
        model.SetName('DistanceModelNode')
        model.SetAndObservePolyData(distanceFilter.GetOutput())
        display = slicer.vtkMRMLModelDisplayNode()
        slicer.mrmlScene.AddNode(display)
        model.SetAndObserveDisplayNodeID(display.GetID())
        display.SetActiveScalarName('Distance')
        display.SetAndObserveColorNodeID('vtkMRMLColorTableNodeFileColdToHotRainbow.txt')
        display.SetScalarVisibility(True)

        [rmin,rmax] = display.GetScalarRange()
        print(rmin)
        print(rmax)

        # Deactivate visibility of segments (deberia actualizarse el checkbox del GUI)
        self.updateSegment1Visibility(False)
        self.updateSegment2Visibility(False)




