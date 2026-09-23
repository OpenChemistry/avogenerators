# SPDX-FileCopyrightText: 2026 Avogadro Project
# SPDX-License-Identifier: BSD 3-Clause
# ******************************************************************************
# This source file is part of the Avogadro project.
#
# This source code is released under the New BSD License, (the "License").
# ******************************************************************************
"""Input generation for ORCA (https://www.faccts.de/orca/)."""

from collections.abc import Sequence

from ..utilities import Element
from .basis_sets import (
    JensenBasisSet,
    PopleBasisSet,
    RelativisticBasisSet,
    ccBasisSet,
    def2BasisSet,
    get_aux_basis,
    get_basis_family,
    get_basis_set,
)
from .dft import Composite, Disp, Functionals
from .implicit_solvation import SolvationModel, Solvent
from .input_blocks import SCF, Basis, ElProp, format_block_keyword
from .simple_keywords import (
    Output,
    RunType,
    match_simple_keyword,
)
from .wft import MP2, CoupledCluster


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


def format_index_list(indices: Sequence[int]) -> str:
    """Format a sorted list of indices using ORCA fragment syntax.

    Runs of consecutive indices are collapsed into ``first:last``, so
    ``[0, 2, 3, 4]`` becomes ``"0 2:4"``.
    """
    ranges = []
    start = previous = indices[0]

    for index in indices[1:]:
        if index == previous + 1:
            previous = index
            continue
        ranges.append(f"{start}" if start == previous else f"{start}:{previous}")
        start = previous = index

    ranges.append(f"{start}" if start == previous else f"{start}:{previous}")
    return " ".join(ranges)


def get_fragments(cjson: dict) -> list[list[int]]:
    """Group the atom indices into fragments, one per Avogadro layer.

    Layer IDs are arbitrary integers while ORCA numbers fragments from
    one, so the sorted layer IDs are mapped onto fragments 1, 2, ...
    Molecules without layers have no fragments at all.
    """
    layers = cjson.get("atoms", {}).get("layer")
    if layers is None:
        return []

    fragments: dict[int, list[int]] = {}
    for atom, layer in enumerate(layers):
        fragments.setdefault(layer, []).append(atom)

    return [fragments[layer] for layer in sorted(fragments)]


def get_fragment_charge_and_multiplicity(cjson: dict, fragment: Sequence[int]) -> tuple[int, int]:
    """Work out the charge and multiplicity of one fragment.

    The formal charges of the fragment's atoms sum to its charge, and the
    lowest multiplicity consistent with the resulting electron count is
    assumed: a singlet, or a doublet if that count is odd. Avogadro only
    writes formal charges when at least one of them is non-zero, so a
    missing key means every fragment is neutral.
    """
    numbers = cjson["atoms"]["elements"]["number"]
    formal_charges = cjson["atoms"].get("formalCharges")

    charge = 0
    if formal_charges is not None:
        charge = sum(formal_charges[atom] for atom in fragment)

    electrons = sum(numbers[atom] for atom in fragment) - charge

    return charge, 1 if electrons % 2 == 0 else 2


def write_frag_block(fragments: Sequence[Sequence[int]]) -> str:
    """Write a %frag block defining each fragment by its atom indices."""
    block = "%frag\n"
    block += "    Definition\n"
    for number, fragment in enumerate(fragments, start=1):
        block += f"        {number} {{{format_index_list(fragment)}}} end\n"
    block += "    end\n"
    block += "end\n"

    return block


def write_coordinates(cjson: dict, fragment: Sequence[int]) -> str:
    """Write an explicit coordinate block for a subset of the atoms.

    Avogadro only substitutes the whole molecule for the ``$$coords$$``
    keyword, so the jobs that hold a single fragment have to spell their
    geometry out. The layout matches the ``____Sxyz`` coordinate spec that
    the other jobs use.
    """
    numbers = cjson["atoms"]["elements"]["number"]
    coords = cjson["atoms"]["coords"]["3d"]

    block = ""
    for atom in fragment:
        symbol = Element(numbers[atom]).symbol
        x, y, z = coords[3 * atom : 3 * atom + 3]
        block += f"    {symbol:<3} {x:>11.6f} {y:>11.6f} {z:>11.6f}\n"

    return block


