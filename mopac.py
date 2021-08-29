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
debug = False


def getOptions():
    userOptions = {}

    userOptions['Title'] = {}
    userOptions['Title']['type'] = 'string'
    userOptions['Title']['default'] = ''

    userOptions['Processor Cores'] = {}
    userOptions['Processor Cores']['type'] = 'integer'
    userOptions['Processor Cores']['default'] = 1
    userOptions['Processor Cores']['minimum'] = 1

    userOptions['Calculation Type'] = {}
    userOptions['Calculation Type']['type'] = "stringList"
    userOptions['Calculation Type']['default'] = 1
    userOptions['Calculation Type']['values'] = \
        ['Single Point', 'Equilibrium Geometry', 'Frequencies', 'Transition State']

    userOptions['Theory'] = {}
    userOptions['Theory']['type'] = "stringList"
    userOptions['Theory']['default'] = 3
    userOptions['Theory']['values'] = \
        ['AM1', 'PM3', 'PM6', 'PM7', 'RM1', 'MNDO', 'MNDOD']

    userOptions['Filename Base'] = {}
    userOptions['Filename Base']['type'] = 'string'
    userOptions['Filename Base']['default'] = 'job'

    userOptions['Multiplicity'] = {}
    userOptions['Multiplicity']['type'] = "integer"
    userOptions['Multiplicity']['default'] = 1
    userOptions['Multiplicity']['minimum'] = 1
    userOptions['Multiplicity']['maximum'] = 6

    userOptions['Charge'] = {}
    userOptions['Charge']['type'] = "integer"
    userOptions['Charge']['default'] = 0
    userOptions['Charge']['minimum'] = -9
    userOptions['Charge']['maximum'] = 9


    userOptions['COSMO'] = {}
    userOptions['COSMO']['type'] = "boolean"
    userOptions['COSMO']['default'] = True

    userOptions['Solvent'] = {}
    userOptions['Solvent']['type'] = "stringList"
    userOptions['Solvent']['default'] = "Water"
    userOptions['Solvent']['toolTip'] = 'Solvent'
    userOptions['Solvent']['values'] = \
        ["OTHER", "Acetic acid", "Acetone", "Acetonitrile", "Anisole", "Benzene",
        "Bromobenzene", "Carbon disulfide", "Carbon tetrachloride",
        "Chlorobenzene", "Chloroform", "Cyclohexane", "Dibutyl ether",
        "o-Dichlorobenzene", "1,2-Dichloroethane", "Dichloromethane",
        "Diethylamine", "Diethylether", "1,2-Dimethoxyethane",
        "N,N-Dimethylacetamide", "N,N-Dimethylformamide",
        "Dimethylsulfoxide", "1,4-Dioxane", "Ethanol",
        "Ethyl acetate", "Ethyl benzoate", "Formamide",
        "Hexamethylphosphoramide", "Isopropyl lcohol",
        "Methanol", "2-Methyl-2-propanol", "Nitrobenzene",
        "Nitromethane", "Pyridine", "Tetrahydrofuran",
        "Toluene", "Trichloroethylene", "Triethylamine",
        "Trifluoroacetic acid", "2,2,2-Trifluoroethanol",
        "Water", "o-Xylene"]

    userOptions['Other Solvent Dielectric'] = {}
    userOptions['Other Solvent Dielectric']['type'] = 'string'
    userOptions['Other Solvent Dielectric']['default'] = '0.00'
    
    userOptions['HF Type'] = {}
    userOptions['HF Type']['type'] = "stringList"
    userOptions['HF Type']['default'] = 'RHF'
    userOptions['HF Type']['toolTip'] = "Open or closed shell"
    userOptions['HF Type']['values'] = ['RHF', 'UHF']

    # TODO Coordinate format (need zmatrix)

    opts = {'userOptions': userOptions}

    return opts


