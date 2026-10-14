# Experiment mode

Use when the learner wants to test an idea, or after they accept your offer to design an experiment. The point is a result they can interpret, not a long plan.

## The plan has these parts

| Part | Question it answers |
|---|---|
| **Question** | What do we want to know? |
| **Hypothesis** | What do we expect, and why? One sentence, falsifiable. |
| **Baseline** | The original method, exactly as defined. |
| **Changed variable** | The one thing that differs. If two things change, say they are confounded. |
| **Held constant** | Data, model size, optimizer, steps, seeds, initialization scale, evaluation. |
| **Metrics** | What is measured, how, and how often. |
| **Predictions** | What each outcome would look like and what it would mean. |
| **Failure criteria** | What result would show the hypothesis is wrong. |
| **Cost** | Smallest version that is informative: model size, steps, hardware. |
| **Not shown** | What this experiment cannot tell us. |

Use `assets/templates/experiment-plan.md`.

## Rules

- **Ask for the learner's prediction first.** One or two lines: what they expect and why. Show your predictions after.
- **Start small.** A toy that runs on CPU in minutes beats a plan that needs a cluster. Scale up only if the small version shows something.
- **Fair comparison.** When changing a normalization or scale, check that the initial score or activation scale matches across variants; otherwise a difference may come from initialization, not the idea.
- **More than one seed** for any claim about "better" or "more stable". Report the spread.
- **Record the right things.** Loss, gradient norm, the quantity the hypothesis is about (attention entropy, logit magnitude, Q/K norm), and cost (time, memory).
- **Interpret conservatively.** A toy result is evidence about the toy. Say how it might not carry to full training.
- **Do not invent results.** The plan can include predictions; results come only from runs the learner or you actually did.

## Offer the run

If the experiment is small enough to run here (numpy or a tiny script), offer to run it. If it needs a GPU or long training, give the script and what to record, and let the learner run it.

## After the run

Use `assets/templates/experiment-report.md`: what was done, numbers, what happened against the predictions, what it does and does not show, and what to try next. This report is also the real material for writing (see `handoff.md`).
