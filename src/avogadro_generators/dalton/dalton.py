# SPDX-FileCopyrightText: 2026 Avogadro Project
# SPDX-License-Identifier: BSD 3-Clause
# ******************************************************************************
# This source file is part of the Avogadro project.
#
# This source code is released under the New BSD License, (the "License").
# ******************************************************************************
"""Input generation for the Dalton suite (https://daltonprogram.org/)."""

# element lookups
symbols = [
    "Xx",
    "H",
    "He",
    "Li",
    "Be",
    "B",
    "C",
    "N",
    "O",
    "F",
    "Ne",
    "Na",
    "Mg",
    "Al",
    "Si",
    "P",
    "S",
    "Cl",
    "Ar",
    "K",
    "Ca",
    "Sc",
    "Ti",
    "V",
    "Cr",
    "Mn",
    "Fe",
    "Co",
    "Ni",
    "Cu",
    "Zn",
    "Ga",
    "Ge",
    "As",
    "Se",
    "Br",
    "Kr",
    "Rb",
    "Sr",
    "Y",
    "Zr",
    "Nb",
    "Mo",
    "Tc",
    "Ru",
    "Rh",
    "Pd",
    "Ag",
    "Cd",
    "In",
    "Sn",
    "Sb",
    "Te",
    "I",
    "Xe",
    "Cs",
    "Ba",
    "La",
    "Ce",
    "Pr",
    "Nd",
    "Pm",
    "Sm",
    "Eu",
    "Gd",
    "Tb",
    "Dy",
    "Ho",
    "Er",
    "Tm",
    "Yb",
    "Lu",
    "Hf",
    "Ta",
    "W",
    "Re",
    "Os",
    "Ir",
    "Pt",
    "Au",
    "Hg",
    "Tl",
    "Pb",
    "Bi",
    "Po",
    "At",
    "Rn",
    "Fr",
    "Ra",
    "Ac",
    "Th",
    "Pa",
    "U",
    "Np",
    "Pu",
    "Am",
    "Cm",
    "Bk",
    "Cf",
    "Es",
    "Fm",
    "Md",
    "No",
    "Lr",
    "Rf",
    "Db",
    "Sg",
    "Bh",
    "Hs",
    "Mt",
    "Ds",
    "Rg",
    "Cn",
    "Nh",
    "Fl",
    "Mc",
    "Lv",
    "Ts",
    "Og",
]


def generateInputFile(input_json: dict) -> tuple[str, str, list[str]]:
    # Collect warning strings as we go
    warnings = []

    # Extract options:
    opts = input_json["options"]
    title = opts["Title"]
    calculate = opts["Calculation Type"]
    theory = opts["Theory"]
    basis = opts["Basis"]
    functional = opts["Functional"]

    generated_input = ""
    coordfile = ""

    # Basis
    coordfile += "BASIS\n"
    coordfile += f"{basis}\n"
    # Title
    coordfile += f" {title}\n"
    coordfile += f" {theory} Generated with Avogadro 2\n"
    # Coordinates
    cjson = input_json["cjson"]
    # roll up the atoms for each element type
    atoms = [[] for i in range(118)]
    start = 0  # index into the coordinate array
    atom_types = 0
    coords3d = cjson["atoms"]["coords"]["3d"]
    for z in cjson["atoms"]["elements"]["number"]:
        coords = coords3d[start : start + 3]
        if len(atoms[z]) == 0:
            atom_types += 1  # a new atom type
        atoms[z].append(coords)
        start += 3
    coordfile += f"Atomtypes={atom_types:d} Angstrom\n"

    for z in range(len(atoms)):
        if len(atoms[z]) > 0:
            coordfile += f"Charge={z:d}.0 Atoms={len(atoms[z])}\n"
            for atom in atoms[z]:
                coordfile += f"{symbols[z]}{atom[0]:15.5f}{atom[1]:15.5f}{atom[2]:15.5f}\n"
    coordfile += ""
    coordfile += "\n\n"

    generated_input += "**DALTON INPUT\n"

    if calculate == "Single Point":
        if theory == "SCF":
            generated_input += ".RUN WAVE FUNCTIONS\n**WAVE FUNCTIONS\n.HF\n**END OF DALTON INPUT\n"
        elif theory == "DFT":
            generated_input += (
                ".RUN WAVE FUNCTIONS\n**WAVE FUNCTIONS\n"
                + ".DFT\n "
                + functional
                + "\n**END OF DALTON INPUT\n"
            )
        elif theory == "MP2":
            generated_input += (
                ".RUN WAVE FUNCTIONS\n**WAVE FUNCTIONS\n.HF\n.MP2\n**END OF DALTON INPUT\n"
            )
        else:
            generated_input += (
                ".RUN WAVE FUNCTIONS\n**WAVE FUNCTIONS\n.CC\n*CC INPUT\n."
                + theory
                + "\n**END OF DALTON INPUT\n"
            )
    if calculate == "Optimize":
        generated_input += ".OPTIMIZE\n**WAVE FUNCTIONS\n.HF\n**END OF DALTON INPUT\n"
    if calculate == "Optimize + Frequencies":
        generated_input += (
            ".OPTIMIZE\n**WAVE FUNCTIONS\n.HF\n**PROPERTIES\n.VIBANA\n**END OF DALTON INPUT\n"
        )
    if calculate == "Frequencies":
        generated_input += (
            ".RUN PROPERTIES\n**WAVE FUNCTIONS\n.HF\n**PROPERTIES\n.VIBANA\n**END OF DALTON INPUT\n"
        )

    generated_input += "\n"

    return coordfile, generated_input, warnings


def generateInput(input_json: dict, debug: bool) -> dict:  # noqa: FBT001

    coordfile, generated_input, warnings = generateInputFile(input_json)

    base_filename = input_json["options"]["Filename Base"]

    result = {
        "files": [
            {"filename": f"{base_filename}.dal", "contents": generated_input},
            {"filename": f"{base_filename}.mol", "contents": coordfile},
        ],
        "mainFile": f"{base_filename}.dal",
    }

    if warnings:
        result["warnings"] = warnings

    return result
