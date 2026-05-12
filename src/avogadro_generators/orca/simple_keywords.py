# SPDX-FileCopyrightText: 2026 Avogadro Project
# SPDX-License-Identifier: BSD 3-Clause
# ******************************************************************************
# This source file is part of the Avogadro project.
#
# This source code is released under the New BSD License, (the "License").
# ******************************************************************************
"""Enums of simple input keywords for ORCA calculations."""

from enum import StrEnum


# fmt: off
class RunType(StrEnum):
    """Types of calculations to run."""

    SP      = "SP"
    ENGRAD  = "EnGrad"
    OPT     = "Opt"
    OPTTS   = "OptTS"
    FREQ    = "Freq"
    NUMFREQ = "NumFreq"


class SemiEmpirical(StrEnum):
    """Semi-empirical methods such as xTB, AM1, and PM3."""

    # xTB-based methods
    GFN0_XTB = "GFN0-xTB"
    GFN1_XTB = "GFN1-xTB"
    GFN2_XTB = "GFN2-xTB"
    GFN1_XTB_NATIVE = "Native-GFN1-xTB"
    GFN2_XTB_NATIVE = "Native-GFN2-xTB"

    # NDO-based methods
    AM1     = "AM1"
    PM3     = "PM3"
    MNDO    = "MNDO"
    ZINDO_1 = "ZINDO/1"
    ZINDO_2 = "ZINDO/2"
    ZINDO_S = "ZINDO/S"
    ZNDDO_1 = "ZNDDO/1"
    ZNDDO_2 = "ZNDDO/2"


class SCFConv(StrEnum):
    """Control SCF Thresholds and other settings."""

    SLOPPYSCF    = "SloppySCF"
    LOOSESCF     = "LooseSCF"
    MEDIUMSCF    = "MediumSCF"
    STRONGSCF    = "StrongSCF"
    TIGHTSCF     = "TightSCF"
    VERYTIGHTSCF = "VeryTightSCF"
    EXTREMESCF   = "ExtremeSCF"


class DeterminantType(StrEnum):
    """Control Reference Determinant(s)."""

    RHF  = "RHF"
    UHF  = "UHF"
    ROHF = "ROHF"
    RKS  = "RKS"
    UKS  = "UKS"
    ROKS = "ROKS"


class Opt(StrEnum):
    """Control Geometry Optimization Thresholds."""

    LOOSEOPT     = "LooseOpt"
    NORMALOPT    = "NormalOpt"
    TIGHTOPT     = "TightOpt"
    VERYTIGHTOPT = "VeryTightOpt"


class Output(StrEnum):
    """Control of Output."""

    MINIPRINT        = "MiniPrint"
    SMALLPRINT       = "SmallPrint"
    NORMALPRINT      = "NormalPrint"
    LARGEPRINT       = "LargePrint"
    PRINTGAP         = "PrintGap"
    PRINTMOS         = "PrintMOs"
    PRINTBASIS       = "PrintBasis"
    AIM              = "AIM"
    XYZFILE          = "XYZFile"
    PDBFILE          = "PDBFile"
    UNO              = "UNO"
    NOPROPFILE       = "NoPropFile"
    KEEPTRANSDENSITY = "KeepTransDensity"


class Symmetry(StrEnum):
    """Control of symmetry handling."""

    USESYM = "UseSym"


class Grid(StrEnum):
    """Control of Numerical Integration Grids."""

    DEFGRID1 = "DEFGRID1"
    DEFGRID2 = "DEFGRID2"
    DEFGRID3 = "DEFGRID3"


class RIApproximation(StrEnum):
    """Control of Resolution of the Identity and Chain of Spheres."""

    COSJXC     = "COSJXC"
    NOCOSX     = "NoCOSX"
    RI         = "RI" # Turns on Split-RI-J by default
    NORI       = "NoRI"
    RIJCOSX    = "RIJCOSX" # Default for Hybrid DFT
    NORIJCOSX  = "NoRIJCOSX"
    SPLITRIJ   = "Split-RI-J" # Default for non-Hybrid DFT
    NOSPLITRIJ = "NoSplit-RI-J"
    RIJK       = "RI-JK"


class PartialCharges(StrEnum):
    """Control of Partial Charges/Population Analysis."""

    AIM       = "AIM"
    CHELPG    = "CHELPG"
    HIRSHFELD = "Hirshfeld"
    LOEWDIN   = "Loewdin"
    MAYER     = "Mayer"
    MBIS      = "MBIS"
    MULLIKEN  = "Mulliken"


class Relativistic(StrEnum):
    """Control of Relativistic Approximations."""

    DKH1    = "DKH1"
    DKH2    = "DKH2"
    DKH     = DKH2
    ZORA    = "ZORA"
    IORA    = "IORA"
    X2C     = "X2C"


class PNO(StrEnum):
    """Control of Pair-Natural Orbital Settings."""

    LOOSEPNO  = "LoosePNO"
    NORMALPNO = "NormalPNO"
    TIGHTPNO  = "TightPNO"
# fmt: on


def match_simple_keyword(kwd: str):
    """Brute force matching of simple keywords."""

    keyword_types = [
        RunType,
        SemiEmpirical,
        SCFConv,
        DeterminantType,
        Opt,
        Output,
        Symmetry,
        Grid,
        RIApproximation,
        PartialCharges,
        Relativistic,
        PNO,
    ]

    for kwd_type in keyword_types:
        for key in kwd_type:
            if str(key) == kwd:
                return key

    return None
