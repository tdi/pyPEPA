from pyparsing import *
from pprint import *
from CSPAst import *

def createAction(str,loc,tok):
    print("Robie actiona", tok[0])
    n = Node(tok[0], "action")
    return n

def createDefinition(str,loc, tok):
    print("Robie definitiona")
    n = Node("=", "definition")
    n.left = tok[0]
    n.right = tok[2]
    n.lhs = tok[0].data
    for key in model.processes.keys():
        if model.processes[key].lhs == tok[0].data:
            error("Process "+tok[0].data+" already defined")
            exit(1)
    model.processes[tok[0]] = n
    return n
    
def createPrefix(str, loc, tok):
    if len(tok) > 1:
        n = Node(".", "prefix")
        lhs = tok[0]
        rhs = tok[2]
        n.left = lhs
        n.right = rhs
        print("Robie prefixa: lhs.rhs")
        return n

def createChoice(str,loc,tok):
    if not tok[0] is None:
        if len(tok) <3:
            print("NIE ma choice")
            return tokens[0]
        else:
            n = Node("+", "choice")
            n.left = tok[0]
            n.right = tok[2]
            return n


def createCoop(tokens):
    if not tokens[0] is None:
        n = Node(tokens[0], "coop")
        if len(tokens) <3:
            print("NIE ma coopa")
            return tokens[0]
        else:
            return n

def createProcess(str, loc, tok):
    print("Robie procesa")
    n = Node(tok[0].data, "process")
    return n


logging = False
model = Model()


def log(string, msg="",prepend="log"):
    if logging:  print(prepend,msg,string)

def error(string):
    print("SYNTAX ERROR: ", string)

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
sync = Word('<').suppress() + ident + ZeroOrMore(col + ident) + Word('>').suppress()
coop_op = parallel | sync

## PEPA Grammar 
expression = Forward()
activity = ident.setParseAction(createAction)

process = (lpar + activity + rpar 
        | ident 
        | lpar + expression + rpar).setParseAction(createProcess)
prefix = (process + ZeroOrMore(prefix_op + process)).setParseAction(createPrefix)
choice = (prefix + ZeroOrMore(choice_op + prefix)).setParseAction(createChoice)
expression << (choice + ZeroOrMore(coop_op + choice)).setParseAction(createCoop)
rmdef = (ident + define + expression + semicol).setParseAction(createDefinition)

pepa =  ZeroOrMore(rmdef).setParseAction(lambda x,y,z: print("MODEL: "))

pepacomment = '//' + restOfLine
pepa.ignore(pepacomment)

if __name__=="__main__":
    with open("csp.pepa","r") as f: 
        try:
            tokens = pepa.parseString(f.read())
            for key in model.processes.keys():
                tree_walker(model.processes[key])
        except ParseException as e:
            error(e)
