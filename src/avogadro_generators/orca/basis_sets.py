# SPDX-FileCopyrightText: 2026 Avogadro Project
# SPDX-License-Identifier: BSD 3-Clause
# ******************************************************************************
# This source file is part of the Avogadro project.
#
# This source code is released under the New BSD License, (the "License").
# ******************************************************************************
import re
from dataclasses import dataclass
from enum import Enum

from ..utilities import Element


@dataclass(init=False, frozen=False)
class BasisSet:
    """Dataclass to store a basis set's name, the supported elements,
    and the ECPs that may required for heavy elements.
    """

    basis_name: str
    elements: tuple[Element]
    ecp: str | None
    ecp_elements: tuple[Element] | None

    def __init__(
        self,
        basis_name: str,
        element_ranges: tuple[str],
        ecp: str | None = None,
        ecp_elements: tuple[str] | None = None,
    ):
        self.basis_name = basis_name
        self.elements = BasisSet.split_elements(element_ranges)
        self.ecp = ecp
        self.ecp_elements = (
            BasisSet.split_elements(ecp_elements) if ecp_elements is not None else None
        )

    @staticmethod
    def split_elements(element_ranges: list[str]) -> tuple[Element]:
        """Take a list of strings of the general form ``["H-Br"]`` and
        convert it into a tuple of ``Element`` that indicate all of the
        elements that are defined in the basis set.
        """
        elements = []
        for elem_range in element_ranges:
            if "-" not in elem_range:
                elements.append(Element[elem_range])
            else:
                elem_range = elem_range.split("-")
                start = Element[elem_range[0]]
                end = Element[elem_range[1]]
                for num in range(start.number, end.number + 1):
                    elements.append(Element(num))

        return tuple(elements)

    def __hash__(self):
        return hash(
            (
                self.basis_name,
                self.elements,
                self.ecp,
                self.ecp_elements,
            )
        )


class BasisSetEnum(BasisSet, Enum):
    """Base class for basis set enums."""

    def __new__(
        cls,
        basis_name: str,
        element_ranges: tuple[str],
        ecp: str | None = None,
        ecp_elements: tuple[str] | None = None,
    ):
        self = BasisSet.__new__(cls)
        self._name_ = basis_name
        self._value_ = basis_name
        return self

    def __str__(self):
        return self.basis_name


# fmt: off
class PopleBasisSet(BasisSetEnum):
    """All Pople-style (X-YZG) basis sets in ORCA.

    Naming convention for members includes a ``b`` at the start, a
    lowercase ``p`` to denote a " + ".

    Basis sets that use the asterisk shorthand (e.g. 6-31G* or 6-31G**)
    are not explicitly written here as the asterisk shorthand maps to
    existing basis sets. One asterisk is equivalent to (d), and two
    asterisks is equivalent to (d,p).

    For example, 6-31G* translates to 6-31G(d), and 6-31G** translates
    to 6-31G(d,p).
    """

    @classmethod
    def _missing_(cls, value: str):
        """Add translation for sets that use an asterisk."""
        if "**" in value:
            value = value.replace("**", "(d,p)")
        elif "*" in value:
            value = value.replace("*", "(d)")

        for member in cls:
            if member.name == value:
                return member
        return None

    bSTO_3G                    = "STO-3G",            ("H-I", )
    b3_21G                     = "3-21G",             ("H-Cs",)
    b3_21GSP                   = "3-21GSP",           ("H-Ar",)
    b4_22GSP                   = "4-22GSP",           ("H-Ar",)
    b6_31G                     = "6-31G",             ("H-Zn",)
    b6_31G_D                   = "6-31G(d)",          ("H-Zn",)
    b6_31G_D_P                 = "6-31G(d,p)",        ("H-Zn",)
    b6_31G_2D                  = "6-31G(2d)",         ("H-Zn",)
    b6_31G_2D_P                = "6-31G(2d,p)",       ("H-Zn",)
    b6_31G_2D_2P               = "6-31G(2d,2p)",      ("H-Zn",)
    b6_31G_2DF                 = "6-31G(2df)",        ("H-Zn",)
    b6_31G_2DF_2P              = "6-31G(2df,2p)",     ("H-Zn",)
    b6_31G_2DF_2PD             = "6-31G(2df,2pd)",    ("H-Zn",)
    b6_31_PLUS_G_D             = "6-31+G(d)",         ("H-Zn",)
    b6_31_PLUS_G_D_P           = "6-31+G(d,p)",       ("H-Zn",)
    b6_31_PLUS_G_2D            = "6-31+G(2d)",        ("H-Zn",)
    b6_31_PLUS_G_2D_P          = "6-31+G(2d,p)",      ("H-Zn",)
    b6_31_PLUS_G_2D_2P         = "6-31+G(2d,2p)",     ("H-Zn",)
    b6_31_PLUS_G_2DF           = "6-31+G(2df)",       ("H-Zn",)
    b6_31_PLUS_G_2DF_2P        = "6-31+G(2df,2p)",    ("H-Zn",)
    b6_31_PLUS_G_2DF_2PD       = "6-31+G(2df,2pd)",   ("H-Zn",)
    b6_31_PLUS_PLUS_G_D_P      = "6-31++G(d,p)",      ("H-Zn",)
    b6_31_PLUS_PLUS_G_2D_P     = "6-31++G(2d,p)",     ("H-Zn",)
    b6_31_PLUS_PLUS_G_2D_2P    = "6-31++G(2d,2p)",    ("H-Zn",)
    b6_31_PLUS_PLUS_G_2DF_2P   = "6-31++G(2df,2p)",   ("H-Zn",)
    b6_31_PLUS_PLUS_G_2DF_2PD  = "6-31++G(2df,2pd)",  ("H-Zn",)
    b6_311G                    = "6-311G",            ("H-Br",)
    b6_311G_D                  = "6-311G(d)",         ("H-Br",)
    b6_311G_D_P                = "6-311G(d,p)",       ("H-Br",)
    b6_311G_2D                 = "6-311G(2d)",        ("H-Br",)
    b6_311G_2D_P               = "6-311G(2d,p)",      ("H-Br",)
    b6_311G_2D_2P              = "6-311G(2d,2p)",     ("H-Br",)
    b6_311G_2DF                = "6-311G(2df)",       ("H-Br",)
    b6_311G_2DF_2P             = "6-311G(2df,2p)",    ("H-Br",)
    b6_311G_2DF_2PD            = "6-311G(2df,2pd)",   ("H-Br",)
    b6_311G_3DF                = "6-311G(3df)",       ("H-Br",)
    b6_311G_3DF_3PD            = "6-311G(3df,3pd)",   ("H-Br",)
    b6_311_PLUS_G_D            = "6-311+G(d)",        ("H-Br",)
    b6_311_PLUS_G_D_P          = "6-311+G(d,p)",      ("H-Br",)
    b6_311_PLUS_G_2D           = "6-311+G(2d)",       ("H-Br",)
    b6_311_PLUS_G_2D_P         = "6-311+G(2d,p)",     ("H-Br",)
    b6_311_PLUS_G_2D_2P        = "6-311+G(2d,2p)",    ("H-Br",)
    b6_311_PLUS_G_2DF          = "6-311+G(2df)",      ("H-Br",)
    b6_311_PLUS_G_2DF_2P       = "6-311+G(2df,2p)",   ("H-Br",)
    b6_311_PLUS_G_2DF_2PD      = "6-311+G(2df,2pd)",  ("H-Br",)
    b6_311_PLUS_G_3DF          = "6-311+G(3df)",      ("H-Br",)
    b6_311_PLUS_G_3DF_2P       = "6-311+G(3df,2p)",   ("H-Br",)
    b6_311_PLUS_G_3DF_3PD      = "6-311+G(3df,3pd)",  ("H-Br",)
    b6_311_PLUS_PLUS_G_D_P     = "6-311++G(d,p)",     ("H-Br",)
    b6_311_PLUS_PLUS_G_2D_P    = "6-311++G(2d,p)",    ("H-Br",)
    b6_311_PLUS_PLUS_G_2D_2P   = "6-311++G(2d,2p)",   ("H-Br",)
    b6_311_PLUS_PLUS_G_2DF_2P  = "6-311++G(2df,2p)",  ("H-Br",)
    b6_311_PLUS_PLUS_G_2DF_2PD = "6-311++G(2df,2pd)", ("H-Br",)
    b6_311_PLUS_PLUS_G_3DF_3PD = "6-311++G(3df,3pd)", ("H-Br",)
    bm6_31G                    = "m6-31G",            ("Sc-Cu",)
    bm6_31G_STAR               = "m6-31G*",           ("Sc-Cu",)


