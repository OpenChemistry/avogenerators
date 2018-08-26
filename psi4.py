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
targetName = 'Psi'
debug = False


def getOptions():
    userOptions = {}

    userOptions['Title'] = {}
    userOptions['Title']['type'] = 'string'
    userOptions['Title']['default'] = ''
    userOptions['Title']['toolTip'] = 'Title of the input file'

    userOptions['Calculation Type'] = {}
    userOptions['Calculation Type']['type'] = 'stringList'
    userOptions['Calculation Type']['default'] = 1
    userOptions['Calculation Type']['toolTip'] = 'Type of calculation to perform'
    userOptions['Calculation Type']['values'] = \
        ['Single Point', 'Geometry Optimization', 'Frequencies']

    userOptions['Theory'] = {}
    userOptions['Theory']['type'] = 'stringList'
    userOptions['Theory']['default'] = 7
    userOptions['Theory']['toolTip'] = 'Hamiltonian or DFT method to use'
    userOptions['Theory']['values'] = \
        ['HF', 'MP2', 'CCSD', 'CCSD(T)', 'B3LYP-D', 'B97-D', 'wB97X-D',
        'SAPT0', 'SAPT2' ]

    userOptions['Basis'] = {}
    userOptions['Basis']['type'] = 'stringList'
    userOptions['Basis']['default'] = 3
    userOptions['Basis']['toolTip'] = 'Gaussian basis set'
    userOptions['Basis']['values'] = \
        ['6-31G(d)', 'cc-pVDZ', 'aug-cc-pVTZ', 'def2-SVP', 'ma-def2-SVP',
        'def2-SVPD', 'def2-TZVP', 'def2-QZVP', 'pc-2', 'aug-pc-2']

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

    # Convert to code-specific strings
    calcStr = ''
    if calculate == 'Single Point':
        calcStr = 'energy'
    elif calculate == 'Geometry Optimization':
        calcStr = 'optimize'
    elif calculate == 'Frequencies':
        calcStr = 'frequencies'
    else:
        raise Exception('Unhandled calculation type: %s' % calculate)

    output = ''
    output += 'set basis {}\n'.format(basis)
    output += 'molecule {\n'
    output += '* xyz {} {}\n'.format(charge, multiplicity)
    output += '$$coords:___Sxyz$$\n'
    output += '}\n'
    if 'SAPT' in theory:
        output += 'auto_fragments(\'\')\n'
    output += '{}({})\n'.format(calcStr, theory)

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
    files.append({'filename': '%s.in' % baseName, 'contents': inp})
    if debug:
        files.append({'filename': 'debug_info', 'contents': stdinStr})
    result['files'] = files
    # Specify the main input file. This will be used by MoleQueue to determine
    # the value of the $$inputFileName$$ and $$inputFileBaseName$$ keywords.
    result['mainFile'] = '%s.in' % baseName
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
