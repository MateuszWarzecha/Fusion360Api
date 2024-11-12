#Author-Autodesk Inc.
#Description-Create bolt

import adsk.core, adsk.fusion, traceback
import math

defaultName = 'Nazwa'
defaultLength = 6.85
defaultLegLength = 12.6267
defaultTopLength = 2.6
defaultDiameter = 6
var1 = 0.6
var2 = 1.4
defaultBotLength = defaultLength-defaultTopLength
defaultHoleHeight = defaultBotLength-var1
defaultTopHoleHeight = defaultBotLength-var2
defaultWyb = 'Czesc'
defaultLegNum = '3'
deg180 = math.pi
defaultHoles1 = False
defaultHoles2 = False
defaultHoles3 = False

# global set of event handlers to keep them referenced for the duration of the command
handlers = []
app = adsk.core.Application.get()
if app:
    ui = app.userInterface

newComp = None
dropdownItems = adsk.core.DropDownCommandInput.cast(None)
dropdownItems2 = adsk.core.DropDownCommandInput.cast(None)

def createNewComponent():
    # Get the active design.
    product = app.activeProduct
    design = adsk.fusion.Design.cast(product)
    rootComp = design.rootComponent
    allOccs = rootComp.occurrences
    newOcc = allOccs.addNewComponent(adsk.core.Matrix3D.create())
    return newOcc.component

def set_dropdown_2_items_for_Leg0():
    #dropdownItems2.listItems.clear()
    dropdownItems2.listItems.add('Orczyk 1', True)
    dropdownItems2.listItems.add('Orczyk 2', False)
    dropdownItems2.listItems.add('Orczyk 3', False)

class MyCommandInputChangedHandler(adsk.core.InputChangedEventHandler):
    def __init__(self):
        super().__init__()
    def notify(self, args):

        #_ui.messageBox(f"MyCommandInputChangedHandler {dropdownItems}")
        try:
            eventArgs = adsk.core.InputChangedEventArgs.cast(args)
            changedInput = eventArgs.inputs

            if dropdownItems.selectedItem.name == 'Noga0':
                dropdownItems2.isEnabled = True
                inputName.isEnabled = True
                inputLength.isVisible = True
                inputDiameter.isVisible = False
                inputLegNum.isVisible = False
                inputHole1.isVisible = False
                inputHole2.isVisible = False
                inputHole3.isVisible = False
                
            elif dropdownItems.selectedItem.name == 'Leg 1':
                dropdownItems2.isEnabled = False
                inputName.isEnabled = True
                inputLength.isVisible = False
                inputDiameter.isVisible = False
                inputLegNum.isVisible = False
                inputHole1.isVisible = False
                inputHole2.isVisible = False
                inputHole3.isVisible = False

            if dropdownItems.selectedItem.name == 'Leg 2':
                dropdownItems2.isEnabled = True
                inputName.isEnabled = True
                inputLength.isVisible = True
                inputDiameter.isVisible = False
                inputLegNum.isVisible = False
                inputHole1.isVisible = False
                inputHole2.isVisible = False
                inputHole3.isVisible = False

            elif dropdownItems.selectedItem.name == 'Body':
                dropdownItems2.isEnabled = False
                inputName.isVisible = True
                inputLength.isVisible = False
                inputDiameter.isVisible = True
                inputLegNum.isVisible = True
                inputHole1.isVisible = True
                inputHole2.isVisible = True
                inputHole3.isVisible = True

            # if inputHole1.value == True:
            #     ui.messageBox(f"Wartość Hole12: {inputHole1.value}")
     
        except:
            ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))

class BoltCommandExecuteHandler(adsk.core.CommandEventHandler):
    def __init__(self):
        super().__init__()
    def notify(self, args):
        try:
            unitsMgr = app.activeProduct.unitsManager
            command = args.firingEvent.sender
            inputs = command.commandInputs

            # eventArgs = adsk.core.CommandEventArgs.cast(args)
            if dropdownItems.selectedItem.name == 'Noga0':
                leg0 = Leg0()
                leg0.Wyb = dropdownItems2.selectedItem.name #### KOD WYKONANY PO WYBRANIU ITEM 1
                for input in inputs:
                    if input.id == 'Name':
                        leg0.Name = input.value
                    elif input.id == 'Length':
                        leg0.Length = unitsMgr.evaluateExpression(input.expression, "cm")
                    elif input.id == 'TopLength':
                        leg0.TopLength = unitsMgr.evaluateExpression(input.expression, "cm")
                    elif input.id == 'BotLength':
                        leg0.BotLength = unitsMgr.evaluateExpression(input.expression, "cm")
                    elif input.id == '2HoleHeight':
                        leg0.HoleHeight = unitsMgr.evaluateExpression(input.expression, "cm")
                    elif input.id == 'TopHoleHeight':
                        leg0.TopHoleHeight = unitsMgr.evaluateExpression(input.expression, "cm")

                leg0.buildLeg0();
                args.isValidResult = True

            elif dropdownItems.selectedItem.name == 'Leg 1':
                leg1 = Leg1()
                for input in inputs:
                    if input.id == 'Name':
                        leg1.Name = input.value
                    elif input.id == 'Length':
                        leg1.Length = unitsMgr.evaluateExpression(input.expression, "cm")
                    elif input.id == 'BotLength':
                        leg1.BotLength = unitsMgr.evaluateExpression(input.expression, "cm")

                leg1.buildLeg1();
                args.isValidResult = True

            if dropdownItems.selectedItem.name == 'Leg 2':
                leg2 = Leg2()
                leg2.Wyb = dropdownItems2.selectedItem.name
                for input in inputs:
                    if input.id == 'Name':
                        leg2.Name = input.value
                    elif input.id == 'Length':
                        leg2.Length = unitsMgr.evaluateExpression(input.expression, "cm")

                leg2.buildLeg2();
                args.isValidResult = True

            elif dropdownItems.selectedItem.name == 'Leg 3':
                leg3 = Leg3()
                for input in inputs:
                    if input.id == 'Name':
                        leg3.Name = input.value
                    elif input.id == 'Length':
                        leg3.Length = unitsMgr.evaluateExpression(input.expression, "cm")
                    elif input.id == 'BotLength':
                        leg3.BotLength = unitsMgr.evaluateExpression(input.expression, "cm")

                leg3.buildLeg3();
                args.isValidResult = True

            elif dropdownItems.selectedItem.name == 'Body':
                body = Body()
                # body.Holes1 == inputHole1.value
                # ui.messageBox(f"Wartość Hole13: {inputHole1.value}")
                #ui.messageBox(f"Wartość LegNum2: {inputLegNum.value}")
                for input in inputs:
                    if input.id == 'Name':
                        body.Name = input.value
                    elif input.id == 'legNum':
                        body.LegNumber = inputLegNum.value
                    elif input.id == 'diameter':
                        body.Diameter = unitsMgr.evaluateExpression(input.expression, "cm")
                    # elif input.id == 'checkbox1':
                    #     ui.messageBox(f"Wartość Hole14: {inputHole1.value}")
                    #     body.Holes1 == inputHole1.value

                body.buildBody();
                args.isValidResult = True

        except:
            if ui:
                ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))

class BoltCommandDestroyHandler(adsk.core.CommandEventHandler):
    def __init__(self):
        super().__init__()
    def notify(self, args):
        try:
            # when the command is done, terminate the script
            # this will release all globals which will remove all event handlers
            adsk.terminate()
        except:
            if ui:
                ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))

class BoltCommandCreatedHandler(adsk.core.CommandCreatedEventHandler):    
    def __init__(self):
        super().__init__()        
    def notify(self, args):
        try:
            cmd = args.command
            cmd.isRepeatable = False
            onExecute = BoltCommandExecuteHandler()
            cmd.execute.add(onExecute)
            onExecutePreview = BoltCommandExecuteHandler()
            cmd.executePreview.add(onExecutePreview)
            onDestroy = BoltCommandDestroyHandler()
            cmd.destroy.add(onDestroy)
            onInputChanged = MyCommandInputChangedHandler()
            cmd.inputChanged.add(onInputChanged)
            # keep the handler referenced beyond this function
            handlers.append(onExecute)
            handlers.append(onExecutePreview)
            handlers.append(onDestroy)
            handlers.append(onInputChanged)

            inputs = cmd.commandInputs

            global dropdownItems
            global dropdownItems2
            global inputName
            global inputLength
            global inputDiameter
            global inputLegNum
            global inputHole1, inputHole2, inputHole3, Hole1value

            ######## TWORZENIE INPUTA
            dropdownItems = inputs.addDropDownCommandInput('dropdown', 'Wybór części', adsk.core.DropDownStyles.TextListDropDownStyle)
            dropdownItems2 = inputs.addDropDownCommandInput('dropdown2', 'Wybór orczyka', adsk.core.DropDownStyles.TextListDropDownStyle)

            ######## DODAWANIE OPCJI DO INPUTA
            dropdownItems.listItems.add('Noga0', True)
            dropdownItems.listItems.add('Leg 1', False)
            dropdownItems.listItems.add('Leg 2', False)
            dropdownItems.listItems.add('Leg 3', False)
            dropdownItems.listItems.add('Body', False)

            set_dropdown_2_items_for_Leg0()

            #define the inputs
            inputs = cmd.commandInputs
            inputName = inputs.addStringValueInput('Name', 'Nazwa', defaultName)

            initLength = adsk.core.ValueInput.createByReal(defaultLength)
            inputLength = inputs.addValueInput('Length', 'Długość','cm',initLength)

            initDiameter = adsk.core.ValueInput.createByReal(defaultDiameter)
            inputDiameter = inputs.addValueInput('diameter', 'Średnica','cm',initDiameter)
            inputDiameter.isVisible = False

            inputLegNum = inputs.addStringValueInput('legNum','Ilość nóg',defaultLegNum)
            inputLegNum.isVisible = False

            inputHole1 = inputs.addBoolValueInput('checkbox1', 'Otwory-prądnice', True, '', defaultHoles1)
            inputHole2 = inputs.addBoolValueInput('checkbox2', 'Otwory-sterownik', True, '', defaultHoles2)
            inputHole3 = inputs.addBoolValueInput('checkbox3', 'Otwory-RPi', True, '', defaultHoles3)
            inputHole1.isVisible = False
            inputHole2.isVisible = False
            inputHole3.isVisible = False

            # ui.messageBox(f"Wartość Hole1: {inputHole1.value}")
            #ui.messageBox(f"Wartość LegNum1: {inputLegNum.value}")

            # initTopLength = adsk.core.ValueInput.createByReal(defaultTopLength)
            # inputs.addValueInput('TopLength', 'Top length', 'cm', initTopLength)

            # initLegLength = adsk.core.ValueInput.createByReal(defaultLegLength)
            # inputs.addValueInput('LegLength', 'LegLength','cm',initLegLength)

        except:
            if ui:
                ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))

