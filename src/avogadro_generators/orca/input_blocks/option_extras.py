# SPDX-FileCopyrightText: 2026 Avogadro Project
# SPDX-License-Identifier: BSD 3-Clause
# ******************************************************************************
# This source file is part of the Avogadro project.
#
# This source code is released under the New BSD License, (the "License").
# ******************************************************************************
"""Tooltips for all of the block keywords

Notes
-----
You may see a key called ``override_type``. This is primarily used to
take options that are floating-point numbers and turn them into strings
so that they can accept scientific notation as an input.

Another common item that you may see is ``add_dummy``. This is used to
add a dummy item at the beginning of a list so that there is not a
default value. The reason this is necessary is because there are checks
in the code for whether or not a keyword is in its default state so
that it can be skipped in writing the input file, and if there was a
default for some of the items then that might remove one of the
potential options for a user.
"""

from .basis import Basis
from .elprop import ElProp
from .scf import SCF

# fmt: off
basis_extras = {
    # Basis.BASIS: {
    #     "label"  : "Basis",
    #     "toolTip": "Specify a basis set.",
    # },
    Basis.AUXJ: {
        "label"  : "AuxJ",
        "toolTip": "Specify a Coulomb-fitting auxiliary basis set.",
        "add_dummy": True,
    },
    Basis.AUXJK: {
        "label"  : "AuxJK",
        "toolTip": "Specify a Coulomb- and Exchange-fitting auxiliary basis set.",
        "add_dummy": True,
    },
    Basis.AUXC: {
        "label"  : "AuxC",
        "toolTip": "Specify a Post-HF auxiliary basis set.",
        "add_dummy": True,
    },
    Basis.CABS: {
        "label"  : "CABS (F12 only)",
        "toolTip": "Specify a Complementary Auxiliary Basis Set (CABS) for F12 calculations.",
    },
    Basis.ECP: {
        "label"  : "ECP",
        "toolTip": "Specify an Effective Core Potential (ECP).",
    },
    Basis.GHOSTECP: {
        "label"  : "Allow Ghost ECPs",
        "toolTip": "Specify whether or not to use ECPs for Ghost atoms.",
    },
    # Basis.DECONTRACT: {
    #     "label"  : "Decontract All",
    #     "toolTip": "Decontract all orbital and auxiliary basis sets.",
    # },
    # Basis.DECONTRACTBAS: {
    #     "label"  : "Decontract Orbital Basis",
    #     "toolTip": "Decontract only orbital basis sets.",
    # },
    # Basis.DECONTRACTAUXJ: {
    #     "label"  : "Decontract AuxJ Basis",
    #     "toolTip": "Decontract only AuxJ basis sets.",
    # },
    # Basis.DECONTRACTAUXJK: {
    #     "label"  : "Decontract AuxJK Basis",
    #     "toolTip": "Decontract only AuxJK basis sets.",
    # },
    # Basis.DECONTRACTAUXC: {
    #     "label"  : "Decontract AuxC Basis",
    #     "toolTip": "Decontract only AuxC basis sets.",
    # },
    # Basis.DECONTRACTCABS: {
    #     "label"  : "Decontract CABS Basis",
    #     "toolTip": "Decontract only CABS basis sets.",
    # },
    # Basis.PCDTRIMBAS: {
    #     "label"  : "Trim Orbital Basis",
    #     "toolTip": "Trim the orbital basis in the overlap metric.",
    # },
    # Basis.PCDTRIMAUXJ: {
    #     "label"  : "Trim AuxJ Basis",
    #     "toolTip": "Trim the AuxJ basis in the Coulomb metric.",
    # },
    # Basis.PCDTRIMAUXJK: {
    #     "label"  : "Trim AuxJK Basis",
    #     "toolTip": "Trim the AuxJK basis in the Coulomb metric.",
    # },
    # Basis.PCDTRIMAUXC: {
    #     "label"  : "Trim AuxC Basis",
    #     "toolTip": "Trim the AuxC basis in the Coulomb metric.",
    # },
    # Basis.PCDTHRESH: {
    #     "label"  : "PCD Threshold",
    #     "toolTip": "Threshold for PCD (suggested 1e-16 to 1e-10, automatically chosen if < 0).",
    # },
    Basis.AUTOAUXSIZE: {
        "label"  : "AutoAux Size",
        "toolTip": "Control size of AutoAux basis sets. Larger value means larger basis.",
    },
    # Basis.AUTOAUXLMAX: {
    #     "label"  : "AutoAux L Max",
    #     "toolTip": "Enable use of highest-possible angular momentum permitted by ORCA",
    # },
    # Basis.AUTOAUXLLIMIT: {
    #     "label"  : "AutoAux L Limit",
    #     "toolTip": "Set the highest allowed angular momentum (-1 means do not set limit)",
    # },
    # Basis.AUTOAUXF_0: {
    #     "label"  : "AutoAux F[0]",
    #     "toolTip": "Factor by which to increase the maximal s-exponent.",
    # },
    # Basis.AUTOAUXF_1: {
    #     "label"  : "AutoAux F[1]",
    #     "toolTip": "Factor by which to increase the maximal p-exponent.",
    # },
    # Basis.AUTOAUXF_2: {
    #     "label"  : "AutoAux F[2]",
    #     "toolTip": "Factor by which to increase the maximal d-exponent.",
    # },
    # Basis.AUTOAUXF_3: {
    #     "label"  : "AutoAux F[3]",
    #     "toolTip": "Factor by which to increase the maximal f-exponent.",
    # },
    # Basis.AUTOAUXF_4: {
    #     "label"  : "AutoAux F[4]",
    #     "toolTip": "Factor by which to increase the maximal g-exponent.",
    # },
    # Basis.AUTOAUXF_5: {
    #     "label"  : "AutoAux F[5]",
    #     "toolTip": "Factor by which to increase the maximal h-exponent.",
    # },
    # Basis.AUTOAUXF_6: {
    #     "label"  : "AutoAux F[6]",
    #     "toolTip": "Factor by which to increase the maximal i-exponent.",
    # },
    # Basis.AUTOAUXF_7: {
    #     "label"  : "AutoAux F[7]",
    #     "toolTip": "Factor by which to increase the maximal j-exponent.",
    # },
    # Basis.AUTOAUXB_0: {
    #     "label"  : "AutoAux B[0]",
    #     "toolTip": "Even-tempered expansion factor for the s-shell.",
    # },
    # Basis.AUTOAUXB_1: {
    #     "label"  : "AutoAux B[1]",
    #     "toolTip": "Even-tempered expansion factor for the p-shell.",
    # },
    # Basis.AUTOAUXB_2: {
    #     "label"  : "AutoAux B[2]",
    #     "toolTip": "Even-tempered expansion factor for the d-shell.",
    # },
    # Basis.AUTOAUXB_3: {
    #     "label"  : "AutoAux B[3]",
    #     "toolTip": "Even-tempered expansion factor for the f-shell.",
    # },
    # Basis.AUTOAUXB_4: {
    #     "label"  : "AutoAux B[4]",
    #     "toolTip": "Even-tempered expansion factor for the g-shell.",
    # },
    # Basis.AUTOAUXB_5: {
    #     "label"  : "AutoAux B[5]",
    #     "toolTip": "Even-tempered expansion factor for the h-shell.",
    # },
    # Basis.AUTOAUXB_6: {
    #     "label"  : "AutoAux B[6]",
    #     "toolTip": "Even-tempered expansion factor for the i-shell.",
    # },
    # Basis.AUTOAUXB_7: {
    #     "label"  : "AutoAux B[7]",
    #     "toolTip": "Even-tempered expansion factor for the j-shell.",
    # },
    # Basis.AUTOAUXTIGHTB: {
    #     "label"  : "AutoAux Tight B",
    #     "toolTip": "Only use AutoAuxB[1] for shells with high L and AutoAuxB[0] for the rest.",
    # },
}