class def2BasisSet(BasisSetEnum):
    """Karlsruhe def2 family of basis sets."""

    DEF2_SVP        = "def2-SVP",         ("H-Rn",), "def2-ECP", ("Rb-Rn",)
    DEF2_SV_P_      = "def2-SV(P)",       ("H-Rn",), "def2-ECP", ("Rb-Rn",)
    DEF2_TZVP       = "def2-TZVP",        ("H-Rn",), "def2-ECP", ("Rb-Rn",)
    DEF2_TZVP_F_    = "def2-TZVP(-f)",    ("H-Rn",), "def2-ECP", ("Rb-Rn",)
    DEF2_TZVPP      = "def2-TZVPP",       ("H-Rn",), "def2-ECP", ("Rb-Rn",)
    DEF2_QZVP       = "def2-QZVP",        ("H-Rn",), "def2-ECP", ("Rb-Rn",)
    DEF2_QZVPP      = "def2-QZVPP",       ("H-Rn",), "def2-ECP", ("Rb-Rn",)

    # Diffuse-Augmented
    DEF2_SVPD       = "def2-SVPD",        ("H-Rn",), "def2-ECP", ("Rb-Rn",)
    DEF2_TZVPD      = "def2-TZVPD",       ("H-Rn",), "def2-ECP", ("Rb-Rn",)
    DEF2_TZVPPD     = "def2-TZVPPD",      ("H-Rn",), "def2-ECP", ("Rb-Rn",)
    DEF2_QZVPD      = "def2-QZVPD",       ("H-Rn",), "def2-ECP", ("Rb-Rn",)
    DEF2_QZVPPD     = "def2-QZVPPD",      ("H-Rn",), "def2-ECP", ("Rb-Rn",)

    # Minimally Augmented
    MA_DEF2_SVP     = "ma-def2-SVP",      ("H-Rn",), "def2-ECP", ("Rb-Rn",)
    MA_DEF2_SV_P_   = "ma-def2-SV(P)",    ("H-Rn",), "def2-ECP", ("Rb-Rn",)
    MA_DEF2_MSVP    = "ma-def2-mSVP",     ("H-Rn",), "def2-ECP", ("Rb-Rn",)
    MA_DEF2_TZVP    = "ma-def2-TZVP",     ("H-Rn",), "def2-ECP", ("Rb-Rn",)
    MA_DEF2_TZVP_F_ = "ma-def2-TZVP(-f)", ("H-Rn",), "def2-ECP", ("Rb-Rn",)
    MA_DEF2_TZVPP   = "ma-def2-TZVPP",    ("H-Rn",), "def2-ECP", ("Rb-Rn",)
    MA_DEF2_QZVPP   = "ma-def2-QZVPP",    ("H-Rn",), "def2-ECP", ("Rb-Rn",)


