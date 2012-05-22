from pyparsing import *
import math

class Node():
    left, right, data = None, None, 0

    def __init__(self,data):
        self.right = None
        self.left = None
        self.data = data

class PTree():
    nodes = []
    root = Node("MODEL")
    last_node = None
    
    def __init__(self):
        self.nodes.append(self.root)

    def add_node(self,node):
        self.last_node = node 
        self.nodes.append(node)

class Model():
    processes = []
    PTree = PTree()

model = Model()

logging = False


def createConstant(tokens):
    print(tokens[0])
    print("RMDEF") 

def createPrefix(tokens):
    print(tokens[3])
    print("PREFIX") 

def log(string, msg="",prepend="log"):
    if logging:  print(prepend,msg,string)

def error(string):
    print("ERROR: ", string)

varStack = {}

def assignVar(toks):
    log(toks, "VAR")
    varStack[toks[0]] = toks[2]

def checkVar(toks):
    try:
        if toks[0] not in ("infty", "T", "tau"):
            varStack[toks[0]]
    except:
        error(toks[0]+" Rate not defined")
        exit()

## Tokens
point = Literal('.')
prefix_op = Literal('.')
choice_op = Literal('+')
parallel = Literal("||")
ident = Word(alphas, alphanums+'_')
lpar = Literal('(').suppress()
rpar = Literal(')').suppress()
define = Literal('=')
semicol = Literal(';').suppress()
col = Literal(',').suppress()
number = Word(nums)
integer = number
floatnumber = Combine( integer + Optional( point + Optional(number)))
passiverate = Word('infty') | Word('T')
internalrate = Word('tau')
peparate = (floatnumber | internalrate | passiverate | ident).setParseAction(checkVar)
peparate_indef = floatnumber | internalrate | passiverate 
sync = Word('<').suppress() + ident + ZeroOrMore(col + ident) + Word('>').suppress()
coop_op = parallel | sync

hiop = coop_op | prefix_op
## RATES Definitions

## PEPA Grammar 
#expression = Forward()
activity = 
operand = ident | lpar + activity + rpar  
expression = operatorPrecedence( operand,
     (hiop, 2, opAssoc.LEFT),
     (choice_op, 2, opAssoc.LEFT),]
)
        


if __name__=="__main__":
    tokens = expression.parseString("Z=(P.C)+E+D+E<a,b>D")
    print(tokens)
