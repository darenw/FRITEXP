# FRITEXP
Code for computing fractionally iterated exponentials, and making plots for a paper.

FRITEXP = FRactionally ITerated EXPonentials



## Why? 

See the PDF paper in doc/ for the full paper. Here is a brief overview:

Multiplying is repeated addition. What is repeated multiplication? Powers. 

But A^B != B^A except special cases, and (A^B)^C != A^(B^C), and it's just ugly. By insisting on symmetry, an identity element, and making the "next" operation distributive over multiplication, I found something better. Then I generalized it to the _next_ operation, and an operation _before_ addition, and operations for every integer. Then wondered if I could define operations _between_ the integer-order operations, to define an operation parametrized by a real number.  

I invented a new operation,  op_u(A,B), or better:  A op_u B, defined as

> A op_u B = exp_u( log_u(A) + log_u(B) )

with special cases 
> A op_0 B = A+B

> A op_1 B = A*B

and where exp_u is the fractionally iterated exponential obeying
> exp_0(x) = x

> exp_1(x) = exp(x)

> exp_a(exp_b(x)) = exp_{a+b}(x)  for any real a,b
and for convenience its inverse

> log_u(x) = exp_{-u}(x)

Well that's great but how the heck do we define exp_u in a practical way? How do we calculate it with arbitrary real numbers u?  Turns out the problem is ambiguous. 


This is "solved" by use of either Abel's equation

>  A(f (x)) = A(x) + 1  with f = exp

or the logically equivalent Shroeder's equation 

>  L(f (x)) = cL(x)  

with f=exp and we choose c= 1/2 for reasons explained in the paper.

These equations are "loose" in that only values of A at integer
spacings are related. Random functions of period 1 may be used to 
define alternative solutions. 

One solution, by Szekeres, fixes A by demanding non-changing signs of all
orders of derivatives for B, the Abel function for exp(x)-1, which has a
fixpoint at zero.  Power series are developed, approximations made, and
an algorithm found to calculate exp_u(x) for arbitrary real u and x.

Another solution is determined by a simple symmetry, 1 = L(x) + L(-x), 
This leads to an algorithm involving generalized integer-order inverses and
integer-iterated exp and log functions.  One starts with x, computes a 
sequence of iteration counts, then converts that to the value of L. Likewise
for the inverse of L.

L has unbounded derivates, a strangely fractal-like appearance, except 
using exp along one dimension instead of scaling.  I believe the function L
and its inverse to be smooth, that is continuous to all orders of derivatives, 
but have no proof.  Maybe I'll work on that someday.


Several suggestions for further research are given, including new orders
of asymptotic growth greater than polynomial but less than exponential,
but not like existing forms such as exp(sqrt(x)).

Best of all, there are no known practical applications. Perfectly pure math!


## Source Code

Source code defining functions to calculate fritexp functions is available in Python, Go, D and Javascript. Maybe more later.  The directories are named in obvious ways.  In each case, there is a source file for the Szekeres-defined functions, and one for the symmetry-based functions. Unit tests, examples, may be included.  Plotting routines are kept separate, in plots/.

   py/  Python: plain real numbers and numpy arrays
   js/  Javascript includes HTML for interactive calculator and plotting
   D/   Just computation of scalars with unit tests
   go/  For the Go language

## Plots

Code to produce plots in the paper may be found in the plots/ directory, written in Python with matplotlib. Type 'make all' to generate .png and .eps files for all plots in the paper. 



## CONTACT

Daren Scot Wilson
darenw@darenscotwilson.com 
https://github.com/darenw
http://www.darenscotwilson.com/


