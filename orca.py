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
targetName = "ORCA"
debug = False


def getOptions():
    userOptions = {"tabName": "Basic"}

    userOptions["Title"] = {
        "type": "string",
        "default": "",
        "toolTip": "Title of the input file",
    }

    userOptions["Processor Cores"] = {
        "type": "integer",
        "default": 1,
        "minimum": 1,
    }

    userOptions["Memory"] = {
        "type": "integer",
        "default": 16,
        "minimum": 1,
    }

    userOptions["Calculation Type"] = {
        "type": "stringList",
        "default": 1,
        "values": [
            "Single Point",
            "Geometry Optimization",
            "Frequencies",
            "Transition State",
            "Dynamics",
        ],
        "toolTip": "Type of calculation to perform",
    }

    userOptions["Print Molecular Orbitals"] = {
        "type": "boolean",
        "default": False,
    }

    userOptions["Theory"] = {
        "type": "stringList",
        "default": 7,
        "values": [
            "HF",
            "MP2",
            "CCSD",
            "CCSD(T)",
            "BLYP",
            "PBE",
            "PBE0",
            "revPBE",
            "B3LYP",
            "B97-3C",
            "M06L",
            "M062X",
            "wB97X-D3",
        ],
    }

    userOptions["RI Approximation"] = {
        "type": "stringList",
        "default": 0,
        "values": ["None", "NORI", "RIJK", "RIJONX", "RIJCOSX"],
    }

    userOptions["Dispersion Correction"] = {
        "type": "stringList",
        "default": 0,
        "values": ["None", "D3ZERO", "D3BJ", "D4"],
        "toolTip": "Any added dispersion corrections",
        "hide": True,
    }

    userOptions["Basis"] = {
        "type": "stringList",
        "default": 8,
        "values": [
            "6-31G(d)",
            "cc-pVDZ",
            "cc-pVTZ",
            "cc-pVQZ",
            "aug-cc-pVDZ",
            "aug-cc-pVTZ",
            "aug-cc-pVQZ",
            "def2-SVP",
            "def2-TZVP",
            "def2-QZVP",
            "def2-TZVPP",
            "def2-QZVPP",
            "def2-TZVPPD",
            "def2-QZVPPD",
            "ma-def2-SVP",
            "ma-def2-TZVP",
            "ma-def2-QZVP",
        ],
        "toolTip": "Gaussian basis set",
    }

    userOptions["Solvation"] = {
        "type": "stringList",
        "default": 0,
        "values": [
            "None (gas)",
            "-",
            "Water",
            "Acetonitrile",
            "Acetone",
            "Ethanol",
            "Methanol",
            "CCl4",
                    "CH2Cl2",
        "Chloroform",
        "DMSO",
        "DMF",
        "Hexane",
        "Toluene",
        "Pyridine",
        "THF",
        "Toluene",
        ],
        "toolTip": "Solvent Model",
    }

    userOptions["Solvation Type"] = {
        "type": "stringList",
        "default": 0,
        "values": ["CPCM", "SMD"],
        "toolTip": "Solvent model",
    }

    userOptions["Filename Base"] = {
        "type": "string",
        "default": "job",
    }

    userOptions["Charge"] = {
        "type": "integer",
        "default": 0,
        "minimum": -9,
        "maximum": 9,
        "toolTip": "Total charge of the system",
    }

    userOptions["Multiplicity"] = {
        "type": "integer",
        "default": 1,
        "minimum": 1,
        "maximum": 6,
        "toolTip": "Total spin multiplicity of the system",
    }

    userOptions["AutoAux"] = {
        "type": "boolean",
        "default": False,
        "toolTip": "Automatically select auxiliary basis set",
    }

    aimdOptions = {"tabName": "Dynamics"}
    aimdOptions["AIMD TimeStep"] = {
        "type": "string",
        "default": "0.5_fs",
    }
    aimdOptions["AIMD Initvel"] = {
        "type": "string",
        "default": "350",
    }
    aimdOptions["AIMD Thermostat Temp"] = {
        "type": "integer",
        "default": 300,
        "maximum": 1000,
        "minimum": 0,
    }
    aimdOptions["AIMD Thermostat Time"] = {
        "type": "string",
        "default": "10_fs",
    }
    aimdOptions["AIMD RunTime"] = {
        "type": "integer",
        "default": 200,
    }

    opts = {"userOptions": [userOptions, aimdOptions]}

    return opts