class Leg0:
    def __init__(self):
        self._Name = defaultName
        self._Length = defaultLength
        self._TopLength = defaultTopLength
        self._BotLength = defaultBotLength
        self._HoleHeight = defaultHoleHeight
        self._TopHoleHeight = defaultTopHoleHeight
        self._Wyb = defaultWyb

    #properties
    @property
    def Name(self):
        return self._Name
    @Name.setter
    def Name(self, value):
        self._Name = value

    @property
    def Length(self):
        return self._Length
    @Length.setter
    def Length(self, value):
        self._Length = value

    @property
    def TopLength(self):
        return self._TopLength
    @TopLength.setter
    def TopLength(self, value):
        self._TopLength = value 

    @property
    def BotLength(self):
        return self._BotLength
    @BotLength.setter
    def BotLength(self, value):
        self._BotLength = value 

    @property
    def HoleHeight(self):
        return self._HoleHeight
    @HoleHeight.setter
    def HoleHeight(self, value):
        self._HoleHeight = value

    @property
    def TopHoleHeight(self):
        return self.TopHoleHeight
    @TopHoleHeight.setter
    def TopHoleHeight(self, value):
        self._TopHoleHeight = value

    @property
    def Wyb(self):
        return self._Wyb
    @Wyb.setter
    def Wyb(self, value):
        self._Wyb = value

    def buildLeg0(self):
        try:
            global newComp
            newComp = createNewComponent()
            if newComp is None:
                ui.messageBox('New component failed to create', 'New Component Failed')
                return
            if self._Wyb == 'Orczyk 1':
                #ui.messageBox('Część1') #### KOD WYKONANY PO WYBRANIU ITEM 1 
                design = adsk.fusion.Design.cast(app.activeProduct)
                rootComp = design.rootComponent
                sketches = rootComp.sketches
                sketch = sketches.add(rootComp.xYConstructionPlane)

                Length = self.Length
                TopLength = self.TopLength
                BotLength = Length-TopLength
                HoleHeight = BotLength-var1
                TopHoleHeight = BotLength-var2

                sketchArc = sketch.sketchCurves.sketchArcs
                sketchLine = sketch.sketchCurves.sketchLines
                sketchCircle = sketch.sketchCurves.sketchCircles
                extrudes = rootComp.features.extrudeFeatures

                #Tworzymy miejsce pod orczyk
                arcStart = adsk.core.Point3D.create(-0.55,0,0)
                arcAlong = adsk.core.Point3D.create(-0.5123,0.2,0)
                arcEnd = adsk.core.Point3D.create(-0.45,0.3162,0)
                sketchArc.addByThreePoints(arcStart,arcAlong,arcEnd)

                p1 = adsk.core.Point3D.create(-0.45,0.3162,0)
                p2 = adsk.core.Point3D.create(-0.4,1.95,0)
                sketchLine.addByTwoPoints(p1,p2)

                arcTopStart = adsk.core.Point3D.create(0,1.95,0)
                sketchArc.addByCenterStartSweep(arcTopStart,p2,-1.5708)

                #Odbicie względem osi Y
                arc2Start = adsk.core.Point3D.create(0.55,0,0)
                arc2Along = adsk.core.Point3D.create(0.5123,0.2,0)
                arc2End = adsk.core.Point3D.create(0.45,0.3162,0)
                sketchArc.addByThreePoints(arc2Start,arc2Along,arc2End)

                p3 = adsk.core.Point3D.create(0.45,0.3162,0)
                p4 = adsk.core.Point3D.create(0.4,1.95,0)
                sketchLine.addByTwoPoints(p3,p4)

                arcTopEnd = adsk.core.Point3D.create(0,1.95,0)
                sketchArc.addByCenterStartSweep(arcTopEnd,p4,1.5708)

                #Odbicie względem osi X
                arc3Start = adsk.core.Point3D.create(0.55,0,0)
                arc3Along = adsk.core.Point3D.create(0.5123,-0.2,0)
                arc3End = adsk.core.Point3D.create(0.45,-0.3162,0)
                sketchArc.addByThreePoints(arc3Start,arc3Along,arc3End)

                p5 = adsk.core.Point3D.create(0.45,-0.3162,0)
                p6 = adsk.core.Point3D.create(0.4,-1.95,0)
                sketchLine.addByTwoPoints(p5,p6)

                arcBotStart = adsk.core.Point3D.create(0,-1.95,0)
                sketchArc.addByCenterStartSweep(arcBotStart,p6,-1.5708)

                arc4Start = adsk.core.Point3D.create(-0.55,0,0)
                arc4Along = adsk.core.Point3D.create(-0.5123,-0.2,0)
                arc4End = adsk.core.Point3D.create(-0.45,-0.3162,0)
                sketchArc.addByThreePoints(arc4Start,arc4Along,arc4End)

                p7 = adsk.core.Point3D.create(-0.45,-0.3162,0)
                p8 = adsk.core.Point3D.create(-0.4,-1.95,0)
                sketchLine.addByTwoPoints(p7,p8)

                arcBotEnd = adsk.core.Point3D.create(0,-1.95,0)
                sketchArc.addByCenterStartSweep(arcBotEnd,p8,1.5708)

                #Extrudujemy miejsce pod orczyk
                prof = sketch.profiles.item(0)
                distance = adsk.core.ValueInput.createByReal(0.2)
                extrude1 = extrudes.addSimple(prof, distance, adsk.fusion.FeatureOperations.NewBodyFeatureOperation)        
                body1 = extrude1.bodies.item(0)
                body1.name = "simple"

                #Tworzymy otwór centralny
                p0 = adsk.core.Point3D.create(0,0,0)
                sketchCircle.addByCenterRadius(p0,0.45)

                #Extrudowanie otworu centralnego
                prof1 = sketch.profiles.item(0)
                distance1 = adsk.core.ValueInput.createByReal(1)
                extrude2 = extrudes.addSimple(prof1, distance1, adsk.fusion.FeatureOperations.CutFeatureOperation)        
                body2 = extrude2.bodies.item(0)
                body2.name = "simple"

                #Tworzymy zewnętrzną część nogi
                pCentRect = adsk.core.Point3D.create(1.5,TopLength,0)
                pCornRect = adsk.core.Point3D.create(-1.5,-BotLength,0)
                sketchLine.addTwoPointRectangle(pCentRect,pCornRect)

                #Extrudujemy zewnętrzną część nogi
                prof2 = sketch.profiles.item(0)
                distance2 = adsk.core.ValueInput.createByReal(0.5)
                extrude3 = extrudes.addSimple(prof2, distance2, adsk.fusion.FeatureOperations.NewBodyFeatureOperation)        
                body3 = extrude3.bodies.item(0)
                body3.name = "simple"

                #Nowy sketch
                sketch = sketches.add(rootComp.xYConstructionPlane)
                sketchArc = sketch.sketchCurves.sketchArcs
                sketchLine = sketch.sketchCurves.sketchLines
                sketchCircle = sketch.sketchCurves.sketchCircles
                extrudes = rootComp.features.extrudeFeatures

                #Tworzymy otwory w orczyku
                circleArray = [0,1,2]
                circleCenterArray = [0.9,1.35,1.8]
                for i in circleArray:
                    circleCenter = adsk.core.Point3D.create(0,circleCenterArray[i],0)
                    sketchCircle.addByCenterRadius(circleCenter,0.08)

                for i in circleArray:
                    circleCenter = adsk.core.Point3D.create(0,-circleCenterArray[i],0)
                    sketchCircle.addByCenterRadius(circleCenter,0.08)

                #Extrudujemy otwory w orczyku
                for i in range(6): 
                    prof3 = sketch.profiles.item(i)
                    distance1 = adsk.core.ValueInput.createByReal(1)
                    extrude4 = extrudes.addSimple(prof3, distance1, adsk.fusion.FeatureOperations.CutFeatureOperation)        
                    body4 = extrude4.bodies.item(0)
                    body4.name = "simple"

                #Nowy sketch
                sketch = sketches.add(rootComp.xYConstructionPlane)
                sketchArc = sketch.sketchCurves.sketchArcs
                sketchLine = sketch.sketchCurves.sketchLines
                sketchCircle = sketch.sketchCurves.sketchCircles
                extrudes = rootComp.features.extrudeFeatures

                pC1 = adsk.core.Point3D.create(0,-TopHoleHeight,0)
                sketchCircle.addByCenterRadius(pC1,0.08)

                pC2 = adsk.core.Point3D.create(0.9,-HoleHeight,0)
                sketchCircle.addByCenterRadius(pC2,0.08)

                pC3 = adsk.core.Point3D.create(-0.9,-HoleHeight,0)
                sketchCircle.addByCenterRadius(pC3,0.08)

                for i in range(3): 
                    prof4 = sketch.profiles.item(i)
                    distance1 = adsk.core.ValueInput.createByReal(1)
                    extrude5 = extrudes.addSimple(prof4, distance1, adsk.fusion.FeatureOperations.CutFeatureOperation)        
                    body5 = extrude5.bodies.item(0)
                    body5.name = "simple"

            elif self._Wyb == 'Orczyk 2':
                design = adsk.fusion.Design.cast(app.activeProduct)
                rootComp = design.rootComponent
                sketches = rootComp.sketches
                sketch = sketches.add(rootComp.xYConstructionPlane)
                sketchArc = sketch.sketchCurves.sketchArcs
                sketchLine = sketch.sketchCurves.sketchLines
                sketchCircle = sketch.sketchCurves.sketchCircles
                extrudes = rootComp.features.extrudeFeatures

                Length = self.Length
                TopLength = self.TopLength
                BotLength = Length-TopLength
                HoleHeight = BotLength-var1
                TopHoleHeight = BotLength-var2

                p0 = adsk.core.Point3D.create(0,0,0)
                sketchCircle.addByCenterRadius(p0,0.45)
                sketchCircle.addByCenterRadius(p0,1)

                pCentRect = adsk.core.Point3D.create(1.5,TopLength,0)
                pCornRect = adsk.core.Point3D.create(-1.5,-BotLength,0)
                sketchLine.addTwoPointRectangle(pCentRect,pCornRect)

                circleArray = [0,1,2]
                circleCenterArray = [-0.35,0,0.35]
                for i in circleArray:
                    circleCenter = adsk.core.Point3D.create(circleCenterArray[i],0.7,0)
                    sketchCircle.addByCenterRadius(circleCenter,0.08)

                for i in circleArray:
                    circleCenter = adsk.core.Point3D.create(circleCenterArray[i],-0.7,0)
                    sketchCircle.addByCenterRadius(circleCenter,0.08)

                for i in circleArray:
                    circleCenter = adsk.core.Point3D.create(0.7,circleCenterArray[i],0)
                    sketchCircle.addByCenterRadius(circleCenter,0.08)

                for i in circleArray:
                    circleCenter = adsk.core.Point3D.create(-0.7,circleCenterArray[i],0)
                    sketchCircle.addByCenterRadius(circleCenter,0.08)

                pC1 = adsk.core.Point3D.create(0,-TopHoleHeight,0)
                sketchCircle.addByCenterRadius(pC1,0.08)

                pC2 = adsk.core.Point3D.create(0.9,-HoleHeight,0)
                sketchCircle.addByCenterRadius(pC2,0.08)

                pC3 = adsk.core.Point3D.create(-0.9,-HoleHeight,0)
                sketchCircle.addByCenterRadius(pC3,0.08)

                #Extrudujemy miejsce pod orczyk
                prof1 = sketch.profiles.item(1)
                distance1 = adsk.core.ValueInput.createByReal(0.2)
                extrude1 = extrudes.addSimple(prof1, distance1, adsk.fusion.FeatureOperations.NewBodyFeatureOperation)        
                body1 = extrude1.bodies.item(0)
                body1.name = "simple"

                #Extrudowanie części głównej
                prof2 = sketch.profiles.item(2)
                distance2 = adsk.core.ValueInput.createByReal(0.5)
                extrude2 = extrudes.addSimple(prof2, distance2, adsk.fusion.FeatureOperations.NewBodyFeatureOperation)        
                body2 = extrude2.bodies.item(0)
                body2.name = "simple"

            elif self._Wyb == 'Orczyk 3':
                design = adsk.fusion.Design.cast(app.activeProduct)
                rootComp = design.rootComponent
                sketches = rootComp.sketches
                sketch = sketches.add(rootComp.xYConstructionPlane)
                extrudes = rootComp.features.extrudeFeatures

                Length = self.Length
                TopLength = 3.4
                BotLength = Length-TopLength
                HoleHeight = BotLength-var1
                TopHoleHeight = BotLength-var2

                sketchArc = sketch.sketchCurves.sketchArcs
                sketchLine = sketch.sketchCurves.sketchLines
                sketchCircle = sketch.sketchCurves.sketchCircles

                p1 = adsk.core.Point3D.create(-0.7,0,0)
                p2 = adsk.core.Point3D.create(-0.35,2.65,0)
                sketchLine.addByTwoPoints(p1,p2)

                arcTop = adsk.core.Point3D.create(0,2.65,0)
                sketchArc.addByCenterStartSweep(arcTop,p2,-1.5708)

                p3 = adsk.core.Point3D.create(0.7,0,0)
                p4 = adsk.core.Point3D.create(0.35,2.65,0)
                sketchLine.addByTwoPoints(p3,p4)

                sketchArc.addByCenterStartSweep(arcTop,p4,1.5708)

                #Odbicie
                p5 = adsk.core.Point3D.create(-0.35,-2.65,0)
                sketchLine.addByTwoPoints(p1,p5)

                arcBot = adsk.core.Point3D.create(0,-2.65,0)
                sketchArc.addByCenterStartSweep(arcBot,p5,1.5708)

                p6 = adsk.core.Point3D.create(0.35,-2.65,0)
                sketchLine.addByTwoPoints(p3,p6)

                sketchArc.addByCenterStartSweep(arcBot,p6,-1.5708)

                #Extrudujemy miejsce pod orczyk
                prof = sketch.profiles.item(0)
                distance = adsk.core.ValueInput.createByReal(0.1)
                extrude1 = extrudes.addSimple(prof, distance, adsk.fusion.FeatureOperations.NewBodyFeatureOperation)        
                body1 = extrude1.bodies.item(0)
                body1.name = "simple"

                #Tworzymy otwór centralny
                p0 = adsk.core.Point3D.create(0,0,0)
                sketchCircle.addByCenterRadius(p0,0.45)

                #Extrudowanie otworu centralnego
                prof1 = sketch.profiles.item(0)
                distance1 = adsk.core.ValueInput.createByReal(1)
                extrude2 = extrudes.addSimple(prof1, distance1, adsk.fusion.FeatureOperations.CutFeatureOperation)        
                body2 = extrude2.bodies.item(0)
                body2.name = "simple"

                #Tworzymy zewnętrzną część nogi
                pCentRect = adsk.core.Point3D.create(1.5,TopLength,0)
                pCornRect = adsk.core.Point3D.create(-1.5,-BotLength,0)
                sketchLine.addTwoPointRectangle(pCentRect,pCornRect)

                #Extrudujemy zewnętrzną część nogi
                prof2 = sketch.profiles.item(0)
                distance2 = adsk.core.ValueInput.createByReal(0.2)
                extrude3 = extrudes.addSimple(prof2, distance2, adsk.fusion.FeatureOperations.NewBodyFeatureOperation)        
                body3 = extrude3.bodies.item(0)
                body3.name = "simple"

                #Nowy sketch
                sketch = sketches.add(rootComp.xYConstructionPlane)
                sketchArc = sketch.sketchCurves.sketchArcs
                sketchLine = sketch.sketchCurves.sketchLines
                sketchCircle = sketch.sketchCurves.sketchCircles
                extrudes = rootComp.features.extrudeFeatures

                #Tworzymy otwory w orczyku
                circleArray = [0,1,2,3]
                circleCenterArray = [1.7,2.0,2.3,2.6]
                for i in circleArray:
                    circleCenter = adsk.core.Point3D.create(0,circleCenterArray[i],0)
                    sketchCircle.addByCenterRadius(circleCenter,0.08)

                for i in circleArray:
                    circleCenter = adsk.core.Point3D.create(0,-circleCenterArray[i],0)
                    sketchCircle.addByCenterRadius(circleCenter,0.08)

                #Extrudujemy otwory w orczyku
                for i in range(8): 
                    prof3 = sketch.profiles.item(i)
                    distance1 = adsk.core.ValueInput.createByReal(1)
                    extrude4 = extrudes.addSimple(prof3, distance1, adsk.fusion.FeatureOperations.CutFeatureOperation)        
                    body4 = extrude4.bodies.item(0)
                    body4.name = "simple"

                #Nowy sketch
                sketch = sketches.add(rootComp.xYConstructionPlane)
                sketchArc = sketch.sketchCurves.sketchArcs
                sketchLine = sketch.sketchCurves.sketchLines
                sketchCircle = sketch.sketchCurves.sketchCircles
                extrudes = rootComp.features.extrudeFeatures

                pC1 = adsk.core.Point3D.create(0,-TopHoleHeight,0)
                sketchCircle.addByCenterRadius(pC1,0.08)

                pC2 = adsk.core.Point3D.create(0.9,-HoleHeight,0)
                sketchCircle.addByCenterRadius(pC2,0.08)

                pC3 = adsk.core.Point3D.create(-0.9,-HoleHeight,0)
                sketchCircle.addByCenterRadius(pC3,0.08)

                for i in range(3): 
                    prof4 = sketch.profiles.item(i)
                    distance1 = adsk.core.ValueInput.createByReal(1)
                    extrude5 = extrudes.addSimple(prof4, distance1, adsk.fusion.FeatureOperations.CutFeatureOperation)        
                    body5 = extrude5.bodies.item(0)
                    body5.name = "simple"

        except:
            if ui:
                ui.messageBox('Failed to compute the bolt. This is most likely because the input values define an invalid bolt.')

