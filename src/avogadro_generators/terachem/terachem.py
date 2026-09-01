# SPDX-FileCopyrightText: 2026 Avogadro Project
# SPDX-License-Identifier: BSD 3-Clause
# ******************************************************************************
# This source file is part of the Avogadro project.
#
# This source code is released under the New BSD License, (the "License").
# ******************************************************************************
"""Input generation for TeraChem."""


def generateInputFile(input_json: dict) -> tuple[str, str, list[str]]:
    # Collect warning strings as we go
    warnings = []

    # Extract options:
    opts = input_json["options"]
    title = opts["Title"]
    calculate = opts["Calculation Type"]
    theory = opts["Theory"]
    unrestricted = opts["Unrestricted"]
    basis = opts["Basis"]
    dispersion = opts["Dispersion"]
    charge = opts["Charge"]
    multiplicity = opts["Multiplicity"]
    baseName = opts["Filename Base"]

    # Convert to code-specific strings
    basisStr = ""
    if basis == "STO-3G":
        basisStr = basis.lower()
    else:
        basisStr = basis

    calcStr = ""
    if calculate == "Single Point":
        calcStr = "energy"
    elif calculate == "Gradient":
        calcStr = "gradient"
    elif calculate == "Equilibrium Geometry":
        calcStr = "minimize"
    else:
        warnings.append(f"Unhandled calculation type: {calculate}")

    theoryStr = ""
    if unrestricted:
        theoryStr += "u"
    elif theory == "HF":
        theoryStr += "r"
    theoryStr += theory.lower()

    dispStr = ""
    if dispersion == "Off":
        dispStr = "no"
    elif dispersion == "On":
        dispStr = "yes"
    else:
        dispStr = dispersion.lower()

    # Create input file
    generated_input = ""

    generated_input += f"#\n# {title}\n#\n\n"

    generated_input += f"{'run':<15}{calcStr}\n\n"

    generated_input += f"{'method':<15}{theoryStr}\n"
    if dispersion != "Off":
        generated_input += f"{'dispersion':<15}{dispStr}\n"
    generated_input += f"{'basis':<15}{basisStr}\n"
    generated_input += f"{'charge':<15}{charge}\n"
    generated_input += f"{'spinmult':<15}{multiplicity}\n\n"

    generated_input += f"{'coordinates':<15}{baseName}.xyz\n\n"

    generated_input += "end\n"

    # Create XYZ file
    coordFile = f"$$atomCount$$\n{title}\n$$coords:Sxyz$$\n"

    return generated_input, coordFile, warnings


def generateInput(input_json: dict, debug: bool) -> dict:  # noqa: FBT001

    generated_input, coordFile, warnings = generateInputFile(input_json)

    base_filename = input_json["options"]["Filename Base"]

    result = {
        "files": [
            {"filename": f"{base_filename}.tcin", "contents": generated_input},
            {"filename": f"{base_filename}.xyz", "contents": coordFile},
        ],
        "mainFile": f"{base_filename}.tcin",
    }

    if warnings:
        result["warnings"] = warnings

    return result