scf_extras = {
    SCF.GUESS: {
        "label"  : "Initial Guess",
        "toolTip": "Pick initial guess for SCF orbitals",
    },
    SCF.GUESSMODE: {
        "label"  : "Guess Mode",
        "toolTip": "Mode for projecting initial guess orbitals onto the basis set (not for Guess=HCore)",
    },
    SCF.AUTOSTART: {
        "label"  : "AutoStart",
        "toolTip": "Try to use orbitals from existing GBW file of the same name (if it exists).",
    },
    SCF.MOINP: {
        "label"  : "MOInp GBW File",
        "toolTip": "GBW file used for MORead",
    },
    SCF.CONVERGENCE: {
        "label"  : "Convergence Tolerance",
        "toolTip": "Set the SCF convergence tolerances.",
    },
    SCF.TOL_E: {
        "label"  : "Energy Tolerance",
        "toolTip": "Set the SCF energy convergence criteria.",
        "override_type": "string",
    },
    SCF.TOL_RMSP: {
        "label"  : "RMS Density Tolerance",
        "toolTip": "Set the SCF RMS density change convergence criteria.",
        "override_type": "string",
    },
    SCF.TOL_MAXP: {
        "label"  : "Max Density Tolerance",
        "toolTip": "Set the SCF maximum density change convergence criteria.",
        "override_type": "string",
    },
    SCF.TOL_ERR: {
        "label"  : "DIIS Error Tolerance",
        "toolTip": "Set the SCF DIIS Error convergence criteria.",
        "override_type": "string",
    },
    SCF.TOL_G: {
        "label"  : "Orbital Gradient Tolerance",
        "toolTip": "Set the SCF orbital gradient convergence criteria.",
        "override_type": "string",
    },
    SCF.TOL_X: {
        "label"  : "Orbital Rotation Angle Tolerance",
        "toolTip": "Set the SCF orbital rotation angle convergence criteria.",
        "override_type": "string",
    },
    SCF.TCUT: {
        "label": "Primitive Integral Prescreening Cutoff",
        "toolTip": "Set the SCF primitive integral prescreening threshold.",
        "override_type": "string",
    },
    SCF.THRESH: {
        "label"  : "Integral Prescreening Threshold",
        "toolTip": "Set the SCF integral prescreening threshold.",
        "override_type": "string",
    },
    SCF.CONVCHECKMODE: {
        "label"  : "Convergence Check Mode",
        "toolTip": "Set the SCF convergence check mode.",
    },
    SCF.CONVFORCED: {
        "label"  : "Require Convergence",
        "toolTip": "Toggle whether or not convergence is mandatory for the next calculation step.",
    },
    # SCF.HFTYP: {
    #     "label"  : "HF Wavefunction Type",
    #     "toolTip": "Set the wavefunction type for HF calculations.",
    # },
    # SCF.ROHF_CASE: {
    #     "label"  : "ROHF Case",
    #     "toolTip": "Type of ROHF wavefunction (only if HFTyp=ROHF).",
    # },
    # SCF.ROHF_NEL: {
    #     "label"  : "ROHF Num. Electrons",
    #     "toolTip": "Number of open-shell electrons (only if HFTyp=ROHF).",
    # },
    # SCF.ROHF_NUMOP: {
    #     "label"  : "ROHF Num. Operators",
    #     "toolTip": "Number of Operators (only if HFTyp=ROHF).",
    # },
    # SCF.ROHF_NORB: {
    #     "label"  : "ROHF Num. Orbitals",
    #     "toolTip": "Number of open-shell orbitals (only if HFTyp=ROHF).",
    # },
    # SCF.ROHF_REF: {
    #     "label"  : "ROHF Orbital Rotations",
    #     "toolTip": "Specify orbital rotations (only if HFTyp=ROHF).",
    # },
    # SCF.ROHF_AFORBS: {
    #     "label"  : "ROHF AF Orbitals",
    #     "toolTip": "User-defined anti-ferromagnetic orbitals (only if HFTyp=ROHF).",
    # },
    # SCF.XTBFOD: {
    #     "label"  : "xTB FOD Printout",
    #     "toolTip": "Enable FOD Printout for native-xTB calculations.",
    # },
    # SCF.USEXTBMIXER: {
    #     "label"  : "Use xTB Mixer",
    #     "toolTip": "Use special SCF settings similar to the ones in xTB.",
    # },
    # SCF.SOSCFMAXSTEP: {
    #     "label"  : "SOSCF Max Step",
    #     "toolTip": "Maximum SOSCF Step Size.",
    # },
    # SCF.SOSCFBLOCKDIAG: {
    #     "label"  : "Use SOSCF Block Diagonalization",
    #     "toolTip": "Perform a diagonalization of the occupied and virtual orbital blocks of the Fock matrix at the start.",
    # },
    # SCF.DELTASCFFROMGS: {
    #     "label"  : "Start ΔSCF From Ground State",
    #     "toolTip": "Start ΔSCF from an input converged ground state solution or assume it is an excited state solution.",
    # },
    # SCF.DOMOM: {
    #     "label"  : "Use Maximum Overlap Method",
    #     "toolTip": "Use maximum overlap method.",
    # },
    # SCF.KEEPINITIALREF: {
    #     "label"  : "Keep Initial Reference",
    #     "toolTip": "Always keep initial reference: IMOM.",
    # },
    # SCF.PMOM: {
    #     "label"  : "Use PMOM Metric",
    #     "toolTip": "Use the PMOM metric instead of regular MOM.",
    # },
    # SCF.ALPHACONF: {
    #     "label"  : "Alpha Configuration",
    #     "toolTip": "Define occupation of frontier orbitals in the alpha spin channel.",
    # },
    # SCF.BETACONF: {
    #     "label"  : "Beta Configuration",
    #     "toolTip": "Define occupation of frontier orbitals in the beta spin channel.",
    # },
    # SCF.IONIZEALPHA: {
    #     "label"  : "Ionize Alpha",
    #     "toolTip": "Remove electrons from specified MOs in alpha spin channel.",
    # },
    # SCF.IONIZEBETA: {
    #     "label"  : "Ionize Beta",
    #     "toolTip": "Remove electrons from specified MOs in beta spin channel.",
    # },
    # SCF.SOSCFHESSUP: {
    #     "label"  : "SOSCF Hessian Update Method",
    #     "toolTip": "Select quasi-Newton method for SOSCF Hessian Update.",
    # },
    # SCF.SOSCFCONSTRAINTS: {
    #     "label"  : "SOSCF Constraints",
    #     "toolTip": "Activate freeze-and-release SOSCF.",
    # },
    # SCF.SOSCFCONSTRAINEDMAXSTEP: {
    #     "label"  : "SOSCF Const. Max Step",
    #     "toolTip": "Maximum step size for the constrained SOSCF minimization.",
    # },
    # SCF.SOSCFCONVFACTOR: {
    #     "label"  : "SOSCF Conv. Factor",
    #     "toolTip": "Factor to multiply convergence criteria with in the constrained minimization. e.g. 100 loosens the criteria by two orders of magnitude.",
    # },
    # SCF.SOSCFCONSTRAINEDHESSUP: {
    #     "label"  : "SOSCF Const. Hess. Update",
    #     "toolTip": "SOSCF Hessian update for constrained minimization.",
    # },
    # SCF.SOSCFWRITECONSTRAINEDGBW: {
    #     "label"  : "Write SOSCF Const. GBW",
    #     "toolTip": "Write a GBW file for the constrained solution.",
    # },
    # SCF.SOSCFDAVIDSONMAXIT: {
    #     "label"  : "SOSCF Davidson MaxIter",
    #     "toolTip": "Maximum number of iterations for Davidson diagonalization in SOSCF procedure.",
    # },
    # SCF.SOSCFDAVIDSONTOLR: {
    #     "label"  : "SOSCF Davidson Residual Tol.",
    #     "toolTip": "SOSCF Davidson convergence tolerance for the maximum component of each residual vector.",
    # },
    # SCF.SOSCFDAVIDSONMAXRED: {
    #     "label"  : "SOSCF Davidson Max Reduction",
    #     "toolTip": "Davidson maximum size of the Krylov subspace per target eigenvector, meaning this will be multiplied by the target saddle point order.",
    # },
    # SCF.SOSCFDAVIDSONFDMODE: {
    #     "label"  : "SOSCF Davidson FD Stencil",
    #     "toolTip": "SOSCF Davidson finite difference stencil.",
    # },
    # SCF.SOSCFDAVIDSONFDSTEP: {
    #     "label"  : "SOSCF Davidson FD Step",
    #     "toolTip": "Davidson finite difference step size.",
    # },
    # SCF.SOSCFPRECONDTYPE: {
    #     "label"  : "SOSCF Preconditioner",
    #     "toolTip": "SOSCF Preconditioner to use",
    # },
    # SCF.SOSCFPRECONDGAMMA: {
    #     "label"  : "SOSCF Preconditioner Gamma (GradientExpansion only)",
    #     "toolTip": "Mixing Factor for GradientExpansion preconditioner",
    # },
    # SCF.SOSCFGMF: {
    #     "label"  : "Use GMF",
    #     "toolTip": "Use generalized mode following (GMF).",
    # },
    # SCF.SOSCFSPO: {
    #     "label"  : "GMF Saddle Point Order (SPO)",
    #     "toolTip": "GMF only: Optional user-defined target saddle point order (SPO).",
    # },
    # SCF.SOSCFSPOEST: {
    #     "label"  : "GMF SPO Estimate",
    #     "toolTip": "GMF only: Target saddle point order estimate.",
    # },
    # SCF.SOSCFUPDATESPOEST: {
    #     "label"  : "GMF Update SPO Estimate",
    #     "toolTip": "GMF only: Update the SPO with the number of negative eigenvalues of the first Davidson run.",
    # },
    # SCF.SOSCFSPOESTNTRIAL: {
    #     "label"  : "GMF SPO Num Eigenvectors",
    #     "toolTip": "GMF Only: How many eigenvectors of the Hessian to target more for the SPO estimate.",
    # },
    # SCF.SOSCFUPDATESPOTHRESH: {
    #     "label"  : "GMF SPO Eigenvalue Threshold",
    #     "toolTip": "GMF Only: Only eigenvalues below this threshold are considered negative enough for the SPO estimate.",
    # },
}