class JensenBasisSet(BasisSetEnum):
    """Jensen polarization-consistent basis sets and their variants."""

    PC_0         = "pc-0",         ("H-Ca", "Ga-Kr")
    PC_1         = "pc-1",         ("H-Kr",)
    PC_2         = "pc-2",         ("H-Kr",)
    PC_3         = "pc-3",         ("H-Kr",)
    PC_4         = "pc-4",         ("H-Kr",)
    AUG_PC_0     = "aug-pc-0",     ("H-Ca", "Ga-Kr")
    AUG_PC_1     = "aug-pc-1",     ("H-Kr",)
    AUG_PC_2     = "aug-pc-2",     ("H-Kr",)
    AUG_PC_3     = "aug-pc-3",     ("H-Kr",)
    AUG_PC_4     = "aug-pc-4",     ("H-Kr",)

    # Segmented contraction variants
    PCSEG_0      = "pcseg-0",      ("H-Kr",)
    PCSEG_1      = "pcseg-1",      ("H-Kr",)
    PCSEG_2      = "pcseg-2",      ("H-Kr",)
    PCSEG_3      = "pcseg-3",      ("H-Kr",)
    PCSEG_4      = "pcseg-4",      ("H-Kr",)
    AUG_PCSEG_0  = "aug-pcseg-0",  ("H-Kr",)
    AUG_PCSEG_1  = "aug-pcseg-1",  ("H-Kr",)
    AUG_PCSEG_2  = "aug-pcseg-2",  ("H-Kr",)
    AUG_PCSEG_3  = "aug-pcseg-3",  ("H-Kr",)
    AUG_PCSEG_4  = "aug-pcseg-4",  ("H-Kr",)

    # Optimized for nuclear magnetic shieldings
    PCSSEG_0     = "pcSseg-0",     ("H-Kr",)
    PCSSEG_1     = "pcSseg-1",     ("H-Kr",)
    PCSSEG_2     = "pcSseg-2",     ("H-Kr",)
    PCSSEG_3     = "pcSseg-3",     ("H-Kr",)
    PCSSEG_4     = "pcSseg-4",     ("H-Kr",)
    AUG_PCSSEG_0 = "aug-pcSseg-0", ("H-Kr",)
    AUG_PCSSEG_1 = "aug-pcSseg-1", ("H-Kr",)
    AUG_PCSSEG_2 = "aug-pcSseg-2", ("H-Kr",)
    AUG_PCSSEG_3 = "aug-pcSseg-3", ("H-Kr",)
    AUG_PCSSEG_4 = "aug-pcSseg-4", ("H-Kr",)

    # Optimized for spin-spin coupling constants
    PCJ_0        = "pcJ-0",        ("H-He", "B-Ne", "Al-Ar")
    PCJ_1        = "pcJ-1",        ("H-He", "B-Ne", "Al-Ar")
    PCJ_2        = "pcJ-2",        ("H-He", "B-Ne", "Al-Ar")
    PCJ_3        = "pcJ-3",        ("H-He", "B-Ne", "Al-Ar")
    PCJ_4        = "pcJ-4",        ("H-He", "B-Ne", "Al-Ar")
    AUG_PCJ_0    = "aug-pcJ-0",    ("H-He", "B-Ne", "Al-Ar")
    AUG_PCJ_1    = "aug-pcJ-1",    ("H-He", "B-Ne", "Al-Ar")
    AUG_PCJ_2    = "aug-pcJ-2",    ("H-He", "B-Ne", "Al-Ar")
    AUG_PCJ_3    = "aug-pcJ-3",    ("H-He", "B-Ne", "Al-Ar")
    AUG_PCJ_4    = "aug-pcJ-4",    ("H-He", "B-Ne", "Al-Ar")

    # Optimized for hyperfine coupling constants
    PCH_1        = "pcH-1",        ("H-He", "B-Ne", "Al-Ar")
    PCH_2        = "pcH-2",        ("H-He", "B-Ne", "Al-Ar")
    PCH_3        = "pcH-3",        ("H-He", "B-Ne", "Al-Ar")
    PCH_4        = "pcH-4",        ("H-He", "B-Ne", "Al-Ar")
    AUG_PCH_1    = "aug-pcH-1",    ("H-He", "B-Ne", "Al-Ar")
    AUG_PCH_2    = "aug-pcH-2",    ("H-He", "B-Ne", "Al-Ar")
    AUG_PCH_3    = "aug-pcH-3",    ("H-He", "B-Ne", "Al-Ar")
    AUG_PCH_4    = "aug-pcH-4",    ("H-He", "B-Ne", "Al-Ar")

    # Optimized for core spectroscopy
    PCX_1        = "pcX-1",        ("Li-Ar",)
    PCX_2        = "pcX-2",        ("Li-Ar",)
    PCX_3        = "pcX-3",        ("Li-Ar",)
    PCX_4        = "pcX-4",        ("Li-Ar",)
    AUG_PCX_1    = "aug-pcX-1",    ("Li-Ar",)
    AUG_PCX_2    = "aug-pcX-2",    ("Li-Ar",)
    AUG_PCX_3    = "aug-pcX-3",    ("Li-Ar",)
    AUG_PCX_4    = "aug-pcX-4",    ("Li-Ar",)


