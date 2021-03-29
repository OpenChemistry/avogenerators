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
targetName = 'PYSCF'
extension = 'py'
debug = False
basis_list = ['STO-3G', '3-21g', 'cc-pvdz']
theory_list = ['RHF', 'ROHF', 'UHF', 'MP2']


def getOptions():
    userOptions = {}

    userOptions['Title'] = {}
    userOptions['Title']['type'] = 'string'
    userOptions['Title']['default'] = ''

    userOptions['Calculation Type'] = {}
    userOptions['Calculation Type']['type'] = 'stringList'
    userOptions['Calculation Type']['default'] = 0
    userOptions['Calculation Type']['values'] = \
        ['Single Point']

    userOptions['Theory'] = {}
    userOptions['Theory']['type'] = 'stringList'
    userOptions['Theory']['default'] = 0
    userOptions['Theory']['values'] = theory_list

    userOptions['Basis'] = {}
    userOptions['Basis']['type'] = 'stringList'
    userOptions['Basis']['default'] = 0
    userOptions['Basis']['values'] = basis_list

    userOptions['Filename Base'] = {}
    userOptions['Filename Base']['type'] = 'string'
    userOptions['Filename Base']['default'] = 'job'

    userOptions['Charge'] = {}
    userOptions['Charge']['type'] = 'integer'
    userOptions['Charge']['default'] = 0
    userOptions['Charge']['minimum'] = -9
    userOptions['Charge']['maximum'] = 9

    userOptions['Multiplicity'] = {}
    userOptions['Multiplicity']['type'] = 'integer'
    userOptions['Multiplicity']['default'] = 1
    userOptions['Multiplicity']['minimum'] = 1
    userOptions['Multiplicity']['maximum'] = 6

    opts = {'userOptions': userOptions}
    opts['inputMoleculeFormat'] = 'cjson'

    return opts


def generateInputFile(cjson, opts):
    title = opts['Title']
    calculate = opts['Calculation Type']
    theory = opts['Theory']
    basis = opts['Basis']
    charge = opts['Charge']
    multiplicity = opts['Multiplicity']

    # Convert to code-specific strings
    basisStr = ''
    if basis in basis_list:
        if basis == '3-21g':
            pybasis = '321g'
            basisStr = pybasis
        if basis == 'cc-pvdz':
            pybasis = 'ccpvdz'
            basisStr = pybasis
        else:
            basisStr = basis
    else:
        raise Exception('Unhandled basis type: {}'.format(basis))

    theoryImport = ''
    theoryLines = []
    # Intentionally not using elif here:
    if theory == 'RHF':
        theoryImport = "from pyscf import gto,scf\n"
        theoryLines.append('mf = scf.{}(mol)\n'.format(theory))
        theoryLines.append('mf.kernel()\n')
    elif theory == 'ROHF':
        theoryImport = "from pyscf import gto,scf\n"
        theoryLines.append('mf = scf.{}(mol)\n'.format(theory))
        theoryLines.append('Amf.kernel()\n')
    elif theory == 'UHF':
        theoryImport = "from pyscf import gto,scf\n"
        theoryLines.append('mf = scf.{}(mol)\n'.format(theory))
        theoryLines.append('mf.kernel()\n')
    elif theory == 'MP2':
        theoryImport = "from pyscf import gto,scf,mp\n"
        theoryLines.append('# Must run SCF before MP2 in PYSCF\n')
        if multiplicity == 1:
            theoryLines.append('mf = scf.RHF(mol)\n')
            theoryLines.append('mf.kernel()\n')
            theoryLines.append('mf2 = mp.{}(mf)\n'.format(theory))
            theoryLines.append('mf2.kernel()\n')
        else:
            theoryLines.append('mf = scf.UHF(mol)\n')
            theoryLines.append('mf.kernel()\n')
            theoryLines.append('mf2 = mp.{}(mf)\n'.format(theory))
            theoryLines.append('mf2.kernel()\n')
    else:
        raise Exception('Unhandled theory type:'.format(theory))

    calcStr = ''
    if calculate == 'Single Point':
        pass
    else:
        raise Exception('Unhandled calculation type:'.format(calculate))

    # Create input file
    output = ''
    output += "# Title: {}\n".format(title)
    output += "{}".format(theoryImport)
    output += "mol = gto.Mole()\n"
    output += "mol.atom = '''\n"
    output += '$$coords:___Sxyz$$\n'
    output += "'''\n"
    output += 'mol.basis = \'{}\'\n'.format(basisStr)
    output += 'mol.charge = {}\n'.format(charge)
    output += 'mol.spin = {}\n'.format(multiplicity - 1)
    output += 'mol.build()\n'
    for line in theoryLines:
        output += line
    return output


def generateInput():
    # Read options from stdin
    stdinStr = sys.stdin.read()

    # Parse the JSON strings
    opts = json.loads(stdinStr)

    # Generate the input file
    inp = generateInputFile(opts['cjson'], opts['options'])

    # Basename for input files:
    baseName = opts['options']['Filename Base']

    # Prepare the result
    result = {}
    # Input file text -- will appear in the same order in the GUI as they are
    # listed in the array:
    files = []
    files.append({'filename': '{}.{}'.format(
        baseName, extension), 'contents': inp})
    if debug:
        files.append({'filename': 'debug_info', 'contents': stdinStr})
    result['files'] = files
    # Specify the main input file. This will be used by MoleQueue to determine
    # the value of the $$inputFileName$$ and $$inputFileBaseName$$ keywords.
    result['mainFile'] = '{}.{}'.format(baseName, extension)
    return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        'Generate a {} input file.'.format(targetName))
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
