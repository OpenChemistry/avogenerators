# SPDX-FileCopyrightText: 2026 Avogadro Project
# SPDX-License-Identifier: BSD 3-Clause
# ******************************************************************************
# This source file is part of the Avogadro project.
#
# This source code is released under the New BSD License, (the "License").
# ******************************************************************************
"""Input generation for Q-Chem (https://www.q-chem.com/)."""


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

    # Convert to code-specific strings
    calcStr = ""
    if calculate == "Single Point":
        calcStr = "SP"
    elif calculate == "Equilibrium Geometry":
        calcStr = "Opt"
    elif calculate == "Frequencies":
        calcStr = "Freq"
    else:
        warnings.append(f"Unhandled calculation type: {calculate}")

    theoryStr = ""
    if theory in ["HF", "B3LYP", "B3LYP5", "EDF1", "M062X", "MP2", "CCSD"]:
        theoryStr = theory
    else:
        warnings.append(f"Unhandled theory type: {theory}")

    basisStr = ""
    if basis in [
        "STO-3G",
        "3-21G",
        "6-31G(d)",
        "6-31G(d,p)",
        "6-31+G(d)",
        "6-311G(d)",
        "cc-pVDZ",
        "cc-pVTZ",
    ]:
        basisStr = f"BASIS {basis}"
    elif basis in ["LANL2DZ", "LACVP"]:
        basisStr = f"ECP {basis}"
    else:
        warnings.append(f"Unhandled basis type: {basis}")

    generated_input = ""

    generated_input += "$rem\n"
    generated_input += f"   JOBTYPE {calcStr}\n"
    generated_input += f"   METHOD {theoryStr}\n"
    generated_input += f"   {basisStr}\n"
    generated_input += "   GUI 2\n"
    generated_input += "$end\n\n"

    generated_input += f"$comment\n   {title}\n$end\n\n"

    generated_input += "$molecule\n"
    generated_input += f"   {charge} {multiplicity}\n"
    generated_input += "$$coords:___Sxyz$$\n"
    generated_input += "$end\n"

    return generated_input, warnings


def generateInput(input_json: dict, debug: bool) -> dict:  # noqa: FBT001

    generated_input, warnings = generateInputFile(input_json)

    filename = input_json["options"]["Filename Base"] + ".qcin"

    result = {
        "files": [
            {"filename": filename, "contents": generated_input},
        ],
        "mainFile": filename,
    }

    if warnings:
        result["warnings"] = warnings

    return result
