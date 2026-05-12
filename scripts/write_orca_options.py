# SPDX-FileCopyrightText: 2026 Avogadro Project
# SPDX-License-Identifier: BSD 3-Clause
# ******************************************************************************
# This source file is part of the Avogadro project.
#
# This source code is released under the New BSD License, (the "License").
# ******************************************************************************
"""This script writes the entirety of the ORCA generator's ``options.toml``
file.

This script is structured in two main parts, the Basic tab and the
Block tabs.

The ``BasicTab`` class is composed of instances of the
``BasicOption`` dataclass, and is generally supposed to be where the
most common user options are placed. It also contains some of the
special options such as ``Title``, ``Theory``, ``Basis``, and so on.
If you are adding a new option to the Basic tab, it should go into
that class.

The function ``write_block_tab`` is designed to allow for automatic
writing of the various input blocks that ORCA offers. If you wish to
add a new block or change an existing block, do not just add the
options using the ``custom_opts`` dict, add the block and its
options into the correct Python module located at
``src/avogadro_generators/orca/input_blocks``, and write the toolTips
and labels to the ``option_extras.py`` file, then just put the relevant
block enum, tab name, and block extras into the ``tabs`` dict near the
bottom of this file.

Notes
-----
If you are supplying a value that is best expressed in scientific
notation, use the ``override_type`` option in ``BlockOption`` to make
the option a string instead of a floating point number. This is because
the Qt widget that is currently used is a ``QDoubleSpinBox``, which can
not handle scientific notation. This may change in the future, but for
now it this is the simplest workaround.

You may notice a large number of commented-out options in the various
block tabs. This is because the current widget handling in Avogadro 2
does not support a scroll bar, so it tries to resize the window to fit
everything on it. Naturally, when a block has >50 options, this means
the windows can be extremely tall and inhibit use of the generator.
Until this is fixed, please test thoroughly and ensure that the options
in the generator do not cause the aforementioned window size issue.
"""

from dataclasses import dataclass
from pathlib import Path

from avogadro_generators.orca.basis_sets import (
    PopleBasisSet,
    def2BasisSet,
    JensenBasisSet,
    ccBasisSet,
    RelativisticBasisSet,
)
from avogadro_generators.orca.dft import Composite, Functionals, Disp
from avogadro_generators.orca.wft import MP2, CoupledCluster
from avogadro_generators.orca.simple_keywords import (
    RunType,
    Output,
)
from avogadro_generators.orca.implicit_solvation import Solvent
from avogadro_generators.orca.input_blocks.elprop import ElProp
from avogadro_generators.orca.input_blocks.basis import Basis
from avogadro_generators.orca.input_blocks.scf import SCF
from avogadro_generators.orca.input_blocks.option_extras import (
    scf_extras,
    basis_extras,
    elprop_extras,
)


@dataclass
class BasicOption:
    """Possible values for a user option."""

    dtype: str  # string, stringList, filePath, boolean, integer, float, text, table
    default: str | int
    label: str
    options: tuple | None = None
    toolTip: str | None = None
    order: int | None = None
    hide: bool | None = None
    minimum: int | float | None = None
    maximum: int | float | None = None


