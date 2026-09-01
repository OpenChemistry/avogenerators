# SPDX-FileCopyrightText: 2026 Avogadro Project
# SPDX-License-Identifier: BSD 3-Clause
# ******************************************************************************
# This source file is part of the Avogadro project.
#
# This source code is released under the New BSD License, (the "License").
# ******************************************************************************
"""Input generation for Gaussian."""


def generateInputFile(input_json: dict) -> tuple[str, list[str]]:
    # Collect warning strings as we go
    warnings = []

    # Extract options:
    opts = input_json["options"]
    title = opts["Title"]
    calculate = opts["Calculation Type"]
    theory = opts["Theory"]
    if opts["Alternate Theory"]:
        theory = opts["Alternate Theory"]
    basis = opts["Alternate Basis Set"] or opts["Basis"]
    multiplicity = opts["Multiplicity"]
    charge = opts["Charge"]
    outputFormat = opts["Output Format"]
    checkpoint = opts["Write Checkpoint File"]
    nCores = opts["Processor Cores"]

    generated_input = ""

    # Number of cores
    generated_input += f"%NProcShared={nCores}\n"
    generated_input += f"%mem={opts['Memory']}GB\n"

    # Checkpoint
    if checkpoint:
        baseName = opts["Filename Base"]
        generated_input += f"%Chk={baseName}.chk\n"

    # Theory/Basis
    if theory in ("AM1", "PM3"):
        generated_input += f"#p {theory}"
        warnings.append("Ignoring basis set for semi-empirical calculation.")
    else:
        generated_input += f"#p {theory}/{basis.replace(' ', '')}"

    # Calculation type
    calc_type = {
        "Single Point": " SP",
        "Equilibrium Geometry": " Opt",
        "Frequencies": " Opt Freq",
    }
    try:
        generated_input += calc_type[calculate]
    except KeyError:
        warnings.append(f"Invalid calculation type: {calculate}")

    # Output format
    if outputFormat == "Standard":
        pass
    elif outputFormat == "Molden":
        generated_input += " gfprint pop=full"
    elif outputFormat == "Molekel":
        generated_input += " gfoldprint pop=full"
    else:
        warnings.append(f"Invalid output format: {outputFormat}")

    # Title
    generated_input += f"\n\n {title}\n\n"

    # Charge/Multiplicity
    generated_input += f"{charge} {multiplicity}\n"

    # Coordinates
    generated_input += "$$coords:Sxyz$$\n"

    # The gaussian code is irritatingly fickle -- it *will* silently crash if
    # this extra, otherwise unnecessary newline is not present at the end of the
    # file.
    generated_input += "\n"

    return generated_input, warnings


def generateInput(input_json: dict, debug: bool) -> dict:  # noqa: FBT001

    generated_input, warnings = generateInputFile(input_json)

    filename = input_json["options"]["Filename Base"] + ".gjf"

    result = {
        "files": [
            {"filename": filename, "contents": generated_input},
        ],
        "mainFile": filename,
    }

    if warnings:
        result["warnings"] = warnings

    return result
