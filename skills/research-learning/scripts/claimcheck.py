"""claimcheck: check the numeric and derivable claims in a lesson by running them.

Write a small script, import this module, state each claim next to the value your code
computes, and print the report. Pure standard library; use numpy in your own script if you
like. Exit code 1 when any claim fails, so a failure cannot be missed.

    from claimcheck import Checks
    c = Checks("Softmax lesson")
    c.approx("softmax weight of the largest score", got=0.665, expected=0.6652, tol=1e-3,
             claim="softmax([1,2,3]) is about [0.09, 0.245, 0.665]")
    c.true("weights sum to 1", abs(sum([0.09, 0.245, 0.665]) - 1) < 1e-3)
    c.grad("d(x^2)/dx = 2x", f=lambda x: x[0] ** 2, x=[3.0], analytic=[6.0])
    raise SystemExit(c.report())

Rules that keep the checks honest:
- Check what the lesson says. Never change a claim or a tolerance to make it pass.
- A failing check is a result. Report it; do not hide it.
- State assumptions in `note=` (for example "random inputs, seed 0").
"""
import math
import sys


class Checks:
    def __init__(self, title=""):
        self.title = title
        self.rows = []

    # -- recording -----------------------------------------------------------------
    def _add(self, name, ok, got, expected, claim, note):
        self.rows.append({"name": name, "ok": bool(ok), "got": got, "expected": expected, "claim": claim or "", "note": note or ""})
        return bool(ok)

    def approx(self, name, got, expected, tol=1e-6, rel=None, claim=None, note=None):
        """Pass when |got - expected| <= tol, or when the relative error is <= rel if rel is given."""
        diff = abs(got - expected)
        ok = diff <= tol if rel is None else diff <= rel * max(abs(expected), 1e-300)
        return self._add(name, ok, got, expected, claim, note)

    def true(self, name, condition, claim=None, note=None):
        return self._add(name, condition, condition, True, claim, note)

    def less(self, name, a, b, claim=None, note=None):
        return self._add(name, a < b, a, f"< {b}", claim, note)

    def monotonic(self, name, values, increasing=True, claim=None, note=None):
        pairs = list(zip(values, values[1:]))
        ok = all(b >= a for a, b in pairs) if increasing else all(b <= a for a, b in pairs)
        return self._add(name, ok, [round(v, 6) for v in values], "increasing" if increasing else "decreasing", claim, note)

    def grad(self, name, f, x, analytic, h=1e-6, tol=1e-5, claim=None, note=None):
        """Compare an analytic gradient with central finite differences. f takes a list and returns a float."""
        numeric = []
        for i in range(len(x)):
            hi = list(x); lo = list(x)
            hi[i] += h; lo[i] -= h
            numeric.append((f(hi) - f(lo)) / (2 * h))
        err = max(abs(a - b) for a, b in zip(analytic, numeric))
        return self._add(name, err <= tol, [round(v, 8) for v in analytic], [round(v, 8) for v in numeric], claim,
                         (note + "; " if note else "") + f"max abs error {err:.2e}")

    # -- reporting -----------------------------------------------------------------
    def report(self, stream=None):
        out = stream or sys.stdout
        title = f" for {self.title}" if self.title else ""
        print(f"Claim checks{title}", file=out)
        print("| # | Result | Check | Got | Expected | Note |", file=out)
        print("|---|---|---|---|---|---|", file=out)
        for i, r in enumerate(self.rows, 1):
            mark = "PASS" if r["ok"] else "FAIL"
            note = r["note"] or (r["claim"] if r["claim"] else "")
            print(f"| {i} | {mark} | {r['name']} | {_fmt(r['got'])} | {_fmt(r['expected'])} | {note} |", file=out)
        failed = [r for r in self.rows if not r["ok"]]
        print(f"\n{len(self.rows) - len(failed)} of {len(self.rows)} checks passed.", file=out)
        if failed:
            print("Failed: " + "; ".join(r["name"] for r in failed), file=out)
        return 1 if failed else 0


def _fmt(v):
    if isinstance(v, float):
        return f"{v:.6g}"
    return str(v)


def softmax(xs):
    """Small helper so simple lessons need no numpy."""
    m = max(xs)
    es = [math.exp(x - m) for x in xs]
    z = sum(es)
    return [e / z for e in es]
