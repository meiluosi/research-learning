import sys, math
import os; sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "skills", "research-learning", "scripts"))
import numpy as np
from claimcheck import Checks, softmax

c = Checks("excerpt: softmax / attention numbers")

# 1
p = softmax([1.0, 2.0, 3.0])
for i, e in enumerate([0.09, 0.245, 0.665]):
    c.approx(f"1. softmax([1,2,3])[{i}]", p[i], e, tol=5e-4, claim="about [0.09,0.245,0.665]")

# 2
p = softmax([10.0, 20.0, 30.0])
c.approx("2. softmax([10,20,30])[2]", p[2], 0.999955, tol=5e-7)
c.less("2. softmax([10,20,30])[0] ~ 0", p[0], 1e-8, note=f"actual {p[0]:.3e}")

# 3
sig = lambda x: 1 / (1 + math.exp(-x))
c.approx("3. sigmoid(2)", sig(2), 0.881, tol=5e-4)

# 4 derivative a(1-a)
table = {0.1: 0.09, 0.3: 0.21, 0.5: 0.25, 0.9: 0.09, 0.99: 0.009, 0.999: 0.000999}
for a, claimed in table.items():
    c.approx(f"4. a(1-a) at a={a}", a * (1 - a), claimed, tol=0.0005 * claimed + 1e-12 if False else 1e-6 + 0.005 * claimed,
             note=f"claimed {claimed}, exact {a*(1-a):.6g}")
# check that the formula itself is the softmax diagonal derivative
s = np.array([0.3, -1.2, 2.0]); h = 1e-6
def sm(x): e = np.exp(x - x.max()); return e / e.sum()
a = sm(s)
num = [(sm(s + h*np.eye(3)[i])[i] - sm(s - h*np.eye(3)[i])[i]) / (2*h) for i in range(3)]
c.true("4. d a_i/d s_i = a_i(1-a_i) (finite diff)", np.allclose(num, a*(1-a), atol=1e-8))

# 5
v = np.array([1.0, 3.0]); y = 3.0
def L(s):
    a = sm(np.array(s)); o = a @ v; return 0.5 * (o - y) ** 2
def analytic(s):
    a = sm(np.array(s)); o = a @ v; g = o - y; return list(a * g * (v - o))
c.grad("5. dL/ds at s=[0,0]", L, [0.0, 0.0], analytic([0, 0]), note="expected [0.5,-0.5]")
c.approx("5. dL/ds_1 at s=[0,0]", analytic([0, 0])[0], 0.5, tol=1e-9)
c.approx("5. dL/ds_2 at s=[0,0]", analytic([0, 0])[1], -0.5, tol=1e-9)
c.grad("5. formula at s=[10,0]", L, [10.0, 0.0], analytic([10, 0]), tol=1e-7)
g10 = analytic([10, 0])
c.approx("5. dL/ds_1 at s=[10,0]", g10[0], 0.00018, tol=5e-6, note=f"exact {g10[0]:.6e}")
c.approx("5. dL/ds_2 at s=[10,0]", g10[1], -0.00018, tol=5e-6, note=f"exact {g10[1]:.6e}")

# 6
rng = np.random.default_rng(0)
for d in (16, 64, 256):
    q = rng.standard_normal((200000, d)); k = rng.standard_normal((200000, d))
    dot = (q * k).sum(1)
    c.approx(f"6. Var(q.k), d={d}", dot.var(), d, rel=0.02, note="200k samples, seed 0, 2% rel tol")
    c.approx(f"6. Var(q.k/sqrt d), d={d}", (dot/np.sqrt(d)).var(), 1.0, rel=0.02, note="200k samples, seed 0")

# 7 + 8
def l2n(x): return x / np.linalg.norm(x, axis=-1, keepdims=True)
def rms(x): return x / np.sqrt((x**2).mean(-1, keepdims=True))
d, n = 64, 128
Q = rng.standard_normal((n, d)); K = rng.standard_normal((n, d))
for scale in (1, 10, 100):
    Qs, Ks = Q*scale, K*scale
    C = np.sqrt(d) * l2n(Qs) @ l2n(Ks).T
    D = rms(Qs) @ rms(Ks).T / np.sqrt(d)
    c.true(f"7. C == D elementwise, scale x{scale}", np.allclose(C, D, atol=1e-9), note=f"max|C-D|={np.abs(C-D).max():.2e}")
    c.true(f"8. std(C) == std(D), scale x{scale}", abs(C.std()-D.std()) < 1e-9, note=f"std C={C.std():.6f}, std D={D.std():.6f}")
C1 = np.sqrt(d) * l2n(Q) @ l2n(K).T
C100 = np.sqrt(d) * l2n(Q*100) @ l2n(K*100).T
c.true("8. C is scale invariant (x1 vs x100)", np.allclose(C1, C100, atol=1e-9))
# contrast: plain scaled dot product DOES change
S1 = Q @ K.T / np.sqrt(d); S100 = (Q*100) @ (K*100).T / np.sqrt(d)
print("plain QK^T/sqrt(d) std at x1, x100:", S1.std(), S100.std())
raise SystemExit(c.report())
