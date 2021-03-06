<!-- Header: Explosive Macros Example -->
<!-- Tag: cpp -->
<!-- Summary: A small code which demonstrates C++ compiler constraints. -->

This code is inspired by a [codeforces problem](http://codeforces.ru/problemset/problem/7/E).
It demonstrates seemingly innocuous macros which blow up compiler.

Main idea is to construct short sequence of macros which generates exponential
output.

<pre class='brush: cpp'>
#include &lt;iostream>

#define AA (BB + BB)
#define BB (CC + CC)
#define CC (DD + DD)
#define DD (EE + EE)
#define EE (FF + FF)
#define FF (GG + GG)
#define GG (HH + HH)
#define HH (II + II)
#define II (JJ + JJ)
#define JJ (KK + KK)
#define KK (LL + LL)
#define LL (MM + MM)
#define MM (NN + NN)
#define NN (OO + OO)
#define OO (PP + PP)
#define PP (QQ + QQ)
#define QQ (RR + RR)
#define RR (SS + SS)
#define SS (TT + TT)
#define TT (UU + UU)
#define UU (VV + VV)
#define VV (WW + WW)
#define WW (XX + XX)
#define XX (YY + YY)
#define YY (ZZ + ZZ)
#define ZZ 1

int main()
{
    std::cout &lt;&lt; "AA = " &lt;&lt; AA &lt;&lt; std::endl;
    return 0;
}
</pre>