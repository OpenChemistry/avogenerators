# SPDX-FileCopyrightText: 2026 Avogadro Project
# SPDX-License-Identifier: BSD 3-Clause
# ******************************************************************************
# This source file is part of the Avogadro project.
#
# This source code is released under the New BSD License, (the "License").
# ******************************************************************************
"""Classes and methods for the %scf block in ORCA."""

# from collections.abc import Sequence
from .block_base import BlockEnum, NestedBlockEnum, ORCAString


# fmt: off
class SCF(BlockEnum):

    CONVERGENCE   = "Convergence",   ORCAString, 2, ("Sloppy", "Loose", "Medium", "Strong", "Tight", "VeryTight", "Extreme")
    TOL_E         = "TolE",          float, 1e-6
    TOL_RMSP      = "TolRMSP",       float, 1e-6
    TOL_MAXP      = "TolMaxP",       float, 1e-5
    TOL_ERR       = "TolErr",        float, 1e-5
    TOL_G         = "TolG",          float, 5e-5
    TOL_X         = "TolX",          float, 5e-5
    THRESH        = "Thresh",        float, 1e-10
    TCUT          = "TCut",          float, 1e-11
    CONVCHECKMODE = "ConvCheckMode", int,   2, None, 0, 2
    CONVFORCED    = "ConvForced",    int,   1, None, 0, 1

    # Wavefunction Types
    # HFTYP       = "HFTyp",       ORCAString, ("RHF", "UHF", "ROHF", "CASSCF")
    # ROHF_CASE   = "ROHF_Case",   ORCAString, ("HighSpin", "CAHF", "SAHF", "USER_CSF", "AF_CSF")
    # ROHF_NEL    = "ROHF_NEl",    Sequence
    # ROHF_NUMOP  = "ROHF_NumOp",  int, None, None, 1, 3
    # ROHF_NORB   = "ROHF_NOrb",   Sequence
    # ROHF_REF    = "ROHF_Ref",    dict
    # ROHF_AFORBS = "ROHF_AFOrbs", Sequence

    # native xTB
    # XTBFOD      = "xTBFOD", bool
    # USEXTBMIXER = "UsexTBMixer", bool

    # ΔSCF Keywords
    # SOSCFMAXSTEP             = "SOSCFMaxStep",             float, 0.2
    # DELTASCFFROMGS           = "DeltaSCFFromGS",           bool,  True
    # SOSCFBLOCKDIAG           = "SOSCFBlockDiag",           bool,  False
    # DOMOM                    = "DoMOM",                    bool,  True
    # KEEPINITIALREF           = "KeepInitialRef",           bool,  True
    # PMOM                     = "PMOM",                     bool,  False
    # ALPHACONF                = "AlphaConf",                int,   None, None, 0, 2
    # BETACONF                 = "BetaConf",                 int,   None, None, 0, 2
    # IONIZEALPHA              = "IonizeAlpha",              int
    # IONIZEBETA               = "IonizeBeta",               int
    # SOSCFHESSUP              = "SOSCFHessUp",              ORCAString, 0, ("LSR1", "LBFGS", "LPowell", "LBOFill")
    # SOSCFCONSTRAINTS         = "SOSCFConstraints",         bool,  False
    # SOSCFCONSTRAINEDMAXSTEP  = "SOSCFConstrainedMaxStep",  float, 0.2
    # SOSCFCONVFACTOR          = "SOSCFConvFactor",          float, 1
    # SOSCFCONSTRAINEDHESSUP   = "SOSCFConstrainedHessUp",   ORCAString, 1, ("LSR1", "LBFGS", "LPowell", "LBOFill")
    # SOSCFWRITECONSTRAINEDGBW = "SOSCFWriteConstrainedGBW", bool,  True
    # SOSCFGMF                 = "SOSCFGMF",                 bool,  False
    # SOSCFDAVIDSONMAXIT       = "SOSCFDavidsonMaxIt",       int,   100
    # SOSCFDAVIDSONTOLR        = "SOSCFDavidsonTolR",        float, 0.01
    # SOSCFDAVIDSONMAXRED      = "SOSCFDavidsonMaxRed",      int,   20
    # SOSCFDAVIDSONFDMODE      = "SOSCFDavidsonFDMode",      ORCAString, 0, ("Forward", "Central")
    # SOSCFDAVIDSONFDSTEP      = "SOSCFDavidsonFDStep",      float, 0.001
    # SOSCFSPO                 = "SOSCFSPO",                 int
    # SOSCFSPOEST              = "SOSCFSPOEst",              ORCAString, 0, ("Auto", "Excitation", "HDiag", "Davidson")
    # SOSCFUPDATESPOEST        = "SOSCFUpdateSPOEst",        bool,  True
    # SOSCFSPOESTNTRIAL        = "SOSCFSPOEstNTrial",        int,   3
    # SOSCFUPDATESPOTHRESH     = "SOSCFUpdateSPOThresh",     float, -1
    # SOSCFPRECONDTYPE         = "SOSCFPrecondType",         ORCAString, 0, ("OrbitalEnergyDiff", "DavidsonUpdate", "GradientExpansion")
    # SOSCFPRECONDGAMMA        = "SOSCFPrecondGamma",        float, 0.25

    # Initial Guess
    GUESS     = "Guess",     ORCAString, 2, ("HCore", "Hueckel", "PAtom", "PModel", "MORead")
    MOINP     = "MOInp",     str
    GUESSMODE = "GuessMode", ORCAString, 0, ("FMatrix", "CMatrix")
    AUTOSTART = "AutoStart", bool, True


class TRAH(NestedBlockEnum):

    MAXRED          = "MaxRed",          int,   24
    NSTART          = "NStart",          int,   2, 2
    TOLFACMICRO     = "TolFacMicro",     float, 0.1
    MINTOLMICRO     = "MinTolMicro",     float, 1e-2
    QUADREGIONSTART = "QuadRegionStart", float, 1e-4
    TRADIUS         = "TRadius",         float, 0.4
    ALPHAMIN        = "AlphaMin",        float, 0.1
    ALPHAMAX        = "AlphaMax",        float, 1000
    RANDOMIZE       = "Randomize",       bool,  True
    PSEUDORAND      = "PseudoRand",      bool,  False
    MAXNOISE        = "MaxNoise",        float, 1e-2
    ORBUPDATE       = "OrbUpdate",       ORCAString, 0, ("Taylor", "Cayley")
    INACTIVEMOS     = "InactiveMOs",     ORCAString, 0, ("Canonical", "NotSet")
    PRECOND         = "Precond",         ORCAString, 0, ("Diag", "Full", "None")
    PRECONMAXRED    = "PreconMaxRed",    int,   250
# fmt: on
