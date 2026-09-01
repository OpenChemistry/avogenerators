# SPDX-FileCopyrightText: 2026 Avogadro Project
# SPDX-License-Identifier: BSD 3-Clause
# ******************************************************************************
# This source file is part of the Avogadro project.
#
# This source code is released under the New BSD License, (the "License").
# ******************************************************************************
"""Input generation for MOPAC (https://openmopac.net/)."""


def generateInputFile(input_json: dict) -> tuple[str, list[str]]:
    # Collect warning strings as we go
    warnings = []

    # Extract options:
    opts = input_json["options"]
    title = opts["Title"]
    calculate = opts["Calculation Type"]
    theory = opts["Theory"]
    multiplicity = opts["Multiplicity"]
    charge = opts["Charge"]
    nCores = int(opts["Processor Cores"])
    solvent = opts["Solvent"]
    optionaldielectric = opts["Other Solvent Dielectric"]
    hftype = opts["HF Type"]
    cosmo = opts["COSMO"]
    solventlist = {
        "Acetic acid": 6.15,
        "Acetone": 20.7,
        "Acetonitrile": 37.5,
        "Anisole": 4.33,
        "Benzene": 2.27,
        "Bromobenzene": 5.17,
        "Carbon disulfide": 2.6,
        "Carbon tetrachloride": 2.24,
        "Chlorobenzene": 5.62,
        "Chloroform": 4.81,
        "Cyclohexane": 2.02,
        "Dibutyl ether": 3.1,
        "o-Dichlorobenzene": 9.93,
        "1,2-Dichloroethane": 10.36,
        "Dichloromethane": 8.93,
        "Diethylamine": 3.6,
        "Diethylether": 4.33,
        "1,2-Dimethoxyethane": 7.2,
        "N,N-Dimethylacetamide": 37.8,
        "N,N-Dimethylformamide": 36.7,
        "Dimethylsulfoxide": 46.7,
        "1,4-Dioxane": 2.25,
        "Ethanol": 24.5,
        "Ethyl acetate": 6.02,
        "Ethyl benzoate": 6.02,
        "Formamide": 111,
        "Hexamethylphosphoramide": 30,
        "Isopropyl lcohol": 17.9,
        "Methanol": 32.7,
        "2-Methyl-2-propanol": 10.9,
        "Nitrobenzene": 34.82,
        "Nitromethane": 35.87,
        "Pyridine": 12.4,
        "Tetrahydrofuran": 7.58,
        "Toluene": 2.38,
        "Trichloroethylene": 3.4,
        "Triethylamine": 2.42,
        "Trifluoroacetic acid": 8.55,
        "2,2,2-Trifluoroethanol": 8.55,
        "Water": 80.1,
        "o-Xylene": 2.57,
    }

    generated_input = ""

    # Multiplicity
    multStr = ""
    if multiplicity == 1:
        multStr = "SINGLET"
    elif multiplicity == 2:
        multStr = "DOUBLET"
    elif multiplicity == 3:
        multStr = "TRIPLET"
    elif multiplicity == 4:
        multStr = "QUARTET"
    elif multiplicity == 5:
        multStr = "QUINTET"
    elif multiplicity == 6:
        multStr = "SEXTET"
    else:
        raise NotImplementedError(f"Unhandled multiplicity: {multiplicity}")

    # Calculation type:
    calcStr = ""
    if calculate == "Single Point":
        calcStr = "NOOPT"
    elif calculate == "Equilibrium Geometry":
        pass
    elif calculate == "Frequencies":
        calcStr = "FORCE"
    elif calculate == "Transition State":
        calcStr = "SADDLE"
    else:
        raise NotImplementedError(f"Unhandled calculation type: {calculate}")

    eps = ""
    dielectric = ""
    if solvent == "OTHER":
        dielectric = optionaldielectric
    else:
        dielectric = str(solventlist[solvent])

    if cosmo is True:
        eps = "EPS=" + dielectric

    if multiplicity > 1:
        hftype = "UHF"

    # Charge, mult, calc type, theory:
    generated_input += f" AUX LARGE CHARGE={charge:d} {multStr} {calcStr} {theory} {eps} PDBOUT THREADS={nCores:d} {hftype}\n"

    # Title
    generated_input += f"{title}\n\n"

    # Coordinates
    if calculate == "Single Point":
        generated_input += "$$coords:Sx0y0z0$$\n"
    else:
        generated_input += "$$coords:Sx1y1z1$$\n"

    return generated_input, warnings


def generateInput(input_json: dict, debug: bool) -> dict:  # noqa: FBT001

    generated_input, warnings = generateInputFile(input_json)

    filename = input_json["options"]["Filename Base"] + ".mop"

    result = {
        "files": [
            {"filename": filename, "contents": generated_input, "highlightStyles": ["default"]}
        ],
        "mainFile": filename,
    }

    if warnings:
        result["warnings"] = warnings

    return result
