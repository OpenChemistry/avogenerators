# SPDX-FileCopyrightText: 2026 Avogadro Project
# SPDX-License-Identifier: BSD 3-Clause
# ******************************************************************************
# This source file is part of the Avogadro project.
#
# This source code is released under the New BSD License, (the "License").
# ******************************************************************************
"""Classes and methods for the %method block in ORCA.

WORK IN PROGRESS!!
"""

from collections.abc import Sequence

from .block_base import BlockEnum, ORCAString


# fmt: off
class Method(BlockEnum):
    """Enumeration of keywords available in the %method block."""

    RUNTYPE = "RunType", ORCAString, 0, ("Energy", "Gradient", "Opt", "Scan", "CIM")
    METHOD = (
        "Method",
        ORCAString,
        0, # Default HF
        (
            "HF", "DFT",
            "AM1", "PM3",
            "MNDO",
            "CNDO_1",  "CNDO_2",  "CNDO_S",
            "INDO_1",  "INDO_2",  "INDO_S",
            "ZINDO_1", "ZINDO_2", "ZINDO_S",
            "ZNDDO_1", "ZNDDO_2",
        ),
    )

    # Integration Grids
    ANGULARGRID  = "AngularGrid",  int,   0, None, 7
    INTACC       = "IntAcc",       float, 5.0
    ANGULARGRIDX = "AngularGridX", Sequence
    NTHETAMAX    = "NThetaMax",    float, 0.4
    GRIDPRUNING  = "GridPruning",  ORCAString, 2, ("Unpruned", "OldPruning", "Adaptive")
    HGRIDREDUCED = "HGridReduced", bool,  True
    BFCUT        = "BFCut",        float, 1e-10
    WEIGHTCUT    = "WeightCut",    float, 1e-14
# fmt: on
