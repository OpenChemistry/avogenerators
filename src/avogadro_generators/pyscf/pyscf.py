# SPDX-FileCopyrightText: 2026 Avogadro Project
# SPDX-License-Identifier: BSD 3-Clause
# ******************************************************************************
# This source file is part of the Avogadro project.
#
# This source code is released under the New BSD License, (the "License").
# ******************************************************************************
"""Input generation for PySCF (https://pyscf.org/)."""

basis_list = ["STO-3G", "3-21g", "cc-pvdz"]
theory_list = ["RHF", "ROHF", "UHF", "MP2"]


def generateInputFile(input_json: dict) -> tuple[str, list[str]]:
    # Collect warning strings as we go
    warnings = []

    opts = input_json["options"]
    title = opts["Title"]
    calculate = opts["Calculation Type"]
    theory = opts["Theory"]
    basis = opts["Basis"]
    charge = opts["Charge"]
    multiplicity = opts["Multiplicity"]

    # Convert to code-specific strings
    basisStr = ""
    if basis in basis_list:
        if basis == "3-21g":
            pybasis = "321g"
            basisStr = pybasis
        if basis == "cc-pvdz":
            pybasis = "ccpvdz"
            basisStr = pybasis
        else:
            basisStr = basis
    else:
        warnings.append(f"Unhandled basis type: {basis}")

    theoryImport = ""
    theoryLines = []
    # Intentionally not using elif here:
    if theory == "RHF":
        theoryImport = "from pyscf import gto,scf\n"
        theoryLines.append(f"mf = scf.{theory}(mol)\n")
        theoryLines.append("mf.kernel()\n")
    elif theory == "ROHF":
        theoryImport = "from pyscf import gto,scf\n"
        theoryLines.append(f"mf = scf.{theory}(mol)\n")
        theoryLines.append("Amf.kernel()\n")
    elif theory == "UHF":
        theoryImport = "from pyscf import gto,scf\n"
        theoryLines.append(f"mf = scf.{theory}(mol)\n")
        theoryLines.append("mf.kernel()\n")
    elif theory == "MP2":
        theoryImport = "from pyscf import gto,scf,mp\n"
        theoryLines.append("# Must run SCF before MP2 in PYSCF\n")
        if multiplicity == 1:
            theoryLines.append("mf = scf.RHF(mol)\n")
            theoryLines.append("mf.kernel()\n")
            theoryLines.append(f"mf2 = mp.{theory}(mf)\n")
            theoryLines.append("mf2.kernel()\n")
        else:
            theoryLines.append("mf = scf.UHF(mol)\n")
            theoryLines.append("mf.kernel()\n")
            theoryLines.append(f"mf2 = mp.{theory}(mf)\n")
            theoryLines.append("mf2.kernel()\n")
    else:
        warnings.append(f"Unhandled theory type:{theory}")

    if calculate == "Single Point":
        pass
    else:
        warnings.append(f"Unhandled calculation type: {calculate}")

    # Create input file
    generated_input = ""
    generated_input += f"# Title: {title}\n"
    generated_input += f"{theoryImport}"
    generated_input += "mol = gto.Mole()\n"
    generated_input += "mol.atom = '''\n"
    generated_input += "$$coords:___Sxyz$$\n"
    generated_input += "'''\n"
    generated_input += f"mol.basis = '{basisStr}'\n"
    generated_input += f"mol.charge = {charge}\n"
    generated_input += f"mol.spin = {multiplicity - 1}\n"
    generated_input += "mol.build()\n"
    for line in theoryLines:
        generated_input += line

    return generated_input, warnings


def generateInput(input_json: dict, debug: bool) -> dict:  # noqa: FBT001

    generated_input, warnings = generateInputFile(input_json)

    filename = input_json["options"]["Filename Base"] + ".py"

    result = {
        "files": [
            {"filename": filename, "contents": generated_input},
        ],
        "mainFile": filename,
    }

    if warnings:
        result["warnings"] = warnings

    return result