def generateInputFile(opts):
    # Extract options:
    title = opts["Title"]
    calculate = opts["Calculation Type"]
    theory = opts["Theory"]
    basis = opts["Basis"]
    charge = opts["Charge"]
    multiplicity = opts["Multiplicity"]
    nCores = int(opts["Processor Cores"])
    memory = int((opts["Memory"] * 1024) / nCores)
    solvtype = opts["Solvation Type"]
    solvent = opts["Solvation"]
    mos = opts["Print Molecular Orbitals"]
    autoaux = opts["AutoAux"]
    disp = opts["Dispersion Correction"]
    ri = opts["RI Approximation"]
    auxbasis = "None"

    rijbasis = {
        "6-31G(d)": "AutoAux",
        "cc-pVDZ": "Def2/J",
        "cc-pVTZ": "Def2/J",
        "cc-pVQZ": "Def2/J",
        "aug-cc-pVDZ": "AutoAux",
        "aug-cc-pVTZ": "AutoAux",
        "aug-cc-pVQZ": "AutoAux",
        "def2-SVP": "Def2/J",
        "def2-TZVP": "Def2/J",
        "def2-QZVP": "Def2/J",
        "def2-TZVPP": "Def2/J",
        "def2-QZVPP": "Def2/J",
        "def2-TZVPPD": "AutoAux",
        "def2-QZVPPD": "AutoAux",
        "ma-def2-SVP": "AutoAux",
        "ma-def2-TZVP": "AutoAux",
        "ma-def2-QZVP": "AutoAux",
    }

    rijkbasis = {
        "6-31G(d)": "AutoAux",
        "cc-pVDZ": "cc-pVDZ/JK",
        "cc-pVTZ": "cc-pVTZ/JK",
        "cc-pVQZ": "cc-pVQZ/JK",
        "aug-cc-pVDZ": "aug-cc-pVDZ/JK",
        "aug-cc-pVTZ": "aug-cc-pVTZ/JK",
        "aug-cc-pVQZ": "aug-cc-pVQZ/JK",
        "def2-SVP": "Def2/JK",
        "def2-TZVP": "Def2/JK",
        "def2-QZVP": "Def2/JK",
        "def2-TZVPP": "Def2/JK",
        "def2-QZVPP": "Def2/JK",
        "def2-TZVPPD": "aug-cc-pVTZ/JK",
        "def2-QZVPPD": "aug-cc-pVQZ/JK",
        "ma-def2-SVP": "aug-cc-pVDZ/JK",
        "ma-def2-TZVP": "aug-cc-pVTZ/JK",
        "ma-def2-QZVP": "aug-cc-pVQZ/JK",
    }

    # Convert to code-specific strings
    calcStr = ""
    if calculate == "Single Point":
        calcStr = "SP"
    elif calculate == "Geometry Optimization":
        calcStr = "Opt"
    elif calculate == "Frequencies":
        calcStr = "Opt Freq"
    elif calculate == "Dynamics":
        calcStr = "MD"
    elif calculate == "Transition State":
        calcStr = "OptTS"
    else:
        raise Exception("Unhandled calculation type: %s" % calculate)

    solvation = ""
    if not "None" in opts["Solvation"] and solvtype == "CPCM":
        solvation = "CPCM(" + solvent + ")"
    elif not "None" in opts["Solvation"] and solvtype == "SMD":
        solvation = "CPCM"

    if disp == "None":
        disp = ""
    else:
        disp = " " + disp

    if ri in ["None", "NORI"]:
        autoaux = False
        ri = ""
    else:
        if ri in ["RIJONX", "RIJCOSX"]:
            auxbasis = rijbasis[basis]
        else:
            auxbasis = rijkbasis[basis]
        ri = " " + ri

    if autoaux == True:
        auxbasis = "AutoAux"

    if auxbasis != "None":
        basis = basis + " " + auxbasis

    theory = theory + disp + ri

    # put the pieces together
    code = f"{calcStr} {theory} {basis} {solvation}"

    output = ""

    output += "# avogadro generated ORCA file\n"
    output += "# " + title + "\n"
    output += "# \n"
    output += f"! {code}\n\n"
    output += "%maxcore " + str(memory) + "\n\n"
    output += "%pal\n"
    output += "   nprocs " + str(nCores) + "\n"
    output += "end\n\n"
    if not "None" in opts["Solvation"] and solvtype == "SMD":
        output += "%cpcm\n"
        output += "   smd true\n"
        output += '   SMDSolvent "' + solvent + '"\n'
        output += "end\n\n"

    if calcStr == "MD":
        output += "%md\n"
        output += "   timestep " + opts["AIMD TimeStep"] + "\n"
        output += "   initvel " + opts["AIMD Initvel"] + "_k\n"
        output += (
            "   thermostat berendsen "
            + str(opts["AIMD Thermostat Temp"])
            + "_k timecon "
            + opts["AIMD Thermostat Time"]
            + "\n"
        )
        output += '   dump position stride 1 filename "trajectory.xyz"\n'
        output += "   run " + str(opts["AIMD RunTime"]) + "\n"
        output += "end\n\n"

    if mos == True:
        output += "%output\n"
        output += "   print[p_mos] 1\n"
        output += "   print[p_basis] 2\n"
        output += "end\n\n"

    output += f"* xyz {charge} {multiplicity}\n"
    output += "$$coords:___Sxyz$$\n"
    output += "*\n\n\n"

    return output


def generateInput():
    # Read options from stdin
    stdinStr = sys.stdin.read()

    # Parse the JSON strings
    opts = json.loads(stdinStr)

    # Generate the input file
    inp = generateInputFile(opts["options"])

    # Basename for input files:
    baseName = opts["options"]["Filename Base"]

    # Prepare the result
    result = {}
    # Input file text -- will appear in the same order in the GUI as they are
    # listed in the array:
    files = []
    files.append({"filename": "%s.inp" % baseName, "contents": inp})
    if debug:
        files.append({"filename": "debug_info", "contents": stdinStr})
    result["files"] = files
    # Specify the main input file. This will be used by MoleQueue to determine
    # the value of the $$inputFileName$$ and $$inputFileBaseName$$ keywords.
    result["mainFile"] = "%s.inp" % baseName
    return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser("Generate a %s input file." % targetName)
    parser.add_argument("--debug", action="store_true")
    parser.add_argument("--print-options", action="store_true")
    parser.add_argument("--generate-input", action="store_true")
    parser.add_argument("--display-name", action="store_true")
    parser.add_argument("--lang", nargs="?", default="en")
    args = vars(parser.parse_args())

    debug = args["debug"]

    if args["display_name"]:
        print(targetName)
    if args["print_options"]:
        print(json.dumps(getOptions()))
    elif args["generate_input"]:
        print(json.dumps(generateInput()))
