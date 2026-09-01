# SPDX-FileCopyrightText: 2026 Avogadro Project
# SPDX-License-Identifier: BSD 3-Clause
# ******************************************************************************
# This source file is part of the Avogadro project.
#
# This source code is released under the New BSD License, (the "License").
# ******************************************************************************
"""Classes and methods for implicit solvation."""

from dataclasses import dataclass
from enum import Enum, Flag, auto


# fmt: off
class SolvationModel(Flag):
    """Solvation models supported in ORCA.

    Access members by string with ``SolvationModel["<member_name>"]``.
    """

    def __str__(self) -> str:
        match self:
            case SolvationModel.CPCM:
                return "CPCM"
            case SolvationModel.SMD:
                return "SMD"
            case SolvationModel.COSMO_RS:
                return "COSMORS"
            case SolvationModel.ALPB:
                return "ALPB"
            case SolvationModel.DDCOSMO:
                return "ddCOSMO"
            case SolvationModel.CPCMX:
                return "CPCMX"
            case _:
                raise ValueError("Invalid Solvent, how did you even get here?")

    CPCM     = auto()
    SMD      = auto()
    COSMO_RS = auto()
    ALPB     = auto()
    DDCOSMO  = auto()
    CPCMX    = auto()
# fmt: on
SM = SolvationModel


@dataclass(frozen=True)
class SolventData:
    aliases: tuple[str]
    models: SolvationModel