class Leg1:
    def __init__(self):
        self._Name = defaultName
        self._LegLength = defaultLegLength
        self._BotLength = defaultBotLength
        self._Wyb = defaultWyb

    #properties
    @property
    def Name(self):
        return self._Name
    @Name.setter
    def Name(self, value):
        self._Name = value

    @property
    def Length(self):
        return self._LegLength
    @Length.setter
    def Length(self, value):
        self._LegLength = value

    @property
    def BotLength(self):
        return self._BotLength
    @BotLength.setter
    def BotLength(self, value):
        self._BotLength = value 

    @property
    def Wyb(self):
        return self._Wyb
    @Wyb.setter
    def Wyb(self, value):
        self._Wyb = value

    def buildLeg1(self):
        try:
            global newComp
            newComp = createNewComponent()
            if newComp is None:
                ui.messageBox('New component failed to create', 'New Component Failed')
                return
            #ui.messageBox('Część1') #### KOD WYKONANY PO WYBRANIU ITEM 1 
            design = adsk.fusion.Design.cast(app.activeProduct)
            rootComp = design.rootComponent
            sketches = rootComp.sketches
            extrudes = rootComp.features.extrudeFeatures

            Length = 10.86
            TopLength = 7.7517
            BotLength = Length-TopLength

            sketch = sketches.add(rootComp.xYConstructionPlane)

            sketchLine = sketch.sketchCurves.sketchLines
            sketchCircle = sketch.sketchCurves.sketchCircles
            sketchArc = sketch.sketchCurves.sketchArcs

            #CZĘŚĆ GŁÓWNA
            p1 = adsk.core.Point3D.create(-1.475,-BotLength,0)
            p2 = adsk.core.Point3D.create(1.525,2.975,0)
            sketchLine.addTwoPointRectangle(p2,p1)

            #Extrudujemy
            prof = sketch.profiles.item(0)
            distance = adsk.core.ValueInput.createByReal(-2.5)
            extrudeInput = extrudes.createInput(prof, adsk.fusion.FeatureOperations.NewBodyFeatureOperation)
            extent_distance = adsk.fusion.DistanceExtentDefinition.create(distance)        
            extrudeInput.setOneSideExtent(extent_distance, adsk.fusion.ExtentDirections.PositiveExtentDirection)
            extrude1 = extrudes.add(extrudeInput) 
            body1 = extrude1.bodies.item(0)
            body1.name = "distance, from profile"

            #OTWÓR CENTRALNY
            p0 = adsk.core.Point3D.create(-1.075,0.75-BotLength,0)
            p3 = adsk.core.Point3D.create(1.075,2.125,0)
            sketchLine.addTwoPointRectangle(p0,p3)

            #Wycinamy
            prof2 = sketch.profiles.item(1)
            distance = adsk.core.ValueInput.createByReal(-2.5)
            extrude2 = extrudes.addSimple(prof2, distance, adsk.fusion.FeatureOperations.CutFeatureOperation)        
            body2 = extrude2.bodies.item(0)
            body2.name = "simple"

            #OBWÓDKA
            p4 = adsk.core.Point3D.create(-1.475,4.725,0)
            sketchLine.addByTwoPoints(p1,p4)
            p5 = adsk.core.Point3D.create(1.525,4.725,0)
            sketchLine.addByTwoPoints(p4,p5)
            p6 = adsk.core.Point3D.create(1.525,-BotLength,0)
            sketchLine.addByTwoPoints(p5,p6)
            p7 = adsk.core.Point3D.create(1.075,-BotLength,0)
            sketchLine.addByTwoPoints(p7,p6)
            p8 = adsk.core.Point3D.create(1.075,2.975,0)
            sketchLine.addByTwoPoints(p7,p8)
            p9 = adsk.core.Point3D.create(-1.075,2.975,0)
            sketchLine.addByTwoPoints(p9,p8)
            p10 = adsk.core.Point3D.create(-1.075,-BotLength,0)
            sketchLine.addByTwoPoints(p9,p10)
            sketchLine.addByTwoPoints(p1,p10)

            #Extrudujemy
            Array = [2,4]
            for i in Array:
                prof3 = sketch.profiles.item(i)
                distance3 = adsk.core.ValueInput.createByReal(1)
                extrude3 = extrudes.addSimple(prof3, distance3, adsk.fusion.FeatureOperations.NewBodyFeatureOperation)        
                body3 = extrude3.bodies.item(0)
                body3.name = "simple"

            #Wycinamy
            prof4 = sketch.profiles.item(5)
            distance4 = adsk.fusion.DistanceExtentDefinition.create(adsk.core.ValueInput.createByString("10mm"))
            distance5 = adsk.fusion.DistanceExtentDefinition.create(adsk.core.ValueInput.createByString("25mm"))
            extrudeInput = extrudes.createInput(prof4, adsk.fusion.FeatureOperations.NewBodyFeatureOperation)
            extrudeInput.setTwoSidesExtent(distance4, distance5)
            # Create the extrusion
            extrude4 = extrudes.add(extrudeInput)
            body4 = extrude4.bodies.item(0)
            body4.name = "symmetric"

            pC1 = adsk.core.Point3D.create(0.5,2.475,0)
            pC2 = adsk.core.Point3D.create(-0.5,2.475,0)
            pC3 = adsk.core.Point3D.create(0.5,0.35-BotLength,0)
            pC4 = adsk.core.Point3D.create(-0.5,0.35-BotLength,0)
            sketchCircle.addByCenterRadius(pC1,0.195)
            sketchCircle.addByCenterRadius(pC2,0.195)
            sketchCircle.addByCenterRadius(pC3,0.195)
            sketchCircle.addByCenterRadius(pC4,0.195)

            for i in range(6,10):
                prof5 = sketch.profiles.item(i)
                wciecie = adsk.core.ValueInput.createByReal(-1)
                extrude5 = extrudes.addSimple(prof5, wciecie, adsk.fusion.FeatureOperations.CutFeatureOperation)        
                body5 = extrude5.bodies.item(0)
                body5.name = "simple"

            #SKETCH BOCZNY

            yzPlane = rootComp.yZConstructionPlane
            sketch = sketches.add(yzPlane)
            sketchLine = sketch.sketchCurves.sketchLines
            sketchCircle = sketch.sketchCurves.sketchCircles
            sketchArc = sketch.sketchCurves.sketchArcs

            p11 = adsk.core.Point3D.create(-0.6,4.325,0)
            p12 = adsk.core.Point3D.create(2.5,-BotLength,0)
            sketchLine.addTwoPointRectangle(p11,p12)

            p28 = adsk.core.Point3D.create(2.3,4.325,0)
            p29 = adsk.core.Point3D.create(2.3,-BotLength,0)
            sketchLine.addByTwoPoints(p28,p29)

            pC5 = adsk.core.Point3D.create(2.5,-BotLength,0)
            sketchCircle.addByCenterRadius(pC5,0.2)
            sketchCircle.addByCenterRadius(pC5,0.4)
            #isFullLength = True

            prof6 = sketch.profiles.item(4)
            distance6 = adsk.fusion.DistanceExtentDefinition.create(adsk.core.ValueInput.createByString("15.25mm"))
            distance7 = adsk.fusion.DistanceExtentDefinition.create(adsk.core.ValueInput.createByString("14.75mm"))
            extrudeInput = extrudes.createInput(prof6, adsk.fusion.FeatureOperations.NewBodyFeatureOperation)
            extrudeInput.setTwoSidesExtent(distance6, distance7)
            # Create the extrusion
            extrude6 = extrudes.add(extrudeInput)
            body6 = extrude6.bodies.item(0)
            body6.name = "symmetric"

            #Wycinamy
            prof7 = sketch.profiles.item(5)
            extrudeInput = extrudes.createInput(prof7, adsk.fusion.FeatureOperations.CutFeatureOperation)
            extrudeInput.setTwoSidesExtent(distance6, distance7)
            # Create the extrusion
            extrude7 = extrudes.add(extrudeInput)
            body7 = extrude7.bodies.item(0)
            body7.name = "symmetric"

            p15 = adsk.core.Point3D.create(2.3,0.925,0)
            p21 = adsk.core.Point3D.create(3.166,2.425,0)
            sketchLine.addByTwoPoints(p15,p21)
            p27 = adsk.core.Point3D.create(4.242,4.287,0)
            sketchLine.addByTwoPoints(p27,p21)
            p16 = adsk.core.Point3D.create(4.466,4.6767,0)
            sketchLine.addByTwoPoints(p27,p16)
            p17 = adsk.core.Point3D.create(-0.86,7.7517,0)
            sketchLine.addByTwoPoints(p16,p17)
            p26 = adsk.core.Point3D.create(-1.085,7.362,0)
            sketchLine.addByTwoPoints(p26,p17)
            p22 = adsk.core.Point3D.create(-2.16,5.5,0)
            sketchLine.addByTwoPoints(p26,p22)
            p18 = adsk.core.Point3D.create(-2.385,5.11,0)
            sketchLine.addByTwoPoints(p18,p22)
            p19 = adsk.core.Point3D.create(2.3,2.405,0)
            sketchLine.addByTwoPoints(p18,p19)
            p20 = adsk.core.Point3D.create(2.3,2.925,0)
            sketchLine.addByTwoPoints(p20,p19)
            sketchLine.addByTwoPoints(p20,p21)
            p23 = adsk.core.Point3D.create(3.375,4.787,0)
            sketchLine.addByTwoPoints(p20,p23)
            p24 = adsk.core.Point3D.create(-1.3806,5.05,0)
            sketchLine.addByTwoPoints(p20,p24)
            p25 = adsk.core.Point3D.create(-0.3056,6.912,0)
            sketchLine.addByTwoPoints(p24,p25)
            sketchLine.addByTwoPoints(p24,p22)
            sketchLine.addByTwoPoints(p26,p25)
            sketchLine.addByTwoPoints(p23,p25)
            sketchLine.addByTwoPoints(p23,p27)

            pC6 = adsk.core.Point3D.create(2.95,2.0508,0)
            sketchCircle.addByCenterRadius(pC6,0.2)
            sketchCircle.addByCenterRadius(pC6,0.4)

            pC7 = adsk.core.Point3D.create(2.869,3.2605,0)
            sketchCircle.addByCenterRadius(pC7,0.195)
            pC8 = adsk.core.Point3D.create(3.369,4.1265,0)
            sketchCircle.addByCenterRadius(pC8,0.195)

            pC9 = adsk.core.Point3D.create(-1.3746,5.7105,0)
            sketchCircle.addByCenterRadius(pC9,0.195)
            pC10 = adsk.core.Point3D.create(-0.8746,6.5765,0)
            sketchCircle.addByCenterRadius(pC10,0.195)

            #DO ZMIANY (NIE WYCIĄGAMY): 1,5,6,7,8,9,12,13,14,17,22,23,24,25
            #DO ZMIANY (WYCIĘCIE): 20, 21, 
            Array2 = [0,1,3,5,10,11,16]
            for i in Array2:
                prof8 = sketch.profiles.item(i)
                distance8 = adsk.fusion.DistanceExtentDefinition.create(adsk.core.ValueInput.createByString("19.75mm"))
                extrudeInput = extrudes.createInput(prof8, adsk.fusion.FeatureOperations.NewBodyFeatureOperation)
                extrudeInput.setTwoSidesExtent(distance6, distance8)
                # Create the extrusion
                extrude8 = extrudes.add(extrudeInput)
                body8 = extrude8.bodies.item(0)
                body8.name = "symmetric"

            Array3 = [2,4,18]
            for i in Array3:
                prof8 = sketch.profiles.item(i)
                distance8 = adsk.fusion.DistanceExtentDefinition.create(adsk.core.ValueInput.createByString("19.75mm"))
                distance9 = adsk.fusion.DistanceExtentDefinition.create(adsk.core.ValueInput.createByString("5.25mm"))
                extrudeInput = extrudes.createInput(prof8, adsk.fusion.FeatureOperations.NewBodyFeatureOperation)
                extrudeInput.setTwoSidesExtent(distance9, distance8)
                # Create the extrusion
                extrude8 = extrudes.add(extrudeInput)
                body8 = extrude8.bodies.item(0)
                body8.name = "symmetric"

            Array4 = [19,20,21]
            for i in Array4:
                prof8 = sketch.profiles.item(i)
                distance8 = adsk.fusion.DistanceExtentDefinition.create(adsk.core.ValueInput.createByString("19.75mm"))
                extrudeInput = extrudes.createInput(prof8, adsk.fusion.FeatureOperations.CutFeatureOperation)
                extrudeInput.setTwoSidesExtent(distance6, distance8)
                # Create the extrusion
                extrude8 = extrudes.add(extrudeInput)
                body8 = extrude8.bodies.item(0)
                body8.name = "symmetric"

            sketch = sketches.add(rootComp.xYConstructionPlane)
            sketchLine = sketch.sketchCurves.sketchLines
            sketchCircle = sketch.sketchCurves.sketchCircles
            sketchArc = sketch.sketchCurves.sketchArcs

            p30 = adsk.core.Point3D.create(0.4,-BotLength-1,-2.3)
            p31 = adsk.core.Point3D.create(-0.4,-BotLength-1,-2.3)
            sketchLine.addByTwoPoints(p30,p31)
            p32 = adsk.core.Point3D.create(-0.4,1-BotLength,-2.3)
            sketchLine.addByTwoPoints(p31,p32)
            p33 = adsk.core.Point3D.create(0.4,1-BotLength,-2.3)
            sketchLine.addByTwoPoints(p33,p32)
            sketchLine.addByTwoPoints(p33,p30)

            prof9 = sketch.profiles.item(0)
            distance8 = adsk.fusion.DistanceExtentDefinition.create(adsk.core.ValueInput.createByString("10mm"))
            distance9 = adsk.fusion.DistanceExtentDefinition.create(adsk.core.ValueInput.createByString("1.5mm"))
            extrudeInput = extrudes.createInput(prof9, adsk.fusion.FeatureOperations.CutFeatureOperation)
            extrudeInput.setTwoSidesExtent(distance9, distance8)
            extrude9 = extrudes.add(extrudeInput)    
            body9 = extrude9.bodies.item(0)
            body9.name = "simple"

            sketch = sketches.add(rootComp.xYConstructionPlane)
            sketchLine = sketch.sketchCurves.sketchLines
            sketchCircle = sketch.sketchCurves.sketchCircles
            sketchArc = sketch.sketchCurves.sketchArcs

            p34 = adsk.core.Point3D.create(0.4,0.41-BotLength,-0.45)
            p35 = adsk.core.Point3D.create(-0.4,0.41-BotLength,-0.45)
            sketchLine.addByTwoPoints(p34,p35)
            p36 = adsk.core.Point3D.create(-0.4,0.75-BotLength,-0.45)
            sketchLine.addByTwoPoints(p35,p36)
            p37 = adsk.core.Point3D.create(0.4,0.75-BotLength,-0.45)
            sketchLine.addByTwoPoints(p36,p37)
            sketchLine.addByTwoPoints(p37,p34)

            prof10 = sketch.profiles.item(0)
            distance10 = adsk.core.ValueInput.createByReal(-1.7)
            extrude10 = extrudes.addSimple(prof10, distance10, adsk.fusion.FeatureOperations.CutFeatureOperation)
            body10 = extrude10.bodies.item(0)
            body10.name = "simple"

        except:
            if ui:
                ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))

