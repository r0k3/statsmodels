import numpy.testing as npt
import numpy as np
from scikits.statsmodels.regression.censored_model import Tobit
from scikits.statsmodels.datasets.fair import load as load_fair
import scikits.statsmodels.api as sm

class CheckTobit(object):

    decimal_params = 4
    def test_params(self):
        npt.assert_almost_equal(self.res1.params, self.res2.params,
                self.decimal_params)

    decimal_bse = 4
    def test_bse(self):
        npt.assert_almost_equal(self.res1.bse, self.res2.bse,
                self.decimal_bse)

    decimal_cov_params = 4
    def test_cov_params(self):
        npt.assert_almost_equal(self.res1.cov_params(),
                self.res2.cov_params, self.decimal_cov_params)

    def test_loglike(self):
        npt.assert_almost_equal(self.res1.llf, self.res2.llf, 4)

    def test_loglike_null(self):
        npt.assert_almost_equal(self.res1.llnull, self.res2.llnull, 4)

    def test_n_lcens(self):
        npt.assert_equal(self.res1.n_lcens, self.res2.n_lcens)

    def test_n_rcens(self):
        npt.assert_equal(self.res1.n_rcens, self.res2.n_rcens)

    def test_n_ucens(self):
        npt.assert_equal(self.res1.n_ucens, self.res2.n_ucens)

    def test_chi2(self):
        npt.assert_almost_equal(self.res1.chi2, self.res2.chi2, 4)

    def test_df_model(self):
        npt.assert_equal(self.res1.df_model, self.res2.df_model)

    def test_df_resid(self):
        npt.assert_equal(self.res1.df_resid, self.res2.df_resid)

    decimal_xb = 4
    def test_predict_xb(self):
        npt.assert_almost_equal(self.res1.predict(), self.res2.predict_xb, 
                                self.decimal_xb)

    decimal_e = 4
    def test_predict_e(self):
        npt.assert_almost_equal(self.res1.predict(typ='e(-inf,inf)'),
                                self.res2.predict_e, self.decimal_e)
        npt.assert_almost_equal(self.res1.predict(typ='e(0,inf)'),
                                self.res2.predict_ea, self.decimal_e)
        npt.assert_almost_equal(self.res1.predict(typ='e(-inf,2)'),
                                self.res2.predict_eb, self.decimal_e)
        npt.assert_almost_equal(self.res1.predict(typ='e(0,2)'),
                                self.res2.predict_eab, self.decimal_e)
        npt.assert_almost_equal(self.res1.predict(typ='e(1,inf)'),                                self.res2.predict_ea1, self.decimal_e)

    decimal_ystar = 4
    def test_predict_ystar(self):
        npt.assert_almost_equal(self.res1.predict(typ='ystar(-inf,inf)'),
                                self.res2.predict_ystar, self.decimal_ystar)
        npt.assert_almost_equal(self.res1.predict(typ='ystar(0,inf)'),
                                self.res2.predict_ystara, self.decimal_ystar)
        npt.assert_almost_equal(self.res1.predict(typ='ystar(-inf,2)'),
                                self.res2.predict_ystarb, self.decimal_ystar)
        npt.assert_almost_equal(self.res1.predict(typ='ystar(0,2)'),
                                self.res2.predict_ystarab, self.decimal_ystar)
        npt.assert_almost_equal(self.res1.predict(typ='ystar(1,inf)'),
                                self.res2.predict_ystara1, self.decimal_ystar)

    decimal_pr = 4
    def test_predict_pr(self):
        npt.assert_almost_equal(self.res1.predict(typ='pr(-inf,inf)'),
                                self.res2.predict_pr, self.decimal_pr)
        npt.assert_almost_equal(self.res1.predict(typ='pr(0,inf)'),
                                self.res2.predict_pra, self.decimal_pr)
        npt.assert_almost_equal(self.res1.predict(typ='pr(-inf,2)'),
                                self.res2.predict_prb, self.decimal_pr)
        npt.assert_almost_equal(self.res1.predict(typ='pr(0,2)'),
                                self.res2.predict_prab, self.decimal_pr)
        npt.assert_almost_equal(self.res1.predict(typ='pr(1,inf)'),
                                self.res2.predict_pra1, self.decimal_pr)

class TestTobit(CheckTobit):
    """
    Test left-censored Tobit
    """
    @classmethod
    def setupClass(cls):
        data = load_fair()
        data.exog = sm.add_constant(data.exog)
        cls.res1 = Tobit(data.endog, data.exog, left=0).fit(disp=0)
        cls.decimal_bse = 3
        cls.decimal_cov_params = 3
        cls.attach_results()

    @classmethod
    def attach_results(cls):
        from results.tobit_left import results
        cls.res2 = results

#class TestTobitNM(TestTobit):
#    @classmethod
#    def setupClass(cls):
#        data = load_fair()
#        data.exog = sm.add_constant(data.exog)
#        cls.res1 = Tobit(data.endog, data.exog, left=0).fit(method='nm',
#                disp=0)
#        cls.attach_results()

class TestTobitBFGS(TestTobit):
    @classmethod
    def setupClass(cls):
        data = load_fair()
        data.exog = sm.add_constant(data.exog)
        cls.res1 = Tobit(data.endog, data.exog, left=0).fit(method='bfgs',
                disp=0)
        cls.predict_xb = 3
        cls.decimal_bse = 3
        cls.decimal_cov_params = 3
        cls.attach_results()

