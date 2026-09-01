# SPDX-FileCopyrightText: 2026 Avogadro Project
# SPDX-License-Identifier: BSD 3-Clause
# ******************************************************************************
# This source file is part of the Avogadro project.
#
# This source code is released under the New BSD License, (the "License").
# ******************************************************************************
"""Classes and methods for the %basis block in ORCA."""

from ..basis_sets import (
    AuxCBasisSet,
    AuxJBasisSet,
    AuxJKBasisSet,
)
from .block_base import BlockEnum, ORCAString


# fmt: off
class Basis(BlockEnum):

    # BASIS    = "Basis", str
    AUXJ     = "AuxJ",  str, 0, tuple(AuxJBasisSet)
    AUXJK    = "AuxJK", str, 0, tuple(AuxJKBasisSet)
    AUXC     = "AuxC",  str, 0, tuple(AuxCBasisSet)
    CABS     = "CABS",  str
    ECP      = "ECP",   ORCAString, 0, ("", "def2-ECP", "SK-MCDHF-RSC", "HayWadt", "dhf-ECP", "vDZP-ECP", "CRENBL-ECP")
    GHOSTECP = "GhostECP", bool, False

    # Decontraction Options
    # DECONTRACT      = "Decontract",      bool, False
    # DECONTRACTBAS   = "DecontractBas",   bool, False
    # DECONTRACTAUXJ  = "DecontractAuxJ",  bool, False
    # DECONTRACTAUXJK = "DecontractAuxJK", bool, False
    # DECONTRACTAUXC  = "DecontractAuxC",  bool, False
    # DECONTRACTCABS  = "DecontractCABS",  bool, False

    #* Not sure if this should be included.
    # Reading basis sets from a file
    # GTONAME      = "GTOName",      str
    # GTOAUXJNAME  = "GTOAuxJName",  str
    # GTOAUXNAME   = "GTOAuxName",   str
    # GTOAUXJKNAME = "GTOAuxJKName", str
    # GTOAUXCNAME  = "GTOAuxCName",  str
    # GTOCABSNAME  = "GTOCABSName",  str

    # Removal of linear dependence
    # PCDTRIMBAS   = "PCDTrimBas",   ORCAString, 0, ("Overlap", "Coulomb")
    # PCDTRIMAUXJ  = "PCDTrimAuxJ",  ORCAString, 1, ("Overlap", "Coulomb")
    # PCDTRIMAUXJK = "PCDTrimAuxJK", ORCAString, 1, ("Overlap", "Coulomb")
    # PCDTRIMAUXC  = "PCDTrimAuxC",  ORCAString, 1, ("Overlap", "Coulomb")
    # PCDTHRESH    = "PCDThresh",    float, -1

    # AutoAux Keywords
    AUTOAUXSIZE   = "AutoAuxSize",   int,   1, None, 0, 3
    # AUTOAUXLMAX   = "AutoAuxLmax",   bool,  False
    # AUTOAUXLLIMIT = "AutoAuxLLimit", int,   -1, None, -1, 7
    # AUTOAUXF_0    = "AutoAuxF[0]",   float, 20.0
    # AUTOAUXF_1    = "AutoAuxF[1]",   float, 7.0
    # AUTOAUXF_2    = "AutoAuxF[2]",   float, 4.0
    # AUTOAUXF_3    = "AutoAuxF[3]",   float, 4.0
    # AUTOAUXF_4    = "AutoAuxF[4]",   float, 3.5
    # AUTOAUXF_5    = "AutoAuxF[5]",   float, 2.5
    # AUTOAUXF_6    = "AutoAuxF[6]",   float, 2.0
    # AUTOAUXF_7    = "AutoAuxF[7]",   float, 2.0
    # AUTOAUXB_0    = "AutoAuxB[0]",   float, 1.8
    # AUTOAUXB_1    = "AutoAuxB[1]",   float, 2.0
    # AUTOAUXB_2    = "AutoAuxB[2]",   float, 2.2
    # AUTOAUXB_3    = "AutoAuxB[3]",   float, 2.2
    # AUTOAUXB_4    = "AutoAuxB[4]",   float, 2.2
    # AUTOAUXB_5    = "AutoAuxB[5]",   float, 2.3
    # AUTOAUXB_6    = "AutoAuxB[6]",   float, 3.0
    # AUTOAUXB_7    = "AutoAuxB[7]",   float, 3.0
    # AUTOAUXTIGHTB = "AutoAuxTightB", bool,  True
# fmt: on
