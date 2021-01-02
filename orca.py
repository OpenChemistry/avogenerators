"""
/******************************************************************************
  This source file is part of the Avogadro project.

  This source code is released under the New BSD License, (the "License").
******************************************************************************/
"""

import argparse
import json
import sys

# Some globals:
targetName = 'ORCA'
debug = True


def getOptions():
    userOptions = {}

    userOptions['Title'] = {}
    userOptions['Title']['type'] = 'string'
    userOptions['Title']['default'] = ''
    userOptions['Title']['toolTip'] = 'Title of the input file'

    userOptions['Processor Cores'] = {}
    userOptions['Processor Cores']['type'] = 'integer'
    userOptions['Processor Cores']['default'] = 1
    userOptions['Processor Cores']['minimum'] = 1

    userOptions['Memory'] = {}
    userOptions['Memory']['type'] = 'integer'
    userOptions['Memory']['default'] = 16
    userOptions['Memory']['minimum'] = 1

    userOptions['Calculation Type'] = {}
    userOptions['Calculation Type']['type'] = 'stringList'
    userOptions['Calculation Type']['default'] = 1
    userOptions['Calculation Type']['toolTip'] = 'Type of calculation to perform'
    userOptions['Calculation Type']['values'] = \
        ['Single Point', 'Geometry Optimization', 'Frequencies', 'AIMD']

    userOptions['Print Molecular Orbitals'] = {}
    userOptions['Print Molecular Orbitals']['type'] = 'boolean'
    userOptions['Print Molecular Orbitals']['defaut'] = False

    userOptions['Theory'] = {}
    userOptions['Theory']['type'] = 'stringList'
    userOptions['Theory']['default'] = 7
    userOptions['Theory']['toolTip'] = 'Hamiltonian or DFT method to use'
    userOptions['Theory']['values'] = \
        ['HF', 'MP2', 'CCSD', 'CCSD(T)', 'BLYP', 'PBE', 'PBE0', 'revPBE', 'B3LYP', 'B97-3C', 'M06L Grid6', 'M062X Grid6', 'wB97X-D3' ]

    userOptions['RI Approximation'] = {}
    userOptions['RI Approximation']['type'] = 'stringList'
    userOptions['RI Approximation']['default'] = 0
    userOptions['RI Approximation']['toolTip'] = 'DFT RI Approximation'
    userOptions['RI Approximation']['values'] = \
        ['None', 'NORI', 'RIJK', 'RIJONX', 'RIJCOSX']

    userOptions['Dispersion Correction'] = {}
    userOptions['Dispersion Correction']['type'] = 'stringList'
    userOptions['Dispersion Correction']['default'] = 0
    userOptions['Dispersion Correction']['toolTip'] = 'Any added dispersion corrections'
    userOptions['Dispersion Correction']['values'] = \
        ['None', 'D2', 'D3ZERO', 'D3BJ', 'D4' ]


    userOptions['Basis'] = {}
    userOptions['Basis']['type'] = 'stringList'
    userOptions['Basis']['default'] = 8
    userOptions['Basis']['toolTip'] = 'Gaussian basis set'
    userOptions['Basis']['values'] = \
        ['6-31G(d)',
        'cc-pVDZ', 'cc-pVTZ', 'cc-pVQZ', 
        'aug-cc-pVDZ', 'aug-cc-pVTZ', 'aug-cc-pVQZ', 
        'def2-SVP', 'def2-TZVP', 'def2-QZVP',
        'def2-TZVPP', 'def2-QZVPP',
        'def2-TZVPPD', 'def2-QZVPPD',
        'ma-def2-SVP', 'ma-def2-TZVP', 'ma-def2-QZVP']

    userOptions['Solvation'] = {}
    userOptions['Solvation']['type'] = 'stringList'
    userOptions['Solvation']['default'] = 0
    userOptions['Solvation']['toolTip'] = 'Solvent'
    userOptions['Solvation']['values'] = \
        ['None (gas)', 'Water', 'Acetonitrile', 'Acetone',
        'Ethanol', 'Methanol', 'CH2Cl2', 'Chloroform',
        'DMSO', 'DMF', 'Hexane', 'Toluene',
        'Pyridine', 'THF']

    userOptions['Solvation Type'] = {}
    userOptions['Solvation Type']['type'] = 'stringList'
    userOptions['Solvation Type']['default'] = 'CPCM'
    userOptions['Solvation Type']['toolTip'] = 'Solvent model'
    userOptions['Solvation Type']['values'] = ['CPCM', 'SMD']

    userOptions['Filename Base'] = {}
    userOptions['Filename Base']['type'] = 'string'
    userOptions['Filename Base']['default'] = 'job'

    userOptions['Charge'] = {}
    userOptions['Charge']['type'] = 'integer'
    userOptions['Charge']['default'] = 0
    userOptions['Charge']['toolTip'] = 'Total charge of the system'
    userOptions['Charge']['minimum'] = -9
    userOptions['Charge']['maximum'] = 9

    userOptions['Multiplicity'] = {}
    userOptions['Multiplicity']['type'] = 'integer'
    userOptions['Multiplicity']['default'] = 1
    userOptions['Multiplicity']['toolTip'] = 'Total spin multiplicity of the system'
    userOptions['Multiplicity']['minimum'] = 1
    userOptions['Multiplicity']['maximum'] = 6

    userOptions['AIMD TimeStep'] = {}
    userOptions['AIMD TimeStep']['type'] = 'string'
    userOptions['AIMD TimeStep']['default'] = '0.5_fs'


    userOptions['AIMD Initvel'] = {}
    userOptions['AIMD Initvel']['type'] = 'string'
    userOptions['AIMD Initvel']['default'] = '350'

    userOptions['AIMD Thermostat Temp'] = {}
    userOptions['AIMD Thermostat Temp']['type'] = 'string'
    userOptions['AIMD Thermostat Temp']['default'] = '350'

    userOptions['AIMD Thermostat Time'] = {}
    userOptions['AIMD Thermostat Time']['type'] = 'string'
    userOptions['AIMD Thermostat Time']['default'] = '10_fs'

    userOptions['AIMD RunTime'] = {}
    userOptions['AIMD RunTime']['type'] = 'string'
    userOptions['AIMD RunTime']['default'] = '200'

    userOptions['AutoAux'] = {}
    userOptions['AutoAux']['type'] = 'boolean'
    userOptions['AutoAux']['default'] = False

    opts = {'userOptions': userOptions}

    return opts


