# SPDX-FileCopyrightText: 2026 Avogadro Project
# SPDX-License-Identifier: BSD 3-Clause
# ******************************************************************************
# This source file is part of the Avogadro project.
#
# This source code is released under the New BSD License, (the "License").
# ******************************************************************************
"""Input generation for NWChem (https://nwchemgit.github.io/)."""


def basisGuiToInput(gui):
    if gui == "3-21 G":
        return "3-21G"
    elif gui == "6-31 G(d)":
        return "6-31G*"
    elif gui == "6-31 G(d,p)":
        return "6-31G**"
    elif gui == "6-31+ G(d)":
        return "6-31+G*"
    elif gui == "6-311 G(d)":
        return "6-311G*"
    elif gui == "LANL2DZ":
        return "LANL2DZ ECP"
    else:
        return gui


def generateInputFile(input_json: dict) -> tuple[str, list[str]]:
    # Collect warning strings as we go
    warnings = []

    # Extract options:
    opts = input_json["options"]
    title = opts["Title"]
    calculate = opts["Calculation Type"]
    theory = opts["Theory"]
    basis = opts["Basis"]
    multiplicity = opts["Multiplicity"]
    charge = opts["Charge"]

    # Preamble
    nwfile = ""
    nwfile += "echo\n\n"
    nwfile += "start molecule\n\n"
    nwfile += f'title "{title}"\n'

    # Charge
    nwfile += f"charge {charge:d}\n\n"

    # Coordinates
    nwfile += "geometry units angstroms print xyz autosym\n"
    nwfile += "$$coords:Sxyz$$\n"
    nwfile += "end\n\n"

    # Basis
    nwfile += "basis"
    if basis == "cc-pVDZ" or basis == "cc-pVTZ":
        nwfile += " spherical"
    nwfile += "\n"
    nwfile += "  * library "
    nwfile += basisGuiToInput(basis)
    nwfile += "\n"
    nwfile += "end\n\n"

    # Theory
    task = ""
    if theory == "RHF":
        task = "scf"
    elif theory == "B3LYP":
        task = "dft"
        nwfile += "dft\n"
        nwfile += "  xc b3lyp\n"
        nwfile += f"  mult {multiplicity:d}\n"
        nwfile += "end\n\n"
    elif theory == "MP2":
        task = "mp2"
        nwfile += "mp2\n"
        nwfile += "  # Exclude core electrons from MP2 treatment:\n"
        nwfile += "  freeze atomic\n"
        nwfile += "end\n\n"
    elif theory == "CCSD":
        task = "ccsd"
        nwfile += "ccsd\n"
        nwfile += "  # Exclude core electrons from coupled cluster perturbations:\n"
        nwfile += "  freeze atomic\n"
        nwfile += "end\n\n"
    else:
        warnings.append(f"Invalid Theory: {theory}")

    # Task
    nwfile += f"task {task} "
    if calculate == "Single Point":
        nwfile += "energy"
    elif calculate == "Equilibrium Geometry":
        nwfile += "optimize"
    elif calculate == "Frequencies":
        nwfile += "freq"
    else:
        warnings.append(f"Invalid calculation type: {calculate}")
    nwfile += "\n"

    return nwfile, warnings


def generateInput(input_json: dict, debug: bool) -> dict:  # noqa: FBT001

    generated_input, warnings = generateInputFile(input_json)

    filename = input_json["options"]["Filename Base"] + ".nw"

    result = {
        "files": [
            {
                "filename": filename,
                "contents": generated_input,
                "highlightStyles": ["default"],
            },
        ],
        "mainFile": filename,
    }

    if warnings:
        result["warnings"] = warnings

    return result