class Leg2:
    def __init__(self):
        self._Name = defaultName
        self._Length = defaultLength
        self._Wyb = defaultWyb

    #properties
    @property
    def Name(self):
        return self._Name
    @Name.setter
    def Name(self, value):
        self._Name = value

    @property
    def Length(self):
        return self._Length
    @Length.setter
    def Length(self, value):
        self._Length = value

    @property
    def Wyb(self):
        return self._Wyb
    @Wyb.setter
    def Wyb(self, value):
        self._Wyb = value

    def buildLeg2(self):
        try:
            global newComp
            newComp = createNewComponent()
            if newComp is None:
                ui.messageBox('New component failed to create', 'New Component Failed')
                return
            if self._Wyb == 'Orczyk 1':
                #ui.messageBox('Część1') #### KOD WYKONANY PO WYBRANIU ITEM 1 
                design = adsk.fusion.Design.cast(app.activeProduct)
                rootComp = design.rootComponent
                sketches = rootComp.sketches
                sketch = sketches.add(rootComp.xYConstructionPlane)

                Length = self.Length
                HalfLength = Length/2

                sketchArc = sketch.sketchCurves.sketchArcs
                sketchLine = sketch.sketchCurves.sketchLines
                sketchCircle = sketch.sketchCurves.sketchCircles
                extrudes = rootComp.features.extrudeFeatures

                #SKETCH BAZA
                p1 = adsk.core.Point3D.create(-2,-HalfLength,0)
                p2 = adsk.core.Point3D.create(-2,HalfLength,0)
                sketchLine.addByTwoPoints(p1,p2)
                p3 = adsk.core.Point3D.create(-0.8,HalfLength,0)
                sketchLine.addByTwoPoints(p3,p2)
                arcTopStart = adsk.core.Point3D.create(0,HalfLength,0)
                sketchArc.addByCenterStartSweep(arcTopStart,p3,-deg180)
                p5 = adsk.core.Point3D.create(0.8,HalfLength,0)
                p6 = adsk.core.Point3D.create(2,HalfLength,0)
                sketchLine.addByTwoPoints(p5,p6)
                p7 = adsk.core.Point3D.create(2,-HalfLength,0)
                sketchLine.addByTwoPoints(p6,p7)
                p8 = adsk.core.Point3D.create(0.8,-HalfLength,0)
                sketchLine.addByTwoPoints(p8,p7)
                arcBotStart = adsk.core.Point3D.create(0,-HalfLength,0)
                sketchArc.addByCenterStartSweep(arcBotStart,p8,-deg180)
                p9 = adsk.core.Point3D.create(-0.8,-HalfLength,0)
                sketchLine.addByTwoPoints(p9,p1)

                #MIEJSCE POD ORCZYK1
                arcStart = adsk.core.Point3D.create(-0.55,HalfLength-1.75,0)
                arcAlong = adsk.core.Point3D.create(-0.5123,HalfLength-1.55,0)
                arcEnd = adsk.core.Point3D.create(-0.45,HalfLength-1.4338,0)
                sketchArc.addByThreePoints(arcStart,arcAlong,arcEnd)

                p10 = adsk.core.Point3D.create(-0.45,HalfLength-1.4338,0)
                p11 = adsk.core.Point3D.create(-0.4,HalfLength+0.2,0)
                sketchLine.addByTwoPoints(p10,p11)

                arcTopStart2 = adsk.core.Point3D.create(0,HalfLength+0.2,0)
                sketchArc.addByCenterStartSweep(arcTopStart2,p11,-1.5708)

                #Odbicie względem osi Y
                arc2Start = adsk.core.Point3D.create(0.55,HalfLength-1.75,0)
                arc2Along = adsk.core.Point3D.create(0.5123,HalfLength-1.55,0)
                arc2End = adsk.core.Point3D.create(0.45,HalfLength-1.4338,0)
                sketchArc.addByThreePoints(arc2Start,arc2Along,arc2End)

                p12 = adsk.core.Point3D.create(0.45,HalfLength-1.4338,0)
                p13 = adsk.core.Point3D.create(0.4,HalfLength+0.2,0)
                sketchLine.addByTwoPoints(p12,p13)

                arcTopEnd2 = adsk.core.Point3D.create(0,HalfLength+0.2,0)
                sketchArc.addByCenterStartSweep(arcTopEnd2,p13,1.5708)

                #Odbicie względem osi X
                arc3Start = adsk.core.Point3D.create(0.55,HalfLength-1.75,0)
                arc3Along = adsk.core.Point3D.create(0.5123,HalfLength-1.95,0)
                arc3End = adsk.core.Point3D.create(0.45,HalfLength-2.0662,0)
                sketchArc.addByThreePoints(arc3Start,arc3Along,arc3End)

                p15 = adsk.core.Point3D.create(0.45,HalfLength-2.0662,0)
                p16 = adsk.core.Point3D.create(0.4,HalfLength-3.7,0)
                sketchLine.addByTwoPoints(p15,p16)

                arcBotStart2 = adsk.core.Point3D.create(0,HalfLength-3.7,0)
                sketchArc.addByCenterStartSweep(arcBotStart2,p16,-1.5708)

                arc4Start = adsk.core.Point3D.create(-0.55,HalfLength-1.75,0)
                arc4Along = adsk.core.Point3D.create(-0.5123,HalfLength-1.95,0)
                arc4End = adsk.core.Point3D.create(-0.45,HalfLength-2.0662,0)
                sketchArc.addByThreePoints(arc4Start,arc4Along,arc4End)

                p17 = adsk.core.Point3D.create(-0.45,HalfLength-2.0662,0)
                p18 = adsk.core.Point3D.create(-0.4,HalfLength-3.7,0)
                sketchLine.addByTwoPoints(p17,p18)

                arcBotEnd2 = adsk.core.Point3D.create(0,HalfLength-3.7,0)
                sketchArc.addByCenterStartSweep(arcBotEnd2,p18,1.5708)

                #Tworzymy otwór centralny
                p19 = adsk.core.Point3D.create(0,HalfLength-1.75,0)
                sketchCircle.addByCenterRadius(p19,0.45)

                #MIEJSCE POD ORCZYK - ODBICIE
                arcStart = adsk.core.Point3D.create(-0.55,-HalfLength+1.75,0)
                arcAlong = adsk.core.Point3D.create(-0.5123,-HalfLength+1.55,0)
                arcEnd = adsk.core.Point3D.create(-0.45,-HalfLength+1.4338,0)
                sketchArc.addByThreePoints(arcStart,arcAlong,arcEnd)

                p20 = adsk.core.Point3D.create(-0.45,-HalfLength+1.4338,0)
                p21 = adsk.core.Point3D.create(-0.4,-HalfLength-0.2,0)
                sketchLine.addByTwoPoints(p20,p21)

                arcTopStart2 = adsk.core.Point3D.create(0,-HalfLength-0.2,0)
                sketchArc.addByCenterStartSweep(arcTopStart2,p21,1.5708)

                #Odbicie względem osi Y
                arc21Start = adsk.core.Point3D.create(0.55,-HalfLength+1.75,0)
                arc21Along = adsk.core.Point3D.create(0.5123,-HalfLength+1.55,0)
                arc21End = adsk.core.Point3D.create(0.45,-HalfLength+1.4338,0)
                sketchArc.addByThreePoints(arc21Start,arc21Along,arc21End)

                p22 = adsk.core.Point3D.create(0.45,-HalfLength+1.4338,0)
                p23 = adsk.core.Point3D.create(0.4,-HalfLength-0.2,0)
                sketchLine.addByTwoPoints(p22,p23)

                arcTopEnd2 = adsk.core.Point3D.create(0,-HalfLength-0.2,0)
                sketchArc.addByCenterStartSweep(arcTopEnd2,p23,-1.5708)

                #Odbicie względem osi X
                arc31Start = adsk.core.Point3D.create(0.55,-HalfLength+1.75,0)
                arc31Along = adsk.core.Point3D.create(0.5123,-HalfLength+1.95,0)
                arc31End = adsk.core.Point3D.create(0.45,-HalfLength+2.0662,0)
                sketchArc.addByThreePoints(arc31Start,arc31Along,arc31End)

                p25 = adsk.core.Point3D.create(0.45,-HalfLength+2.0662,0)
                p26 = adsk.core.Point3D.create(0.4,-HalfLength+3.7,0)
                sketchLine.addByTwoPoints(p25,p26)

                arcBotStart21 = adsk.core.Point3D.create(0,-HalfLength+3.7,0)
                sketchArc.addByCenterStartSweep(arcBotStart21,p26,1.5708)

                arc41Start = adsk.core.Point3D.create(-0.55,-HalfLength+1.75,0)
                arc41Along = adsk.core.Point3D.create(-0.5123,-HalfLength+1.95,0)
                arc41End = adsk.core.Point3D.create(-0.45,-HalfLength+2.0662,0)
                sketchArc.addByThreePoints(arc41Start,arc41Along,arc41End)

                p27 = adsk.core.Point3D.create(-0.45,-HalfLength+2.0662,0)
                p28 = adsk.core.Point3D.create(-0.4,-HalfLength+3.7,0)
                sketchLine.addByTwoPoints(p27,p28)

                arcBotEnd21 = adsk.core.Point3D.create(0,-HalfLength+3.7,0)
                sketchArc.addByCenterStartSweep(arcBotEnd21,p28,-1.5708)

                #TWORZYMY OTWORY CENTRALNE ORCZYKÓW
                p29 = adsk.core.Point3D.create(0,-HalfLength+1.75,0)
                sketchCircle.addByCenterRadius(p29,0.45)

                #TWORZYMY OTWORY ORCZYKÓW
                circleCenterArray = [HalfLength-3.55,HalfLength-3.1,HalfLength-2.65,HalfLength-0.85,HalfLength-0.4,HalfLength+0,5]
                for i in range(6):
                    circleCenter = adsk.core.Point3D.create(0,circleCenterArray[i],0)
                    sketchCircle.addByCenterRadius(circleCenter,0.08)

                for i in range(6):
                    circleCenter = adsk.core.Point3D.create(0,-circleCenterArray[i],0)
                    sketchCircle.addByCenterRadius(circleCenter,0.08)

                #PODPÓRKI
                p301 = adsk.core.Point3D.create(-2,0.8,0)
                p31 = adsk.core.Point3D.create(-1.2,0.8,0)
                sketchLine.addByTwoPoints(p301,p31)
                p32 = adsk.core.Point3D.create(-1.2,0.3,0)
                sketchLine.addByTwoPoints(p32,p31)
                p33 = adsk.core.Point3D.create(1.2,0.3,0)
                sketchLine.addByTwoPoints(p32,p33)
                p34 = adsk.core.Point3D.create(1.2,0.8,0)
                sketchLine.addByTwoPoints(p34,p33)
                p351 = adsk.core.Point3D.create(2,0.8,0)
                sketchLine.addByTwoPoints(p34,p351)
                #Odbicie
                p302 = adsk.core.Point3D.create(-2,-0.8,0)
                p31 = adsk.core.Point3D.create(-1.2,-0.8,0)
                sketchLine.addByTwoPoints(p302,p31)
                p32 = adsk.core.Point3D.create(-1.2,-0.3,0)
                sketchLine.addByTwoPoints(p32,p31)
                p33 = adsk.core.Point3D.create(1.2,-0.3,0)
                sketchLine.addByTwoPoints(p32,p33)
                p34 = adsk.core.Point3D.create(1.2,-0.8,0)
                sketchLine.addByTwoPoints(p34,p33)
                p352 = adsk.core.Point3D.create(2,-0.8,0)
                sketchLine.addByTwoPoints(p34,p352)

                sketchLine.addByTwoPoints(p301,p302)
                sketchLine.addByTwoPoints(p351,p352)

                p36 = adsk.core.Point3D.create(-2,1.3,0)
                p37 = adsk.core.Point3D.create(-1.6,1.3,0)
                sketchLine.addByTwoPoints(p36,p37)
                arc5Along = adsk.core.Point3D.create(-1.3,1.6,0)
                p38 = adsk.core.Point3D.create(-1.6,1.9,0)
                sketchArc.addByThreePoints(p37,arc5Along,p38)
                p39 = adsk.core.Point3D.create(-2,1.9,0)
                sketchLine.addByTwoPoints(p38,p39)
                sketchLine.addByTwoPoints(p36,p39)

                p36 = adsk.core.Point3D.create(2,1.3,0)
                p37 = adsk.core.Point3D.create(1.6,1.3,0)
                sketchLine.addByTwoPoints(p36,p37)
                arc5Along = adsk.core.Point3D.create(1.3,1.6,0)
                p38 = adsk.core.Point3D.create(1.6,1.9,0)
                sketchArc.addByThreePoints(p37,arc5Along,p38)
                p39 = adsk.core.Point3D.create(2,1.9,0)
                sketchLine.addByTwoPoints(p38,p39)
                sketchLine.addByTwoPoints(p36,p39)

                p36 = adsk.core.Point3D.create(2,-1.3,0)
                p37 = adsk.core.Point3D.create(1.6,-1.3,0)
                sketchLine.addByTwoPoints(p36,p37)
                arc5Along = adsk.core.Point3D.create(1.3,-1.6,0)
                p38 = adsk.core.Point3D.create(1.6,-1.9,0)
                sketchArc.addByThreePoints(p37,arc5Along,p38)
                p39 = adsk.core.Point3D.create(2,-1.9,0)
                sketchLine.addByTwoPoints(p38,p39)
                sketchLine.addByTwoPoints(p36,p39)

                p36 = adsk.core.Point3D.create(-2,-1.3,0)
                p37 = adsk.core.Point3D.create(-1.6,-1.3,0)
                sketchLine.addByTwoPoints(p36,p37)
                arc5Along = adsk.core.Point3D.create(-1.3,-1.6,0)
                p38 = adsk.core.Point3D.create(-1.6,-1.9,0)
                sketchArc.addByThreePoints(p37,arc5Along,p38)
                p39 = adsk.core.Point3D.create(-2,-1.9,0)
                sketchLine.addByTwoPoints(p38,p39)
                sketchLine.addByTwoPoints(p36,p39)

                #TWORZYMY DZIURY W PODPÓRCE
                circleCenterArray = [-1.6,0,1.6]
                for i in range(3):
                    circleCenter = adsk.core.Point3D.create(-1.6,circleCenterArray[i],0)
                    sketchCircle.addByCenterRadius(circleCenter,0.22)

                for i in range(3):
                    circleCenter = adsk.core.Point3D.create(1.6,circleCenterArray[i],0)
                    sketchCircle.addByCenterRadius(circleCenter,0.22)

                Array = [0,2]
                for i in Array:
                    prof1 = sketch.profiles.item(i)
                    distance = adsk.core.ValueInput.createByReal(0.2)
                    extrude1 = extrudes.addSimple(prof1, distance, adsk.fusion.FeatureOperations.NewBodyFeatureOperation)        
                    body1 = extrude1.bodies.item(0)
                    body1.name = "simple"

                Array = [16,18,19,20,21]
                for i in Array:
                    prof1 = sketch.profiles.item(i)
                    distance = adsk.core.ValueInput.createByReal(2.2)
                    extrude1 = extrudes.addSimple(prof1, distance, adsk.fusion.FeatureOperations.NewBodyFeatureOperation)        
                    body1 = extrude1.bodies.item(0)
                    body1.name = "simple"

                Array = [17,22]
                for i in Array:
                    prof1 = sketch.profiles.item(i)
                    distance = adsk.core.ValueInput.createByReal(0.5)
                    extrude1 = extrudes.addSimple(prof1, distance, adsk.fusion.FeatureOperations.NewBodyFeatureOperation)        
                    body1 = extrude1.bodies.item(0)
                    body1.name = "simple"

            elif self._Wyb == 'Orczyk 2':
                design = adsk.fusion.Design.cast(app.activeProduct)
                rootComp = design.rootComponent
                sketches = rootComp.sketches
                sketch = sketches.add(rootComp.xYConstructionPlane)
                sketchArc = sketch.sketchCurves.sketchArcs
                sketchLine = sketch.sketchCurves.sketchLines
                sketchCircle = sketch.sketchCurves.sketchCircles
                extrudes = rootComp.features.extrudeFeatures

                Length = self.Length
                HalfLength = Length/2

                p1 = adsk.core.Point3D.create(-2,-HalfLength,0)
                p2 = adsk.core.Point3D.create(-2,HalfLength,0)
                sketchLine.addByTwoPoints(p1,p2)
                p3 = adsk.core.Point3D.create(-0.8,HalfLength,0)
                sketchLine.addByTwoPoints(p3,p2)
                arcTopStart = adsk.core.Point3D.create(0,HalfLength,0)
                sketchArc.addByCenterStartSweep(arcTopStart,p3,-deg180)
                p5 = adsk.core.Point3D.create(0.8,HalfLength,0)
                p6 = adsk.core.Point3D.create(2,HalfLength,0)
                sketchLine.addByTwoPoints(p5,p6)
                p7 = adsk.core.Point3D.create(2,-HalfLength,0)
                sketchLine.addByTwoPoints(p6,p7)
                p8 = adsk.core.Point3D.create(0.8,-HalfLength,0)
                sketchLine.addByTwoPoints(p8,p7)
                arcBotStart = adsk.core.Point3D.create(0,-HalfLength,0)
                sketchArc.addByCenterStartSweep(arcBotStart,p8,-deg180)
                p9 = adsk.core.Point3D.create(-0.8,-HalfLength,0)
                sketchLine.addByTwoPoints(p9,p1)

                p10 = adsk.core.Point3D.create(0,HalfLength-1.75,0)
                sketchCircle.addByCenterRadius(p10,0.45)
                sketchCircle.addByCenterRadius(p10,1)

                circleArray = [0,1,2]
                circleCenterArray = [-0.35,0,0.35]
                circleCenterArrayY = [HalfLength-2.1,HalfLength-1.75,HalfLength-1.4]
                for i in circleArray:
                    circleCenter = adsk.core.Point3D.create(circleCenterArray[i],HalfLength-1.05,0)
                    sketchCircle.addByCenterRadius(circleCenter,0.08)

                for i in circleArray:
                    circleCenter = adsk.core.Point3D.create(circleCenterArray[i],HalfLength-2.45,0)
                    sketchCircle.addByCenterRadius(circleCenter,0.08)

                for i in circleArray:
                    circleCenter = adsk.core.Point3D.create(0.7,circleCenterArrayY[i],0)
                    sketchCircle.addByCenterRadius(circleCenter,0.08)

                for i in circleArray:
                    circleCenter = adsk.core.Point3D.create(-0.7,circleCenterArrayY[i],0)
                    sketchCircle.addByCenterRadius(circleCenter,0.08)

                p11 = adsk.core.Point3D.create(0,-HalfLength+1.75,0)
                sketchCircle.addByCenterRadius(p11,0.45)
                sketchCircle.addByCenterRadius(p11,1)

                circleArray = [0,1,2]
                circleCenterArray = [-0.35,0,0.35]
                circleCenterArrayY = [-HalfLength+2.1,-HalfLength+1.75,-HalfLength+1.4]
                for i in circleArray:
                    circleCenter = adsk.core.Point3D.create(circleCenterArray[i],-HalfLength+1.05,0)
                    sketchCircle.addByCenterRadius(circleCenter,0.08)

                for i in circleArray:
                    circleCenter = adsk.core.Point3D.create(circleCenterArray[i],-HalfLength+2.45,0)
                    sketchCircle.addByCenterRadius(circleCenter,0.08)

                for i in circleArray:
                    circleCenter = adsk.core.Point3D.create(0.7,circleCenterArrayY[i],0)
                    sketchCircle.addByCenterRadius(circleCenter,0.08)

                for i in circleArray:
                    circleCenter = adsk.core.Point3D.create(-0.7,circleCenterArrayY[i],0)
                    sketchCircle.addByCenterRadius(circleCenter,0.08)

                #PODPÓRKI
                p201 = adsk.core.Point3D.create(-2,0.8,0)
                p21 = adsk.core.Point3D.create(-1.2,0.8,0)
                sketchLine.addByTwoPoints(p201,p21)
                p22 = adsk.core.Point3D.create(-1.2,0.3,0)
                sketchLine.addByTwoPoints(p22,p21)
                p23 = adsk.core.Point3D.create(1.2,0.3,0)
                sketchLine.addByTwoPoints(p22,p23)
                p24 = adsk.core.Point3D.create(1.2,0.8,0)
                sketchLine.addByTwoPoints(p24,p23)
                p251 = adsk.core.Point3D.create(2,0.8,0)
                sketchLine.addByTwoPoints(p24,p251)
                #Odbicie
                p202 = adsk.core.Point3D.create(-2,-0.8,0)
                p21 = adsk.core.Point3D.create(-1.2,-0.8,0)
                sketchLine.addByTwoPoints(p202,p21)
                p22 = adsk.core.Point3D.create(-1.2,-0.3,0)
                sketchLine.addByTwoPoints(p22,p21)
                p23 = adsk.core.Point3D.create(1.2,-0.3,0)
                sketchLine.addByTwoPoints(p22,p23)
                p24 = adsk.core.Point3D.create(1.2,-0.8,0)
                sketchLine.addByTwoPoints(p24,p23)
                p252 = adsk.core.Point3D.create(2,-0.8,0)
                sketchLine.addByTwoPoints(p24,p252)

                sketchLine.addByTwoPoints(p201,p202)
                sketchLine.addByTwoPoints(p251,p252)

                p26 = adsk.core.Point3D.create(-2,1.3,0)
                p27 = adsk.core.Point3D.create(-1.6,1.3,0)
                sketchLine.addByTwoPoints(p26,p27)
                arc5Along = adsk.core.Point3D.create(-1.3,1.6,0)
                p28 = adsk.core.Point3D.create(-1.6,1.9,0)
                sketchArc.addByThreePoints(p27,arc5Along,p28)
                p29 = adsk.core.Point3D.create(-2,1.9,0)
                sketchLine.addByTwoPoints(p28,p29)
                sketchLine.addByTwoPoints(p26,p29)

                p26 = adsk.core.Point3D.create(2,1.3,0)
                p27 = adsk.core.Point3D.create(1.6,1.3,0)
                sketchLine.addByTwoPoints(p26,p27)
                arc5Along = adsk.core.Point3D.create(1.3,1.6,0)
                p28 = adsk.core.Point3D.create(1.6,1.9,0)
                sketchArc.addByThreePoints(p27,arc5Along,p28)
                p29 = adsk.core.Point3D.create(2,1.9,0)
                sketchLine.addByTwoPoints(p28,p29)
                sketchLine.addByTwoPoints(p26,p29)

                p26 = adsk.core.Point3D.create(2,-1.3,0)
                p27 = adsk.core.Point3D.create(1.6,-1.3,0)
                sketchLine.addByTwoPoints(p26,p27)
                arc5Along = adsk.core.Point3D.create(1.3,-1.6,0)
                p28 = adsk.core.Point3D.create(1.6,-1.9,0)
                sketchArc.addByThreePoints(p27,arc5Along,p28)
                p29 = adsk.core.Point3D.create(2,-1.9,0)
                sketchLine.addByTwoPoints(p28,p29)
                sketchLine.addByTwoPoints(p26,p29)

                p26 = adsk.core.Point3D.create(-2,-1.3,0)
                p27 = adsk.core.Point3D.create(-1.6,-1.3,0)
                sketchLine.addByTwoPoints(p26,p27)
                arc5Along = adsk.core.Point3D.create(-1.3,-1.6,0)
                p28 = adsk.core.Point3D.create(-1.6,-1.9,0)
                sketchArc.addByThreePoints(p27,arc5Along,p28)
                p29 = adsk.core.Point3D.create(-2,-1.9,0)
                sketchLine.addByTwoPoints(p28,p29)
                sketchLine.addByTwoPoints(p26,p29)

                #TWORZYMY DZIURY W PODPÓRCE
                circleCenterArray = [-1.6,0,1.6]
                for i in range(3):
                    circleCenter = adsk.core.Point3D.create(-1.6,circleCenterArray[i],0)
                    sketchCircle.addByCenterRadius(circleCenter,0.22)

                for i in range(3):
                    circleCenter = adsk.core.Point3D.create(1.6,circleCenterArray[i],0)
                    sketchCircle.addByCenterRadius(circleCenter,0.22)

                Array = [1,15]
                for i in Array:
                    prof1 = sketch.profiles.item(i)
                    distance = adsk.core.ValueInput.createByReal(0.2)
                    extrude1 = extrudes.addSimple(prof1, distance, adsk.fusion.FeatureOperations.NewBodyFeatureOperation)        
                    body1 = extrude1.bodies.item(0)
                    body1.name = "simple"

                Array = [28,30,31,32,33]
                for i in Array:
                    prof1 = sketch.profiles.item(i)
                    distance = adsk.core.ValueInput.createByReal(2.2)
                    extrude1 = extrudes.addSimple(prof1, distance, adsk.fusion.FeatureOperations.NewBodyFeatureOperation)        
                    body1 = extrude1.bodies.item(0)
                    body1.name = "simple"

                Array = [29,34]
                for i in Array:
                    prof1 = sketch.profiles.item(i)
                    distance = adsk.core.ValueInput.createByReal(0.5)
                    extrude1 = extrudes.addSimple(prof1, distance, adsk.fusion.FeatureOperations.NewBodyFeatureOperation)        
                    body1 = extrude1.bodies.item(0)
                    body1.name = "simple"

            elif self._Wyb == 'Orczyk 3':
                design = adsk.fusion.Design.cast(app.activeProduct)
                rootComp = design.rootComponent
                sketches = rootComp.sketches
                sketch = sketches.add(rootComp.xYConstructionPlane)
                sketchArc = sketch.sketchCurves.sketchArcs
                sketchLine = sketch.sketchCurves.sketchLines
                sketchCircle = sketch.sketchCurves.sketchCircles
                extrudes = rootComp.features.extrudeFeatures

                Length = self.Length
                HalfLength = Length/2

                p1 = adsk.core.Point3D.create(-2,-HalfLength,0)
                p2 = adsk.core.Point3D.create(-2,HalfLength,0)
                sketchLine.addByTwoPoints(p1,p2)
                p3 = adsk.core.Point3D.create(-0.8,HalfLength,0)
                sketchLine.addByTwoPoints(p3,p2)
                arcTopStart = adsk.core.Point3D.create(0,HalfLength,0)
                sketchArc.addByCenterStartSweep(arcTopStart,p3,-deg180)
                p5 = adsk.core.Point3D.create(0.8,HalfLength,0)
                p6 = adsk.core.Point3D.create(2,HalfLength,0)
                sketchLine.addByTwoPoints(p5,p6)
                p7 = adsk.core.Point3D.create(2,-HalfLength,0)
                sketchLine.addByTwoPoints(p6,p7)
                p8 = adsk.core.Point3D.create(0.8,-HalfLength,0)
                sketchLine.addByTwoPoints(p8,p7)
                arcBotStart = adsk.core.Point3D.create(0,-HalfLength,0)
                sketchArc.addByCenterStartSweep(arcBotStart,p8,-deg180)
                p9 = adsk.core.Point3D.create(-0.8,-HalfLength,0)
                sketchLine.addByTwoPoints(p9,p1)

                p10 = adsk.core.Point3D.create(0,HalfLength-2.5,0)
                sketchCircle.addByCenterRadius(p10,0.45)

                #Orczyk
                p11 = adsk.core.Point3D.create(-0.7,HalfLength-2.5,0)
                p12 = adsk.core.Point3D.create(-0.35,HalfLength+0.15,0)
                sketchLine.addByTwoPoints(p11,p12)
                arcTop = adsk.core.Point3D.create(0,HalfLength+0.15,0)
                sketchArc.addByCenterStartSweep(arcTop,p12,-1.5708)
                p13 = adsk.core.Point3D.create(0.7,HalfLength-2.5,0)
                p14 = adsk.core.Point3D.create(0.35,HalfLength+0.15,0)
                sketchLine.addByTwoPoints(p13,p14)
                sketchArc.addByCenterStartSweep(arcTop,p14,1.5708)

                #Odbicie
                p15 = adsk.core.Point3D.create(-0.35,HalfLength-5.15,0)
                sketchLine.addByTwoPoints(p11,p15)
                arcBot = adsk.core.Point3D.create(0,HalfLength-5.15,0)
                sketchArc.addByCenterStartSweep(arcBot,p15,1.5708)
                p16 = adsk.core.Point3D.create(0.35,HalfLength-5.15,0)
                sketchLine.addByTwoPoints(p13,p16)
                sketchArc.addByCenterStartSweep(arcBot,p16,-1.5708)

                #Tworzymy otwory w orczyku
                circleArray = [0,1,2,3,4,5,6,7]
                circleCenterArray = [HalfLength-5.1,HalfLength-4.8,HalfLength-4.5,HalfLength-4.2,HalfLength-0.8,HalfLength-0.5,HalfLength-0.2,HalfLength+0.1]
                for i in circleArray:
                    circleCenter = adsk.core.Point3D.create(0,circleCenterArray[i],0)
                    sketchCircle.addByCenterRadius(circleCenter,0.08)

                for i in circleArray:
                    circleCenter = adsk.core.Point3D.create(0,-circleCenterArray[i],0)
                    sketchCircle.addByCenterRadius(circleCenter,0.08)

                p10 = adsk.core.Point3D.create(0,-HalfLength+2.5,0)
                sketchCircle.addByCenterRadius(p10,0.45)

                #Orczyk
                p11 = adsk.core.Point3D.create(-0.7,-HalfLength+2.5,0)
                p12 = adsk.core.Point3D.create(-0.35,-HalfLength-0.15,0)
                sketchLine.addByTwoPoints(p11,p12)
                arcTop = adsk.core.Point3D.create(0,-HalfLength-0.15,0)
                sketchArc.addByCenterStartSweep(arcTop,p12,1.5708)
                p13 = adsk.core.Point3D.create(0.7,-HalfLength+2.5,0)
                p14 = adsk.core.Point3D.create(0.35,-HalfLength-0.15,0)
                sketchLine.addByTwoPoints(p13,p14)
                sketchArc.addByCenterStartSweep(arcTop,p14,-1.5708)

                #Odbicie
                p15 = adsk.core.Point3D.create(-0.35,-HalfLength+5.15,0)
                sketchLine.addByTwoPoints(p11,p15)
                arcBot = adsk.core.Point3D.create(0,-HalfLength+5.15,0)
                sketchArc.addByCenterStartSweep(arcBot,p15,-1.5708)
                p16 = adsk.core.Point3D.create(0.35,-HalfLength+5.15,0)
                sketchLine.addByTwoPoints(p13,p16)
                sketchArc.addByCenterStartSweep(arcBot,p16,1.5708)

                #PODPÓRKI
                p201 = adsk.core.Point3D.create(-2,0.8,0)
                p21 = adsk.core.Point3D.create(-1.2,0.8,0)
                sketchLine.addByTwoPoints(p201,p21)
                p22 = adsk.core.Point3D.create(-1.2,0.3,0)
                sketchLine.addByTwoPoints(p22,p21)
                p23 = adsk.core.Point3D.create(1.2,0.3,0)
                sketchLine.addByTwoPoints(p22,p23)
                p24 = adsk.core.Point3D.create(1.2,0.8,0)
                sketchLine.addByTwoPoints(p24,p23)
                p251 = adsk.core.Point3D.create(2,0.8,0)
                sketchLine.addByTwoPoints(p24,p251)
                #Odbicie
                p202 = adsk.core.Point3D.create(-2,-0.8,0)
                p21 = adsk.core.Point3D.create(-1.2,-0.8,0)
                sketchLine.addByTwoPoints(p202,p21)
                p22 = adsk.core.Point3D.create(-1.2,-0.3,0)
                sketchLine.addByTwoPoints(p22,p21)
                p23 = adsk.core.Point3D.create(1.2,-0.3,0)
                sketchLine.addByTwoPoints(p22,p23)
                p24 = adsk.core.Point3D.create(1.2,-0.8,0)
                sketchLine.addByTwoPoints(p24,p23)
                p252 = adsk.core.Point3D.create(2,-0.8,0)
                sketchLine.addByTwoPoints(p24,p252)

                sketchLine.addByTwoPoints(p201,p202)
                sketchLine.addByTwoPoints(p251,p252)

                p26 = adsk.core.Point3D.create(-2,1.3,0)
                p27 = adsk.core.Point3D.create(-1.6,1.3,0)
                sketchLine.addByTwoPoints(p26,p27)
                arc5Along = adsk.core.Point3D.create(-1.3,1.6,0)
                p28 = adsk.core.Point3D.create(-1.6,1.9,0)
                sketchArc.addByThreePoints(p27,arc5Along,p28)
                p29 = adsk.core.Point3D.create(-2,1.9,0)
                sketchLine.addByTwoPoints(p28,p29)
                sketchLine.addByTwoPoints(p26,p29)

                p26 = adsk.core.Point3D.create(2,1.3,0)
                p27 = adsk.core.Point3D.create(1.6,1.3,0)
                sketchLine.addByTwoPoints(p26,p27)
                arc5Along = adsk.core.Point3D.create(1.3,1.6,0)
                p28 = adsk.core.Point3D.create(1.6,1.9,0)
                sketchArc.addByThreePoints(p27,arc5Along,p28)
                p29 = adsk.core.Point3D.create(2,1.9,0)
                sketchLine.addByTwoPoints(p28,p29)
                sketchLine.addByTwoPoints(p26,p29)

                p26 = adsk.core.Point3D.create(2,-1.3,0)
                p27 = adsk.core.Point3D.create(1.6,-1.3,0)
                sketchLine.addByTwoPoints(p26,p27)
                arc5Along = adsk.core.Point3D.create(1.3,-1.6,0)
                p28 = adsk.core.Point3D.create(1.6,-1.9,0)
                sketchArc.addByThreePoints(p27,arc5Along,p28)
                p29 = adsk.core.Point3D.create(2,-1.9,0)
                sketchLine.addByTwoPoints(p28,p29)
                sketchLine.addByTwoPoints(p26,p29)

                p26 = adsk.core.Point3D.create(-2,-1.3,0)
                p27 = adsk.core.Point3D.create(-1.6,-1.3,0)
                sketchLine.addByTwoPoints(p26,p27)
                arc5Along = adsk.core.Point3D.create(-1.3,-1.6,0)
                p28 = adsk.core.Point3D.create(-1.6,-1.9,0)
                sketchArc.addByThreePoints(p27,arc5Along,p28)
                p29 = adsk.core.Point3D.create(-2,-1.9,0)
                sketchLine.addByTwoPoints(p28,p29)
                sketchLine.addByTwoPoints(p26,p29)

                #TWORZYMY DZIURY W PODPÓRCE
                circleCenterArray = [-1.6,0,1.6]
                for i in range(3):
                    circleCenter = adsk.core.Point3D.create(-1.6,circleCenterArray[i],0)
                    sketchCircle.addByCenterRadius(circleCenter,0.22)

                for i in range(3):
                    circleCenter = adsk.core.Point3D.create(1.6,circleCenterArray[i],0)
                    sketchCircle.addByCenterRadius(circleCenter,0.22)

                Array = [1,19]
                for i in Array:
                    prof1 = sketch.profiles.item(i)
                    distance = adsk.core.ValueInput.createByReal(0.2)
                    extrude1 = extrudes.addSimple(prof1, distance, adsk.fusion.FeatureOperations.NewBodyFeatureOperation)        
                    body1 = extrude1.bodies.item(0)
                    body1.name = "simple"

                Array = [20,22,23,24,25]
                for i in Array:
                    prof1 = sketch.profiles.item(i)
                    distance = adsk.core.ValueInput.createByReal(2.2)
                    extrude1 = extrudes.addSimple(prof1, distance, adsk.fusion.FeatureOperations.NewBodyFeatureOperation)        
                    body1 = extrude1.bodies.item(0)
                    body1.name = "simple"

                Array = [21,26]
                for i in Array:
                    prof1 = sketch.profiles.item(i)
                    distance = adsk.core.ValueInput.createByReal(0.5)
                    extrude1 = extrudes.addSimple(prof1, distance, adsk.fusion.FeatureOperations.NewBodyFeatureOperation)        
                    body1 = extrude1.bodies.item(0)
                    body1.name = "simple"

        except:
            if ui:
                ui.messageBox('Failed to compute the bolt. This is most likely because the input values define an invalid bolt.')