elprop_extras = {
    ElProp.DIPOLE: {
        "label"  : "Dipole",
        "toolTip": "Calculate dipole moment.",
    },
    ElProp.QUADRUPOLE: {
        "label"  : "Quadrupole",
        "toolTip": "Calculate quadrupole moment.",
    },
    ElProp.POLAR: {
        "label"  : "Polar",
        "toolTip": "Calculate dipole-dipole polarizability.",
    },
    ElProp.POLARVELOCITY: {
        "label"  : "Velocity Polarizability",
        "toolTip": "Calculate polarizability with respect to velocity perturbations.",
    },
    ElProp.POLARDIPQUAD: {
        "label"  : "Dipole-Quadrupole Polarizability",
        "toolTip": "Calculate dipole-quadrupole polarizability.",
    },
    ElProp.POLARQUADQUAD: {
        "label"  : "Quadrupole-Quadrupole Polarizability",
        "toolTip": "Calculate quadrupole-quadrupole polarizability.",
    },
    ElProp.HYPERPOL: {
        "label"  : "Dip-Dip-Dip Hyperpolarizability",
        "toolTip": "Calculate Dipole-Dipole Polarizability.",
    },
    ElProp.FREQ_R: {
        "label"  : "Real Frequency",
        "toolTip": "Purely real frequency, leave blank for static calculation.",
    },
    ElProp.FREQ_I: {
        "label"  : "Imaginary Frequency",
        "toolTip": "Purely imaginary frequency, leave blank for static calculation.",
    },
    ElProp.SOLVER: {
        "label"  : "CP-SCF Solver",
        "toolTip": "CG: Conjugate Gradient, DIIS: Direct Inversion in the Iterative Subspace.",
    },
    ElProp.MAXDIIS: {
        "label"  : "Max DIIS Dimension",
        "toolTip": "Maximum dimension of DIIS method.",
    },
    ElProp.SHIFT: {
        "label"  : "DIIS Level Shift",
        "toolTip": "Level shift used in DIIS solver",
    },
    ElProp.TOL: {
        "label"  : "CP-SCF Convergence Tolerance",
        "toolTip": "Convergence of Coupled-Perturbed SCF Equations (norm of the residual).",
        "override_type": "string",
    },
    ElProp.MAXITER: {
        "label"  : "Maximum Iterations",
        "toolTip": "Maximum number of iterations in the CP-SCF solver.",
    },
    ElProp.PRINTLEVEL: {
        "label"  : "Print Level",
        "toolTip": "Control print level for electric property calculation.",
    },
    ElProp.ORIGIN: {
        "label"  : "Origin",
        "toolTip": "Origin to use for electric properties.",
    },
}
# fmt: on
