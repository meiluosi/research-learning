# Verify mode

Verification is **optional and never part of a default lesson**. Use it when the user asks, or after they say yes to the one-line offer at the end of a lesson. It runs small checks on the lesson's numbers and derivations so the learner does not have to trust them.

## What to verify

Verify the claims the learner will **rely on**, not every sentence:

- **Numbers in worked examples** (softmax of [1, 2, 3], a gradient value, a table entry).
- **Derived formulas**: compare an analytic gradient or identity with a finite-difference or direct computation.
- **Qualitative claims that can be measured**: "the score variance grows with d", "the gradient first rises then falls with temperature".
- **Experiments in the lesson**: do the code snippets run, and do they print what the lesson says they will?

What code cannot verify: whether a conceptual explanation is the right one, what a paper intended, or whether a result holds at scale. List those separately as **not verified**.

## How

1. Write a short script. Prefer pure Python or numpy and small sizes; it should run on a laptop CPU in seconds. Avoid heavy dependencies.
2. Use `scripts/claimcheck.py`:

```python
from claimcheck import Checks, softmax
c = Checks("Softmax saturation")
p = softmax([10.0, 20.0, 30.0])
c.approx("weight on the largest score", got=p[2], expected=0.999955, tol=1e-6,
         claim="softmax([10,20,30]) is about [0, 0.000045, 0.999955]")
c.grad("softmax-weighted output gradient", f=loss, x=[0.0, 0.0], analytic=[0.5, -0.5])
raise SystemExit(c.report())
```

3. **Run it.** Show the result table.
4. Report in the lesson's terms: each claim, pass or fail, the value, the tolerance, and the assumptions of the check (random seed, sizes).

## Rules

- **Check what the lesson says.** Do not change a claim or a tolerance to make a check pass.
- **A failure is a finding.** Say what was wrong and what the correct value is. Small slips (a rounded table entry) and structural ones (an experiment that cannot tell two variants apart) both matter.
- **Check the experiment design, not only the numbers.** If two treatments produce identical outputs in the snippet, say so.
- **Randomness.** Fix a seed and say it. For a statistical claim, run enough samples and report the spread.
- **If you cannot run code** in this environment, say "not verified", give the script, and tell the learner how to run it.
- **Do not claim more than the check shows.** A passing numerical check supports the example; it does not prove the general statement.

## Report shape

```markdown
Checked N claims with scripts/claimcheck.py (Python 3, numpy not required).
| # | Result | Claim | Got | Expected |
...
Failures: ... (what the lesson should say)
Not verified: ... (conceptual or needs training at scale)
```