def generateInputFile(opts):
    # Extract options:
    title = opts['Title']
    calculate = opts['Calculation Type']
    theory = opts['Theory']
    basis = opts['Basis']
    charge = opts['Charge']
    multiplicity = opts['Multiplicity']
    nCores = int(opts['Processor Cores'])
    memory = int((opts['Memory']*1024)/nCores)
    solvtype = opts['Solvation Type']
    solvent = opts['Solvation']
    mos = opts['Print Molecular Orbitals']
    autoaux = opts['AutoAux']
    disp = opts['Dispersion Correction']
    ri = opts['RI Approximation']
    auxbasis = 'None'

    rijbasis = {'6-31G(d)':'AutoAux',
    'cc-pVDZ':'Def2/J', 'cc-pVTZ':'Def2/J', 'cc-pVQZ':'Def2/J',
    'aug-cc-pVDZ':'AutoAux', 'aug-cc-pVTZ':'AutoAux', 'aug-cc-pVQZ':'AutoAux',
    'def2-SVP':'Def2/J', 'def2-TZVP':'Def2/J', 'def2-QZVP':'Def2/J',
    'def2-TZVPP':'Def2/J', 'def2-QZVPP':'Def2/J',
    'def2-TZVPPD':'AutoAux', 'def2-QZVPPD':'AutoAux',
    'ma-def2-SVP':'AutoAux', 'ma-def2-TZVP':'AutoAux', 'ma-def2-QZVP':'AutoAux'}

    rijkbasis = {'6-31G(d)':'AutoAux',
    'cc-pVDZ':'cc-pVDZ/JK', 'cc-pVTZ':'cc-pVTZ/JK', 'cc-pVQZ':'cc-pVQZ/JK',
    'aug-cc-pVDZ':'aug-cc-pVDZ/JK', 'aug-cc-pVTZ':'aug-cc-pVTZ/JK', 'aug-cc-pVQZ':'aug-cc-pVQZ/JK',
    'def2-SVP':'Def2/JK', 'def2-TZVP':'Def2/JK', 'def2-QZVP':'Def2/JK',
    'def2-TZVPP':'Def2/JK', 'def2-QZVPP':'Def2/JK',
    'def2-TZVPPD':'aug-cc-pVTZ/JK', 'def2-QZVPPD':'aug-cc-pVQZ/JK',
    'ma-def2-SVP':'aug-cc-pVDZ/JK', 'ma-def2-TZVP':'aug-cc-pVTZ/JK', 'ma-def2-QZVP':'aug-cc-pVQZ/JK'}

    # Convert to code-specific strings
    calcStr = ''
    if calculate == 'Single Point':
        calcStr = 'SP'
    elif calculate == 'Geometry Optimization':
        calcStr = 'Opt'
    elif calculate == 'Frequencies':
        calcStr = 'Opt Freq'
    elif calculate == 'AIMD':
        calcStr = 'MD'
    else:
        raise Exception('Unhandled calculation type: %s' % calculate)

    solvation = ''
    if not 'None' in opts['Solvation'] and solvtype == 'CPCM':
        solvation = 'CPCM(' + solvent + ')'
    elif not 'None' in opts['Solvation'] and solvtype == 'SMD':
        solvation = 'CPCM'

    if disp == 'None':
        disp = ''
    else:
        disp = ' ' + disp

    if ri in ['None', 'NORI']:
        autoaux = False
        ri = ''
    else:
        if ri in ['RIJONX', 'RIJCOSX']:
            auxbasis = rijbasis[basis]
        else:
            auxbasis = rijkbasis[basis]
        ri = ' ' + ri
    

    if autoaux == True:
        auxbasis = 'AutoAux'

    if auxbasis != 'None':
        basis = basis + ' ' + auxbasis

    theory = theory + disp + ri

    # put the pieces together
    code = '{} {} {} {}'.format(calcStr, theory, basis, solvation)

    output = ''

    output += '# avogadro generated ORCA file\n'
    output += '# ' + title + '\n'
    output += '# \n'
    output += '! {}\n\n'.format(code)
    output += '%maxcore ' + str(memory) + '\n\n'
    output += '%pal\n'
    output += '   nprocs ' + str(nCores) + '\n'
    output += 'end\n\n'
    if not 'None' in opts['Solvation'] and solvtype == 'SMD':
        output += '%cpcm\n'
        output += '   smd true\n'
        output += '   SMDSolvent \"' + solvent + '\"\n'
        output += 'end\n\n'

    if calcStr == 'MD':
        output += '%md\n'
        output += '   timestep ' + opts['AIMD TimeStep'] + '\n'
        output += '   initvel ' + opts['AIMD Initvel'] + '_k\n'
        output += '   thermostat berendsen ' + opts['AIMD Thermostat Temp'] + '_k timecon ' + opts['AIMD Thermostat Time'] + '\n'
        output += '   dump position stride 1 filename \"trajectory.xyz\"\n'
        output += '   run ' + opts['AIMD RunTime'] + '\n'
        output += 'end\n\n'

    if mos == True:
        output += '%output\n'
        output += '   print[p_mos] 1\n'
        output += '   print[p_basis] 2\n'
        output += 'end\n\n'

    output += '* xyz {} {}\n'.format(charge, multiplicity)
    output += '$$coords:___Sxyz$$\n'
    output += '*\n\n\n'

    return output


