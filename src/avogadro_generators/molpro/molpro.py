# SPDX-FileCopyrightText: 2026 Avogadro Project
# SPDX-License-Identifier: BSD 3-Clause
# ******************************************************************************
# This source file is part of the Avogadro project.
#
# This source code is released under the New BSD License, (the "License").
# ******************************************************************************
"""Input generation for Molpro (https://www.molpro.net/)."""


def generateInputFile(input_json: dict) -> tuple[str, list[str]]:
    # Collect warning strings as we go
    warnings = []

    # Extract options:
    opts = input_json["options"]
    title = opts["Title"]
    calculate = opts["Calculation Type"]
    theory = opts["Theory"]
    basis = opts["Basis"]
    charge = opts["Charge"]
    multiplicity = opts["Multiplicity"]
    oldVersion = opts["Use Pre-2009.1 Format"]

    # Convert to code-specific strings
    basisStr = ""
    if basis in ["STO-3G", "3-21G", "6-31G", "6-31G(d)", "6-31G(d,p)", "6-31+G(d)", "6-311G(d)"]:
        basisStr = basis
    elif basis == "cc-pVDZ":
        basisStr = "vdz"
    elif basis == "cc-pVTZ":
        basisStr = "vtz"
    elif basis == "AUG-cc-pVDZ":
        basisStr = "avdz"
    elif basis == "AUG-cc-pVTZ":
        basisStr = "avtz"
    else:
        warnings.append(f"Unhandled basis type: {basis}")

    cjson = input_json["cjson"]

    # MOLPRO needs us to calculate some rough wavefunction parameters:
    numElectrons = -charge
    try:
        for z in cjson["atoms"]["elements"]["number"]:
            numElectrons += z
    except KeyError:
        numElectrons = 0
    wavefnStr = f"wf,{numElectrons:d},1,{multiplicity - 1:d}"

    theoryStr = ""
    if theory != "B3LYP":
        theoryStr += f"{{rhf\n{wavefnStr}}}\n"
    # Intentionally not using elif here:
    if theory != "RHF":
        theoryKey = ""
        if theory in ["MP2", "CCSD", "CCSD(T)"]:
            theoryKey = theory.lower()
        elif theory == "B3LYP":
            theoryKey = "uks,b3lyp"
        else:
            warnings.append(f"Unhandled theory type: {theory}")
        theoryStr += f"{{{theoryKey}\n{wavefnStr}}}\n"

    calcStr = ""
    if calculate == "Single Point":
        pass
    elif calculate == "Equilibrium Geometry":
        calcStr = "{optg}\n\n"
    elif calculate == "Frequencies":
        calcStr = "{optg}\n{frequencies}\n\n"
    else:
        warnings.append(f"Unhandled calculation type: {calculate}")

    # Create input file
    generated_input = ""

    generated_input += f"*** {title}\n\n"
    generated_input += "gprint,basis\n"
    generated_input += "gprint,orbital\n\n"

    generated_input += f"basis, {basisStr}\n\n"

    if oldVersion:
        generated_input += "geomtyp=xyz\n"
    generated_input += "geometry={\n"
    if oldVersion:
        numAtoms = 0
        try:
            numAtoms = len(cjson["atoms"]["elements"]["number"])
        except KeyError:
            numAtoms = 0
        generated_input += f"{numAtoms:d}\n\n"

    generated_input += "$$coords:Sxyz$$\n"
    generated_input += "}\n\n"

    generated_input += f"{theoryStr}\n"

    generated_input += f"{calcStr}"

    generated_input += "---\n"

    return generated_input, warnings


def generateInput(input_json: dict, debug: bool) -> dict:  # noqa: FBT001

    generated_input, warnings = generateInputFile(input_json)

    filename = input_json["options"]["Filename Base"] + ".inp"

    result = {
        "files": [
            {"filename": filename, "contents": generated_input},
        ],
        "mainFile": filename,
    }

    if warnings:
        result["warnings"] = warnings

    return result
