# SPDX-FileCopyrightText: 2026 Avogadro Project
# SPDX-License-Identifier: BSD 3-Clause
# ******************************************************************************
# This source file is part of the Avogadro project.
#
# This source code is released under the New BSD License, (the "License").
# ******************************************************************************
"""Input generation for Psi4 (https://psicode.org/)."""


def generateInputFile(input_json: dict) -> tuple[str, list[str]]:
    # Collect warning strings as we go
    warnings = []

    # Extract options:
    opts = input_json["options"]
    calculate = opts["Calculation Type"]
    theory = opts["Theory"]

    if opts["Alternate Basis Set"] is True:
        basis = opts["Alternate Basis Set Name"]
    else:
        basis = opts["Basis"]
    charge = opts["Charge"]
    multiplicity = opts["Multiplicity"]
    nCores = int(opts["Processor Cores"])
    memory = int(opts["Memory"])

    # Convert to code-specific strings
    calcStr = ""
    if calculate == "Single Point":
        calcStr = "energy"
    elif calculate == "Geometry Optimization":
        calcStr = "optimize"
    elif calculate == "Frequencies":
        calcStr = "frequencies"
    else:
        warnings.append(f"Unhandled calculation type: {calculate}")

    generated_input = ""

    generated_input += "set_num_threads(" + str(nCores) + ")\n"
    generated_input += "memory " + str(memory) + "GB\n"
    generated_input += f"set basis {basis}\n"
    generated_input += "molecule {\n"
    generated_input += f"{charge} {multiplicity}\n"
    generated_input += "$$coords:___Sxyz$$\n"
    generated_input += "}\n\n"
    if calcStr == "optimize":
        generated_input += "set optking {\n"
        generated_input += "   print_trajectory_xyz_file\tTrue\n"
        generated_input += "}\n\n"
    if "SAPT" in theory:
        generated_input += "auto_fragments('')\n"

    generated_input += f'{calcStr}("{theory}")\n'

    return generated_input, warnings


def generateInput(input_json: dict, debug: bool) -> dict:  # noqa: FBT001

    generated_input, warnings = generateInputFile(input_json)

    filename = input_json["options"]["Filename Base"] + ".in"

    result = {
        "files": [
            {"filename": filename, "contents": generated_input},
        ],
        "mainFile": filename,
    }

    if warnings:
        result["warnings"] = warnings

    return result