class BasicTab:
    """Class for writing the Basic tab"""

    name = "Basic"
    # fmt: off
    inputs = {
        "Title": BasicOption(
            dtype="string",
            default="",
            label="Title",
            toolTip="Title of the input file (not recognized by ORCA)",
        ),
        "Filename Base": BasicOption(
            dtype="string",
            default="job",
            label="Filename Base",
        ),
        "Processor Cores": BasicOption(
            dtype="integer",
            default=1,
            label="Number of Processes",
            minimum=1,
        ),
        "Memory": BasicOption(
            dtype="integer",
            default=4,
            label="Memory",
            minimum=1,
            toolTip="Total available memory (divided by nprocs to get memory per core)",
        ),
        "Calculation Type": BasicOption(
            dtype="stringList",
            default=2,  # Opt
            label="Calculation Type",
            options=(
                RunType.SP,
                RunType.ENGRAD,
                RunType.OPT,
                RunType.OPTTS,
                RunType.FREQ,
                RunType.NUMFREQ,
            ),
            toolTip="Type of calculation to run",
        ),
        "Theory": BasicOption(
            dtype="stringList",
            default=0,  # r2SCAN-3c
            label="Theory",
            options=(
                Composite.R2SCAN_3C,
                Composite.PBEH_3C,
                Composite.B97_3C,
                Composite.WB97X_3C,
                Functionals.LDA,
                Functionals.PBE,
                Functionals.B97M_V,
                Functionals.B97M_D4,
                Functionals.R2SCAN,
                Functionals.PBE0,
                Functionals.R2SCAN0,
                Functionals.WB97X_D4,
                Functionals.WB97X_V,
                Functionals.WB97M_D4,
                Functionals.WB97M_V,
                Functionals.PR2SCAN69,
                Functionals.B2GP_PLYP,
                "HF",
                MP2.RI_MP2,
                MP2.DLPNO_MP2,
                MP2.SCS_DLPNO_MP2,
                CoupledCluster.RI_CCSD_T_,
                CoupledCluster.DLPNO_CCSD_T_,
                CoupledCluster.DLPNO_CCSD_T1_,
            ),
        ),
        "Basis": BasicOption(
            dtype="stringList",
            default=1,  # def2-TZVP
            label="Basis",
            options=(
                def2BasisSet.DEF2_SVP,
                def2BasisSet.DEF2_TZVP,
                def2BasisSet.DEF2_QZVP,
                def2BasisSet.DEF2_TZVPP,
                def2BasisSet.DEF2_QZVPP,
                def2BasisSet.DEF2_SVPD,
                def2BasisSet.DEF2_TZVPPD,
                def2BasisSet.DEF2_QZVPPD,
                ccBasisSet.CC_PVDZ,
                ccBasisSet.CC_PVTZ,
                ccBasisSet.CC_PVQZ,
                ccBasisSet.AUG_CC_PVDZ,
                ccBasisSet.AUG_CC_PVTZ,
                ccBasisSet.AUG_CC_PVQZ,
                JensenBasisSet.PC_1,
                JensenBasisSet.PC_2,
                JensenBasisSet.PC_3,
                JensenBasisSet.AUG_PC_1,
                JensenBasisSet.AUG_PC_2,
                JensenBasisSet.AUG_PC_3,
            ),
        ),
        "Charge": BasicOption(
            dtype="integer",
            default=0,
            label="Charge",
            minimum=-9,
            maximum=9
        ),
        "Multiplicity": BasicOption(
            dtype="integer",
            default=1,
            label="Multiplicity",
            minimum=1,
            toolTip="Calculated as 2S+1 where S is the number of unpaired electrons",
        ),
        "Solvent": BasicOption(
            dtype="stringList",
            default=0,
            label="Solvent",
            options=(
                Solvent.s_NONE,
                Solvent.s_WATER,
                Solvent.s_ACETONITRILE,
                Solvent.s_ACETONE,
                Solvent.s_ETHANOL,
                Solvent.s_METHANOL,
                Solvent.s_CARBON_TETRACHLORIDE,
                Solvent.s_DICHLOROMETHANE,
                Solvent.s_CHLOROFORM,
                Solvent.s_DIMETHYLSULFOXIDE,
                Solvent.s_NN_DIMETHYLFORMAMIDE,
                Solvent.s_N_HEXANE,
                Solvent.s_TOLUENE,
                Solvent.s_PYRIDINE,
                Solvent.s_TETRAHYDROFURAN,
            ),
        ),
        "Solvation Model": BasicOption(
            dtype="stringList",
            default=0,  # CPCM, but really is nothing without Solvent
            label="Solvation Model",
            options=(
                "CPCM",
                "SMD",
                "COSMO_RS",
                "ALPB",
                "ddCOSMO",
                "CPCMX",
            ),
        ),
        "basic_disp_corr": BasicOption(
            dtype="stringList",
            default=0,
            label="Dispersion Correction",
            order=0,
            options=(
                Disp.NODISP,
                Disp.D3BJ,
                Disp.D3ZERO,
                Disp.D4,
                Disp.NL,
                Disp.SCNL,
            ),
        ),
        "basic_print_mos": BasicOption(
            dtype="boolean",
            default=True,
            label="Print Molecular Orbitals",
            order=1,
        ),
        "basic_constrain": BasicOption(
            dtype="boolean",
            default=False,
            label="Use Constraints",
            order=2,
        ),
        "basic_print_level": BasicOption(
            dtype="stringList",
            default=2,  # NormalPrint
            label="Print Level",
            order=3,
            options=(
                Output.MINIPRINT,
                Output.SMALLPRINT,
                Output.NORMALPRINT,
                Output.LARGEPRINT,
            ),
        ),
        "basic_use_symmetry": BasicOption(
            dtype="boolean",
            default=False,
            label="Use Symmetry",
            toolTip="Emit the UseSym simple keyword.",
            order=4,
        ),
        "basic_simple_keywords": BasicOption(
            dtype="string",
            default="",
            label="Additional Simple Keywords",
            toolTip="Comma- or whitespace-separated list of simple input keywords.",
            order=5,
        ),
    }
    # fmt: on
    @classmethod
    def write_tab(cls) -> str:
        """Write the ``options.toml`` entry for this tab."""

        tab = ""
        for key, val in cls.inputs.items():
            tab += f'["{key}"]\n'
            tab += f'label = "{val.label}"\n'
            tab += f'type = "{val.dtype}"\n'
            if val.dtype == "string":
                tab += f'default = "{val.default}"\n'
            elif val.dtype == "boolean":
                tab += f"default = {str(val.default).lower()}\n"
            else:
                tab += f"default = {val.default}\n"

            if val.options is not None:
                tab += "values = [\n"
                for option in val.options:
                    tab += f'    "{option}",\n'
                tab += "]\n"

            if val.minimum is not None:
                tab += f"minimum = {val.minimum}\n"

            if val.maximum is not None:
                tab += f"maximum = {val.maximum}\n"

            if val.toolTip is not None:
                tab += f'toolTip = "{val.toolTip}"\n'

            if val.order is not None:
                tab += f"order = {val.order}\n"

            tab += f'tab = "{cls.name}"\n\n'

        return tab