def generateInput():
    # Read options from stdin
    stdinStr = sys.stdin.read()

    # Parse the JSON strings
    opts = json.loads(stdinStr)

    # Generate the input file
    inp = generateInputFile(opts['options'])

    # Basename for input files:
    baseName = opts['options']['Filename Base']

    # Prepare the result
    result = {}
    # Input file text -- will appear in the same order in the GUI as they are
    # listed in the array:
    files = []
    files.append({'filename': '%s.inp' % baseName, 'contents': inp})
    if debug:
        files.append({'filename': 'debug_info', 'contents': stdinStr})
    result['files'] = files
    # Specify the main input file. This will be used by MoleQueue to determine
    # the value of the $$inputFileName$$ and $$inputFileBaseName$$ keywords.
    result['mainFile'] = '%s.inp' % baseName
    return result

if __name__ == "__main__":
    parser = argparse.ArgumentParser('Generate a %s input file.' % targetName)
    parser.add_argument('--debug', action='store_true')
    parser.add_argument('--print-options', action='store_true')
    parser.add_argument('--generate-input', action='store_true')
    parser.add_argument('--display-name', action='store_true')
    parser.add_argument('--lang', nargs='?', default='en')
    args = vars(parser.parse_args())

    debug = args['debug']

    if args['display_name']:
        print(targetName)
    if args['print_options']:
        print(json.dumps(getOptions()))
    elif args['generate_input']:
        print(json.dumps(generateInput()))
