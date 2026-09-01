# SPDX-FileCopyrightText: 2026 Avogadro Project
# SPDX-License-Identifier: BSD 3-Clause
# ******************************************************************************
# This source file is part of the Avogadro project.
#
# This source code is released under the New BSD License, (the "License").
# ******************************************************************************
from dataclasses import dataclass
from enum import Enum, Flag, StrEnum, auto


class Disp(Flag):
    """Dispersion corrections available in ORCA.

    Attributes
    ----------
    NODISP : 0
        Either no dispersion correction available, or the correction is
        part of the functional's name. (e.g. wB97M-V)
    D3BJ : 1
        D3 dispersion w/ Becke-Johnson Damping
    D3 : D3BJ
        Alias for `D3BJ`
    D3ZERO : 2
        D3 dispersion w/out Becke-Johnson Damping
    D4 : 4
        D4 dispersion
    NL : 8
        Non-local dispersion via the VV10 vdW correlation functional
    SCNL : 16
        Self-consistent variant of the non-local dispersion

    Notes
    -----
    The DFT-D and DFT-D2 dispersion corrections are deprecated, and so
    are not included here.

    The ``D3`` keyword automatically activates D3(BJ) dispersion in
    ORCA, so it is merely an alias for ``D3BJ`` here.

    You can access members by string with ``Disp["<member_name>"]``.
    """

    def __str__(self) -> str:
        match self:
            case Disp.NODISP:
                return ""
            case Disp.D3BJ:
                return "D3BJ"
            case Disp.D3ZERO:
                return "D3ZERO"
            case Disp.D4:
                return "D4"
            case Disp.NL:
                return "NL"
            case Disp.SCNL:
                return "SCNL"
            case _:
                raise ValueError("Invalid Dispersion, how did you even get here?")

    # fmt: off
    NODISP = 0
    D3BJ   = auto()
    D3     = D3BJ
    D3ZERO = auto()
    D4     = auto()
    NL     = auto() # VV10 Non-local dispersion correction
    SCNL   = auto() # Self-consistent variant
    # fmt: on


@dataclass
class Functional:
    """Class storing a functional's name and the available dispersion
    corrections.
    """

    func_name: str
    disp: Disp


# fmt: off

class Composite(StrEnum):
    """Composite -3c methods."""

    HF_3C     = "HF-3c"
    B97_3C    = "B97-3c"
    R2SCAN_3C = "r2SCAN-3c"
    PBEH_3C   = "PBEh-3c"
    B3LYP_3C  = "B3LYP-3c"
    WB97X_3C  = "wB97X-3c"


