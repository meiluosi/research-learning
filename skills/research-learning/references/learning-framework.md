# Learning framework

The spine is always: **original design, mathematical principle, design limits, improvements, experiments.** What each step contains depends on what is being learned.

## Contents
- Routing by object
- Variants of the five steps
- Lesson shape
- Stage depth

## Routing by object

If the user does not say, infer it. If it is mixed, use the main one and borrow from another for one step.

| Object | Examples | Emphasize | Watch for |
|---|---|---|---|
| Theoretical concept | Attention, softmax, KL divergence | Intuition, derivation, assumptions | Skipping the assumptions |
| Model architecture | Transformer block, RoPE, MoE | Modules, information flow, parameter and compute cost | Describing parts without the flow |
| Training algorithm | PPO, GRPO, DPO, RLVR | Objective, gradient, sampling, stability | Hiding what the gradient actually pushes |
| Systems optimization | FlashAttention, KV cache, CUDA kernels | Hardware bottleneck, memory hierarchy, cost model, measurement | Claiming speed-ups without a measurement plan |
| Research paper | A new method or result | Contribution, evidence, ablations, reproducibility, limits | Taking the abstract as the result |

## Variants of the five steps

| Step | Concept or architecture | Training algorithm | Systems optimization | Paper |
|---|---|---|---|---|
| 1 Original design | The problem and the earlier solution | The learning problem and the previous method | The workload and where time or memory goes | What problem the paper takes on and what was known |
| 2 Mathematical principle | Formula, why each term, numeric example | Objective, gradient, update; what the gradient pushes | Cost model (FLOPs, bytes moved, arithmetic intensity) | The method's formulation, in the reader's notation |
| 3 Design limits | Assumptions that break; scale and cost limits | Instability, variance, reward hacking, mismatch between objective and goal | What bounds it: bandwidth, occupancy, capacity | Threats: weak baselines, missing ablations, narrow evaluation |
| 4 Improvements | Later variants and what each fixes and costs | Variants of the objective or sampling | Other kernels, layouts, hardware | Follow-up work; what a replication would need |
| 5 Experiments | Controlled comparison on a small model | A small run that exposes the failure and the fix | A micro-benchmark with a profile | What you could reproduce cheaply; what you'd have to trust |

## Lesson shape

```
[Response to the learner's earlier answers, if any]
1. Original design
2. Mathematical principle   (intuition, then formula, then a worked example)
3. Design limits
4. Improvements
5. Experiments              (sketch)
Key claims and status      (table)
Two questions              (principle, research)
One-line offer             (verify or experiment, once)
```

## Stage depth

- **Quick:** steps 1, 2 (intuition and the main formula only), the main limit. No experiment section. About 400 words or 800 Chinese characters.
- **Standard:** all five steps, compact. About 1,200 to 2,000 words, or 3,000 to 5,000 Chinese characters.
- **Deep:** one step per round. After each, wait for the learner's reaction or answer before going on. Include the derivation, a runnable snippet, and critical analysis.

### Standard budget (in Chinese characters; scale for English at about 1 word per 2.5 characters)

| Part | Budget |
|---|---|
| Assumptions line | 100 |
| 1 Original design | 400 |
| 2 Mathematical principle (one derivation, one worked example, at most one table) | 1,500 |
| 3 Design limits | 600 |
| 4 Improvements (a table, one line each) | 600 |
| 5 Experiments (three bullets and a prediction prompt) | 400 |
| Claims table | 400 |
| Two questions and the offer | 300 |

### Length check before sending

Estimate the length of the reply. If a Standard lesson is past about 5,000 Chinese characters (2,000 words), cut: keep only the most important derivation, put the rest into "next round", merge limits into a short list, and shorten the experiment sketch. Say what was left for the next round in one line. Longer lessons are for Deep mode, delivered in rounds. A shorter lesson the learner can follow beats a complete one they cannot.
