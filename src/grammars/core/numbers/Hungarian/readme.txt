Usage:
* chmod a+x c tf t
* Compiling: ./c
* Testing on list of test cases: ./tf
   The input files end in _in.txt
   The output files have the extension .out.
   The reference files end in _ref.txt
* Testing manually: ./t

It uses the Western factorizer, with one '0' preserved only if there are no non-zero digits. 

It can handle cardinals, ordinals (e.g. "1."), and decimal fractions (e.g. "1,2").

For decimal fractions, it needs a final "<denominator> factorized denominator", as Hungarian decimals are read similarly to Russian ones.
E.g. "1,2" -> "1,2<denominator>1<E1>" -> "egy egész kettõ tized", 
meaning "one whole two tenth" (as we don't use plural when there is a quantifier).
