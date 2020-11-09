import unittest
from dnplab import dnpdata
from numpy.testing import assert_array_equal
import dnplab.dnpImport as wrapper
import dnplab.dnpNMR as nmr
import dnplab.dnpFit as efit
import dnplab as dnp
import numpy as np
import os


class dnpFit_tester(unittest.TestCase):
    def setUp(self):
        path = os.path.join(".", "data", "topspin", "304")
        self.data = wrapper.load(path, data_type="topspin")
        self.ws = dnp.create_workspace()
        self.ws["raw"] = self.data
        self.ws.copy("raw", "proc")

    def test_fit_functions(self):
        self.ws = nmr.remove_offset(self.ws)
        self.ws = nmr.window(
            self.ws, type="lorentz_gauss", linewidth=5, gauss_linewidth=10
        )
        self.ws = nmr.fourier_transform(self.ws, zero_fill_factor=2)
        self.ws = nmr.autophase(self.ws, method="search", order="zero")
        self.ws = nmr.baseline(self.ws, type="poly", order=2, reference_slice=None)
        self.ws = nmr.integrate(
            self.ws, dim="t2", integrate_center=0, integrate_width=50
        )
        efit.exponentialFit(self.ws, type="T1")
        self.assertEqual(self.ws["fit"].attrs["T1"], 2.620063458731661)

        efit.exponentialFit(self.ws, type="T2")
        self.assertEqual(self.ws["fit"].attrs["T2"], 1.0682212598985381)

        efit.exponentialFit(self.ws, type="T2", stretched=True)
        self.assertEqual(self.ws["fit"].attrs["T2"], 0.8938213879865939)

        efit.exponentialFit(self.ws, type="mono")
        self.assertEqual(self.ws["fit"].attrs["tau"], 2.620074855961468)

        efit.exponentialFit(self.ws, type="bi")
        self.assertEqual(self.ws["fit"].attrs["tau1"], 1.9438613863808594)
        self.assertEqual(self.ws["fit"].attrs["tau2"], -64860.88976717187)