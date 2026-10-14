# Claim status

Learners tend to trust everything in a lesson equally. Mark the **key claims** (4 to 8 per lesson, not every sentence) with where they come from.

## The five statuses

| Status | Meaning | Example |
|---|---|---|
| **Paper** | Stated or shown by a source you were given or fetched | "The original Transformer paper says unscaled dot products can push softmax into regions with tiny gradients." |
| **Derived** | Follows from the math shown in this lesson, under stated assumptions | "If q and k have independent unit-variance entries, Var(q·k) = d." |
| **Checked** | Run in code in this session, with the result shown. Use it only after the user asked for verification; otherwise a computable number is "Derived". | "softmax([10,20,30]) puts 0.999955 on the last entry (checked)." |
| **Conjecture** | Plausible but not shown | "This head probably learns positional patterns." |
| **Untested** | A question an experiment could answer | "Whether a learned temperature helps at scale." |

## Rules

- **When unsure, downgrade.** If you recall a result but have not seen the source, it is a conjecture or "from memory, not checked", not "Paper".
- **State assumptions with every Derived claim.** A derivation under independence and unit variance explains the original design's motive; it does not prove real layers behave that way. Say so.
- **Do not turn an experiment into a fact.** A toy run under random initialization shows what happens there, not that a design is better in full training.
- **Separate "what the paper claims" from "what the paper shows".** Abstracts claim; sections and tables show.
- **Citations.** Give a link or a precise reference only for sources you fetched or were given. For anything else write "from memory, not checked".

## Where to put the labels

Inline for the conclusion that matters ("... (derived, assuming independent entries)"), and a short table at the end:

```markdown
| Claim | Status | Basis |
|---|---|---|
| Scaling by 1/sqrt(d) keeps score variance near 1 | Derived | Independent unit-variance entries |
| Without scaling, softmax saturates as d grows | Checked | Ran d = 16 to 1024 |
| Sigmoid attention matches softmax when normalized | Paper | arXiv 2409.04431 abstract |
| A learned temperature may be unstable | Conjecture | Not tested |
```