# fmt: off
class Solvent(SolventData, Enum):

    def __new__(
        cls,
        aliases: tuple[str],
        models: SolvationModel,
    ):
        self = SolventData.__new__(cls)
        self._name_ = aliases[0]
        self._value_ = aliases[0]
        return self


    def __str__(self):
        return self.aliases[0]

    s_NONE                           = ("",), 0
    s_111_TRICHLOROETHANE            = ("1,1,1-trichloroethane",),                     SM.CPCM | SM.SMD | SM.COSMO_RS
    s_112_TRICHLOROETHANE            = ("1,1,2-trichloroethane",),                     SM.CPCM | SM.SMD
    s_124_TRIMETHYLBENZENE           = ("1,2,4-trimethylbenzene",),                    SM.CPCM | SM.SMD | SM.COSMO_RS
    s_12_DIBROMOETHANE               = ("1,2-dibromoethane",),                         SM.CPCM | SM.SMD
    s_12_DICHLOROETHANE              = ("1,2-dichloroethane",),                        SM.CPCM | SM.SMD
    s_12_ETHANEDIOL                  = ("1,2-ethanediol",),                            SM.CPCM | SM.SMD
    s_14_DIOXANE                     = ("1,4-dioxane", "dioxane"),                     SM.CPCM | SM.SMD              
    s_1_BROMO_2_METHYLPROPANE        = ("1-bromo-2-methylpropane",),                   SM.CPCM | SM.SMD
    s_1_BROMOOCTANE                  = ("1-bromooctane", "bromooctane"),               SM.CPCM | SM.SMD
    s_1_BROMOPENTANE                 = ("1-bromopentane",),                            SM.CPCM | SM.SMD
    s_1_BROMOPROPANE                 = ("1-bromopropane",),                            SM.CPCM | SM.SMD
    s_1_BUTANOL                      = ("1-butanol", "butanol"),                       SM.CPCM | SM.SMD | SM.COSMO_RS
    s_1_CHLOROHEXANE                 = ("1-chlorohexane", "chlorohexane"),             SM.CPCM | SM.SMD | SM.COSMO_RS
    s_1_CHLOROPENTANE                = ("1-chloropentane",),                           SM.CPCM | SM.SMD
    s_1_CHLOROPROPANE                = ("1-chloropropane",),                           SM.CPCM | SM.SMD
    s_1_DECANOL                      = ("1-decanol", "decanol"),                       SM.CPCM | SM.SMD | SM.COSMO_RS
    s_1_FLUOROOCTANE                 = ("1-fluorooctane",),                            SM.CPCM | SM.SMD | SM.COSMO_RS
    s_1_HEPTANOL                     = ("1-heptanol", "heptanol"),                     SM.CPCM | SM.SMD | SM.COSMO_RS
    s_1_HEXANOL                      = ("1-hexanol", "hexanol"),                       SM.CPCM | SM.SMD | SM.COSMO_RS
    s_1_HEXENE                       = ("1-hexene",),                                  SM.CPCM | SM.SMD
    s_1_HEXYNE                       = ("1-hexyne",),                                  SM.CPCM | SM.SMD
    s_1_IODOBUTANE                   = ("1-iodobutane"),                               SM.CPCM | SM.SMD
    s_1_IODOHEXADECANE               = ("1-iodohexadecane", "hexadecyliodide"),        SM.CPCM | SM.SMD | SM.COSMO_RS
    s_1_IODOPENTANE                  = ("1-iodopentane",),                             SM.CPCM | SM.SMD
    s_1_IODOPROPANE                  = ("1-iodopropane",),                             SM.CPCM | SM.SMD
    s_1_NITROPROPANE                 = ("1-nitropropane",),                            SM.CPCM | SM.SMD
    s_1_NONANOL                      = ("1-nonanol", "nonanol"),                       SM.CPCM | SM.SMD | SM.COSMO_RS
    s_1_OCTANOL                      = ("1-octanol", "octanol"),                       SM.CPCM | SM.SMD | SM.COSMO_RS
    s_1_PENTANOL                     = ("1-pentanol", "pentanol"),                     SM.CPCM | SM.SMD | SM.COSMO_RS
    s_1_PENTENE                      = ("1-pentene",),                                 SM.CPCM | SM.SMD
    s_1_PROPANOL                     = ("1-propanol", "propanol"),                     SM.CPCM | SM.SMD | SM.COSMO_RS
    s_222_TRIFLUOROETHANOL           = ("2,2,2-trifluoroethanol",),                    SM.CPCM | SM.SMD
    s_224_TRIMETHYLPENTANE           = ("2,2,4-trimethylpentane", "isooctane"),        SM.CPCM | SM.SMD | SM.COSMO_RS
    s_24_DIMETHYLPENTANE             = ("2,4-dimethylpentane",),                       SM.CPCM | SM.SMD
    s_24_DIMETHYLPYRIDINE            = ("2,4-dimethylpyridine",),                      SM.CPCM | SM.SMD
    s_26_DIMETHYLPYRIDINE            = ("2,6-dimethylpyridine",),                      SM.CPCM | SM.SMD | SM.COSMO_RS
    s_2_BROMOPROPANE                 = ("2-bromopropane",),                            SM.CPCM | SM.SMD
    s_2_BUTANOL                      = ("2-butanol", "secbutanol"),                    SM.CPCM | SM.SMD | SM.COSMO_RS
    s_2_CHLOROBUTANE                 = ("2-chlorobutane",),                            SM.CPCM | SM.SMD
    s_2_HEPTANONE                    = ("2-heptanone",),                               SM.CPCM | SM.SMD
    s_2_HEXANONE                     = ("2-hexanone",),                                SM.CPCM | SM.SMD
    s_2_METHOXYETHANOL               = ("2-methoxyethanol", "methoxyethanol"),         SM.CPCM | SM.SMD | SM.COSMO_RS
    s_2_METHYL_1_PROPANOL            = ("2-methyl-1-propanol", "isobutanol"),          SM.CPCM | SM.SMD | SM.COSMO_RS
    s_2_METHYL_2_PROPANOL            = ("2-methyl-2-propanol",),                       SM.CPCM | SM.SMD
    s_2_METHYLPENTANE                = ("2-methylpentane",),                           SM.CPCM | SM.SMD
    s_2_METHYLPYRIDINE               = ("2-methylpyridine", "2methylpyridine"),        SM.CPCM | SM.SMD | SM.COSMO_RS
    s_2_NITROPROPANE                 = ("2-nitropropane",),                            SM.CPCM | SM.SMD
    s_2_OCTANONE                     = ("2-octanone",),                                SM.CPCM | SM.SMD
    s_2_PENTANONE                    = ("2-pentanone",),                               SM.CPCM | SM.SMD
    s_2_PROPANOL                     = ("2-propanol", "isopropanol"),                  SM.CPCM | SM.SMD | SM.COSMO_RS
    s_2_PROPEN_1_OL                  = ("2-propen-1-ol",),                             SM.CPCM | SM.SMD
    s_E_2_PENTENE                    = ("e-2-pentene",),                               SM.CPCM | SM.SMD
    s_3_METHYLPYRIDINE               = ("3-methylpyridine",),                          SM.CPCM | SM.SMD
    s_3_PENTANONE                    = ("3-pentanone",),                               SM.CPCM | SM.SMD
    s_4_HEPTANONE                    = ("4-heptanone",),                               SM.CPCM | SM.SMD
    s_4_METHYL_2_PENTANONE           = ("4-methyl-2-pentanone", "4methyl2pentanone"),  SM.CPCM | SM.SMD | SM.COSMO_RS
    s_4_METHYLPYRIDINE               = ("4-methylpyridine",),                          SM.CPCM | SM.SMD
    s_5_NONANONE                     = ("5-nonanone",),                                SM.CPCM | SM.SMD
    s_ACETIC_ACID                    = ("acetic acid", "aceticacid"),                  SM.CPCM | SM.SMD | SM.COSMO_RS
    s_ACETONE                        = ("acetone",),                                   SM.CPCM | SM.SMD | SM.COSMO_RS
    s_ACETONITRILE                   = ("acetonitrile", "mecn", "ch3cn"),              SM.CPCM | SM.SMD | SM.COSMO_RS
    s_ACETOPHENONE                   = ("acetophenone",),                              SM.CPCM | SM.SMD | SM.COSMO_RS
    s_AMMONIA                        = ("ammonia",),                                   SM.CPCM          | SM.COSMO_RS
    s_ANILINE                        = ("aniline",),                                   SM.CPCM | SM.SMD | SM.COSMO_RS
    s_ANISOLE                        = ("anisole",),                                   SM.CPCM | SM.SMD | SM.COSMO_RS
    s_BENZALDEHYDE                   = ("benzaldehyde",),                              SM.CPCM | SM.SMD | SM.COSMO_RS
    s_BENZENE                        = ("benzene",),                                   SM.CPCM | SM.SMD | SM.COSMO_RS
    s_BENZONITRILE                   = ("benzonitrile",),                              SM.CPCM | SM.SMD | SM.COSMO_RS
    s_BENZYL_ALCOHOL                 = ("benzyl alcohol", "benzylalcohol"),            SM.CPCM | SM.SMD | SM.COSMO_RS
    s_BROMOBENZENE                   = ("bromobenzene",),                              SM.CPCM | SM.SMD | SM.COSMO_RS
    s_BROMOETHANE                    = ("bromoethane",),                               SM.CPCM | SM.SMD | SM.COSMO_RS
    s_BROMOFORM                      = ("bromoform",),                                 SM.CPCM | SM.SMD | SM.COSMO_RS
    s_BUTANAL                        = ("butanal",),                                   SM.CPCM | SM.SMD
    s_BUTANOIC_ACID                  = ("butanoic acid",),                             SM.CPCM | SM.SMD
    s_BUTANONE                       = ("butanone",),                                  SM.CPCM | SM.SMD | SM.COSMO_RS
    s_BUTANONITRILE                  = ("butanonitrile",),                             SM.CPCM | SM.SMD
    s_BUTYL_ETHANOATE                = ("butyl ethanoate", "butyl acetate", "butylacetate"),  SM.CPCM | SM.SMD | SM.COSMO_RS
    s_BUTYLAMINE                     = ("butylamine",),                                SM.CPCM | SM.SMD
    s_N_BUTYLBENZENE                 = ("n-butylbenzene", "butylbenzene"),             SM.CPCM | SM.SMD | SM.COSMO_RS
    s_SEC_BUTYLBENZENE               = ("sec-butylbenzene", "secbutylbenzene"),        SM.CPCM | SM.SMD | SM.COSMO_RS
    s_TERT_BUTYLBENZENE              = ("tert-butylbenzene", "tbutylbenzene"),         SM.CPCM | SM.SMD | SM.COSMO_RS
    s_CARBON_DISULFIDE               = ("carbon disulfide", "carbondisulfide", "cs2"), SM.CPCM | SM.SMD | SM.COSMO_RS
    s_CARBON_TETRACHLORIDE           = ("carbon tetrachloride", "ccl4"),               SM.CPCM | SM.SMD | SM.COSMO_RS
    s_CHLOROBENZENE                  = ("chlorobenzene",),                             SM.CPCM | SM.SMD | SM.COSMO_RS
    s_CHLOROFORM                     = ("chloroform", "chcl3"),                        SM.CPCM | SM.SMD | SM.COSMO_RS
    s_A_CHLOROTOLUENE                = ("a-chlorotoluene",),                           SM.CPCM | SM.SMD
    s_O_CHLOROTOLUENE                = ("o-chlorotoluene",),                           SM.CPCM | SM.SMD
    s_CONDUCTOR                      = ("conductor",),                                 SM.CPCM
    s_M_CRESOL                       = ("m-cresol", "mcresol"),                        SM.CPCM | SM.SMD | SM.COSMO_RS
    s_O_CRESOL                       = ("o-cresol",),                                  SM.CPCM | SM.SMD
    s_CYCLOHEXANE                    = ("cyclohexane",),                               SM.CPCM | SM.SMD | SM.COSMO_RS
    s_CYCLOHEXANONE                  = ("cyclohexanone",),                             SM.CPCM | SM.SMD | SM.COSMO_RS
    s_CYCLOPENTANE                   = ("cyclopentane",),                              SM.CPCM | SM.SMD
    s_CYCLOPENTANOL                  = ("cyclopentanol",),                             SM.CPCM | SM.SMD
    s_CYCLOPENTANONE                 = ("cyclopentanone",),                            SM.CPCM | SM.SMD
    s_DECALIN                        = ("decalin",),                                   SM.CPCM | SM.SMD | SM.COSMO_RS
    s_CIS_DECALIN                    = ("cis-decalin",),                               SM.CPCM | SM.SMD
    s_N_DECANE                       = ("n-decane", "decane"),                         SM.CPCM | SM.SMD | SM.COSMO_RS
    s_DIBROMOMETHANE                 = ("dibromomethane",),                            SM.CPCM | SM.SMD
    s_DIBUTYLETHER                   = ("dibutylether",),                              SM.CPCM | SM.SMD | SM.COSMO_RS
    s_O_DICHLOROBENZENE              = ("o-dichlorobenzene", "odichlorobenzene"),      SM.CPCM | SM.SMD | SM.COSMO_RS
    s_E_12_DICHLOROETHENE            = ("e-1,2-dichloroethene",),                      SM.CPCM | SM.SMD
    s_Z_12_DICHLOROETHENE            = ("z-1,2-dichloroethene",),                      SM.CPCM | SM.SMD
    s_DICHLOROMETHANE                = ("dichloromethane", "ch2cl2", "dcm"),           SM.CPCM | SM.SMD | SM.COSMO_RS
    s_DIETHYL_ETHER                  = ("diethyl ether", "diethylether"),              SM.CPCM | SM.SMD | SM.COSMO_RS
    s_DIETHYL_SULFIDE                = ("diethyl sulfide",),                           SM.CPCM | SM.SMD
    s_DIETHYLAMINE                   = ("diethylamine",),                              SM.CPCM | SM.SMD
    s_DIIODOMETHANE                  = ("diiodomethane",),                             SM.CPCM | SM.SMD
    s_DIISOPROPYL_ETHER              = ("diisopropyl ether", "diisopropylether"),      SM.CPCM | SM.SMD | SM.COSMO_RS
    s_CIS_12_DIMETHYLCYCLOHEXANE     = ("cis-1,2-dimethylcyclohexane",),               SM.CPCM | SM.SMD
    s_DIMETHYL_DISULFIDE             = ("dimethyl disulfide",),                        SM.CPCM | SM.SMD
    s_NN_DIMETHYLACETAMIDE           = ("n,n-dimethylacetamide", "dimethylacetamide"), SM.CPCM | SM.SMD | SM.COSMO_RS
    s_NN_DIMETHYLFORMAMIDE           = ("n,n-dimethylformamide", "dimethylformamide", "dmf"), SM.CPCM | SM.SMD | SM.COSMO_RS
    s_DIMETHYLSULFOXIDE              = ("dimethylsulfoxide", "dmso"),                  SM.CPCM | SM.SMD | SM.COSMO_RS
    s_DIPHENYLETHER                  = ("diphenylether",),                             SM.CPCM | SM.SMD | SM.COSMO_RS
    s_DIPROPYLAMINE                  = ("dipropylamine",),                             SM.CPCM | SM.SMD
    s_N_DODECANE                     = ("n-dodecane", "dodecane"),                     SM.CPCM | SM.SMD | SM.COSMO_RS
    s_ETHANETHIOL                    = ("ethanethiol",),                               SM.CPCM | SM.SMD
    s_ETHANOL                        = ("ethanol",),                                   SM.CPCM | SM.SMD | SM.COSMO_RS
    s_ETHYL_ACETATE                  = ("ethyl acetate", "ethylacetate", "ethanoate"), SM.CPCM | SM.SMD | SM.COSMO_RS
    s_ETHYL_METHANOATE               = ("ethyl methanoate",),                          SM.CPCM | SM.SMD
    s_ETHYL_PHENYL_ETHER             = ("ethyl phenyl ether", "ethoxybenzene"),        SM.CPCM | SM.SMD | SM.COSMO_RS
    s_ETHYLBENZENE                   = ("ethylbenzene",),                              SM.CPCM | SM.SMD | SM.COSMO_RS
    s_FLUOROBENZENE                  = ("fluorobenzene",),                             SM.CPCM | SM.SMD | SM.COSMO_RS
    s_FORMAMIDE                      = ("formamide",),                                 SM.CPCM | SM.SMD
    s_FORMIC_ACID                    = ("formic acid",),                               SM.CPCM | SM.SMD
    s_FURAN                          = ("furan", "furane"),                                               SM.COSMO_RS
    s_N_HEPTANE                      = ("n-heptane", "heptane"),                       SM.CPCM | SM.SMD | SM.COSMO_RS
    s_N_HEXADECANE                   = ("n-hexadecane", "hexadecane"),                 SM.CPCM | SM.SMD | SM.COSMO_RS
    s_N_HEXANE                       = ("n-hexane", "hexane"),                         SM.CPCM | SM.SMD | SM.COSMO_RS
    s_HEXANOIC_ACID                  = ("hexanoic acid",),                             SM.CPCM | SM.SMD
    s_IODOBENZENE                    = ("iodobenzene",),                               SM.CPCM | SM.SMD | SM.COSMO_RS
    s_IODOETHANE                     = ("iodoethane",),                                SM.CPCM | SM.SMD
    s_IODOMETHANE                    = ("iodomethane",),                               SM.CPCM | SM.SMD
    s_ISOPROPYLBENZENE               = ("isopropylbenzene",),                          SM.CPCM | SM.SMD | SM.COSMO_RS
    s_P_ISOPROPYLTOLUENE             = ("p-isopropyltoluene", "isopropyltoluene"),     SM.CPCM | SM.SMD
    s_MESITYLENE                     = ("mesitylene",),                                SM.CPCM | SM.SMD | SM.COSMO_RS
    s_METHANOL                       = ("methanol",),                                  SM.CPCM | SM.SMD | SM.COSMO_RS
    s_METHYL_BENZOATE                = ("methyl benzoate",),                           SM.CPCM | SM.SMD
    s_METHYL_BUTANOATE               = ("methyl butanoate",),                          SM.CPCM | SM.SMD
    s_METHYL_ETHANOATE               = ("methyl ethanoate",),                          SM.CPCM | SM.SMD
    s_METHYL_METHANOATE              = ("methyl methanoate",),                         SM.CPCM | SM.SMD
    s_METHYL_PROPANOATE              = ("methyl propanoate",),                         SM.CPCM | SM.SMD
    s_N_METHYLANILINE                = ("n-methylaniline",),                           SM.CPCM | SM.SMD
    s_METHYLCYCLOHEXANE              = ("methylcyclohexane",),                         SM.CPCM | SM.SMD
    s_N_METHYLFORMAMIDE              = ("n-methylformamide", "methylformamide"),       SM.CPCM | SM.SMD | SM.COSMO_RS
    s_NITROBENZENE                   = ("nitrobenzene", "phno2"),                      SM.CPCM | SM.SMD | SM.COSMO_RS
    s_NITROETHANE                    = ("nitroethane",),                               SM.CPCM | SM.SMD | SM.COSMO_RS
    s_NITROMETHANE                   = ("nitromethane", "meno2"),                      SM.CPCM | SM.SMD | SM.COSMO_RS
    s_O_NITROTOLUENE                 = ("o-nitrotoluene", "onitrotoluene"),            SM.CPCM | SM.SMD
    s_N_NONANE                       = ("n-nonane", "nonane"),                         SM.CPCM | SM.SMD | SM.COSMO_RS
    s_N_OCTANE                       = ("n-octane", "octane"),                         SM.CPCM | SM.SMD | SM.COSMO_RS
    s_N_PENTADECANE                  = ("n-pentadecane", "pentadecane"),               SM.CPCM | SM.SMD | SM.COSMO_RS
    s_PENTANAL                       = ("pentanal",),                                  SM.CPCM | SM.SMD
    s_N_PENTANE                      = ("n-pentane", "pentane"),                       SM.CPCM | SM.SMD | SM.COSMO_RS
    s_PENTANOIC_ACID                 = ("pentanoic acid",),                            SM.CPCM | SM.SMD
    s_PENTYL_ETHANOATE               = ("pentyl ethanoate",),                          SM.CPCM | SM.SMD
    s_PENTYLAMINE                    = ("pentylamine",),                               SM.CPCM | SM.SMD
    s_PERFLUOROBENZENE               = ("perfluorobenzene", "hexafluorobenzene"),      SM.CPCM | SM.SMD | SM.COSMO_RS
    s_PHENOL                         = ("phenol",),                                    SM.CPCM          | SM.COSMO_RS
    s_PROPANAL                       = ("propanal",),                                  SM.CPCM | SM.SMD
    s_PROPANOIC_ACID                 = ("propanoic acid",),                            SM.CPCM | SM.SMD
    s_PROPANONITRILE                 = ("propanonitrile",),                            SM.CPCM | SM.SMD
    s_PROPYL_ETHANOATE               = ("propyl ethanoate",),                          SM.CPCM | SM.SMD
    s_PROPYLAMINE                    = ("propylamine",),                               SM.CPCM | SM.SMD
    s_PYRIDINE                       = ("pyridine",),                                  SM.CPCM | SM.SMD | SM.COSMO_RS
    s_TETRACHLOROETHENE              = ("tetrachloroethene", "c2cl4"),                 SM.CPCM | SM.SMD | SM.COSMO_RS
    s_TETRAHYDROFURAN                = ("tetrahydrofuran", "thf"),                     SM.CPCM | SM.SMD | SM.COSMO_RS
    s_TETRAHYDROTHIOPHENE_SS_DIOXIDE = ("tetrahydrothiophene-s,s-dioxide", "tetrahydrothiophenedioxide", "sulfolane"), SM.CPCM
    s_TETRALIN                       = ("tetralin",),                                  SM.CPCM | SM.SMD | SM.COSMO_RS
    s_THIOPHENE                      = ("thiophene",),                                 SM.CPCM | SM.SMD
    s_THIOPHENOL                     = ("thiophenol",),                                SM.CPCM | SM.SMD
    s_TOLUENE                        = ("toluene",),                                   SM.CPCM | SM.SMD | SM.COSMO_RS
    s_TRANS_DECALIN                  = ("trans-decalin",),                             SM.CPCM | SM.SMD
    s_TRIBUTYLPHOSPHATE              = ("tributylphosphate",),                         SM.CPCM | SM.SMD | SM.COSMO_RS
    s_TRICHLOROETHENE                = ("trichloroethene",),                           SM.CPCM | SM.SMD
    s_TRIETHYLAMINE                  = ("triethylamine",),                             SM.CPCM | SM.SMD | SM.COSMO_RS
    s_N_UNDECANE                     = ("n-undecane", "undecane"),                     SM.CPCM | SM.SMD | SM.COSMO_RS
    s_WATER                          = ("water", "h2o"),                               SM.CPCM | SM.SMD | SM.COSMO_RS
    s_XYLENE                         = ("xylene",),                                    SM.CPCM | SM.SMD
    s_M_XYLENE                       = ("m-xylene",),                                  SM.CPCM | SM.SMD
    s_O_XYLENE                       = ("o-xylene",),                                  SM.CPCM | SM.SMD
    s_P_XYLENE                       = ("p-xylene",),                                  SM.CPCM | SM.SMD


