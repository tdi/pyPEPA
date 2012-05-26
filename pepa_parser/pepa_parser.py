from pyparsing import *
from CSPAst import *
import sys

model = Model()
logging = False
logging_pa = True

def log_pa(string, msg="",prepend="[PARSEACT]"):
    fname = sys._getframe(1).f_code.co_name
    if logging_pa:  print(prepend+"["+fname+"]",msg,string)

def log(string, msg="",prepend="log"):
    if logging:  print(prepend,msg,string)

def error(string):
    print("SYNTAX ERROR: ", string)


def createActivity(str,loc,tok):
    log_pa("Token: "+tok[0])
    n = Node("act("+tok[0]+","+tok[1]+")", "activity")
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
            if tok[1].actions is not None:
                n = Node("<"+str(tok[1].actions)+">", "coop")
            else:
                n = Node("||", "coop")
            if type(tok[2]).__name__ == "str":
                log_pa("String: "+tok[2])
            else:
                log_pa("Right token: "+tok[2].data)
            n.left = tok[0]
            n.right= tok[2]
            return n

def createSyncSet(string, loc, tok):
    if len(tok) >1:
        log_pa("Non empty synset: "+str(tok))
        n = Node(tok, "syncset")
        n.actions = tok
    else:
        log_pa("Parallel")
        n = Node("||", "syncset")
    return n


def createProcess(string, loc, tok):
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


def createSystemEQ(string, loc, tok):
    log_pa("Creating system EQ")
    model.systemeq = tok[0]


def createRates(string, loc, tok):
    model.rates = varStack

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
        exit(1)


## Tokens
point = Literal('.')
prefix_op = Literal('.')
choice_op = Literal('+')
parallel = Literal("||") | Literal("<>")
#ident = Word(alphas, alphanums+'_')
ratename = Word(alphas.lower(),alphanums.lower())
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
pound = Literal('#').suppress()
peparate = (floatnumber | internalrate | passiverate | ratename).setParseAction(checkVar)
peparate_indef = floatnumber | internalrate | passiverate
sync = Word('<').suppress() + ratename + ZeroOrMore(col + ratename) + Word('>').suppress()
coop_op = (parallel | sync).setParseAction(createSyncSet)
activity = (ratename + col + peparate).setParseAction(createActivity)
procdef = Word(alphas.upper(), alphanums+"_").setParseAction(createProcdef)
## RATES Definitions
ratedef = (ratename + define + peparate_indef).setParseAction(assignVar) + semicol

expression = Forward()
prefix = Forward()
choice = Forward()
coop = Forward()

process = ( activity
         | procdef
         | lpar + coop + rpar
        ).setParseAction(createProcess)
prefix  << (process + ZeroOrMore(prefix_op + prefix)).setParseAction(createPrefix)
choice << (prefix + ZeroOrMore(choice_op + choice)).setParseAction(createChoice)
coop << (choice + ZeroOrMore(coop_op + coop)).setParseAction(createCoop)
rmdef = (Optional(pound) + procdef + define + coop + semicol).setParseAction(createDefinition)


system_eq =  Optional(pound) + coop

pepa = (ZeroOrMore(ratedef)  + ZeroOrMore(rmdef)
        + system_eq.setParseAction(createSystemEQ)
        ).setParseAction(createRates)

pepacomment = '//' + restOfLine
pepa.ignore(pepacomment)

def PEPAparse(string):
        pepa.parseString(string)
        return model 



if __name__=="__main__":
   with open("lan4.pepa","r") as f: 
         try:
             tokens = pepa.parseString(f.read())
             print("============= >> SEQ Procs TREE << ===============")
             for key in model.processes.keys():
                 tree_walker(model.processes[key])
             print("============= >> System EQ TREE << ===============")
             tree_walker(model.systemeq)
         except ParseException as e:
            print("LLALLAAA")
            error(e)
