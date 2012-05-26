from pyparsing import *
from pprint import *
from CSPAst import *
import sys 

def createEvent(str,loc,tok):
    log_pa("Token: "+tok[0])
    n = Node(tok[0], "event")
    return n

def createProcdef(str,loc,tok):
    log_pa("Token: "+tok[0])
    n = Node(tok[0], "procdef")
    return n

def createDefinition(str,loc, tok):
    log_pa("Start")
    log_pa("Left token: "+tok[0].data)
    log_pa("Right token: "+tok[2].data) 
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
    
def createPrefix(string, loc, tok):
    log_pa("Start<<<")
    log_pa("Tokens: "+str( len(tok) ))
    if len(tok) > 1:
        log_pa("Left token: "+tok[0].data)
        log_pa("Right token: "+tok[2].data) 
        n = Node(".", "prefix")
        lhs = tok[0]
        rhs = tok[2]
        n.left = lhs
        n.right = rhs
#        print("Robie prefixa: lhs.rhs")
        return n
    else:
        log_pa("Token: "+tok[0].data)
        return tok[0]

def createChoice(string,loc,tok):
    log_pa("Start")
    log_pa("Tokens: "+str( len(tok) ))
    if not tok[0] is None:
        if len(tok) <3:
            log_pa("Token: "+tok[0].data)
            return tok[0]
        else:
            log_pa("Left token: "+tok[0].data)
            log_pa("Right token: "+tok[2].data)
            n = Node("+", "choice")
            n.left = tok[0]
            n.right = tok[2]
            return n


def createCoop(string, loc, tok):
    if not tok[0] is None:
        if len(tok) <3:
            log_pa("Token: "+tok[0].data)
            return tok[0]
        else:
            log_pa("Left token: "+tok[0].data)
            log_pa("Right token: "+tok[2].data)
            n = Node("<>", "coop")
            n.left = tok[0]
            n.right= tok[2]
            return n

def createProcess(str, loc, tok):
    log_pa("Start")
    if tok[0].left is not None or tok[0].right is not None:
        log_pa("Token: "+tok[0].data)
        log_pa("Non terminal - passing")
        return tok[0]
    else:
        n = Node(tok[0].data, "process")
        log_pa("Terminal - creating Node")
        log_pa("Token: "+tok[0].data)
    return n


logging = False
logging_pa = True
model = Model()


def log_pa(string, msg="",prepend="[PARSEACT]"):
    fname = sys._getframe(1).f_code.co_name
    if logging_pa:  print(prepend+"["+fname+"]",msg,string)

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
stop = Literal('0') | Word('STOP')
coop_op = parallel | sync
event = Word(alphanums.lower()).setParseAction(createEvent)

procdef = Word(alphanums.upper()).setParseAction(createProcdef)
coop = Forward()
choice = Forward()
prefix = Forward()
prefix = Forward()


process = (
         event
         |  procdef 
         | lpar + coop + rpar
        ).setParseAction(createProcess)
prefix  << (process + ZeroOrMore(prefix_op + prefix)).setParseAction(createPrefix)
choice << (prefix + ZeroOrMore(choice_op + choice)).setParseAction(createChoice)
coop << (choice + ZeroOrMore(coop_op + coop)).setParseAction(createCoop)
rmdef = (procdef + define + coop + semicol).setParseAction(createDefinition)

pepa =  ZeroOrMore(rmdef)

comment = '//' + restOfLine
pepa.ignore(comment)

if __name__=="__main__":
    with open("csp.pepa","r") as f: 
        try:
            tokens = pepa.parseString(f.read())
            print("============= >> TREE << ===============")
            for key in model.processes.keys():
                tree_walker(model.processes[key])
        except ParseException as e:
            error(e)