class ccBasisSet(BasisSetEnum):
    """Correlation Consistent basis sets, cc-pVnZ."""

    CC_PVDZ               = "cc-pVDZ",          ("H-Ar", "Ca-Kr")
    CC_PVTZ               = "cc-pVTZ",          ("H-Ar", "Ca-Kr", "Y", "Ag", "Au")
    CC_PVQZ               = "cc-pVQZ",          ("H-Ar", "Ca-Kr")
    CC_PV5Z               = "cc-pV5Z",          ("H-Ar", "Ca-Kr")
    CC_PV6Z               = "cc-pV6Z",          ("H-He", "Be-Ne", "Al-Ar")
    AUG_CC_PVDZ           = "aug-cc-pVDZ",      ("H-Ar", "Sc-Kr")
    AUG_CC_PVTZ           = "aug-cc-pVTZ",      ("H-Ar", "Sc-Kr", "Ag", "Au")
    AUG_CC_PVQZ           = "aug-cc-pVQZ",      ("H-Ar", "Sc-Kr")
    AUG_CC_PV5Z           = "aug-cc-pV5Z",      ("H-Ar", "Sc-Kr")
    AUG_CC_PV6Z           = "aug-cc-pV6Z",      ("H-He", "B-Ne", "Al-Ar")
    CC_PVD_PLUS_D_Z       = "cc-pVD(+d)Z",      ("Na-Ar",)
    CC_PVT_PLUS_D_Z       = "cc-pVT(+d)Z",      ("Na-Ar",)
    CC_PVQ_PLUS_D_Z       = "cc-pVQ(+d)Z",      ("Na-Ar",)
    CC_PV5_PLUS_D_Z       = "cc-pV5(+d)Z",      ("Na-Ar",)
    AUG_CC_PVD_PLUS_D_Z   = "aug-cc-pVD(+d)Z",  ("Al-Ar",)
    AUG_CC_PVT_PLUS_D_Z   = "aug-cc-pVT(+d)Z",  ("Al-Ar",)
    AUG_CC_PVQ_PLUS_D_Z   = "aug-cc-pVQ(+d)Z",  ("Al-Ar",)
    AUG_CC_PV5_PLUS_D_Z   = "aug-cc-pV5(+d)Z",  ("Al-Ar",)
    AUG_CC_PV6_PLUS_D_Z   = "aug-cc-pV6(+d)Z",  ("Al-Ar",)
    APR_CC_PV_Q_PLUS_D_Z  = "apr-cc-pV(Q+d)Z",  ("H-Ar",)
    MAY_CC_PV_T_PLUS_D_Z  = "may-cc-pV(T+d)Z",  ("H-Ar",)
    MAY_CC_PV_Q_PLUS_D_Z  = "may-cc-pV(Q+d)Z",  ("H-Ar",)
    JUN_CC_PV_D_PLUS_D_Z  = "jun-cc-pV(D+d)Z",  ("H-Ar",)
    JUN_CC_PV_T_PLUS_D_Z  = "jun-cc-pV(T+d)Z",  ("H-Ar",)
    JUN_CC_PV_Q_PLUS_D_Z  = "jun-cc-pV(Q+d)Z",  ("H-Ar",)
    JUL_CC_PV_D_PLUS_D_Z  = "jul-cc-pV(D+d)Z",  ("H-Ar",)
    JUL_CC_PV_T_PLUS_D_Z  = "jul-cc-pV(T+d)Z",  ("H-Ar",)
    JUL_CC_PV_Q_PLUS_D_Z  = "jul-cc-pV(Q+d)Z",  ("H-Ar",)
    MAUG_CC_PV_D_PLUS_D_Z = "maug-cc-pV(D+d)Z", ("H-Ar",)
    MAUG_CC_PV_T_PLUS_D_Z = "maug-cc-pV(T+d)Z", ("H-Ar",)
    MAUG_CC_PV_Q_PLUS_D_Z = "maug-cc-pV(Q+d)Z", ("H-Ar",)
    CC_PCVDZ              = "cc-pCVDZ",         ("H-Ar", "Ca",   "Ga-Kr")
    CC_PCVTZ              = "cc-pCVTZ",         ("H-Ar", "Ca",   "Ga-Kr")
    CC_PCVQZ              = "cc-pCVQZ",         ("H-Ar", "Ca",   "Ga-Kr")
    CC_PCV5Z              = "cc-pCV5Z",         ("H-Ar", "Ca",   "Ga-Kr")
    CC_PCV6Z              = "cc-pCV6Z",         ("H-He", "B-Ne", "Al-Ar")
    AUG_CC_PCVDZ          = "aug-cc-pCVDZ",     ("H-Ar", "Ga-Kr")
    AUG_CC_PCVTZ          = "aug-cc-pCVTZ",     ("H-Ar", "Ga-Kr")
    AUG_CC_PCVQZ          = "aug-cc-pCVQZ",     ("H-Ar", "Ga-Kr")
    AUG_CC_PCV5Z          = "aug-cc-pCV5Z",     ("H-Ar", "Ga-Kr")
    AUG_CC_PCV6Z          = "aug-cc-pCV6Z",     ("H-He", "B-Ne",  "Al-Ar")
    CC_PWCVDZ             = "cc-pwCVDZ",        ("H-Ar", "Ca",    "Ga-Kr")
    CC_PWCVTZ             = "cc-pwCVTZ",        ("H-Ar", "Ca-Kr", "Ag", "Au")
    CC_PWCVQZ             = "cc-pwCVQZ",        ("H-Ar", "Ca-Kr")
    CC_PWCV5Z             = "cc-pwCV5Z",        ("H-Ar", "Ca-Kr")
    AUG_CC_PWCVDZ         = "aug-cc-pwCVDZ",    ("H-Ar", "Ga-Kr")
    AUG_CC_PWCVTZ         = "aug-cc-pwCVTZ",    ("H-Ar", "Sc-Kr", "Ag", "Au")
    AUG_CC_PWCVQZ         = "aug-cc-pwCVQZ",    ("H-Ar", "Sc-Kr")
    AUG_CC_PWCV5Z         = "aug-cc-pwCV5Z",    ("H-Ar", "Sc-Kr")