class Leg3:
    def __init__(self):
        self._Name = defaultName
        self._LegLength = defaultLegLength
        self._BotLength = defaultBotLength
        self._Wyb = defaultWyb

    #properties
    @property
    def Name(self):
        return self._Name
    @Name.setter
    def Name(self, value):
        self._Name = value

    @property
    def Length(self):
        return self._LegLength
    @Length.setter
    def Length(self, value):
        self._LegLength = value

    @property
    def BotLength(self):
        return self._BotLength
    @BotLength.setter
    def BotLength(self, value):
        self._BotLength = value 

    @property
    def Wyb(self):
        return self._Wyb
    @Wyb.setter
    def Wyb(self, value):
        self._Wyb = value

    def buildLeg3(self):
        try:
            global newComp
            newComp = createNewComponent()
            if newComp is None:
                ui.messageBox('New component failed to create', 'New Component Failed')
                return
            design = adsk.fusion.Design.cast(app.activeProduct)
            rootComp = design.rootComponent
            sketches = rootComp.sketches
            sketch = sketches.add(rootComp.xYConstructionPlane)

            sketchArc = sketch.sketchCurves.sketchArcs
            sketchLine = sketch.sketchCurves.sketchLines
            sketchCircle = sketch.sketchCurves.sketchCircles
            extrudes = rootComp.features.extrudeFeatures

            #Tworzymy dolny łuk
            arcStart = adsk.core.Point3D.create(-3.4908,-6.0752,0)
            arcAlong = adsk.core.Point3D.create(-2.9705,-6.9967,0)
            arcEnd = adsk.core.Point3D.create(-1.7126,-6.5779,0)
            sketchArc.addByThreePoints(arcStart,arcAlong,arcEnd)

            p1 = adsk.core.Point3D.create(-1.5713,0,0)
            sketchLine.addByTwoPoints(arcStart,p1)
            p2 = adsk.core.Point3D.create(-1.3502,5.4015,0)
            sketchLine.addByTwoPoints(p2,p1)
            arc = adsk.core.Point3D.create(-0.4142,6.2639,0)
            p3 = adsk.core.Point3D.create(-1.2766,7.2,0)
            sketchArc.addByThreePoints(p2,arc,p3)
            p4 = adsk.core.Point3D.create(-1.2643,7.5,0)
            sketchLine.addByTwoPoints(p3,p4)
            p5 = adsk.core.Point3D.create(-0.8313,7.75,0)
            sketchLine.addByTwoPoints(p5,p4)
            p6 = adsk.core.Point3D.create(3.8113,10.4304,0)
            sketchLine.addByTwoPoints(p5,p6)
            p7 = adsk.core.Point3D.create(4.1483,10.625,0)
            sketchLine.addByTwoPoints(p7,p6)
            p8 = adsk.core.Point3D.create(2.357,0,0)
            sketchLine.addByTwoPoints(p7,p8)
            sketchLine.addByTwoPoints(arcEnd,p8)

            #WEWNĘTRZNE
            arcStart2 = adsk.core.Point3D.create(-3.2022,-6.1568,0)
            arcAlong2 = adsk.core.Point3D.create(-2.723,-6.7556,0)
            arcEnd2 = adsk.core.Point3D.create(-2.0013,-6.4963,0)
            sketchArc.addByThreePoints(arcStart2,arcAlong2,arcEnd2)
            p9 = adsk.core.Point3D.create(-1.2713,0,0)
            sketchLine.addByTwoPoints(arcStart2,p9)
            p10 = adsk.core.Point3D.create(-1.061,5.1331,0)
            sketchLine.addByTwoPoints(p10,p9)
            arc2 = adsk.core.Point3D.create(-0.1243,6.8153,0)
            p11 = adsk.core.Point3D.create(-0.8409,7.398,0)
            sketchArc.addByThreePoints(p10,arc2,p11)
            sketchLine.addByTwoPoints(p11,p5)
            p12 = adsk.core.Point3D.create(2.057,0,0)
            sketchLine.addByTwoPoints(p6,p12)
            sketchLine.addByTwoPoints(arcEnd2,p12)

            #GÓRNA CZĘŚĆ
            p13 = adsk.core.Point3D.create(-1.4354,7.7964,0)
            sketchLine.addByTwoPoints(p13,p4)
            p14 = adsk.core.Point3D.create(-2.5104,9.6584,0)
            sketchLine.addByTwoPoints(p13,p14)
            p15 = adsk.core.Point3D.create(-2.7354,10.0481,0)
            sketchLine.addByTwoPoints(p15,p14)
            p16 = adsk.core.Point3D.create(2.6772,13.1731,0)
            sketchLine.addByTwoPoints(p15,p16)
            p17 = adsk.core.Point3D.create(2.9022,12.7834,0)
            sketchLine.addByTwoPoints(p17,p16)
            p18 = adsk.core.Point3D.create(3.9772,10.9214,0)
            sketchLine.addByTwoPoints(p17,p18)
            sketchLine.addByTwoPoints(p7,p18)
            p19 = adsk.core.Point3D.create(3.1112,10.4214,0)
            sketchLine.addByTwoPoints(p19,p18)
            p20 = adsk.core.Point3D.create(-0.5694,8.2964,0)
            sketchLine.addByTwoPoints(p19,p20)
            sketchLine.addByTwoPoints(p13,p20)
            p21 = adsk.core.Point3D.create(-1.6444,10.1584,0)
            sketchLine.addByTwoPoints(p21,p20)
            sketchLine.addByTwoPoints(p21,p14)
            p22 = adsk.core.Point3D.create(2.0362,12.2834,0)
            sketchLine.addByTwoPoints(p21,p22)
            sketchLine.addByTwoPoints(p19,p22)
            sketchLine.addByTwoPoints(p17,p22)

            pC1 = adsk.core.Point3D.create(-1.1659,8.6795,0)
            sketchCircle.addByCenterRadius(pC1,0.195)
            pC2 = adsk.core.Point3D.create(-1.6659,9.5455,0)
            sketchCircle.addByCenterRadius(pC2,0.195)
            pC3 = adsk.core.Point3D.create(3.0766,11.1295,0)
            sketchCircle.addByCenterRadius(pC3,0.195)
            pC4 = adsk.core.Point3D.create(2.5766,11.9955,0)
            sketchCircle.addByCenterRadius(pC4,0.195)

            prof1 = sketch.profiles.item(6)
            distance1 = adsk.fusion.DistanceExtentDefinition.create(adsk.core.ValueInput.createByString("10mm"))
            distance2 = adsk.fusion.DistanceExtentDefinition.create(adsk.core.ValueInput.createByString("5mm"))
            extrudeInput = extrudes.createInput(prof1, adsk.fusion.FeatureOperations.NewBodyFeatureOperation)
            extrudeInput.setTwoSidesExtent(distance2, distance1)
            extrude1 = extrudes.add(extrudeInput)
            body1 = extrude1.bodies.item(0)
            body1.name = "symmetric"

            # Array1 = [4]
            # for i in Array1:
            #     prof1 = sketch.profiles.item(i)
            #     distance1 = adsk.fusion.DistanceExtentDefinition.create(adsk.core.ValueInput.createByString("10mm"))
            #     distance2 = adsk.fusion.DistanceExtentDefinition.create(adsk.core.ValueInput.createByString("5mm"))
            #     extrudeInput = extrudes.createInput(prof1, adsk.fusion.FeatureOperations.NewBodyFeatureOperation)
            #     extrudeInput.setTwoSidesExtent(distance2, distance1)
            #     extrude1 = extrudes.add(extrudeInput)
            #     body1 = extrude1.bodies.item(0)
            #     body1.name = "symmetric"

            Array2 = [0,2]
            for i in Array2:
                prof2 = sketch.profiles.item(i)
                distance = adsk.core.ValueInput.createByReal(-2.5)
                extrude2 = extrudes.addSimple(prof2, distance, adsk.fusion.FeatureOperations.NewBodyFeatureOperation)
                body2 = extrude2.bodies.item(0)
                body2.name = "simple"

            Array3 = [3,4]
            for i in Array3:
                prof1 = sketch.profiles.item(i)
                distance1 = adsk.fusion.DistanceExtentDefinition.create(adsk.core.ValueInput.createByString("25mm"))
                distance2 = adsk.fusion.DistanceExtentDefinition.create(adsk.core.ValueInput.createByString("10mm"))
                extrudeInput = extrudes.createInput(prof1, adsk.fusion.FeatureOperations.NewBodyFeatureOperation)
                extrudeInput.setTwoSidesExtent(distance2, distance1)
                extrude1 = extrudes.add(extrudeInput)
                body1 = extrude1.bodies.item(0)
                body1.name = "symmetric"

            prof1 = sketch.profiles.item(5)
            distance1 = adsk.fusion.DistanceExtentDefinition.create(adsk.core.ValueInput.createByString("15mm"))
            distance2 = adsk.fusion.DistanceExtentDefinition.create(adsk.core.ValueInput.createByString("10mm"))
            extrudeInput = extrudes.createInput(prof1, adsk.fusion.FeatureOperations.NewBodyFeatureOperation)
            extrudeInput.setTwoSidesExtent(distance2, distance1)
            extrude1 = extrudes.add(extrudeInput)
            body1 = extrude1.bodies.item(0)
            body1.name = "symmetric"

        except:
            if ui:
                ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))