class Functionals(Functional, Enum):
    """Enumeration of all density functionals available via simple
    input keyword.

    Notes
    -----
    Functionals that already have a dispersion correction in their name
    are marked as having no dispersion corrections available. This is
    because trying to add a dispersion correction keyword to these
    functionals is either redundant or incorrect.

    Three functionals have a dispersion correction in their name,
    B97M-V, ωB97M-V, and ωB97X-V, but are marked with ``Disp.SCNL``.
    This is because these functionals, by default, use the
    non-self-consistent version of the NL correction, but it is still
    possible to switch on the self-consistent version with the SCNL
    keyword.
    """

    def __new__(
        cls,
        func_name: str,
        dispersion: Disp,
    ):
        functional = Functional.__new__(cls)
        functional._value_ = func_name
        return functional

    def __str__(self) -> str:
        return self.value

    # Local Density Approximation (LDA)
    HFS    = "HFS",   Disp.NODISP
    LDA    = "LDA",   Disp.NODISP
    LSD    = LDA
    VWN_5  = "VWN5",  Disp.NODISP
    VWN_3  = "VWN3",  Disp.NODISP
    PW_LDA = "PWLDA", Disp.NODISP

    # Generalized Gradient Approximation (GGA)
    BP86     = "BP86",       Disp.D4 | Disp.D3BJ | Disp.D3ZERO | Disp.NL | Disp.SCNL
    BLYP     = "BLYP",       Disp.D4 | Disp.D3BJ | Disp.D3ZERO | Disp.NL | Disp.SCNL
    OLYP     = "OLYP",       Disp.D4 | Disp.D3BJ
    GLYP     = "GLYP",       Disp.D4
    XLYP     = "XLYP",       Disp.D4
    PW91     = "PW91",       Disp.D4
    MPWPW    = "mPWPW",      Disp.D4
    MPWLYP   = "mPWLYP",     Disp.D4 | Disp.D3BJ | Disp.D3ZERO
    PBE      = "PBE",        Disp.D4 | Disp.D3BJ | Disp.D3ZERO | Disp.NL | Disp.SCNL
    RPBE     = "RPBE",       Disp.D4 | Disp.D3BJ | Disp.D3ZERO | Disp.NL | Disp.SCNL
    REVPBE   = "revPBE",     Disp.D4 | Disp.D3BJ | Disp.D3ZERO | Disp.NL | Disp.SCNL
    RPW86PBE = "RPW86PBE",   Disp.D4 | Disp.D3BJ | Disp.D3ZERO | Disp.NL | Disp.SCNL
    PWP      = "PWP",        Disp.D4

    # Meta GGA (mGGA)
    B97M_V    = "B97M-V",    Disp.SCNL
    B97M_D3BJ = "B97M-D3BJ", Disp.NODISP
    B97M_D4   = "B97M-D4",   Disp.NODISP
    SCANFUNC  = "SCANFUNC",  Disp.D4 | Disp.D3BJ | Disp.D3ZERO | Disp.NL | Disp.SCNL
    RSCAN     = "rSCAN",     Disp.D4 | Disp.D3BJ | Disp.D3ZERO | Disp.NL | Disp.SCNL
    R2SCAN    = "r2SCAN",    Disp.D4 | Disp.D3BJ | Disp.D3ZERO | Disp.NL | Disp.SCNL
    M06_L     = "M06L",      Disp.D4 | Disp.D3ZERO
    TPSS      = "TPSS",      Disp.D4 | Disp.D3BJ | Disp.D3ZERO | Disp.NL | Disp.SCNL
    REVTPSS   = "revTPSS",   Disp.D4

    # Hybrid GGA (hGGA)
    B1LYP     = "B1LYP",     Disp.D4
    B3LYP     = "B3LYP",     Disp.D4 | Disp.D3BJ | Disp.D3ZERO | Disp.NL | Disp.SCNL
    B3LYP_G   = "B3LYP/G",   Disp.NL | Disp.SCNL
    O3LYP     = "O3LYP",     Disp.D4
    X3LYP     = "X3LYP",     Disp.D4
    B1P86     = "B1P86",     Disp.NODISP
    B3P86     = "B3P86",     Disp.D4 | Disp.NL | Disp.SCNL
    B3PW91    = "B3PW91",    Disp.D4 | Disp.D3BJ | Disp.D3ZERO | Disp.NL | Disp.SCNL
    PW1PW     = "PW1PW",     Disp.D4 | Disp.NL | Disp.SCNL
    MPW1PW    = "mPW1PW",    Disp.D4 | Disp.NL | Disp.SCNL
    MPW1LYP   = "mPW1LYP",   Disp.D4
    PBE0      = "PBE0",      Disp.D4 | Disp.D3BJ | Disp.D3ZERO | Disp.NL | Disp.SCNL
    REVPBE0   = "revPBE0",   Disp.D4 | Disp.D3BJ | Disp.D3ZERO | Disp.NL | Disp.SCNL
    REVPBE38  = "revPBE38",  Disp.D4 | Disp.D3BJ | Disp.D3ZERO | Disp.NL | Disp.SCNL
    BHANDHLYP = "BHandHLYP", Disp.D4 | Disp.D3BJ | Disp.D3ZERO

    # Hybrid mGGA (hmGGA)
    M06      = "M06",      Disp.D4 | Disp.D3ZERO
    M06_2X   = "M062X",    Disp.D3ZERO
    PW6B95   = "PW6B95",   Disp.D4 | Disp.D3BJ | Disp.D3ZERO | Disp.NL | Disp.SCNL
    TPSSH    = "TPSSh",    Disp.D4 | Disp.D3BJ | Disp.D3ZERO | Disp.NL | Disp.SCNL
    TPSS0    = "TPSS0",    Disp.D4 | Disp.D3BJ | Disp.D3ZERO | Disp.NL | Disp.SCNL
    R2SCANH  = "r2SCANh",  Disp.D4 | Disp.D3BJ | Disp.NL | Disp.SCNL
    R2SCAN0  = "r2SCAN0",  Disp.D4 | Disp.D3BJ | Disp.NL | Disp.SCNL
    R2SCAN50 = "r2SCAN50", Disp.D4 | Disp.D3BJ | Disp.NL | Disp.SCNL

    # Range-Separated hGGA (rshGGA)
    WB97        = "wB97",        Disp.NODISP
    WB97X       = "wB97X",       Disp.NODISP
    WB97X_V     = "wB97X-V",     Disp.SCNL
    WB97X_D3    = "wB97X-D3",    Disp.NODISP
    WB97X_D3BJ  = "wB97X-D3BJ",  Disp.NODISP
    WB97X_D4    = "wB97X-D4",    Disp.NODISP
    WB97X_D4REV = "wB97X-D4rev", Disp.NODISP
    CAM_B3LYP   = "CAM-B3LYP",   Disp.D4 | Disp.D3BJ | Disp.D3ZERO
    LC_BLYP     = "LC-BLYP",     Disp.D4
    LC_PBE      = "LC-PBE",      Disp.NODISP

    # Range-Separated hmGGA (rshmGGA)
    WB97M_V     = "wB97M-V",     Disp.SCNL
    WB97M_D3BJ  = "wB97M-D3BJ",  Disp.NODISP
    WB97M_D4    = "wB97M-D4",    Disp.NODISP
    WB97M_D4REV = "wB97M-D4rev", Disp.NODISP
    WR2SCAN     = "wr2SCAN",     Disp.D4 | Disp.D3BJ | Disp.NL | Disp.SCNL

    # Double Hybrids (DH)
    DSD_BLYP              = "DSD-BLYP D3BJ",         Disp.NODISP
    DSD_BLYP_NODISP_2013  = "DSD-BLYP/2013",         Disp.D3BJ | Disp.NL | Disp.SCNL
    DSD_BLYP_2013_D3BJ    = "DSD-BLYP/2013 D3BJ",    Disp.NODISP
    DSD_PBEP86_D3BJ       = "DSD-PBEP86 D3BJ",       Disp.NODISP
    DSD_PBEP86_2013       = "DSD-PBEP86/2013",       Disp.NL | Disp.SCNL
    DSD_PBEP86_2013_D3BJ  = "DSD-PBEP86/2013 D3BJ",  Disp.NODISP
    DSD_PBEB95            = "DSD-PBEB95",            Disp.NODISP
    DSD_PBEB95_D3BJ       = "DSD-PBEB95 D3BJ",       Disp.NODISP
    B2PLYP                = "B2PLYP",                Disp.D4 | Disp.D3BJ | Disp.D3ZERO | Disp.NL | Disp.SCNL
    MPW2PLYP              = "mPW2PLYP",              Disp.D4
    B2GP_PLYP             = "B2GP-PLYP",             Disp.D4 | Disp.D3BJ | Disp.D3ZERO
    B2K_PLYP              = "B2K-PLYP",              Disp.NODISP
    B2T_PLYP              = "B2T-PLYP",              Disp.NODISP
    B2NC_PLYP             = "B2NC-PLYP",             Disp.NODISP
    PWPB95                = "PWPB95",                Disp.D4 | Disp.D3BJ | Disp.D3ZERO | Disp.NL | Disp.SCNL
    PBE_QIDH              = "PBE-QIDH",              Disp.D3BJ | Disp.D3ZERO
    PBE0_DH               = "PBE0-DH",               Disp.D3BJ | Disp.D3ZERO
    REVDSD_PBEP86_2021    = "revDSD-PBEP86/2021",    Disp.NODISP
    REVDSD_PBEP86_D4_2021 = "revDSD-PBEP86-D4/2021", Disp.NODISP
    REVDOD_PBEP86_2021    = "revDOD-PBEP86/2021",    Disp.NODISP
    REVDOD_PBEP86_D4_2021 = "revDOD-PBEP86-D4/2021", Disp.NODISP
    R2SCAN_CIDH           = "r2SCAN-CIDH",           Disp.D4 | Disp.D3BJ
    R2SCAN_QIDH           = "r2SCAN-QIDH",           Disp.D4 | Disp.D3BJ
    R2SCAN0_2             = "r2SCAN0-2",             Disp.D4 | Disp.D3BJ
    R2SCAN0_DH            = "r2SCAN0-DH",            Disp.D4 | Disp.D3BJ
    PR2SCAN50             = "Pr2SCAN50",             Disp.D4 | Disp.D3BJ | Disp.NL | Disp.SCNL
    PR2SCAN69             = "Pr2SCAN69",             Disp.D4 | Disp.D3BJ | Disp.NL | Disp.SCNL
    KPR2SCAN50            = "kPr2SCAN",              Disp.D4 | Disp.D3BJ | Disp.NL | Disp.SCNL
    SCS_SOS_B2PLYP21      = "SCS/SOS-B2PLYP21",      Disp.NODISP
    SCS_PBE_QIDH          = "SCS-PBE-QIDH",          Disp.NODISP
    SOS_PBE_QIDH          = "SOS-PBE-QIDH",          Disp.NODISP
    SCS_B2GP_PLYP21       = "SCS-B2GP-PLYP21",       Disp.NODISP
    SOS_B2GP_PLYP21       = "SOS-B2GP-PLYP21",       Disp.NODISP
# fmt: on
