import io
import unittest

from claimcheck import Checks, softmax


def run(c):
    buf = io.StringIO()
    rc = c.report(buf)
    return rc, buf.getvalue()


class ClaimCheck(unittest.TestCase):
    def test_passing_checks_return_zero(self):
        c = Checks("demo")
        c.approx("a", 1.0, 1.0005, tol=1e-3)
        c.true("b", True)
        c.less("c", 1, 2)
        c.monotonic("d", [1, 2, 2, 3])
        rc, text = run(c)
        self.assertEqual(rc, 0)
        self.assertIn("4 of 4 checks passed", text)

    def test_failure_is_reported_and_returns_one(self):
        c = Checks()
        c.approx("wrong value", 0.009, 0.0099, tol=1e-4, claim="a(1-a) at 0.99 is 0.009")
        rc, text = run(c)
        self.assertEqual(rc, 1)
        self.assertIn("FAIL", text)
        self.assertIn("Failed: wrong value", text)

    def test_relative_tolerance(self):
        c = Checks()
        self.assertTrue(c.approx("big", 1000.0, 1001.0, rel=2e-3))
        self.assertFalse(c.approx("big2", 1000.0, 1100.0, rel=2e-3))

    def test_grad_matches_finite_difference(self):
        c = Checks()
        ok = c.grad("quadratic", f=lambda x: x[0] ** 2 + 3 * x[1], x=[2.0, 5.0], analytic=[4.0, 3.0])
        self.assertTrue(ok)
        bad = c.grad("wrong gradient", f=lambda x: x[0] ** 2, x=[2.0], analytic=[5.0])
        self.assertFalse(bad)

    def test_monotonic_detects_a_turn(self):
        c = Checks()
        self.assertFalse(c.monotonic("rises then falls", [1, 3, 2]))
        self.assertTrue(c.monotonic("falls", [3, 2, 1], increasing=False))

    def test_softmax_helper(self):
        p = softmax([1.0, 2.0, 3.0])
        self.assertAlmostEqual(sum(p), 1.0)
        self.assertAlmostEqual(p[2], 0.665, places=3)


if __name__ == "__main__":
    unittest.main()
