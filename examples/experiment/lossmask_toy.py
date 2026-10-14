"""Toy loss-mask experiment, numpy only, CPU, a few minutes.

Loss = (sum_answer_tokens nll + lam * sum_prompt_tokens nll) / n_answer_tokens
  lam = 0    -> loss mask (answer only)           [baseline]
  lam = 1    -> loss on all tokens (same per-answer-token weight as baseline)
  0<lam<1    -> in between (dose-response)
Dividing by the number of ANSWER tokens in every arm keeps the answer-token
gradient scale identical, so lam is the ONLY changed variable.

Task: prompt = P random tokens (unpredictable, entropy log V per token).
      answer_j = (prompt[a_j] + prompt[b_j]) mod V  (needs capacity to learn).
Model: tiny MLP language model over (all earlier tokens, position), manual backprop.
Run:   python3 lossmask_toy.py            (full: 2 data sizes x 4 lam x 5 seeds, about 15 min on a laptop CPU)
       python3 lossmask_toy.py --quick    (smoke test)
"""
import sys, time
import numpy as np

V, P, A, D, H = 8, 8, 3, 8, 64     # vocab, prompt len, answer len, emb dim, hidden
T = P + A
PAIRS = [(0, 3), (1, 5), (2, 7)]    # which prompt positions feed answer j

def make_data(n, rng):
    pr = rng.integers(0, V, size=(n, P))
    ans = np.stack([(pr[:, a] + pr[:, b]) % V for a, b in PAIRS], 1)
    return np.concatenate([pr, ans], 1)

class Model:
    def __init__(self, rng):
        s = 0.1
        self.E = rng.normal(0, s, (V, D))
        self.W1 = rng.normal(0, 1 / np.sqrt(T * D + T), (T * D + T, H))
        self.b1 = np.zeros(H)
        self.W2 = rng.normal(0, 1 / np.sqrt(H), (H, V))
        self.b2 = np.zeros(V)
        self.params = ["E", "W1", "b1", "W2", "b2"]
        self.m = {k: np.zeros_like(getattr(self, k)) for k in self.params}
        self.v = {k: np.zeros_like(getattr(self, k)) for k in self.params}
        self.t = 0
        # causal mask: position t sees tokens s < t
        self.mask = (np.arange(T)[None, :] < np.arange(T)[:, None]).astype(float)  # (t, s)

    def forward(self, X):
        B = X.shape[0]
        emb = self.E[X]                                              # (B,T,D)
        ctx = emb[:, None, :, :] * self.mask[None, :, :, None]       # (B,t,s,D)
        U = np.concatenate([ctx.reshape(B, T, T * D),
                            np.broadcast_to(np.eye(T), (B, T, T))], 2)
        h = np.tanh(U @ self.W1 + self.b1)
        logits = h @ self.W2 + self.b2
        logits -= logits.max(-1, keepdims=True)
        p = np.exp(logits); p /= p.sum(-1, keepdims=True)
        return U, h, p

    def nll(self, X):
        _, _, p = self.forward(X)
        return -np.log(np.take_along_axis(p, X[..., None], 2)[..., 0] + 1e-12)  # (B,T)

    def step(self, X, lam, lr):
        B = X.shape[0]
        U, h, p = self.forward(X)
        w = np.where(np.arange(T) >= P, 1.0, lam)                   # per-position weight
        dl = p.copy()
        np.put_along_axis(dl, X[..., None], np.take_along_axis(dl, X[..., None], 2) - 1, 2)
        dl *= (w[None, :, None] / (A * B))
        g = {}
        g["W2"] = h.reshape(-1,H).T @ dl.reshape(-1,V); g["b2"] = dl.sum((0, 1))
        dh = dl @ self.W2.T
        dpre = dh * (1 - h ** 2)
        g["W1"] = U.reshape(-1,U.shape[-1]).T @ dpre.reshape(-1,H); g["b1"] = dpre.sum((0, 1))
        dU = (dpre @ self.W1.T)[:, :, :T * D].reshape(B, T, T, D) * self.mask[None, :, :, None]
        dE_pos = dU.sum(1)                                           # (B,s,D)
        g["E"] = np.zeros_like(self.E); np.add.at(g["E"], X, dE_pos)
        self.t += 1
        for k in self.params:
            self.m[k] = 0.9 * self.m[k] + 0.1 * g[k]
            self.v[k] = 0.999 * self.v[k] + 0.001 * g[k] ** 2
            mh = self.m[k] / (1 - 0.9 ** self.t); vh = self.v[k] / (1 - 0.999 ** self.t)
            setattr(self, k, getattr(self, k) - lr * mh / (np.sqrt(vh) + 1e-8))

def run(lam, seed, n_train, steps, bs=64, lr=3e-3):
    rng = np.random.default_rng(seed)
    Xtr, Xva = make_data(n_train, rng), make_data(2000, np.random.default_rng(999))  # same val set
    m = Model(np.random.default_rng(seed + 1000)); brng = np.random.default_rng(seed + 2000)
    hit = None
    for s in range(1, steps + 1):
        m.step(Xtr[brng.integers(0, n_train, bs)], lam, lr)
        if s % 250 == 0 or s == steps:
            pv = m.nll(Xva)
            acc = np.mean(np.argmax(m.forward(Xva)[2], -1)[:, P:] == Xva[:, P:])
            if hit is None and acc >= 0.9: hit = s
    ptr, ntr = m.nll(Xtr), m.nll(Xva)
    return dict(val_ans_nll=ntr[:, P:].mean(), val_ans_acc=acc, train_ans_nll=ptr[:, P:].mean(),
                val_prompt_nll=ntr[:, :P].mean(), train_prompt_nll=ptr[:, :P].mean(), steps_to_90=hit)

if __name__ == "__main__":
    quick = "--quick" in sys.argv
    seeds = [0, 1] if quick else [0, 1, 2, 3, 4]
    steps = 600 if quick else 6000
    lams = [0.0, 0.1, 0.3, 1.0]
    print(f"floor for prompt NLL = log V = {np.log(V):.3f}; chance answer acc = {1/V:.3f}")
    for n_train in ([500] if quick else [500, 5000]):
        print(f"\n=== n_train = {n_train}, steps = {steps}, seeds = {seeds}")
        print("lam | val_ans_acc (mean±sd) | val_ans_nll | train_ans_nll | val_prompt_nll | train_prompt_nll | steps_to_90%")
        for lam in lams:
            t0 = time.time()
            r = [run(lam, s, n_train, steps) for s in seeds]
            f = lambda k: np.array([x[k] for x in r], float)
            h = f("steps_to_90")
            print(f"{lam:3.1f} | {f('val_ans_acc').mean():.3f}±{f('val_ans_acc').std():.3f} | "
                  f"{f('val_ans_nll').mean():.3f} | {f('train_ans_nll').mean():.3f} | "
                  f"{f('val_prompt_nll').mean():.3f} | {f('train_prompt_nll').mean():.3f} | "
                  f"{np.nanmean(h) if np.isfinite(h).any() else float('nan'):.0f} "
                  f"({int(np.isfinite(h).sum())}/{len(h)} reached)  [{time.time()-t0:.0f}s]", flush=True)