class TestTobitPowell(TestTobit):
    @classmethod
    def setupClass(cls):
        data = load_fair()
        data.exog = sm.add_constant(data.exog)
        cls.res1 = Tobit(data.endog, data.exog, left=0).fit(method='powell',
                disp=0, ftol=1e-9)
        cls.decimal_cov_params = 3
        cls.attach_results()


class TestTobitCG(TestTobit):
    @classmethod
    def setupClass(cls):
        data = load_fair()
        data.exog = sm.add_constant(data.exog)
        cls.res1 = Tobit(data.endog, data.exog, left=0).fit(method='cg',
                disp=0, maxiter=1000)
        cls.decimal_bse = 3
        cls.decimal_params = 3
        cls.decimal_xb = 3
        cls.decimal_cov_params = 3
        cls.decimal_e = 3
        cls.decimal_ystar = 3
        cls.decimal_pr = 3
        cls.attach_results()


class TestTobitNCG(TestTobit):
    @classmethod
    def setupClass(cls):
        data = load_fair()
        data.exog = sm.add_constant(data.exog)
        cls.res1 = Tobit(data.endog, data.exog, left=0).fit(method='ncg',
                disp=0)
        cls.decimal_params = 3
        cls.decimal_cov_params = 3
        cls.attach_results()

class TobitRight(TestTobit):
    @classmethod
    def setupClass(cls):
        data = load_fair()
        data.exog = sm.add_constant(data.exog)
        cls.res1 = Tobit(data.endog, data.exog, right=2).fit(disp=0)
        cls.attach_results()

    @classmethod
    def attach_results(cls):
        from results.tobit_right import results
        cls.res2 = results

#class TobitRightNM(TobitRight):
#    @classmethod
#    def setupClass(cls):
#        data = load_fair()
#        data.exog = sm.add_constant(data.exog)
#        cls.res1 = Tobit(data.endog, data.exog, right=2).fit(method='nm',
#                disp=0)
#        cls.attach_results()

class TobitRightBFGS(TobitRight):
    @classmethod
    def setupClass(cls):
        data = load_fair()
        data.exog = sm.add_constant(data.exog)
        cls.res1 = Tobit(data.endog, data.exog, left=False,
                right=2).fit(method='bfgs', disp=0)
        cls.attach_results()

class TobitRightPowell(TobitRight):
    @classmethod
    def setupClass(cls):
        data = load_fair()
        data.exog = sm.add_constant(data.exog)
        cls.res1 = Tobit(data.endog, data.exog, left=False,
                right=2).fit(method='powell', disp=0)
        cls.attach_results()

class TobitRightCG(TobitRight):
    @classmethod
    def setupClass(cls):
        data = load_fair()
        data.exog = sm.add_constant(data.exog)
        cls.res1 = Tobit(data.endog, data.exog, left=False,
                right=2).fit(method='cg', disp=0)
        cls.attach_results()

class TobitRightNCG(TobitRight):
    @classmethod
    def setupClass(cls):
        data = load_fair()
        data.exog = sm.add_constant(data.exog)
        cls.res1 = Tobit(data.endog, data.exog, left=False,
                right=2).fit(method='ncg', disp=0)
        cls.attach_results()

class TobitBoth(TestTobit):
    @classmethod
    def setupClass(cls):
        data = load_fair()
        data.exog = sm.add_constant(data.exog)
        cls.res1 = Tobit(data.endog, data.exog, left=0,
                    right=2).fit(method='nm', disp=0)
        cls.attach_results()

    @classmethod
    def attach_results(cls):
        from results.tobit_both import results
        cls.res2 = results

#class TobitBothNM(TobitBoth):
#    @classmethod
#    def setupClass(cls):
#        data = load_fair()
#        data.exog = sm.add_constant(data.exog)
#        cls.res1 = Tobit(data.endog, data.exog, left=0,
#                        right=2).fit(method='nm', disp=0)
#        cls.attach_results()

class TobitBothBFGS(TobitBoth):
    @classmethod
    def setupClass(cls):
        data = load_fair()
        data.exog = sm.add_constant(data.exog)
        cls.res1 = Tobit(data.endog, data.exog, left=0,
                        right=2).fit(method='bfgs', disp=0)
        cls.attach_results()

class TobitBothPowell(TobitBoth):
    @classmethod
    def setupClass(cls):
        data = load_fair()
        data.exog = sm.add_constant(data.exog)
        cls.res1 = Tobit(data.endog, data.exog, left=0,
                        right=2).fit(method='powell', disp=0)
        cls.attach_results()

class TobitBothCG(TobitBoth):
    @classmethod
    def setupClass(cls):
        data = load_fair()
        data.exog = sm.add_constant(data.exog)
        cls.res1 = Tobit(data.endog, data.exog, left=0,
                            right=2).fit(method='cg', disp=0)
        cls.attach_results()

class TobitBothNCG(TobitBoth):
    @classmethod
    def setupClass(cls):
        data = load_fair()
        data.exog = sm.add_constant(data.exog)
        cls.res1 = Tobit(data.endog, data.exog, left=0,
                            right=2).fit(method='ncg', disp=0)
        cls.attach_results()