# SPDX-FileCopyrightText: 2026 Avogadro Project
# SPDX-License-Identifier: BSD 3-Clause
# ******************************************************************************
# This source file is part of the Avogadro project.
#
# This source code is released under the New BSD License, (the "License").
# ******************************************************************************
"""Input generation for ORCA (https://www.faccts.de/orca/)."""

from .input_blocks import SCF, Basis, ElProp, format_block_keyword
from .simple_keywords import (
    RunType,
    Output,
    match_simple_keyword,
)
from .dft import Composite, Functionals, Disp
from .wft import MP2, CoupledCluster
from .basis_sets import (
    PopleBasisSet,
    def2BasisSet,
    JensenBasisSet,
    ccBasisSet,
    RelativisticBasisSet,
    get_basis_set,
    get_aux_basis,
    get_basis_family,
)
from .implicit_solvation import Solvent, SolvationModel
from ..utilities import Element


def write_block(block_name: str, keys_vals: dict):
    """Write an input block."""
    block = f"%{block_name}\n"

    for key, value in keys_vals.items():
        if key._dtype is str:
            block += f'    {key.name} = "{value}"\n'
        else:
            block += f"    {key.name} = {value}\n"

    block += "end\n"
    return block


def get_method(
    value: str,
) -> str | Functionals | Composite | MP2 | CoupledCluster:
    """Get a method from a string."""

    if value == "HF":
        return value
    elif "MP2" in value:
        return MP2(value)
    elif "CCSD" in value:
        return CoupledCluster(value)
    elif "-3c" in value:
        return Composite(value)
    else:
        return Functionals(value)