class RelativisticBasisSet(BasisSetEnum):
    """Relativistic basis sets for the DKH, ZORA, or X2C approaches."""

    # Recontracted Ahlrichs Basis Sets
    DKH_SV_P_   = "DKH-SV(P)",   ("H-Kr",)
    DKH_SVP     = "DKH-SVP",     ("H-Kr",)
    DKH_TZV_P_  = "DKH-TZV(P)",  ("H-Kr",)
    DKH_TZVP    = "DKH-TZVP",    ("H-Kr",)
    DKH_TZVPP   = "DKH-TZVPP",   ("H-Kr",)
    DKH_QZVP    = "DKH-QZVP",    ("H-Kr",)
    DKH_QZVPP   = "DKH-QZVPP",   ("H-Kr",)
    ZORA_SV_P_  = "ZORA-SV(P)",  ("H-Kr",)
    ZORA_SVP    = "ZORA-SVP",    ("H-Kr",)
    ZORA_TZV_P_ = "ZORA-TZV(P)", ("H-Kr",)
    ZORA_TZVP   = "ZORA-TZVP",   ("H-Kr",)
    ZORA_TZVPP  = "ZORA-TZVPP",  ("H-Kr",)
    ZORA_QZVP   = "ZORA-QZVP",   ("H-Kr",)
    ZORA_QZVPP  = "ZORA-QZVPP",  ("H-Kr",)

    # Recontracted def2 basis sets
    DKH_DEF2_SVP         = "DKH-def2-SVP",          ("H-Kr",)
    DKH_DEF2_SV_P_       = "DKH-def2-SV(P)",        ("H-Kr",)
    DKH_DEF2_TZVP        = "DKH-def2-TZVP",         ("H-Kr",)
    DKH_DEF2_TZVP_F_     = "DKH-def2-TZVP(-f)",     ("H-Kr",)
    DKH_DEF2_TZVPP       = "DKH-def2-TZVPP",        ("H-Kr",)
    DKH_DEF2_QZVPP       = "DKH-def2-QZVPP",        ("H-Kr",)
    ZORA_DEF2_SVP        = "ZORA-def2-SVP",         ("H-Kr",)
    ZORA_DEF2_SV_P_      = "ZORA-def2-SV(P)",       ("H-Kr",)
    ZORA_DEF2_TZVP       = "ZORA-def2-TZVP",        ("H-Kr",)
    ZORA_DEF2_TZVP_F_    = "ZORA-def2-TZVP(-f)",    ("H-Kr",)
    ZORA_DEF2_TZVPP      = "ZORA-def2-TZVPP",       ("H-Kr",)
    ZORA_DEF2_QZVPP      = "ZORA-def2-QZVPP",       ("H-Kr",)
    # Minimally augmented variants
    MA_DKH_DEF2_SVP      = "ma-DKH-def2-SVP",       ("H-Kr",)
    MA_DKH_DEF2_SV_P_    = "ma-DKH-def2-SV(P)",     ("H-Kr",)
    MA_DKH_DEF2_TZVP     = "ma-DKH-def2-TZVP",      ("H-Kr",)
    MA_DKH_DEF2_TZVP_F_  = "ma-DKH-def2-TZVP(-f)",  ("H-Kr",)
    MA_DKH_DEF2_TZVPP    = "ma-DKH-def2-TZVPP",     ("H-Kr",)
    MA_DKH_DEF2_QZVPP    = "ma-DKH-def2-QZVPP",     ("H-Kr",)
    MA_ZORA_DEF2_SVP     = "ma-ZORA-def2-SVP",      ("H-Kr",)
    MA_ZORA_DEF2_SV_P_   = "ma-ZORA-def2-SV(P)",    ("H-Kr",)
    MA_ZORA_DEF2_TZVP    = "ma-ZORA-def2-TZVP",     ("H-Kr",)
    MA_ZORA_DEF2_TZVP_F_ = "ma-ZORA-def2-TZVP(-f)", ("H-Kr",)
    MA_ZORA_DEF2_TZVPP   = "ma-ZORA-def2-TZVPP",    ("H-Kr",)
    MA_ZORA_DEF2_QZVPP   = "ma-ZORA-def2-QZVPP",    ("H-Kr",)

    # Segmented all-electron relativistically contracted basis sets
    SARC_DKH_SVP    = "SARC-DKH-SVP",    ("Hf-Hg",)
    SARC_DKH_TZVP   = "SARC-DKH-TZVP",   ("Rb-Rn", "Ac-Lr")
    SARC_DKH_TZVPP  = "SARC-DKH-TZVPP",  ("Rb-Rn", "Ac-Lr")
    SARC_ZORA_SVP   = "SARC-ZORA-SVP",   ("Hf-Hg",)
    SARC_ZORA_TZVP  = "SARC-ZORA-TZVP",  ("Rb-Rn", "Ac-Lr")
    SARC_ZORA_TZVPP = "SARC-ZORA-TZVPP", ("Rb-Rn", "Ac-Lr")

    # Quadruple-zeta SARC basis sets for lanthanides
    SARC2_DKH_QZV   = "SARC2-DKH-QZV",   ("La-Lu",)
    SARC2_DKH_QZVP  = "SARC2-DKH-QZVP",  ("La-Lu",)
    SARC2_ZORA_QZV  = "SARC2-ZORA-QZV",  ("La-Lu",)
    SARC2_ZORA_QZVP = "SARC2-ZORA-QZVP", ("La-Lu",)

    # All-electron X2C Basis Sets
    X2C_SV_P_ALL      = "x2c-SV(P)all",      ("H-Rn",)
    X2C_SVPALL        = "x2c-SVPall",        ("H-Rn",)
    X2C_TZVPALL       = "x2c-TZVPall",       ("H-Rn",)
    X2C_TZVPPALL      = "x2c-TZVPPall",      ("H-Rn",)
    X2C_QZVPALL       = "x2c-QZVPall",       ("H-Rn",)
    X2C_QZVPPALL      = "x2c-QZVPPall",      ("H-Rn",)
    # NMR Shielding Optimized
    X2C_SV_P_ALL_S    = "x2c-SV(P)all-s",    ("H-Rn",)
    X2C_SVPALL_S      = "x2c-SVPall-s",      ("H-Rn",)
    X2C_TZVPALL_S     = "x2c-TZVPall-s",     ("H-Rn",)
    X2C_TZVPPALL_S    = "x2c-TZVPPall-s",    ("H-Rn",)
    X2C_QZVPALL_S     = "x2c-QZVPall-s",     ("H-Rn",)
    X2C_QZVPPALL_S    = "x2c-QZVPPall-s",    ("H-Rn",)
    # Two-component variants, not actually implemented yet
    # X2C_SV_P_ALL_2C   = "x2c-SV(P)all-2c",   ("H-Rn",)
    # X2C_SVPALL_2C     = "x2c-SVPall-2c",     ("H-Rn",)
    # X2C_TZVPALL_2C    = "x2c-TZVPall-2c",    ("H-Rn",)
    # X2C_TZVPPALL_2C   = "x2c-TZVPPall-2c",   ("H-Rn",)
    # X2C_QZVPALL_2C    = "x2c-QZVPall-2c",    ("H-Rn",)
    # X2C_QZVPPALL_2C   = "x2c-QZVPPall-2c",   ("H-Rn",)
    # X2C_QZVPALL_2C_S  = "x2c-QZVPall-2c-s",  ("H-Rn",)
    # X2C_QZVPPALL_2C_S = "x2c-QZVPPall-2c-s", ("H-Rn",)

    # Correlation-Consistent Relativistic Basis Set
    CC_PVDZ_DK       = "cc-pVDZ-DK",       ("H-Ar", "Sc-Kr")
    CC_PVTZ_DK       = "cc-pVTZ-DK",       ("H-Ar", "Sc-Kr", "Y-Xe",  "Hf-Rn")
    CC_PVQZ_DK       = "cc-pVQZ-DK",       ("H-Ar", "Sc-Kr", "In-Xe", "Tl-Rn")
    CC_PV5Z_DK       = "cc-pV5Z-DK",       ("H-Ar", "Sc-Kr")
    CC_PVDZ_DK3      = "cc-pVDZ-DK3",      ("U",)
    CC_PVTZ_DK3      = "cc-pVTZ-DK3",      ("U",)
    CC_PVQZ_DK3      = "cc-pVQZ-DK3",      ("U",)
    AUG_CC_PVDZ_DK   = "aug-cc-pVDZ-DK",   ("H-Ar", "Sc-Kr")
    AUG_CC_PVTZ_DK   = "aug-cc-pVTZ-DK",   ("H-Ar", "Sc-Kr", "Y-Xe",  "Hf-Rn")
    AUG_CC_PVQZ_DK   = "aug-cc-pVQZ-DK",   ("H-Ar", "Sc-Kr", "In-Xe", "Tl-Rn")
    AUG_CC_PV5Z_DK   = "aug-cc-pV5Z-DK",   ("H-Ar", "Sc-Kr")
    CC_PWCVDZ_DK     = "cc-pwCVDZ-DK",     ("H-Be", "Na-Mg", "Ca-Zn")
    CC_PWCVTZ_DK     = "cc-pwCVTZ-DK",     ("H-Be", "Na-Mg", "Ca-Zn", "Y-Xe",  "Hf-Rn")
    CC_PWCVQZ_DK     = "cc-pwCVQZ-DK",     ("H-Be", "Na-Mg", "Ca-Zn", "In-Xe", "Tl-Rn")
    CC_PWCV5Z_DK     = "cc-pwCV5Z-DK",     ("H-Be", "Na-Mg", "Ca-Zn")
    CC_PWCVDZ_DK3    = "cc-pwCVDZ-DK3",    ("U",)
    CC_PWCVTZ_DK3    = "cc-pwCVTZ-DK3",    ("U",)
    CC_PWCVQZ_DK3    = "cc-pwCVQZ-DK3",    ("U",)
    AUG_CC_PWCVDZ_DK = "aug-cc-pwCVDZ-DK", ("H-Be", "Na-Mg", "Sc-Zn")
    AUG_CC_PWCVTZ_DK = "aug-cc-pwCVTZ-DK", ("H-Be", "Na-Mg", "Sc-Zn", "Y-Xe",  "Hf-Rn")
    AUG_CC_PWCVQZ_DK = "aug-cc-pwCVQZ-DK", ("H-Be", "Na-Mg", "Sc-Zn", "In-Xe", "Tl-Rn")
    AUG_CC_PWCV5Z_DK = "aug-cc-pwCV5Z-DK", ("H-Be", "Na-Mg", "Sc-Zn")

    # Relativistically Contracted ANO Basis Sets
    ANO_RCC_Full = "ANO-RCC-Full", ("H-Cm",)
    ANO_RCC_DZP  = "ANO-RCC-DZP",  ("H-Cm",)
    ANO_RCC_TZP  = "ANO-RCC-TZP",  ("H-Cm",)
    ANO_RCC_QZP  = "ANO-RCC-QZP",  ("H-Cm",)
