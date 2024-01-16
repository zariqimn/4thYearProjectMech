# -*- coding: mbcs -*-
from part import *
from material import *
from section import *
from assembly import *
from step import *
from interaction import *
from load import *
from mesh import *
from optimization import *
from job import *
from sketch import *
from visualization import *
from connectorBehavior import *
import os
from odbAccess import *



def dynamic_explicit(filepath,filename, directory):
    
    def job_(filepath, filename, directory):
        os.chdir(directory)
        mdb.ModelFromInputFile(inputFileName=
            filepath, name=filename) 
        del mdb.models['Model-1']
        mdb.models[filename].Material(name='PA12')
        mdb.models[filename].materials['PA12'].Density(table=((1.02e-09, ), ))
        mdb.models[filename].materials['PA12'].Elastic(table=((1731.0, 0.3), ))
        mdb.models[filename].materials['PA12'].Plastic(table=((41.004, 0.0), (
            42.398, 0.005), (43.792, 0.01), (45.186, 0.015), (46.218, 0.02), (47.221, 
            0.025), (48.223, 0.03), (49.225, 0.035), (50.063, 0.04), (50.444, 0.045), (
            50.825, 0.05), (51.206, 0.055), (51.587, 0.06), (51.968, 0.065), (52.251, 
            0.07), (52.502, 0.075), (52.752, 0.08), (53.003, 0.085), (53.267, 0.09), (
            53.662, 0.095), (54.057, 0.1), (54.451, 0.105), (54.846, 0.11), (55.241, 
            0.115), (55.436, 0.12), (55.573, 0.125), (55.709, 0.13), (55.845, 0.135), (
            55.982, 0.14), (56.117, 0.145), (56.251, 0.15), (56.385, 0.155), (56.519, 
            0.16)))
        mdb.models[filename].HomogeneousSolidSection(material='PA12', name=
            'Section-1', thickness=None)
        mdb.models[filename].parts['PART-1'].Set(elements=
            mdb.models[filename].parts['PART-1'].elements.getSequenceFromMask(
            mask=('[#ffffffff:50000 #fffff ]', ), ), name='Set-1')
        mdb.models[filename].parts['PART-1'].SectionAssignment(offset=0.0, 
            offsetField='', offsetType=MIDDLE_SURFACE, region=
            mdb.models[filename].parts['PART-1'].sets['Set-1'], sectionName=
            'Section-1', thicknessAssignment=FROM_SECTION)
        mdb.models[filename].rootAssembly.regenerate()
        mdb.models[filename].ExplicitDynamicsStep(improvedDtMethod=ON, 
            massScaling=((SEMI_AUTOMATIC, MODEL, AT_BEGINNING, 0.0, 5e-05, BELOW_MIN, 
            0, 0, 0.0, 0.0, 0, None), ), name='Step-1', previous='Initial', timePeriod=
            0.09)
        mdb.models[filename].fieldOutputRequests['F-Output-1'].setValues(
            variables=('MISES', 'U', 'RF', 'EVF', 'MVF'))
        mdb.models[filename].HistoryOutputRequest(createStepName='Step-1', name=
            'H-Output-2', rebar=EXCLUDE, region=
            mdb.models[filename].rootAssembly.sets['NODESET2'], sectionPoints=
            DEFAULT, variables=('U3', 'RF3'))
        mdb.models[filename].historyOutputRequests['H-Output-2'].setValues(
            numIntervals=100)
        mdb.models[filename].historyOutputRequests['H-Output-1'].setValues(
            numIntervals=200)
        mdb.models[filename].ContactProperty('IntProp-1')
        mdb.models[filename].interactionProperties['IntProp-1'].TangentialBehavior(
            dependencies=0, directionality=ISOTROPIC, elasticSlipStiffness=None, 
            formulation=PENALTY, fraction=0.005, maximumElasticSlip=FRACTION, 
            pressureDependency=OFF, shearStressLimit=None, slipRateDependency=OFF, 
            table=((0.3, ), ), temperatureDependency=OFF)
        mdb.models[filename].interactionProperties['IntProp-1'].NormalBehavior(
            allowSeparation=ON, constraintEnforcementMethod=DEFAULT, 
            pressureOverclosure=HARD)
        mdb.models[filename].ContactExp(createStepName='Step-1', name='Int-1')
        mdb.models[filename].interactions['Int-1'].includedPairs.setValuesInStep(
            stepName='Step-1', useAllstar=ON)
        mdb.models[filename].interactions['Int-1'].contactPropertyAssignments.appendInStep(
            assignments=((GLOBAL, SELF, 'IntProp-1'), ), stepName='Step-1')
        mdb.models[filename].EncastreBC(createStepName='Step-1', localCsys=None, 
            name='BC-1', region=
            mdb.models[filename].rootAssembly.sets['NODESET1'])
        mdb.models[filename].SmoothStepAmplitude(data=((0.0, 0.0), (0.09, 1.0)), 
            name='Amp-1', timeSpan=STEP)
        mdb.models[filename].VelocityBC(amplitude='Amp-1', createStepName=
            'Step-1', distributionType=UNIFORM, fieldName='', localCsys=None, name=
            'BC-2', region=mdb.models[filename].rootAssembly.sets['NODESET2'], 
            v1=UNSET, v2=UNSET, v3=5000.0, vr1=UNSET, vr2=UNSET, vr3=UNSET)
        mdb.models[filename].boundaryConditions['BC-1'].move('Step-1', 'Initial')
        sim_job = mdb.Job(activateLoadBalancing=False, atTime=None, contactPrint=OFF, 
            description='', echoPrint=OFF, explicitPrecision=SINGLE, historyPrint=OFF, 
            memory=90, memoryUnits=PERCENTAGE, model=filename, modelPrint=OFF, 
            multiprocessingMode=DEFAULT, name=filename, nodalOutputPrecision=SINGLE, 
            numCpus=1, numDomains=1, parallelizationMethodExplicit=DOMAIN, queue=None, 
            resultsFormat=ODB, scratch='', type=ANALYSIS, userSubroutine='', waitHours=
            0, waitMinutes=0)
        sim_job.submit(consistencyChecking=OFF)
        sim_job.waitForCompletion()
        path = r'D:\Temp\mohdhisham_m\playground\\model_abaqus_files\\' + filename+'\\'+filename+'.cae'
        mdb.saveAs(path)
        
        
        
        odb_name = filename + '.odb'
        f = session.openOdb(name= odb_name)
        Internal_Energy =f.steps['Step-1'].historyRegions['Assembly ASSEMBLY'].historyOutputs['ALLIE'].data[-1][-1]
        Elastic_energy =f.steps['Step-1'].historyRegions['Assembly ASSEMBLY'].historyOutputs['ALLSE'].data[-1][-1]
        plastic_energy=f.steps['Step-1'].historyRegions['Assembly ASSEMBLY'].historyOutputs['ALLPD'].data[-1][-1]
        combined_data = [str(Internal_Energy), str(Elastic_energy), str(plastic_energy)]
        
        
        text_file_name = filename + 'data.txt'
        with open(text_file_name,'w') as file_data:
            file_data.write('\n'.join(combined_data))
            
        mdb.close()
        
        
        
        
            
            
    job_(filepath, filename, directory)

    #
# Save by mohdhisham_m on 2023_05_04-16.57.45; build 2018 2017_11_07-17.21.41 127140


