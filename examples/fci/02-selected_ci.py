#!/usr/bin/env python
#
# Author: Qiming Sun <osirpt.sun@gmail.com>
#

'''
Use selected CI solver for given 1-electron and 2-electron Hamiltonian
'''

import numpy
from pyscf import fci

numpy.random.seed(12)
norb = 6
h1 = numpy.random.random((norb,norb))
h2 = numpy.random.random((norb,norb,norb,norb))
# Restore permutation symmetry
h1 = h1 + h1.T
h2 = h2 + h2.transpose(1,0,2,3)
h2 = h2 + h2.transpose(0,1,3,2)
h2 = h2 + h2.transpose(2,3,0,1)

#
# select_ci.kernel can handle all systems
#
e, fcivec = fci.select_ci.kernel(h1, h2, norb, 8, verbose=5)

#
# SCI object offers more options to control the calculation.
#
cisolver = fci.SCI()
cisolver.max_cycle = 100
cisolver.conv_tol = 1e-8
e, fcivec = cisolver.kernel(h1, h2, norb, 8)
e, fcivec = cisolver.kernel(h1, h2, norb, (5,4))  # 5 alpha, 4 beta electrons
e, fcivec = cisolver.kernel(h1, h2, norb, (3,1))  # 3 alpha, 1 beta electrons

#
# If you are sure the system ground state is singlet, you can use spin0 solver.
# Spin symmetry is considered in spin0 solver to reduce cimputation cost.
#
cisolver = fci.select_ci_spin0.SCI()
cisolver.verbose = 5
e, fcivec = cisolver.kernel(h1, h2, norb, 8)