def generateInputFile(opts):
    # Extract options:
    title = opts['Title']
    calculate = opts['Calculation Type']
    theory = opts['Theory']
    multiplicity = opts['Multiplicity']
    charge = opts['Charge']
    nCores = int(opts['Processor Cores'])
    solvent = opts['Solvent']
    optionaldielectric = opts['Other Solvent Dielectric']
    hftype = opts['HF Type']
    cosmo = opts['COSMO']
    solventlist = {"Acetic acid": 6.15, "Acetone": 20.7, "Acetonitrile": 37.5,
    "Anisole": 4.33, "Benzene": 2.27, "Bromobenzene": 5.17, "Carbon disulfide": 2.6,
    "Carbon tetrachloride": 2.24, "Chlorobenzene": 5.62, "Chloroform": 4.81,
    "Cyclohexane": 2.02, "Dibutyl ether": 3.1, "o-Dichlorobenzene": 9.93,
    "1,2-Dichloroethane": 10.36, "Dichloromethane": 8.93, "Diethylamine": 3.6,
    "Diethylether": 4.33, "1,2-Dimethoxyethane": 7.2, "N,N-Dimethylacetamide": 37.8,
    "N,N-Dimethylformamide": 36.7, "Dimethylsulfoxide": 46.7, "1,4-Dioxane": 2.25,
    "Ethanol": 24.5, "Ethyl acetate": 6.02, "Ethyl benzoate": 6.02, "Formamide": 111,
    "Hexamethylphosphoramide": 30, "Isopropyl lcohol": 17.9, "Methanol": 32.7,
    "2-Methyl-2-propanol": 10.9, "Nitrobenzene": 34.82, "Nitromethane": 35.87,
    "Pyridine": 12.4, "Tetrahydrofuran": 7.58, "Toluene": 2.38, "Trichloroethylene": 3.4,
    "Triethylamine": 2.42, "Trifluoroacetic acid": 8.55, "2,2,2-Trifluoroethanol": 8.55,
    "Water": 80.1, "o-Xylene": 2.57}

    output = ''

    # Multiplicity
    multStr = ''
    if multiplicity == 1:
        multStr = 'SINGLET'
    elif multiplicity == 2:
        multStr = 'DOUBLET'
    elif multiplicity == 3:
        multStr = 'TRIPLET'
    elif multiplicity == 4:
        multStr = 'QUARTET'
    elif multiplicity == 5:
        multStr = 'QUINTET'
    elif multiplicity == 6:
        multStr = 'SEXTET'
    else:
        raise Exception('Unhandled multiplicity: %d' % multiplicity)

    # Calculation type:
    calcStr = ''
    if calculate == 'Single Point':
        calcStr = 'NOOPT'
    elif calculate == 'Equilibrium Geometry':
        pass
    elif calculate == 'Frequencies':
        calcStr = 'FORCE'
    elif calculate == 'Transition State':
        calcStr = 'SADDLE'
    else:
        raise Exception('Unhandled calculation type: %s' % calculate)

    eps = ""
    dielectric = ""
    if solvent == "OTHER":
        dielectric = optionaldielectric
    else:
        dielectric = str(solventlist[solvent])

    if cosmo == True:
        eps = "EPS=" + dielectric

    if multiplicity > 1:
        hftype = 'UHF'

    # Charge, mult, calc type, theory:
    output += ' AUX LARGE CHARGE=%d %s %s %s %s PDBOUT THREADS=%d %s\n' %\
        (charge, multStr, calcStr, theory, eps, nCores, hftype)

    # Title
    output += '%s\n\n' % title

    # Coordinates
    if calculate == 'Single Point':
        output += '$$coords:Sx0y0z0$$\n'
    else:
        output += '$$coords:Sx1y1z1$$\n'

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
    files.append({'filename': '%s.mop' % baseName, 'contents': inp})
    if debug:
        files.append({'filename': 'debug_info', 'contents': stdinStr})
    result['files'] = files
    # Specify the main input file. This will be used by MoleQueue to determine
    # the value of the $$inputFileName$$ and $$inputFileBaseName$$ keywords.
    result['mainFile'] = '%s.mop' % baseName
    return result

if __name__ == "__main__":
    parser = argparse.ArgumentParser('Generate a MOPAC input file.')
    parser.add_argument('--debug', action='store_true')
    parser.add_argument('--print-options', action='store_true')
    parser.add_argument('--generate-input', action='store_true')
    parser.add_argument('--display-name', action='store_true')
    parser.add_argument('--lang', nargs='?', default='en')
    args = vars(parser.parse_args())

    debug = args['debug']

    if args['display_name']:
        print("MOPAC")
    if args['print_options']:
        print(json.dumps(getOptions()))
    elif args['generate_input']:
        print(json.dumps(generateInput()))
