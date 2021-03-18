<!-- Header: Dual Nature of the Program -->
<!-- Tag: design -->
<!-- Tag: math -->
<!-- Summary: An attempt to verbosely describe the difference between program as it is -->
<!-- Summary: represented by software and as it is understood by a human. -->

This entry is devoted to the difference between two comprehensions of idea
of software program. First comprehension is the one which perceives a program
via its philosophic idea and functional structure. Second comprehension is
the engineering vision of the program which is more localized and devoted to
details. One could figuratively distinguish these perceptions as _"outer"_
and _"inner"_ correspondingly.

This distinction, which can be called topological, is caused by the way we
approach the program. Once we approach it from the outside, the program is a
black box for us. We don't know what is inside and we don't need to know it.
We are just interested in its function. On the contrary, creator of the
program perceives its function as a restriction and masters out program
internally within prescribed restriction. Let us come into more detail.

## Outer Perception

### Program as a Function

First idea which comes to mind when one would like to define a program by its
function is to interpret the program as a function:

$$
F: I \to O
$$

where \(I\) and \(O\) denotes sets of inputs and outputs correspondingly.
This interpretation only make sense in specific cases when program is supposed
to terminate in a _"finite"_ time. By finite execution time we mean programs
which are supposed to terminate independently of external actions. Examples are
compilers or some deterministic computational scripts.

There are plenty of real world programs which does not fit into this
interpretations like servers or IDEs. These programs are supposed to run
indefinitely long. In order to handle such cases we need to come up with more
versatile scheme.

### Program as a Process

Interpretation provided below consists of only those aspects of _"program
idea"_ which constitutes its perception by the outer user. What are these
aspects?

Each program is interesting to its client because of results it could provide
to him. In order to generate these results, program should be provided with
task information. Gluing entity between input information and output results
is the program state. So the program should necessary contain:

* output
* state
* input

We would like to stick to discrete conception of the program. In view of such
a conception output could be naturally interpreted as the sequence
\(o_i \cup \{o_n\}_{n=0}^\infty\) of observable states of everything which is
affected by program execution. Value of program affectee at the time moment
\(n\) is denoted by \(o_n\), initial state of affectee is denoted by \(o_i\).
Similarly state could be interpreted as the sequence
\(s_i \cup \{s_n\}_{n=0}^\infty\) where \(s_i\) stands for initial state.

In case of input we are not needed initial state so input could be interpreted
as the sequence \(\{i_n\}_{n=0}^\infty\) of states of everything which could
affect the program. All the aforementioned consideration are summed up in
the scheme:

\begin{equation}
\begin{array}{ccccc}
 & & s_i & & i_0 \\
 & & \downarrow & \swarrow & \\
o_i & & s_0 & & i_1 \\
\downarrow & \swarrow & \downarrow & \swarrow & \\
o_0 & & s_1 & & i_2 \\
\downarrow & \swarrow & \downarrow & \swarrow & \\
o_1 & & s_2 & & i_3 \\
\downarrow & \swarrow & \downarrow & \swarrow & \\
\dots & & \dots & & \dots
\end{array}
\label{eq:main_diagram}
\end{equation}

where by arrows we denote dependencies. Transition to the next row is
encapsulated in two operators \(S\) and \(O\) such that

\begin{equation}
\begin{array}{ccc}
 s_n & = & S(s_{n-1}, i_n) \\
 o_n & = & O(o_{n-1}, s_n) \\
\label{eq:operators_inro}
\end{array}
\end{equation}

for \(n > 0\). For \(n=0\) initial states should be naturally placed instead
of values with negative indices.

### Pure Setting vs Applied Setting

What we could say about values in diagram \eqref{eq:main_diagram}? Answer
depends on a setting in which we works. If we works in the setting of pure
mathematics then we could allow ourselves luxury to chose value sets among any
sets we want. In the applied setting we are bounded by architecture and its
limitations.

People develop algorithms into mathematical settings and then implement them
in applied setting of specific architecture. Let us firstly think about pure
setting. In this setting we would denote set of all values of \(o_\*\) as
\(\mathbb{O}\), set of all values of \(s_\*\) as \(\mathbb{S}\) and the set of
all values of \(i_\*\) as \(\mathbb{I}\). In light of introduced notations we
could formulate domains and codomains of operators in \eqref{eq:operators_inro}
as

\begin{equation}
\begin{array}{ccccc}
S: & \mathbb{S} \times \mathbb{I} & \to & \mathbb{S} \\
O: & \mathbb{O} \times \mathbb{S} & \to & \mathbb{O}
\label{eq:operators_pure}
\end{array}
\end{equation}

In pure setting state sets \(\mathbb{O}\), \(\mathbb{S}\) and \(\mathbb{I}\)
could be constructed via mathematical objects such as integer or real numbers.
In applied setting we are restricted by the global finiteness. Let us denote
target architecture with \(A\). Then this architecture choice leads us to
specialization of subsets \(\mathbb{O}_A \hookrightarrow \mathbb{O}\),
\(\mathbb{S}_A \hookrightarrow \mathbb{S}\) and
\(\mathbb{I}_A \hookrightarrow \mathbb{I}\). For instance, if pure sets are
described with the notion of an integer number, in approximate sets integer
number could be exchanged with 32-bit integer numbers.

With specialization of state sets we are also required to downgrade
recalculation operators \eqref{eq:operators_pure} to their specific versions

\begin{equation}
\begin{array}{ccccc}
S_A: & \mathbb{S}_A \times \mathbb{I}_A & \to & \mathbb{S}_A \\
O_A: & \mathbb{O}_A \times \mathbb{S}_A & \to & \mathbb{O}_A
\label{eq:operators_applied}
\end{array}
\end{equation}

This downgrade should naturally satisfy commutativity of the next diagrams

\begin{equation}
\require{AMScd}
\begin{CD}
\mathbb{S}_A \times \mathbb{I}_A @>S_A>> \mathbb{S}_A\\
@VVV @VVV\\
\mathbb{S} \times \mathbb{I} @>S>> \mathbb{S}
\end{CD}
\qquad
\begin{CD}
\mathbb{O}_A \times \mathbb{S}_A @>O_A>> \mathbb{O}_A\\
@VVV @VVV\\
\mathbb{O} \times \mathbb{S} @>O>> \mathbb{O}
\end{CD}
\label{eq:com_diag}
\end{equation}

Commutativity of these diagrams verifies that with specialization of the states
sets we do model pure scheme \eqref{eq:main_diagram} on a finite model.

It worth to notice that outer perception is mainly about bottom level of the
diagrams \eqref{eq:com_diag}. Pure mathematics setting is best fitted for
reflection of ideas. Inner representation deals with bottom level. It is
about details of implementations and architecture restrictions.

## Inner Perception
