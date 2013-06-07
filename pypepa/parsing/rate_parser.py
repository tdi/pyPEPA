#!/usr/bin/env python
""" 
This parser is inspired by fourFn.py example by Paul McGuire. Thank You Paul
for amazing pyparsing library.
"""
from pyparsing import Literal,CaselessLiteral,Word,Combine,Group,Optional,\
        ZeroOrMore,Forward,nums,alphas, alphanums
import readline
import operator
import re

class RateParser(object):
    """ 
    Parses and evaluates expresssions mathematical
    expressions, ops supported: +, -, *, /, ^
    """

    def __init__(self):
        self.bnf = None
        self.expr_stack = []
        self.variables = {}
        self.var_stack = []
        self.opn = { "+" : operator.add,
                "-" : operator.sub,
                "*" : operator.mul,
                "/" : operator.truediv,
                "^" : operator.pow }


    def _pushFirst(self, string, loc, toks):
        self.expr_stack.append(toks[0])

    def _assignVar(self, str, loc, toks):
        self.var_stack.append(toks[0])

    def BNF(self):
        if not self.bnf:
            point = Literal( "." )
            fnumber = Combine( Word( "+-"+nums, nums ) + 
                               Optional( point + Optional( Word( nums ) ) ) 
                               )
            ident = Word(alphas, alphanums+"_")
            plus  = Literal( "+" )
            minus = Literal( "-" )
            mult  = Literal( "*" )
            passiverate = Word('infty') | Word('T')
            internalrate = Word('tau')
            div   = Literal( "/" )
            comma = Literal(",")
            lpar  = Literal( "(" ).suppress()
            rpar  = Literal( ")" ).suppress()
            addop  = plus | minus
            multop = mult | div
            assign = Literal('=')
            expop = Literal( "^" )
            expr = Forward()
            args = ident + ZeroOrMore(ident + comma)| fnumber + ZeroOrMore(ident + comma)
            atom = Optional("-") + ( fnumber | ident + lpar + expr + rpar | ident).setParseAction(self._pushFirst ) | lpar + expr.suppress() + rpar 
            factor = Forward()
            factor << atom + ZeroOrMore( ( expop + factor )
                    .setParseAction(self._pushFirst) )
            term = factor + ZeroOrMore( ( multop + factor )
                    .setParseAction(self._pushFirst) )
            expr << term + ZeroOrMore( ( addop + term )
                    .setParseAction(self._pushFirst ) )
            bnf = internalrate | passiverate | (ident + assign).setParseAction(self._assignVar) + expr
            self.bnf = bnf
        return self.bnf


    def parse_rate_expr(self, rate):
        # var_stack = []
        # L = self.BNF().parseString(rate)
        result = self.evaluate(self.expr_stack)
        self.expr_stack = []
        if len(self.var_stack) == 1:
            self.variables[self.var_stack.pop()] = result
        return result


    def evaluate(self,s):
        op = s.pop()
        if op in self.opn:
            op2 = self.evaluate(s)
            op1 = self.evaluate(s)
            return self.opn[op](op1, op2)
        elif  re.search('^[a-zA-Z][a-zA-Z0-9_]*$',op):
            return self.variables.get(op, float(0))
        elif op[0].isalpha():
            return 0
        else:
            return float( op )

if __name__ == "__main__":
    parser = RateParser()
    input_string = ''
    input_string = input("> ")
    while input_string != 'quit':
        if input_string != '':
            result = parser.parse_rate_expr(input_string)
            print(result)
        input_string = input("> ")