class Body:
    def __init__(self):
        self._Name = defaultName
        self._Diameter = defaultDiameter
        self._LegNumber = defaultLegNum
        # self._Holes1 = defaultHoles1

    #properties
    @property
    def Name(self):
        return self._Name
    @Name.setter
    def Name(self, value):
        self._Name = value

    @property
    def Diameter(self):
        return self._Diameter
    @Diameter.setter
    def Diameter(self, value):
        self._Diameter = value

    @property
    def LegNumber(self):
        return self._LegNumber
    @LegNumber.setter
    def LegNumber(self, value):
        self._LegNumber = value 

    # @property
    # def Holes1(self):
    #     return self._Holes1
    # @Holes1.setter
    # def Holes1(self, value):
    #     self._Holes1 = value

    def buildBody(self):
        try:
            global newComp
            newComp = createNewComponent()
            if newComp is None:
                ui.messageBox('New component failed to create', 'New Component Failed')
                return
            design = adsk.fusion.Design.cast(app.activeProduct)
            rootComp = design.rootComponent
            sketches = rootComp.sketches

            #ui.messageBox(f"Wartość LegNum3: {self.LegNumber}")
            LegNumber = int(self.LegNumber)
            Diameter = self.Diameter
            Place = Diameter-2.0805
            # ui.messageBox(f"Wartość Hole11: {self.Holes1}")
            # ui.messageBox(f"Wartość Hole14: {inputHole1.value}")
            Holes1 = inputHole1.value
            Holes2 = inputHole2.value
            Holes3 = inputHole3.value

            sketch = sketches.add(rootComp.xYConstructionPlane)

            sketchArc = sketch.sketchCurves.sketchArcs
            sketchLine = sketch.sketchCurves.sketchLines
            sketchCircle = sketch.sketchCurves.sketchCircles
            extrudes = rootComp.features.extrudeFeatures

            pC0 = adsk.core.Point3D.create(0,0,0)
            sketchCircle.addByCenterRadius(pC0,Diameter)

            #Extrudujemy
            prof1 = sketch.profiles.item(0)
            distance = adsk.core.ValueInput.createByReal(1)
            extrude1 = extrudes.addSimple(prof1, distance, adsk.fusion.FeatureOperations.NewBodyFeatureOperation)        
            body1 = extrude1.bodies.item(0)
            body1.name = "simple"

            #MIEJSCA NA NOGI
            sketch = sketches.add(rootComp.xYConstructionPlane)
            sketchArc = sketch.sketchCurves.sketchArcs
            sketchLine = sketch.sketchCurves.sketchLines
            sketchCircle = sketch.sketchCurves.sketchCircles
            extrudes = rootComp.features.extrudeFeatures

            p1 = adsk.core.Point3D.create(-1.59,Diameter,0.5)
            p2 = adsk.core.Point3D.create(-1.59,Place,0.5)
            sketchLine.addByTwoPoints(p1,p2)
            p3 = adsk.core.Point3D.create(1.59,Place,0.5)
            sketchLine.addByTwoPoints(p3,p2)
            p4 = adsk.core.Point3D.create(1.59,Diameter,0.5)
            sketchLine.addByTwoPoints(p3,p4)
            sketchLine.addByTwoPoints(p1,p4)

            pC1 = adsk.core.Point3D.create(0,Diameter-0.5905,0)
            sketchCircle.addByCenterRadius(pC1,0.08)
            pC2 = adsk.core.Point3D.create(-0.9,Diameter-1.3095,0)
            sketchCircle.addByCenterRadius(pC2,0.08)
            pC3 = adsk.core.Point3D.create(0.9,Diameter-1.3095,0)
            sketchCircle.addByCenterRadius(pC3,0.08)

            for i in range(4):
                prof2 = sketch.profiles.item(i)
                distance = adsk.core.ValueInput.createByReal(1)
                extrude2 = extrudes.addSimple(prof2, distance, adsk.fusion.FeatureOperations.CutFeatureOperation)        
                body2 = extrude2.bodies.item(0)
                body2.name = "simple"
                cylFace = extrude1.sideFaces.item(0)
                circularPatterns = rootComp.features.circularPatternFeatures
                entities = adsk.core.ObjectCollection.create()
                entities.add(extrude2)
                cylFace = extrude1.sideFaces.item(0)        
                patternInput = circularPatterns.createInput(entities, cylFace)
                numTeethInput = adsk.core.ValueInput.createByReal(LegNumber)
                patternInput.quantity = numTeethInput
                patternInput.patternComputeOption = adsk.fusion.PatternComputeOptions.IdenticalPatternCompute    
                pattern = circularPatterns.add(patternInput)

            #PODPÓRKI
            sketch = sketches.add(rootComp.xYConstructionPlane)
            sketchArc = sketch.sketchCurves.sketchArcs
            sketchLine = sketch.sketchCurves.sketchLines
            sketchCircle = sketch.sketchCurves.sketchCircles
            extrudes = rootComp.features.extrudeFeatures

            deg0 = 360/(2*LegNumber)
            deg1 = 90 - deg0 - 36/Diameter
            deg2 = 90 - deg0 + 36/Diameter
            rad0 = math.radians(90-deg0)
            rad1 = math.radians(deg1)
            rad2 = math.radians(deg2)

            p18 = adsk.core.Point3D.create(math.cos(rad1)*(Diameter+0.1), math.sin(rad1)*(Diameter+0.1), 0.8)
            p19 = adsk.core.Point3D.create(math.cos(rad1)*(Diameter-0.5), math.sin(rad1)*(Diameter-0.5), 0.8)
            sketchLine.addByTwoPoints(p18,p19)
            p20 = adsk.core.Point3D.create(math.cos(rad2)*(Diameter+0.1), math.sin(rad2)*(Diameter+0.1), 0.8)
            p21 = adsk.core.Point3D.create(math.cos(rad2)*(Diameter-0.5), math.sin(rad2)*(Diameter-0.5), 0.8)
            sketchLine.addByTwoPoints(p20,p21)
            p22 = adsk.core.Point3D.create(math.cos(rad0)*(Diameter-1.0757), math.sin(rad0)*(Diameter-1.0757), 0.8)
            sketchArc.addByThreePoints(p19,p22,p21)
            sketchLine.addByTwoPoints(p18,p20)

            pC4 = adsk.core.Point3D.create(math.cos(rad0)*(Diameter-0.5), math.sin(rad0)*(Diameter-0.5), 0)
            sketchCircle.addByCenterRadius(pC4,0.08)

            for i in range(2):
                prof3 = sketch.profiles.item(i)
                distance = adsk.core.ValueInput.createByReal(1)
                extrude3 = extrudes.addSimple(prof3, distance, adsk.fusion.FeatureOperations.CutFeatureOperation)        
                body3 = extrude3.bodies.item(0)
                body3.name = "simple"
                cylFace = extrude1.sideFaces.item(0)
                circularPatterns = rootComp.features.circularPatternFeatures
                entities = adsk.core.ObjectCollection.create()
                entities.add(extrude3)
                cylFace = extrude1.sideFaces.item(0)        
                patternInput = circularPatterns.createInput(entities, cylFace)
                numTeethInput = adsk.core.ValueInput.createByReal(LegNumber)
                patternInput.quantity = numTeethInput
                patternInput.patternComputeOption = adsk.fusion.PatternComputeOptions.IdenticalPatternCompute    
                pattern = circularPatterns.add(patternInput)

            #OTWORY POD PRZETWORNICE
            if Holes1 == True:
                sketch = sketches.add(rootComp.xYConstructionPlane)
                sketchArc = sketch.sketchCurves.sketchArcs
                sketchLine = sketch.sketchCurves.sketchLines
                sketchCircle = sketch.sketchCurves.sketchCircles
                extrudes = rootComp.features.extrudeFeatures

                Array = [1.016,-1.016]
                for i in range(2):
                    circleCenter = adsk.core.Point3D.create(Array[i],Diameter-4.4125,0)
                    sketchCircle.addByCenterRadius(circleCenter,0.08)
                    circleCenter1 = adsk.core.Point3D.create(Array[i],Diameter-2.3805,0)
                    sketchCircle.addByCenterRadius(circleCenter1,0.08)

                for i in range(4):
                    prof4 = sketch.profiles.item(i)
                    distance = adsk.core.ValueInput.createByReal(1)
                    extrude4 = extrudes.addSimple(prof4, distance, adsk.fusion.FeatureOperations.CutFeatureOperation)        
                    body4 = extrude4.bodies.item(0)
                    body4.name = "simple"
                    cylFace = extrude1.sideFaces.item(0)
                    circularPatterns = rootComp.features.circularPatternFeatures
                    entities = adsk.core.ObjectCollection.create()
                    entities.add(extrude4)
                    cylFace = extrude1.sideFaces.item(0)        
                    patternInput = circularPatterns.createInput(entities, cylFace)
                    numTeethInput = adsk.core.ValueInput.createByReal(LegNumber)
                    patternInput.quantity = numTeethInput
                    patternInput.patternComputeOption = adsk.fusion.PatternComputeOptions.IdenticalPatternCompute    
                    pattern = circularPatterns.add(patternInput)

            if Holes2 == True:
                sketch = sketches.add(rootComp.xYConstructionPlane)
                sketchArc = sketch.sketchCurves.sketchArcs
                sketchLine = sketch.sketchCurves.sketchLines
                sketchCircle = sketch.sketchCurves.sketchCircles
                extrudes = rootComp.features.extrudeFeatures

                circleCenter = adsk.core.Point3D.create(3.6821,2.8224,0)
                sketchCircle.addByCenterRadius(circleCenter,0.08)
                circleCenter1 = adsk.core.Point3D.create(1.1516,0.6649,0)
                sketchCircle.addByCenterRadius(circleCenter1,0.08)

                for i in range(2):
                    prof4 = sketch.profiles.item(i)
                    distance = adsk.core.ValueInput.createByReal(1)
                    extrude4 = extrudes.addSimple(prof4, distance, adsk.fusion.FeatureOperations.CutFeatureOperation)        
                    body4 = extrude4.bodies.item(0)
                    body4.name = "simple"

            if Holes3 == True:
                sketch = sketches.add(rootComp.xYConstructionPlane)
                sketchArc = sketch.sketchCurves.sketchArcs
                sketchLine = sketch.sketchCurves.sketchLines
                sketchCircle = sketch.sketchCurves.sketchCircles
                extrudes = rootComp.features.extrudeFeatures

                vert = 2.45
                pc5 = adsk.core.Point3D.create(-vert,3.7,0)
                sketchCircle.addByCenterRadius(pc5,0.08)
                pc6 = adsk.core.Point3D.create(vert,3.7,0)
                sketchCircle.addByCenterRadius(pc6,0.08)
                pc7 = adsk.core.Point3D.create(-vert,-2.1,0)
                sketchCircle.addByCenterRadius(pc7,0.08)
                pc8 = adsk.core.Point3D.create(vert,-2.1,0)
                sketchCircle.addByCenterRadius(pc8,0.08)

                for i in range(4):
                    prof4 = sketch.profiles.item(i)
                    distance = adsk.core.ValueInput.createByReal(1)
                    extrude4 = extrudes.addSimple(prof4, distance, adsk.fusion.FeatureOperations.CutFeatureOperation)        
                    body4 = extrude4.bodies.item(0)
                    body4.name = "simple"

        except:
            if ui:
                ui.messageBox('Failed to compute the bolt. This is most likely because the input values define an invalid bolt.')

def run(context):
    try:
        product = app.activeProduct
        design = adsk.fusion.Design.cast(product)
        if not design:
            ui.messageBox('It is not supported in current workspace, please change to MODEL workspace and try again.')
            return
        commandDefinitions = ui.commandDefinitions
        #check the command exists or not
        cmdDef = commandDefinitions.itemById('Orczyk')
        if not cmdDef:
            cmdDef = commandDefinitions.addButtonDefinition('Orczyk',
                    'Stwórz orczyk',
                    'Stwórz orczyk.')

        onCommandCreated = BoltCommandCreatedHandler()
        cmdDef.commandCreated.add(onCommandCreated)
        # keep the handler referenced beyond this function
        handlers.append(onCommandCreated)
        inputs = adsk.core.NamedValues.create()
        cmdDef.execute(inputs)

        # prevent this module from being terminate when the script returns, because we are waiting for event handlers to fire
        adsk.autoTerminate(False)
    except:
        if ui:
            ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))
