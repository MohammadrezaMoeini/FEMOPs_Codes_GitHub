# -*- coding: utf-8 -*-
"""
Created on Fri Dec 15 15:31:40 2023
@author: Mohammadreza Moeini


This script includes the required functions to run the FE simulation of the beam.
Insert the properties with mm, N, s
"""

from abaqus import *
from abaqusConstants import *
import __main__
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
    
    
def beam_geometry(L):
    """
    Create the beam with a dimension of L
    
    Parameters
    ----------
        L: the length of the beam (mm)
    """
    
    s1 = mdb.models['Model-1'].ConstrainedSketch(name='__profile__', 
        sheetSize=1200.0)
    g, v, d, c = s1.geometry, s1.vertices, s1.dimensions, s1.constraints
    s1.setPrimaryObject(option=STANDALONE)
    s1.Line(point1=(0.0, 0.0), point2=(L, 0.0))
    s1.HorizontalConstraint(entity=g[2], addUndoState=False)
    p = mdb.models['Model-1'].Part(name='beam', dimensionality=TWO_D_PLANAR, 
        type=DEFORMABLE_BODY)
    p = mdb.models['Model-1'].parts['beam']
    p.BaseWire(sketch=s1)
    s1.unsetPrimaryObject()
    p = mdb.models['Model-1'].parts['beam']
    session.viewports['Viewport: 1'].setValues(displayedObject=p)
    del mdb.models['Model-1'].sketches['__profile__']

def material(material_name, E, v):
    """
    Defines the material properties.  

    Parameters
    ----------
    material_name: name of the material (string)
    E: Youngs modulus of the material (float)
    v: Poisson's ratio (float)
    
    """
    mdb.models['Model-1'].Material(name = material_name)
    mdb.models['Model-1'].materials[material_name].Elastic(table=((E, v), ))

def Section(width, hight):
    """
    Creates and asign the section with a dimension of  width*hight

    Parameters
    ----------
    width: The width of the beam cross section (float)
    hight: The hight of the beam cross section (float)
    """
    
    mdb.models['Model-1'].RectangularProfile(name='Profile-1', a=width, b=hight)
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

    a1 = mdb.models['Model-1'].rootAssembly
    a1.DatumCsysByDefault(CARTESIAN)
    p = mdb.models['Model-1'].parts['beam']
    a1.Instance(name='beam-1', part=p, dependent=ON)

def Step():
    """
    Defines static step.

    """
    mdb.models['Model-1'].StaticStep(name='Step-1', previous='Initial')


def Bounday_conditions():
    """
    Apply a fixed boundary conditions on the left side (point 0,0).
    (i.e.; all DOF are fixed U1=U2=0 and UR=0) at the initial point which is the 
    clamped boundary condition or cantilever beam.

    """
    a = mdb.models['Model-1'].rootAssembly
    v1 = a.instances['beam-1'].vertices
    verts1 = v1.getSequenceFromMask(mask=('[#1 ]', ), )
    region = a.Set(vertices=verts1, name='Set-1')
    mdb.models['Model-1'].DisplacementBC(name='BC-1', createStepName='Step-1', 
        region=region, u1=0.0, u2=0.0, ur3=0.0, amplitude=UNSET, fixed=OFF, 
        distributionType=UNIFORM, fieldName='', localCsys=None)
    
def Loading(F1, F2):   
    """
    Applied force vector of (F1, F2) at the ending point of the beam (L, 0)
    
    Parameters
    ----------
    F1: Force a value Iin direction of x or 1 (float)
    F2: Force a value Iin direction of y or 2 (float)

    """
    a = mdb.models['Model-1'].rootAssembly
    v1 = a.instances['beam-1'].vertices
    verts1 = v1.getSequenceFromMask(mask=('[#2 ]', ), )
    region = a.Set(vertices=verts1, name='Set-2')
    mdb.models['Model-1'].ConcentratedForce(name='Load-1', createStepName='Step-1', 
        region=region, cf1=F1, cf2=F2, distributionType=UNIFORM, field='', 
        localCsys=None)


def Mesh(element_size):
    """
    Mesh the beam with an element size of element_size.
    It creates linear element:
        B21:  A 2-node linear beam in a plane.

    Parameters
    ----------
    element_size: element size of the beam
    hight: The hight of the beam cross section (float)
    """
    p = mdb.models['Model-1'].parts['beam']
    p.seedPart(size=element_size, deviationFactor=0.1, minSizeFactor=0.1)
    p.generateMesh()
    a1 = mdb.models['Model-1'].rootAssembly
    a1.regenerate()

    
def Job(job_name):
    """
    Creates the job and submit it to run the simulation

    Parameters
    ----------
    job_name: name of the job (string)
    
    """
    mdb.Job(name= job_name, model='Model-1', description='', type=ANALYSIS, 
        atTime=None, waitMinutes=0, waitHours=0, queue=None, memory=90, 
        memoryUnits=PERCENTAGE, getMemoryFromAnalysis=True, 
        explicitPrecision=SINGLE, nodalOutputPrecision=SINGLE, echoPrint=OFF, 
        modelPrint=OFF, contactPrint=OFF, historyPrint=OFF, userSubroutine='', 
        scratch='', resultsFormat=ODB, multiprocessingMode=DEFAULT, numCpus=1, 
        numGPUs=0)
    mdb.jobs[job_name].submit(consistencyChecking=OFF)



def Run_simulation(L, material_name, 
                   E, v, width, hight, F1, F2, element_size, job_name):
    beam_geometry(L)
    material(material_name, E, v)
    Section(width, hight)
    Step()
    Bounday_conditions()
    Loading(F1, F2)
    Mesh(element_size)
    Job(job_name)

L = 1000.0 # mm
material_name = "Steel"
E = 200e3 # MPa 
v = 0.3
width = 100.0 # mm
hight = 20.0 # mm
F1 = 0.0 # N
F2 = -100.0 # N
element_size = 100.0 # mm
job_name = "example01_test01"

Run_simulation(L, 
               material_name, E, v, 
               width, hight, 
               F1, F2, 
               element_size,
               job_name)