# fmt: on


@dataclass(init=False, frozen=False)
class AuxBasisSet:
    """Dataclass to store a basis set's name, the supported elements,
    and the ECPs that may required for heavy elements.
    """

    basis_name: str
    elements: tuple[Element]
    # ecp: str | None
    # ecp_elements: tuple[Element] | None

    def __init__(
        self,
        name: str,
        element_ranges: tuple[str],
        parent_basis: PopleBasisSet
        | def2BasisSet
        | JensenBasisSet
        | ccBasisSet
        | RelativisticBasisSet,
        # ecp: str | None = None,
        # ecp_elements: tuple[str] | None = None,
    ):
        self.basis_name = name
        self.elements = BasisSet.split_elements(element_ranges)
        self.parent_basis = parent_basis.__name__

    def __hash__(self):
        return hash((self.basis_name, self.elements, self.parent_basis))


class AuxBasisSetEnum(AuxBasisSet, Enum):
    """Base class for auxiliary basis set enums."""

    def __new__(
        cls,
        basis_name: str,
        element_ranges: tuple[str],
        parent_basis: PopleBasisSet
        | def2BasisSet
        | JensenBasisSet
        | ccBasisSet
        | RelativisticBasisSet,
    ):
        self = BasisSet.__new__(cls)
        self._name_ = basis_name
        self._value_ = basis_name
        return self

    def __str__(self):
        return self.basis_name