def write_block_tab(block_enum, tab_name: str, extras: dict) -> str:
    """Write the ``options.toml`` entry for an input block."""
    tab = ""
    for option in block_enum:
        # fmt: off
        key = option.get_json_key() # e.g. ElProp_DIPOLE
        toolTip       = extras[option]["toolTip"]
        label         = extras[option]["label"]
        override_type = extras[option].get("override_type", None)
        add_dummy     = extras[option].get("add_dummy", False)
        # fmt: on
        tab += f"[{key}]\n"
        tab += f'label = "{label}"\n'

        if override_type is not None:
            tab += f'type = "{override_type}"\n'
        else:
            tab += f'type = "{option.dtype}"\n'

        if option.dtype == "string" and option.default is not None:
            if option.options is None:
                tab += f'default = "{option.default}"\n'
            else:
                tab += f"default = {option.default}\n"
        elif option.dtype == "boolean" and option.default is not None:
            tab += f"default = {str(option.default).lower()}\n"
        elif option.default is not None:
            tab += f"default = {option.default}\n"

        if option.options is not None:
            tab += "values = [\n"
            if add_dummy:  # Add a blank option at the beginning.
                tab += '    "",\n'
            for opt in option.options:
                tab += f'    "{opt}",\n'
            tab += "]\n"

        if option.minimum is not None:
            tab += f"minimum = {option.minimum}\n"

        if option.maximum is not None:
            tab += f"maximum = {option.maximum}\n"

        tab += f'toolTip = "{toolTip}"\n'

        tab += f'tab = "{tab_name}"\n\n'

    return tab


"""This is where you should put any custom options that have special
behavior. It is currently used to put lists of every basis set into
the Basis tab.
"""
custom_opts = {
    "Basis_pople": {
        "type": "stringList",
        "default": 0,
        "label": "Pople Basis Set",
        "values": [""] + [str(i) for i in PopleBasisSet],
        "toolTip": "Pople-style split-valence basis sets.",
        "tab": "Basis",
    },
    "Basis_def2": {
        "type": "stringList",
        "default": 0,
        "label": "def2 Basis Set",
        "values": [""] + [str(i) for i in def2BasisSet],
        "toolTip": "Karlsruhe def2-n(Z)VP basis sets.",
        "tab": "Basis",
    },
    "Basis_cc": {
        "type": "stringList",
        "default": 0,
        "label": "cc-pVnZ Basis Set",
        "values": [""] + [str(i) for i in ccBasisSet],
        "toolTip": "Correlation Consistent basis sets.",
        "tab": "Basis",
    },
    "Basis_jensen": {
        "type": "stringList",
        "default": 0,
        "label": "pc-n Basis Set",
        "values": [""] + [str(i) for i in JensenBasisSet],
        "toolTip": "Jensen's Polarization-Consistent basis sets.",
        "tab": "Basis",
    },
    "Basis_relativistic": {
        "type": "stringList",
        "default": 0,
        "label": "Relativistic Basis Set",
        "values": [""] + [str(i) for i in RelativisticBasisSet],
        "toolTip": "Relativistic SARC/ZORA/DKH/x2c basis sets.",
        "tab": "Basis",
    },
}

tabs = {
    SCF: {
        "name": "SCF",
        "extras": scf_extras,
    },
    Basis: {
        "name": "Basis",
        "extras": basis_extras,
    },
    ElProp: {
        "name": "Electric Properties",
        "extras": elprop_extras,
    },
}

if __name__ == "__main__":
    orca_toml = (
        Path(__file__).parent.parent / "src/avogadro_generators/orca/options.toml"
    )

    toml = "# This file was automatically generated, do NOT modify manually!\n\n"

    toml += f'tabs = ["{BasicTab.name}"'
    for info in tabs.values():
        toml += f', "{info["name"]}"'
    toml += "]\n\n"

    toml += BasicTab.write_tab()

    for key, opt in custom_opts.items():
        toml += f"[{key}]\n"
        toml += f'label = "{opt["label"]}"\n'
        toml += f'type = "{opt["type"]}"\n'
        toml += f"default = {opt['default']}\n"
        if "values" in opt:
            toml += "values = [\n"
            for item in opt["values"]:
                toml += f'    "{item}",\n'
            toml += "]\n"
        if "minimum" in opt:
            toml += f"minimum = {opt['minimum']}"
        if "maximum" in opt:
            toml += f"maximum = {opt['maximum']}"

        toml += f'toolTip = "{opt["toolTip"]}"\n'
        toml += f'tab = "{opt["tab"]}"\n\n'

    for block, info in tabs.items():
        tab_string = write_block_tab(block, info["name"], info["extras"])
        toml += tab_string

    with open(orca_toml, "w") as orca:
        orca.write(toml)
