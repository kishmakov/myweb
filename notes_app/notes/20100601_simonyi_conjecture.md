<!-- Header: Simonyi Conjecture -->
<!-- Tag: math -->
<!-- Summary: Attractive short formulation of an open combinatorics problem. -->

Gabor Simonyi, while he was working on some omnidirectional codes, formulated
the following conjecture.

Let \(X = \{1, 2, \dots, n\}\) be a set of \(n\) elements.
Let \(\mathcal{A, B} \subset 2^X\) be such a collections of subsets of $X$
that \(\forall A_1, A_2 \in \mathcal{A}\) and \(\forall B_1, B_2 \in \mathcal{B}\)
next two conditions are satisfied:

$$A_1 \cup B_1 = A_2 \cup B_2 \Rightarrow A_1 = A_2$$
$$A_1 \cap B_1 = A_2 \cap B_2 \Rightarrow B_1 = B_2$$

Then the product of cardinalities of \(\mathcal{A}\) and \(\mathcal{B}\)
is bounded:

$$|\mathcal{A}||\mathcal{B}| \leqslant 2^n$$

It is known that this estimate is sharp. One could construct a family of
examples which satisfies inequality. Let \(Y \subset X\) be an arbitrary
subset of \(X\) then we suppose \(\mathcal{B}\) to be the set of all
subsets of \(Y\) and \(\mathcal{A}\) to be the set of all supsets of \(Y\).

Holzman and Korner proved estimate of the form \(\theta^n\) for
\(\theta \approx 2.3264\) in [their paper](http://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.105.4613&rep=rep1&type=pdf).
In this proof authors don't use assumptions fully.