# fmt: off
class AuxJBasisSet(AuxBasisSetEnum):
    """Coulomb-fitting auxiliary basis sets."""

    DEF2_J        = "def2/J",        ("H-Lr",), def2BasisSet
    DEF2_MTZVP_J  = "def2-mTZVP/J",  ("H-Lr",), def2BasisSet
    DEF2_MTZVPP_J = "def2-mTZVPP/J", ("H-Lr",), def2BasisSet
    X2C_J         = "x2c/J",         ("H-Rn",),         RelativisticBasisSet
    SARC_J        = "SARC/J",        ("H-Rn", "Ac-Lr"), RelativisticBasisSet


class AuxJKBasisSet(AuxBasisSetEnum):
    """Coulomb- and exchange-fitting auxiliary basis sets."""

    DEF2_JK            = "def2/JK",            ("H-Rn",),         def2BasisSet
    DEF2_JK_SMALL      = "def2/JKsmall",       ("H-Ra", "Th-Lr"), def2BasisSet

    CC_PVTZ_JK         = "cc-pVTZ/JK",         ("H", "B-F", "Al-Cl", "Ga-Br"), ccBasisSet
    CC_PVQZ_JK         = "cc-pVQZ/JK",         ("H", "B-F", "Al-Cl", "Ga-Br"), ccBasisSet
    CC_PV5Z_JK         = "cc-pV5Z/JK",         ("H", "B-F", "Al-Cl", "Ga-Br"), ccBasisSet
    AUG_CC_PVTZ_JK     = "aug-cc-pVTZ/JK",     ("H", "B-F", "Al-Cl", "Ga-Br"), ccBasisSet
    AUG_CC_PVQZ_JK     = "aug-cc-pVQZ/JK",     ("H", "B-F", "Al-Cl", "Ga-Br"), ccBasisSet
    AUG_CC_PV5Z_JK     = "aug-cc-pV5Z/JK",     ("H", "B-F", "Al-Cl", "Ga-Br"), ccBasisSet

    SARC2_DKH_QZV_JK   = "SARC2-DKH-QZV/JK",   ("La-Lu",), RelativisticBasisSet
    SARC2_DKH_QZVP_JK  = "SARC2-DKH-QZVP/JK",  ("La-Lu",), RelativisticBasisSet
    SARC2_ZORA_QZV_JK  = "SARC2-ZORA-QZV/JK",  ("La-Lu",), RelativisticBasisSet
    SARC2_ZORA_QZVP_JK = "SARC2-ZORA-QZVP/JK", ("La-Lu",), RelativisticBasisSet


