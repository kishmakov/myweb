<!-- Header: Lucky Tickets -->
<!-- Tag: math -->
<!-- Summary: Computation of the probability of getting a "lucky ticket". -->

In the public transit of Saint Petersburg each passenger is provided a paper
ticket once he bought a ride. These tickets are numbered with 6 digits where
leading zeros are possible (like `010107`). Some of the tickets are considered
lucky. There are two definitions of lucky tickets.

First one is the most popular: the ticket called lucky if the sum of first
three digits equals to the sum of the last three digits.

It is not very many of such tickets: there are only 55252 of them
or **5.5%** of total number.

Probability of getting such a number is quite small. So for those people,
who both want to feel themselves lucky and to exercise their mind, there
is a second definition. It states that the ticket is lucky if it is possible
to put signs of basic arithmetics operations and some brackets to prescribe
the order of computations so that result is __one hundred__. It is possible to put
unary minuses. Any group of digits not splitted by signs or brackets turns
into a number. Between adjacent digits it is possible to put only one sign.
For instance ticket `869308` could be turned to the hundred as `8+6*9+30+8`.

This definitions is more interesting because it is harder to check luckiness
of the ticket: sometimes you could spend entire journey in futile attempts
and at the end, if you didn't reach the goal, it is still unclear: is it
unlucky ticket or one didn't put enough effort. Since 10th grade I didn't
make a hundred from supposingly 30 tickets at most thrice.

For a long time I was interested to know how big is the probability to get
a lucky ticket with respect to this definition. Finally I wrote a program:
it turns out that there are 924587 of such tickets of **92.4%** total number.
This definition is much more optimistic because it lets you catch a lucky
ticket much more often :)
