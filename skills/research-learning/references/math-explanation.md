# Explaining math

## Order

1. **Purpose in plain words.** What is this formula trying to do?
2. **A tiny concrete case** with numbers small enough to follow by hand.
3. **The formula**, built piece by piece. Say what each symbol is and why it is there.
4. **Behavior.** What happens at the extremes, and how does it change with size (dimension, sequence length)?
5. **The result in a sentence**, with its conditions.

Do not open with the general formula and then explain it backwards.

## Derivations

- Show the steps that carry the idea; skip routine algebra but say it was skipped.
- Name the assumptions before using them (independence, zero mean, unit variance, small perturbation, fixed temperature).
- After a derivation, say **how far it reaches**. A result under idealized assumptions explains a design motive; it does not guarantee real behavior.
- If two derivations look equivalent, say when they stop being equivalent (for example when a learned scale or an epsilon enters).

## Worked examples

- Use numbers a reader can check: [1, 2, 3], two tokens with values 1 and 3, a 2-dimensional vector.
- Show the intermediate numbers, not only the result.
- Prefer one example that exposes the idea over several that repeat it.
- Where a table of values helps (a gradient at several scales), give it; it is easier to trust than a sentence.

## Gradients

- State what the gradient pushes toward, not only its formula.
- Name every path the gradient takes. A small gradient on one path does not mean learning stops; say which others remain.
- For normalization and saturation, show how the gradient changes with the value.

## Notation

Use the standard notation of the field. Define a symbol at first use. Keep one symbol for one meaning inside a lesson.

## Honesty in math

- Give approximate numbers as approximate ("about 0.665"), exact ones as exact.
- Do not round a value in a table in a way that changes a conclusion.
- If a number matters to the argument, it is a good candidate for verify mode.