def generateInputFile(input_json: dict) -> tuple[str, list[str], list[str]]:
    # Collect warning strings as we go
    warnings = []
    syntax_groups = ["default"]
    # fmt: off
    opts  = input_json["options"]
    cjson = input_json["cjson"]

    # Extract undefined options:
    title: str          = opts["Title"]
    charge: int         = opts["Charge"]
    multiplicity: int   = opts["Multiplicity"]
    nprocs: int         = opts["Processor Cores"]
    max_mem: int        = opts["Memory"]
    extra_keywords: str = opts["basic_simple_keywords"]

    # Extract defined options
    run_type        = RunType(opts["Calculation Type"])
    method          = get_method(opts["Theory"])
    basis_set       = get_basis_set(opts["Basis"])
    solvent         = opts["Solvent"]
    disp            = opts["basic_disp_corr"]
    print_mos: bool = opts["basic_print_mos"]
    use_symmetry: bool = opts["basic_use_symmetry"]
    print_level     = Output(opts["basic_print_level"])
    constrain: bool = opts["basic_constrain"]

    # Extract some items from other tabs
    auxj_basis  = get_aux_basis(opts["Basis_AUXJ"])
    auxjk_basis = get_aux_basis(opts["Basis_AUXJK"])
    auxc_basis  = get_aux_basis(opts["Basis_AUXC"])
    # fmt: on
    override_bases = {
        "Basis_pople": PopleBasisSet,
        "Basis_def2": def2BasisSet,
        "Basis_cc": ccBasisSet,
        "Basis_jensen": JensenBasisSet,
        "Basis_relativistic": RelativisticBasisSet,
    }

    for basis, basis_type in override_bases.items():
        basis = opts[basis]
        if basis == "":
            pass
        else:
            basis_set = basis_type(basis)

    simple_keywords = []

    if "atoms" in cjson:
        for element in set(cjson["atoms"]["elements"]["number"]):
            element = Element(element)
            if element not in basis_set.elements:
                warnings.append(
                    f"Element {element.symbol} is not defined for the {basis_set.value} basis set!"
                )

    if isinstance(method, Functionals):
        if disp == "":
            simple_keywords.extend([method.value, basis_set])
        elif Disp[disp] not in method.disp:
            warnings.append(
                f"The dispersion correction {Disp[disp]} is not available for {method.value}!"
            )
            simple_keywords.extend([method.value, basis_set])
        else:
            simple_keywords.extend([method.value, disp, basis_set])
    elif isinstance(method, Composite):
        basis_set = ""
        simple_keywords.append(method.value)
    elif isinstance(method, (MP2, CoupledCluster)):
        if auxc_basis is None:
            warnings.append(
                "No AuxC basis selected, please select one from the Basis tab."
            )
            simple_keywords.extend([method.value, basis_set])
        elif auxc_basis.parent_basis != basis_set.__class__.__name__:
            aux_fam = get_basis_family(auxc_basis.parent_basis)
            main_fam = get_basis_family(basis_set.__class__.__name__)
            warnings.append(
                f"The auxiliary basis {auxc_basis.basis_name} belongs to the {aux_fam} family, but your primary basis is of the {main_fam} family."
            )
            simple_keywords.extend([method.value, basis_set, auxc_basis])
        else:
            simple_keywords.extend([method.value, basis_set, auxc_basis])
    elif method == "HF":
        simple_keywords.extend([method, basis_set])

    if auxj_basis is not None:
        simple_keywords.append(auxj_basis)

    if auxjk_basis is not None:
        simple_keywords.append(auxjk_basis)

    if solvent != "":
        solvent = Solvent(solvent)
        solvent_model = SolvationModel[opts["Solvation Model"].upper()]
        if solvent_model not in solvent.models:
            warnings.append(
                f"Solvation model {solvent_model} not available for solvent {solvent.aliases[0]}!"
            )
        else:
            simple_keywords.append(f"{solvent_model}({solvent})")
        syntax_groups.append("solvent")

    if print_mos:
        simple_keywords.extend([Output.PRINTMOS, Output.PRINTBASIS])

    if use_symmetry:
        simple_keywords.append("UseSym")

    if print_level != "NormalPrint":
        simple_keywords.append(print_level)

    for keyword in extra_keywords.replace(",", " ").split():
        kwd = match_simple_keyword(keyword)
        if kwd is not None:
            simple_keywords.append(kwd)
        else:
            warnings.append(f"Keyword {keyword} is not recognized!")
    # fmt: off
    generated_input = (
        "# File Generated with Avogadro\n"
       f"# {title}\n"
       f"#\n"
    )
    # fmt: on
    generated_input += f"!{run_type.value}"
    for kwd in simple_keywords:
        generated_input += f" {kwd}"
    # Trailing whitespace to avoid syntax highlighting bugs
    generated_input += " \n"

    if max_mem != 4:
        generated_input += f"%MaxCore {int(max_mem * 1024 / nprocs)}\n"

    if nprocs != 1:
        generated_input += f"%pal\n    nprocs = {nprocs}\nend\n"

    if (
        constrain is True
        and "atoms" in cjson
        and ("constraints" in cjson or "frozen" in cjson)
    ):
        # check for constraints and frozen atoms in cjson
        generated_input += "%geom\n"
        generated_input += "    Constraints \n"

        # look for bond, angle, torsion constraints
        if "constraints" in cjson:
            # loop through the output
            # e.g. "{ B N1 N2 value C }"
            for constraint in cjson["constraints"]:
                generated_input += " " * 8  # Add indentation
                if len(constraint) == 3:
                    # distance
                    value, atom1, atom2 = constraint
                    generated_input += f"{{ B {atom1} {atom2} {value:.6f} C }} \n"
                if len(constraint) == 4:
                    # angle
                    value, atom1, atom2, atom3 = constraint
                    generated_input += (
                        f"{{ A {atom1} {atom2} {atom3} {value:.6f} C }} \n"
                    )
                if len(constraint) == 5:
                    # torsion / dihedral
                    value, atom1, atom2, atom3, atom4 = constraint
                    generated_input += (
                        f"{{ D {atom1} {atom2} {atom3} {atom4} {value:.6f} C }} \n"
                    )

        # look for frozen atoms
        if "frozen" in cjson["atoms"]:
            # two possibilities - same number of atoms
            # or .. 3*number of atoms
            frozen = cjson["atoms"]["frozen"]
            atomCount = len(cjson["atoms"]["elements"]["number"])
            if len(frozen) == atomCount:
                # look for 1 or 0
                for i in range(len(frozen)):
                    if frozen[i] == 1:
                        generated_input += f"{' ' * 8}{{ C {i} C }} \n"
            elif len(frozen) == 3 * atomCount:
                # look for 1 or 0 - x, y, z for each atom
                for i in range(0, len(frozen), 3):
                    if frozen[i] == 0:
                        generated_input += f"{' ' * 8}{{ X {i} C }} \n"
                    if frozen[i + 1] == 0:
                        generated_input += f"{' ' * 8}{{ Y {i} C }} \n"
                    if frozen[i + 2] == 0:
                        generated_input += f"{' ' * 8}{{ Z {i} C }} \n"

        generated_input += "    end\n"
        generated_input += "end\n"

    scf_block = []
    for kwd in SCF:
        val = opts[kwd.get_json_key()]
        try:
            val = kwd._dtype(val)
        except ValueError:
            pass
        if not kwd.is_default(val):
            scf_block.append(format_block_keyword(kwd, val))

    basis_block = []
    for kwd in Basis:
        val = opts[kwd.get_json_key()]
        try:
            val = kwd._dtype(val)
        except ValueError:
            pass
        if not kwd.is_default(val):
            basis_block.append(format_block_keyword(kwd, val))

    elprop_block = []
    for kwd in ElProp:
        val = opts[kwd.get_json_key()]
        try:
            val = kwd._dtype(val)
        except ValueError:
            pass
        if not kwd.is_default(val):
            elprop_block.append(format_block_keyword(kwd, val))

    if len(scf_block) != 0:
        syntax_groups.append("scf")

        generated_input += "%scf\n"
        for item in scf_block:
            generated_input += item
        generated_input += "end\n"

    if len(basis_block) != 0:
        syntax_groups.append("basis")

        generated_input += "%basis\n"
        for item in basis_block:
            generated_input += item
        generated_input += "end\n"

    if len(elprop_block) != 0:
        syntax_groups.append("elprop")

        generated_input += "%elprop\n"
        for item in elprop_block:
            generated_input += item
        generated_input += "end\n"

    generated_input += f"* xyz {charge} {multiplicity}\n"
    generated_input += "$$coords:____Sxyz$$\n"
    generated_input += "*\n\n\n"

    return generated_input, warnings, syntax_groups


def generateInput(input_json: dict, debug: bool) -> dict:

    generated_input, warnings, syntax_groups = generateInputFile(input_json)

    filename = input_json["options"]["Filename Base"] + ".inp"

    result = {
        "files": [
            {
                "filename": filename,
                "contents": generated_input,
                "highlightStyles": syntax_groups,
            },
        ],
        "mainFile": filename,
    }

    if warnings:
        result["warnings"] = warnings

    return result
