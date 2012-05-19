from pyparsing import Word, alphas, ParseException, Literal \
, Combine, Optional, nums, Or, Forward, ZeroOrMore, OneOrMore, StringEnd, alphanums, alphas, ZeroOrMore, restOfLine
import math

## Tokens
point = Literal('.')
prefix_op = Literal('.')
choice_op = Literal('+')
parallel = Literal("||")
ident = Word(alphas, alphanums).setName('process')
lpar = Literal('(').suppress()
rpar = Literal(')').suppress()
define = Literal('=').setName('rmdef')
semicol = Literal(';').suppress()
col = Literal(',').suppress()

number = Word(nums)
integer = number
floatnumber = Combine( integer + Optional( point + Optional(number)))
passiverate = Word('infty') | Word('T')
internalrate = Word('tau')
peparate = floatnumber | internalrate | passiverate | ident
sync = Word('<').suppress() + ident + ZeroOrMore(col + ident) + Word('>').suppress()
coop_op = parallel | sync



## RATES Definitions
ratedef = ident + define + peparate + semicol

## PEPA Grammar 
expression = Forward()
activity = ident + col + peparate
process = lpar + activity + rpar | ident | lpar + expression + rpar
prefix = process + ZeroOrMore(prefix_op + process)
choice = prefix + ZeroOrMore(choice_op + prefix)
expression = choice + ZeroOrMore(coop_op + choice)
rmdef = ident + define + expression + semicol



systemeq = ident + ZeroOrMore(coop_op + ident)
pepa = ZeroOrMore(ratedef) + ZeroOrMore(rmdef) + ZeroOrMore(systemeq)


pepacomment = '//' + restOfLine
pepa.ignore(pepacomment)
#tokens = pepa.parseString("Client = (cipa,tau).Client;


with open("test.pepa","r") as f: 
    tokens = pepa.parseString(f.read())
    print(tokens)

