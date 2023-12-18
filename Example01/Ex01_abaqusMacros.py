# -*- coding: mbcs -*-
# Do not delete the following import lines
from abaqus import *
from abaqusConstants import *
import __main__

def Macro1():
    import section
    import regionToolset
    import displayGroupMdbToolset as dgm
    import part
    import material
    import assembly
    import step
    import interaction
    import load
    import mesh
    import optimization
    import job
    import sketch
    import visualization
    import xyPlot
    import displayGroupOdbToolset as dgo
    import connectorBehavior
    s1 = mdb.models['Model-1'].ConstrainedSketch(name='__profile__', 
        sheetSize=1200.0)
    g, v, d, c = s1.geometry, s1.vertices, s1.dimensions, s1.constraints
    s1.setPrimaryObject(option=STANDALONE)
    s1.Line(point1=(0.0, 0.0), point2=(1000.0, 0.0))
    s1.HorizontalConstraint(entity=g[2], addUndoState=False)
    p = mdb.models['Model-1'].Part(name='beam', dimensionality=TWO_D_PLANAR, 
        type=DEFORMABLE_BODY)
    p = mdb.models['Model-1'].parts['beam']
    p.BaseWire(sketch=s1)
    s1.unsetPrimaryObject()
    p = mdb.models['Model-1'].parts['beam']
    session.viewports['Viewport: 1'].setValues(displayedObject=p)
    del mdb.models['Model-1'].sketches['__profile__']
    session.viewports['Viewport: 1'].partDisplay.setValues(sectionAssignments=ON, 
        engineeringFeatures=ON)
    session.viewports['Viewport: 1'].partDisplay.geometryOptions.setValues(
        referenceRepresentation=OFF)
    mdb.models['Model-1'].Material(name='steel')
    mdb.models['Model-1'].materials['steel'].Elastic(table=((200000.0, 0.3), ))
    mdb.models['Model-1'].RectangularProfile(name='Profile-1', a=100.0, b=20.0)
    mdb.models['Model-1'].BeamSection(name='Section-1', 
        integration=DURING_ANALYSIS, poissonRatio=0.0, profile='Profile-1', 
        material='steel', temperatureVar=LINEAR, consistentMassMatrix=False)
    p = mdb.models['Model-1'].parts['beam']
    e = p.edges
    edges = e.getSequenceFromMask(mask=('[#1 ]', ), )
    region = p.Set(edges=edges, name='Set-1')
    p = mdb.models['Model-1'].parts['beam']
    p.SectionAssignment(region=region, sectionName='Section-1', offset=0.0, 
        offsetType=MIDDLE_SURFACE, offsetField='', 
        thicknessAssignment=FROM_SECTION)
    p = mdb.models['Model-1'].parts['beam']
    e = p.edges
    edges = e.getSequenceFromMask(mask=('[#1 ]', ), )
    region=p.Set(edges=edges, name='Set-2')
    p = mdb.models['Model-1'].parts['beam']
    p.assignBeamSectionOrientation(region=region, method=N1_COSINES, n1=(0.0, 0.0, 
        -1.0))
    a = mdb.models['Model-1'].rootAssembly
    session.viewports['Viewport: 1'].setValues(displayedObject=a)
    a1 = mdb.models['Model-1'].rootAssembly
    a1.DatumCsysByDefault(CARTESIAN)
    p = mdb.models['Model-1'].parts['beam']
    a1.Instance(name='beam-1', part=p, dependent=ON)
    session.viewports['Viewport: 1'].assemblyDisplay.setValues(
        adaptiveMeshConstraints=ON)
    mdb.models['Model-1'].StaticStep(name='Step-1', previous='Initial')
    session.viewports['Viewport: 1'].assemblyDisplay.setValues(step='Step-1')
    session.viewports['Viewport: 1'].assemblyDisplay.setValues(loads=ON, bcs=ON, 
        predefinedFields=ON, connectors=ON, adaptiveMeshConstraints=OFF)
    a = mdb.models['Model-1'].rootAssembly
    v1 = a.instances['beam-1'].vertices
    verts1 = v1.getSequenceFromMask(mask=('[#1 ]', ), )
    region = a.Set(vertices=verts1, name='Set-1')
    mdb.models['Model-1'].DisplacementBC(name='BC-1', createStepName='Step-1', 
        region=region, u1=0.0, u2=0.0, ur3=0.0, amplitude=UNSET, fixed=OFF, 
        distributionType=UNIFORM, fieldName='', localCsys=None)
    a = mdb.models['Model-1'].rootAssembly
    v1 = a.instances['beam-1'].vertices
    verts1 = v1.getSequenceFromMask(mask=('[#2 ]', ), )
    region = a.Set(vertices=verts1, name='Set-2')
    mdb.models['Model-1'].ConcentratedForce(name='Load-1', createStepName='Step-1', 
        region=region, cf2=-100.0, distributionType=UNIFORM, field='', 
        localCsys=None)
    session.viewports['Viewport: 1'].assemblyDisplay.setValues(mesh=ON, loads=OFF, 
        bcs=OFF, predefinedFields=OFF, connectors=OFF)
    session.viewports['Viewport: 1'].assemblyDisplay.meshOptions.setValues(
        meshTechnique=ON)
    p = mdb.models['Model-1'].parts['beam']
    session.viewports['Viewport: 1'].setValues(displayedObject=p)
    session.viewports['Viewport: 1'].partDisplay.setValues(sectionAssignments=OFF, 
        engineeringFeatures=OFF, mesh=ON)
    session.viewports['Viewport: 1'].partDisplay.meshOptions.setValues(
        meshTechnique=ON)
    p = mdb.models['Model-1'].parts['beam']
    p.seedPart(size=100.0, deviationFactor=0.1, minSizeFactor=0.1)
    p = mdb.models['Model-1'].parts['beam']
    p.generateMesh()
    a1 = mdb.models['Model-1'].rootAssembly
    a1.regenerate()
    a = mdb.models['Model-1'].rootAssembly
    session.viewports['Viewport: 1'].setValues(displayedObject=a)
    session.viewports['Viewport: 1'].assemblyDisplay.setValues(mesh=OFF)
    session.viewports['Viewport: 1'].assemblyDisplay.meshOptions.setValues(
        meshTechnique=OFF)
    mdb.Job(name='example01_job01', model='Model-1', description='', type=ANALYSIS, 
        atTime=None, waitMinutes=0, waitHours=0, queue=None, memory=90, 
        memoryUnits=PERCENTAGE, getMemoryFromAnalysis=True, 
        explicitPrecision=SINGLE, nodalOutputPrecision=SINGLE, echoPrint=OFF, 
        modelPrint=OFF, contactPrint=OFF, historyPrint=OFF, userSubroutine='', 
        scratch='', resultsFormat=ODB, multiprocessingMode=DEFAULT, numCpus=1, 
        numGPUs=0)
    mdb.jobs['example01_job01'].submit(consistencyChecking=OFF)


