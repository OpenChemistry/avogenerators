# SPDX-FileCopyrightText: 2026 Avogadro Project
# SPDX-License-Identifier: BSD 3-Clause
# ******************************************************************************
# This source file is part of the Avogadro project.
#
# This source code is released under the New BSD License, (the "License").
# ******************************************************************************
"""Entry point for all the input generators."""

import argparse
import json
import sys


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--debug", action="store_true")
    parser.add_argument("--lang", nargs="?", default="en")
    parser.add_argument("generator", action="store")
    args = parser.parse_args()

    match args.generator:
        # Do imports lazily so only the relevant file is imported when called
        case "dalton":
            from .dalton.dalton import generateInput
        case "gamessuk":
            from .gamessuk.gamessuk import generateInput
        case "gaussian":
            from .gaussian.gaussian import generateInput
        case "molpro":
            from .molpro.molpro import generateInput
        case "mopac":
            from .mopac.mopac import generateInput
        case "nwchem":
            from .nwchem.nwchem import generateInput
        case "orca":
            from .orca import generateInput
        case "pyscf":
            from .pyscf.pyscf import generateInput
        case "psi4":
            from .psi4.psi4 import generateInput
        case "qchem":
            from .qchem.qchem import generateInput
        case "terachem":
            from .terachem.terachem import generateInput

    # Load the JSON passed by Avogadro
    inp = json.load(sys.stdin)
    output = generateInput(inp, args.debug)

    if args.debug:
        output["files"].append({"filename": "debug_info", "contents": inp})

    print(json.dumps(output))