class AuxCBasisSet(AuxBasisSetEnum):
    """Auxiliary basis sets for correlated wavefunction methods."""

    DEF2_SVP_C    = "def2-SVP/C",        ("H-Rn",),         def2BasisSet
    DEF2_TZVP_C   = "def2-TZVP/C",       ("H-Rn",),         def2BasisSet
    DEF2_TZVPP_C  = "def2-TZVPP/C",      ("H-Rn",),         def2BasisSet
    DEF2_QZVPP_C  = "def2-QZVPP/C",      ("H-Rn",),         def2BasisSet
    DEF2_SVPD_C   = "def2-SVPD/C",       ("H-La", "Hf-Rn"), def2BasisSet
    DEF2_TZVPD_C  = "def2-TZVPD/C",      ("H-La", "Hf-Rn"), def2BasisSet
    DEF2_TZVPPD_C = "def2-TZVPPD/C",     ("H-La", "Hf-Rn"), def2BasisSet
    DEF2_QZVPPD_C = "def2-QZVPPD/C",     ("H-La", "Hf-Rn"), def2BasisSet

    CC_PVDZ_C     = "cc-pVDZ/C",         ("H-Ar", "Ga-Kr"),                   ccBasisSet
    CC_PVTZ_C     = "cc-pVTZ/C",         ("H-Ar", "Sc-Kr"),                   ccBasisSet
    CC_PVQZ_C     = "cc-pVQZ/C",         ("H-Ar", "Sc-Kr"),                   ccBasisSet
    CC_PV5Z_C     = "cc-pV5Z/C",         ("H-Ar", "Ga-Kr"),                   ccBasisSet
    CC_PV6Z_C     = "cc-pV6Z/C",         ("H-He", "B-Ne",  "Al-Ar"),          ccBasisSet
    AUG_CC_PVDZ_C = "aug-cc-pVDZ/C",     ("H-He", "Be-Ne", "Mg-Ar", "Ga-Kr"), ccBasisSet
    AUG_CC_PVTZ_C = "aug-cc-pVTZ/C",     ("H-He", "Be-Ne", "Mg-Ar", "Sc-Kr"), ccBasisSet
    AUG_CC_PVQZ_C = "aug-cc-pVQZ/C",     ("H-He", "Be-Ne", "Mg-Ar", "Sc-Kr"), ccBasisSet
    AUG_CC_PV5Z_C = "aug-cc-pV5Z/C",     ("H-Ne", "Al-Ar", "Ga-Kr"),          ccBasisSet
    AUG_CC_PV6Z_C   = "aug-cc-pV6Z/C",   ("H-He", "B-Ne", "Al-Ar"),           ccBasisSet
    CC_PWCVDZ_C     = "cc-pwCVDZ/C",     ("H-He", "B-Ne", "Al-Ar", "Ga-Kr"),  ccBasisSet
    CC_PWCVTZ_C     = "cc-pwCVTZ/C",     ("H-He", "B-Ne", "Al-Ar", "Sc-Kr"),  ccBasisSet
    CC_PWCVQZ_C     = "cc-pwCVQZ/C",     ("H-He", "B-Ne", "Al-Ar", "Ga-Kr"),  ccBasisSet
    CC_PWCV5Z_C     = "cc-pwCV5Z/C",     ("H-Ne", "Al-Ar"),                   ccBasisSet
    AUG_CC_PWCVDZ_C = "aug-cc-pwCVDZ/C", ("H-He", "B-Ne", "Al-Ar", "Ga-Kr"),  ccBasisSet
    AUG_CC_PWCVTZ_C = "aug-cc-pwCVTZ/C", ("H-He", "B-Ne", "Al-Ar", "Sc-Kr"),  ccBasisSet
    AUG_CC_PWCVQZ_C = "aug-cc-pwCVQZ/C", ("H-He", "B-Ne", "Al-Ar", "Ga-Kr"),  ccBasisSet
    AUG_CC_PWCV5Z_C = "aug-cc-pwCV5Z/C", ("H-Ne", "Al-Ar"),                   ccBasisSet


def get_basis_set(
    value: str
) -> PopleBasisSet | def2BasisSet | JensenBasisSet | ccBasisSet | RelativisticBasisSet:
    """Get a basis set enum member from a basis set."""

    pople_pattern = re.compile(
        pattern=r"\b(m?[346]-[23][12]*\+*G(?:\([23]?[dfp]{1,2},?[23]?[dfp]{0,2}\)|\**)?[SP]{0,2})\b",
        flags=re.IGNORECASE,
    )
    def2_pattern = re.compile(
        pattern=r"\b((?:ma-)?def2-m?[STQ]?[ZVPD()]{1,5}(?:\(-f\))?(?:\/J|\/C)?)\b",
        flags=re.IGNORECASE,
    )
    jensen_pattern = re.compile(
        pattern=r"\b((?:aug-)?pc[XJH]?S?(?:seg)?-[0-9]?)\b",
        flags=re.IGNORECASE,
    )
    cc_pattern = re.compile(
        pattern=r"\b((?:m?aug-|apr-|may-|ju[nl]-)?cc-p[wC]{0,2}V[DTQ56]?(?:[DTQ56]|\([DTQ56]?\+d\))Z(?:-DK3?)?(?:\/JK|\/C)?)\b",
        flags=re.IGNORECASE,
    )
    relativistic_pattern = re.compile(
        pattern=r"\b((?:ma-)?(?:SARC-|SARC2-)?(?:DKH-|ZORA-){1}(?:def2-)?m?[STQ]?[ZVPD()]{1,5}\(?-?f?\)?(?:\/JK)?)\b",
        flags=re.IGNORECASE,
    )

    patterns = {
        pople_pattern: PopleBasisSet,
        def2_pattern: def2BasisSet,
        jensen_pattern: JensenBasisSet,
        cc_pattern: ccBasisSet,
        relativistic_pattern: RelativisticBasisSet,
    }


    for pattern, basis_set in patterns.items():
        if pattern.match(value) is not None:
            return basis_set(value)
# fmt: on


def get_aux_basis(value: str) -> AuxJBasisSet | AuxJKBasisSet | AuxCBasisSet:
    """Get a basis set enum member from a basis set."""

    if "/J" in value:
        return AuxJBasisSet(value)
    elif "/JK" in value:
        return AuxJKBasisSet(value)
    elif "/C" in value:
        return AuxCBasisSet(value)
    else:
        return None


def get_basis_family(basis_class: str) -> str:
    """Get the recognizable name from the name of a basis set enum."""

    match basis_class:
        case "def2BasisSet":
            return "def2-n(Z)VP"
        case "ccBasisSet":
            return "cc-pVnZ"
        case "JensenBasisSet":
            return "Jensen"
        case "RelativisticBasisSet":
            return "SARC/DKH/ZORA/x2c"
        case "PopleBasisSet":
            return "Pople"
        case _:
            return "Unknown"