def write_counterpoise_jobs(
    header: str,
    blocks: str,
    frag_block: str,
    fragments: Sequence[Sequence[int]],
    cjson: dict,
    charge: int,
    multiplicity: int,
) -> str:
    """Write the job sequence for a Boys-Bernardi counterpoise correction.

    The first job is the whole complex. Each fragment is then computed
    twice, both times at the geometry of the complex: once with the basis
    functions of the other fragments still present as ghost atoms, and once
    on its own. The counterpoise-corrected interaction energy is the energy
    of the complex less the ghosted fragment energies, and the BSSE is how
    much each ghosted fragment falls below the same fragment on its own.
    """
    jobs: list[str] = [
        (
            "# Boys-Bernardi counterpoise correction, one job per fragment.\n"
            "# Writing E(i) for a fragment in its own basis set and E(i, ghost)\n"
            "# for the same fragment in the basis set of the complex:\n"
            "#\n"
            "#   interaction energy = E(complex) - sum_i E(i, ghost)\n"
            "#   BSSE               = sum_i [ E(i) - E(i, ghost) ]\n"
            "#\n"
            "# Both are at the geometry of the complex, so neither includes the\n"
            "# energy the fragments gain by relaxing once they come apart.\n"
            "\n"
            "# The complex, in its own basis set\n"
            f"{header}"
            '%id "complex"\n'
            f"{frag_block}"
            f"{blocks}"
            f"* xyz {charge} {multiplicity}\n"
            "$$coords:____Sxyz$$\n"
            "*\n"
        )
    ]

    numbers = list(range(1, len(fragments) + 1))

    # The fragments in their own basis sets, giving the BSSE itself. These
    # come before the ghosted jobs because a $new_job keeps whatever the
    # previous job set, and an inherited GhostFrags would quietly ghost the
    # only fragment these jobs have. Their atoms are renumbered from zero,
    # so they redefine %frag as well rather than inherit indices that no
    # longer point at anything.
    for number, fragment in zip(numbers, fragments, strict=True):
        frag_charge, frag_multiplicity = get_fragment_charge_and_multiplicity(cjson, fragment)
        jobs.append(
            f"# Fragment {number} in its own basis set\n"
            f"{header}"
            f'%id "fragment{number}"\n'
            f"{write_frag_block([range(len(fragment))])}"
            f"{blocks}"
            f"* xyz {frag_charge} {frag_multiplicity}\n"
            f"{write_coordinates(cjson, fragment)}"
            "*\n"
        )

    # The same fragments in the basis set of the complex, giving the
    # CP-corrected interaction energy once subtracted from its energy
    for number, fragment in zip(numbers, fragments, strict=True):
        ghosts = [other for other in numbers if other != number]
        frag_charge, frag_multiplicity = get_fragment_charge_and_multiplicity(cjson, fragment)
        jobs.append(
            f"# Fragment {number} in the basis set of the complex\n"
            f"{header}"
            f'%id "fragment{number}_ghost"\n'
            f"{frag_block}"
            "%geom\n"
            f"    GhostFrags {{{format_index_list(ghosts)}}} end\n"
            "end\n"
            f"{blocks}"
            f"* xyz {frag_charge} {frag_multiplicity}\n"
            "$$coords:____Sxyz$$\n"
            "*\n"
        )

    return "\n$new_job\n".join(jobs)


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
    # Counterpoise is not an ORCA keyword: it expands to a series of single
    # points, so the run type written into the input file is still SP
    counterpoise    = run_type is RunType.COUNTERPOISE
    if counterpoise:
        run_type = RunType.SP
    method          = get_method(opts["Theory"])
    basis_set       = get_basis_set(opts["Basis"])
    solvent         = opts["Solvent"]
    disp            = opts["basic_disp_corr"]
    print_mos: bool = opts["basic_print_mos"]
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
            warnings.append("No AuxC basis selected, please select one from the Basis tab.")
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

    if print_level != "NormalPrint":
        simple_keywords.append(print_level)

    for keyword in extra_keywords.replace(",", " ").split():
        kwd = match_simple_keyword(keyword)
        if kwd is not None:
            simple_keywords.append(kwd)
        else:
            warnings.append(f"Keyword {keyword} is not recognized!")
    # fmt: off
    preamble = (
        "# File Generated with Avogadro\n"
       f"# {title}\n"
       f"#\n"
    )
    # fmt: on
    header = f"!{run_type.value}"
    for kwd in simple_keywords:
        header += f" {kwd}"
    # Trailing whitespace to avoid syntax highlighting bugs
    header += " \n"

    blocks = ""

    if max_mem != 4:
        header += f"%MaxCore {int(max_mem * 1024 / nprocs)}\n"

    if nprocs != 1:
        header += f"%pal\n    nprocs = {nprocs}\nend\n"

    # check for constraints and frozen atoms in cjson
    has_constraints = (
        constrain is True and "atoms" in cjson and ("constraints" in cjson or "frozen" in cjson)
    )

    if has_constraints and counterpoise:
        warnings.append(
            "The constraints were left out of the input file. A counterpoise "
            "correction is a series of single points, and its %geom block "
            "holds the ghost fragments instead."
        )

    if has_constraints and not counterpoise:
        blocks += "%geom\n"
        blocks += "    Constraints \n"

        # look for bond, angle, torsion constraints
        if "constraints" in cjson:
            # loop through the output
            # e.g. "{ B N1 N2 value C }"
            for constraint in cjson["constraints"]:
                blocks += " " * 8  # Add indentation
                if len(constraint) == 3:
                    # distance
                    value, atom1, atom2 = constraint
                    blocks += f"{{ B {atom1} {atom2} {value:.6f} C }} \n"
                if len(constraint) == 4:
                    # angle
                    value, atom1, atom2, atom3 = constraint
                    blocks += f"{{ A {atom1} {atom2} {atom3} {value:.6f} C }} \n"
                if len(constraint) == 5:
                    # torsion / dihedral
                    value, atom1, atom2, atom3, atom4 = constraint
                    blocks += f"{{ D {atom1} {atom2} {atom3} {atom4} {value:.6f} C }} \n"

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
                        blocks += f"{' ' * 8}{{ C {i} C }} \n"
            elif len(frozen) == 3 * atomCount:
                # look for 1 or 0 - x, y, z for each atom
                for i in range(0, len(frozen), 3):
                    if frozen[i] == 0:
                        blocks += f"{' ' * 8}{{ X {i} C }} \n"
                    if frozen[i + 1] == 0:
                        blocks += f"{' ' * 8}{{ Y {i} C }} \n"
                    if frozen[i + 2] == 0:
                        blocks += f"{' ' * 8}{{ Z {i} C }} \n"

        blocks += "    end\n"
        blocks += "end\n"

    # Each Avogadro layer becomes an ORCA fragment, if there is more than one
    fragments = get_fragments(cjson)
    frag_block = write_frag_block(fragments) if len(fragments) > 1 else ""

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

        blocks += "%scf\n"
        for item in scf_block:
            blocks += item
        blocks += "end\n"

    if len(basis_block) != 0:
        syntax_groups.append("basis")

        blocks += "%basis\n"
        for item in basis_block:
            blocks += item
        blocks += "end\n"

    if len(elprop_block) != 0:
        syntax_groups.append("elprop")

        blocks += "%elprop\n"
        for item in elprop_block:
            blocks += item
        blocks += "end\n"

    if counterpoise and len(fragments) < 2:
        warnings.append(
            "A counterpoise correction needs at least two fragments. "
            "Put each molecule of the complex into its own layer, then "
            "generate the input again."
        )
        counterpoise = False

    # ORCA names the coordinate format on the block header, so the choice is
    # made here rather than left to Avogadro. A counterpoise job writes each
    # fragment out separately and stays Cartesian.
    zmatrix = not counterpoise and opts.get("Coordinates", "").startswith("Z-Matrix")

    if counterpoise:
        fragment_charges = [
            get_fragment_charge_and_multiplicity(cjson, fragment) for fragment in fragments
        ]
        if sum(frag_charge for frag_charge, _ in fragment_charges) != charge:
            warnings.append(
                "The formal charges of the fragments do not add up to the "
                "charge of the complex. Check the charge on each fragment "
                "in the generated input file."
            )
        if multiplicity != 1:
            warnings.append(
                "The lowest multiplicity was assumed for every fragment. "
                "Check the multiplicity on each fragment in the generated "
                "input file."
            )

        generated_input = preamble + write_counterpoise_jobs(
            header, blocks, frag_block, fragments, cjson, charge, multiplicity
        )
        generated_input += "\n"
    else:
        generated_input = preamble + header + frag_block + blocks
        if zmatrix:
            # "gzmt" is the Gaussian-style z-matrix; ORCA's own "int" format
            # puts the three reference columns before the values instead.
            generated_input += f"* gzmt {charge} {multiplicity}\n"
            generated_input += "$$zmat:____S_I_R_J_A_K_T$$\n"
        else:
            generated_input += f"* xyz {charge} {multiplicity}\n"
            generated_input += "$$coords:____Sxyz$$\n"
        generated_input += "*\n\n\n"

    return generated_input, warnings, syntax_groups


def generateInput(input_json: dict, debug: bool) -> dict:  # noqa: FBT001

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
