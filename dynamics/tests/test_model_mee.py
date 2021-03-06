"""Created on Wed Sep 07 2016 12:09.

@author: Nathan Budd
"""
import unittest
import numpy as np
import numpy.matlib as npm
import matplotlib.pyplot as plt
from ..model_mee import ModelMEE
from ..perturb_zero import PerturbZero
from ..reference_mee import ReferenceMEE
from ..warm_start_constant import WarmStartConstant
from ...mcpi.mcpi import MCPI
from ...mcpi.mcpi_approx import MCPIapprox
from ...orbital_mech.orbit import Orbit
from ...orbital_mech.element_sets.orb_coe import OrbCOE
from ...orbital_mech.element_sets.orb_mee import OrbMEE


class TestModelMEE(unittest.TestCase):
    """Test class for ModelMEE."""

    def setUp(self):
        mu = 1.
        self.mmee = ModelMEE(mu)

    def test_instantiation(self):
        self.assertIsInstance(self.mmee, ModelMEE)

    def test_getattr(self):
        self.assertEqual(self.mmee.mu, 1)

    def test_setattr(self):
        self.mmee.mu = 2.
        self.assertEqual(self.mmee.mu, 2)

    def test_dynamics(self):
        x = np.array([[2., .5, 1., .1, .1, 0.],
                      [4., .5, 1., .1, .1, 0.],
                      [8., .5, 1., .1, .1, 0.]])
        t = np.array([[0.], [1.], [2.]])

        xdot = self.mmee(t, x)
        print(self.mmee.Xdot)
        self.assertEqual(xdot.shape, (3, 6))

    def test_dynamics_integration(self):
        domains = (0., 30.)
        N = 20,
        X0 = Orbit(OrbCOE({'p': 2., 'e': 0., 'i': .5, 'W': 0., 'w': 0.,
                           'nu': 0.})).mee().list()[:-1]
        tol = 1e-10

        mcpi = MCPI(self.mmee, domains, N, WarmStartConstant(), X0, tol)
        X_approx = mcpi.solve_serial()
        print(mcpi.iterations)

        T = np.linspace(domains[0], domains[1], 100).reshape((100, 1))
        x_approx = X_approx(T)
        plt_p, = plt.plot(T, [row[0] for row in x_approx], label='p')
        plt_f, = plt.plot(T, [row[1] for row in x_approx], label='f')
        plt_g, = plt.plot(T, [row[2] for row in x_approx], label='g')
        plt_h, = plt.plot(T, [row[3] for row in x_approx], label='h')
        plt_k, = plt.plot(T, [row[4] for row in x_approx], label='k')
        plt_L, = plt.plot(T, [row[5] for row in x_approx], label='L')
        plt.legend(handles=[plt_p, plt_f, plt_g, plt_h, plt_k, plt_L])
        plt.show()
        self.assertIsInstance(X_approx, MCPIapprox)

    def test_reference(self):
        domains = (0., 1.)
        T = np.linspace(domains[0], domains[1], 100).reshape((100, 1))
        X0 = np.array([[2., .1, .1, 0., 0., 0.]])
        # X = self.mmee.reference(np.array(T).T, X0).tolist()
        X = ReferenceMEE(X0, 1.)(T).tolist()

        plt_p, = plt.plot(T, [row[0] for row in X], label='p')
        plt_e, = plt.plot(T, [row[1] for row in X], label='e')
        plt_i, = plt.plot(T, [row[2] for row in X], label='i')
        plt_W, = plt.plot(T, [row[3] for row in X], label='W')
        plt_w, = plt.plot(T, [row[4] for row in X], label='w')
        plt_f, = plt.plot(T, [row[5] for row in X], label='f')
        plt.legend(handles=[plt_p, plt_e, plt_i, plt_W, plt_w, plt_f])
        plt.show()
        self.assertEqual(X[-1][0], X0[0,0])