class XTBSolvent(SolventData, Enum):
    """Solvents available through the ALPB, ddCOSMO, or CPCMX methods.
    
    Notes
    -----
    Only the ALPB method is available through the native ORCA GFN1- and
    GFN2-xTB implementations.
    """

    s_NONE                           = (""), 0
    s_124_TRIMETHYLBENZENE           = ("1,2,4-trimethylbenzene",),                     SM.CPCMX
    s_12_DIBROMOETHANE               = ("1,2-dibromoethane",),                          SM.CPCMX
    s_14_DIOXANE                     = ("1,4-dioxane", "dioxane"),                                 SM.ALPB | SM.DDCOSMO
    s_1_BUTANOL                      = ("1-butanol", "butanol"),                        SM.CPCMX
    s_1_CHLOROHEXANE                 = ("1-chlorohexane", "chlorohexane"),              SM.CPCMX
    s_1_DECANOL                      = ("1-decanol", "decanol"),                        SM.CPCMX
    s_1_FLUOROOCTANE                 = ("1-fluorooctane",),                             SM.CPCMX
    s_1_HEPTANOL                     = ("1-heptanol", "heptanol"),                      SM.CPCMX
    s_1_HEXANOL                      = ("1-hexanol", "hexanol"),                        SM.CPCMX
    s_1_IODOHEXADECANE               = ("1-iodohexadecane", "hexadecyliodide"),         SM.CPCMX
    s_1_NONANOL                      = ("1-nonanol", "nonanol"),                        SM.CPCMX
    s_1_OCTANOL                      = ("1-octanol", "octanol"),                        SM.CPCMX | SM.ALPB | SM.DDCOSMO
    s_1_PENTANOL                     = ("1-pentanol", "pentanol"),                      SM.CPCMX
    s_1_PROPANOL                     = ("1-propanol", "propanol"),                      SM.CPCMX
    s_224_TRIMETHYLPENTANE           = ("2,2,4-trimethylpentane", "isooctane"),         SM.CPCMX
    s_26_DIMETHYLPYRIDINE            = ("2,6-dimethylpyridine",),                       SM.CPCMX
    s_2_BUTANOL                      = ("2-butanol", "secbutanol"),                     SM.CPCMX
    s_2_METHOXYETHANOL               = ("2-methoxyethanol", "methoxyethanol"),          SM.CPCMX
    s_2_METHYL_1_PROPANOL            = ("2-methyl-1-propanol", "isobutanol"),           SM.CPCMX
    s_2_METHYLPYRIDINE               = ("2-methylpyridine", "2methylpyridine"),         SM.CPCMX
    s_2_PROPANOL                     = ("2-propanol", "isopropanol"),                   SM.CPCMX
    s_4_METHYL_2_PENTANONE           = ("4-methyl-2-pentanone", "4methyl2pentanone"),   SM.CPCMX
    s_ACETIC_ACID                    = ("acetic acid", "aceticacid"),                   SM.CPCMX
    s_ACETONE                        = ("acetone",),                                               SM.ALPB | SM.DDCOSMO
    s_ACETONITRILE                   = ("acetonitrile", "mecn", "ch3cn"),               SM.CPCMX | SM.ALPB | SM.DDCOSMO
    s_ACETOPHENONE                   = ("acetophenone",),                               SM.CPCMX
    s_ANILINE                        = ("aniline",),                                    SM.CPCMX | SM.ALPB | SM.DDCOSMO
    s_ANISOLE                        = ("anisole",),                                    SM.CPCMX
    s_BENZALDEHYDE                   = ("benzaldehyde",),                                          SM.ALPB | SM.DDCOSMO
    s_BENZENE                        = ("benzene",),                                    SM.CPCMX | SM.ALPB | SM.DDCOSMO
    s_BENZONITRILE                   = ("benzonitrile",),                               SM.CPCMX
    s_BENZYL_ALCOHOL                 = ("benzyl alcohol", "benzylalcohol"),             SM.CPCMX
    s_BROMOBENZENE                   = ("bromobenzene",),                               SM.CPCMX
    s_BROMOETHANE                    = ("bromoethane",),                                SM.CPCMX
    s_BROMOFORM                      = ("bromoform",),                                  SM.CPCMX
    s_BUTANONE                       = ("butanone",),                                   SM.CPCMX
    s_BUTYL_ETHANOATE                = ("butyl ethanoate", "butyl acetate", "butylacetate"), SM.CPCMX
    s_N_BUTYLBENZENE                 = ("n-butylbenzene", "butylbenzene"),              SM.CPCMX
    s_SEC_BUTYLBENZENE               = ("sec-butylbenzene", "secbutylbenzene"),         SM.CPCMX
    s_TERT_BUTYLBENZENE              = ("tert-butylbenzene", "tbutylbenzene"),          SM.CPCMX
    s_CARBON_DISULFIDE               = ("carbon disulfide", "carbondisulfide", "cs2"),  SM.CPCMX | SM.ALPB | SM.DDCOSMO
    s_CARBON_TETRACHLORIDE           = ("carbon tetrachloride", "ccl4"),                SM.CPCMX
    s_CHLOROBENZENE                  = ("chlorobenzene",),                              SM.CPCMX
    s_CHLOROFORM                     = ("chloroform", "chcl3"),                         SM.CPCMX | SM.ALPB | SM.DDCOSMO
    s_CONDUCTOR                      = ("conductor",),                                                       SM.DDCOSMO
    s_M_CRESOL                       = ("m-cresol", "mcresol"),                         SM.CPCMX
    s_CYCLOHEXANE                    = ("cyclohexane",),                                SM.CPCMX
    s_CYCLOHEXANONE                  = ("cyclohexanone",),                              SM.CPCMX
    s_DECALIN                        = ("decalin",),                                    SM.CPCMX
    s_N_DECANE                       = ("n-decane", "decane"),                          SM.CPCMX
    s_DIBROMOMETHANE                 = ("dibromomethane",),                             SM.CPCMX
    s_DIBUTYLETHER                   = ("dibutylether",),                               SM.CPCMX
    s_O_DICHLOROBENZENE              = ("o-dichlorobenzene", "odichlorobenzene"),       SM.CPCMX
    s_DICHLOROMETHANE                = ("dichloromethane", "ch2cl2", "dcm"),            SM.CPCMX | SM.ALPB | SM.DDCOSMO
    s_DIETHYL_ETHER                  = ("diethyl ether", "diethylether"),               SM.CPCMX | SM.ALPB | SM.DDCOSMO
    s_DIISOPROPYL_ETHER              = ("diisopropyl ether", "diisopropylether"),       SM.CPCMX
    s_NN_DIMETHYLACETAMIDE           = ("n,n-dimethylacetamide", "dimethylacetamide"),  SM.CPCMX
    s_NN_DIMETHYLFORMAMIDE           = ("n,n-dimethylformamide", "dimethylformamide", "dmf"), SM.CPCMX | SM.ALPB | SM.DDCOSMO
    s_DIMETHYLSULFOXIDE              = ("dimethylsulfoxide", "dmso"),                   SM.CPCMX | SM.ALPB | SM.DDCOSMO
    s_DIPHENYLETHER                  = ("diphenylether",),                              SM.CPCMX
    s_N_DODECANE                     = ("n-dodecane", "dodecane"),                      SM.CPCMX
    s_ETHANOL                        = ("ethanol",),                                    SM.CPCMX | SM.ALPB | SM.DDCOSMO
    s_ETHYL_ACETATE                  = ("ethyl acetate", "ethylacetate", "ethanoate"),  SM.CPCMX | SM.ALPB | SM.DDCOSMO
    s_ETHYL_PHENYL_ETHER             = ("ethyl phenyl ether", "ethoxybenzene"),         SM.CPCMX
    s_ETHYLBENZENE                   = ("ethylbenzene",),                               SM.CPCMX
    s_FLUOROBENZENE                  = ("fluorobenzene",),                              SM.CPCMX
    s_FURAN                          = ("furan", "furane"),                                        SM.ALPB | SM.DDCOSMO
    s_N_HEPTANE                      = ("n-heptane", "heptane"),                        SM.CPCMX
    s_N_HEXADECANE                   = ("n-hexadecane", "hexadecane"),                  SM.CPCMX | SM.ALPB | SM.DDCOSMO
    s_N_HEXANE                       = ("n-hexane", "hexane"),                          SM.CPCMX | SM.ALPB | SM.DDCOSMO
    s_IODOBENZENE                    = ("iodobenzene",),                                SM.CPCMX
    s_ISOPROPYLBENZENE               = ("isopropylbenzene",),                           SM.CPCMX
    s_P_ISOPROPYLTOLUENE             = ("p-isopropyltoluene", "isopropyltoluene"),      SM.CPCMX
    s_MESITYLENE                     = ("mesitylene",),                                 SM.CPCMX
    s_METHANOL                       = ("methanol",),                                   SM.CPCMX | SM.ALPB | SM.DDCOSMO
    s_N_METHYLFORMAMIDE              = ("n-methylformamide", "methylformamide"),        SM.CPCMX
    s_NITROBENZENE                   = ("nitrobenzene", "phno2"),                       SM.CPCMX
    s_NITROETHANE                    = ("nitroethane",),                                SM.CPCMX
    s_NITROMETHANE                   = ("nitromethane", "meno2"),                       SM.CPCMX | SM.ALPB | SM.DDCOSMO
    s_O_NITROTOLUENE                 = ("o-nitrotoluene", "onitrotoluene"),             SM.CPCMX
    s_N_NONANE                       = ("n-nonane", "nonane"),                          SM.CPCMX
    s_N_OCTANE                       = ("n-octane", "octane"),                          SM.CPCMX
    s_N_PENTADECANE                  = ("n-pentadecane", "pentadecane"),                SM.CPCMX
    s_OCTANOL_WET_                   = ("octanol(wet)", "wetoctanol", "woctanol"),                 SM.ALPB | SM.DDCOSMO
    s_N_PENTANE                      = ("n-pentane", "pentane"),                        SM.CPCMX
    s_PERFLUOROBENZENE               = ("perfluorobenzene", "hexafluorobenzene"),       SM.CPCMX
    s_PHENOL                         = ("phenol",),                                                SM.ALPB | SM.DDCOSMO
    s_PYRIDINE                       = ("pyridine",),                                   SM.CPCMX
    s_TETRACHLOROETHENE              = ("tetrachloroethene", "c2cl4"),                  SM.CPCMX
    s_TETRAHYDROFURAN                = ("tetrahydrofuran", "thf"),                      SM.CPCMX | SM.ALPB | SM.DDCOSMO
    s_TETRAHYDROTHIOPHENE_SS_DIOXIDE = ("tetrahydrothiophene-s,s-dioxide", "tetrahydrothiophenedioxide", "sulfolane"), SM.CPCMX
    s_TETRALIN                       = ("tetralin",),                                   SM.CPCMX
    s_TOLUENE                        = ("toluene",),                                    SM.CPCMX | SM.ALPB | SM.DDCOSMO
    s_TRIBUTYLPHOSPHATE              = ("tributylphosphate",),                          SM.CPCMX
    s_TRIETHYLAMINE                  = ("triethylamine",),                              SM.CPCMX
    s_N_UNDECANE                     = ("n-undecane", "undecane"),                      SM.CPCMX
    s_WATER                          = ("water", "h2o"),                                SM.CPCMX | SM.ALPB | SM.DDCOSMO
    s_XYLENE                         = ("xylene",),                                     SM.CPCMX
# fmt: on
