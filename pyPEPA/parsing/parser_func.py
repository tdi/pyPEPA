#!/usr/bin/env python
"""
PEPA Parser
"""
from pyparsing import Word, Literal, alphas, alphanums, nums, Combine, Optional, ZeroOrMore, Forward, restOfLine
import sys
from parsing.pepa_ast import *

_logging_pa = False
_var_stack = None
_processes = None
_systemeq = None

def __init__(logging_pa = False):
    _logging_pa = logging_pa
    _processes = {}
    _var_stack = {}

def log_pa(string, msg="", prepend="[PARSEACT]"):
    fname = sys._getframe(1).f_code.co_name
    if _logging_pa:  print(prepend + "[" + fname + "]", msg, string)

def error(string):
    print("SYNTAX ERROR: ", string)


def _create_activity(string, loc,tok):
    log_pa("Token: "+tok[0])
    n = ActivityNode("(" + tok[0] + "," + tok[1] + ")", "activity")
    n.action = tok[0]
    n.rate = tok[1]
    return n

def _create_procdef(string, loc, tok):
    log_pa("Token: "+tok[0])
    n = ProcdefNode(tok[0], "procdef")
    if len(tok) > 1:
        n.aggregation = True
        if tok[1] in _var_stack:
            n.aggr_num = int(_var_stack[tok[1]])
        else:
            n.aggr_num = int(tok[1])
    n.name = tok[0]
    return n

def _create_definition(string, loc, tok):
    log_pa("Left token: "+tok[0].data)
    log_pa("Right token: "+tok[2].data)
    n = DefNode("=", "definition")
    n.left = tok[0]
    n.right = tok[2]
    n.process = tok[0].data
    for key in _processes.keys():
        if _processes[key].process == tok[0].data:
            error("Process "+tok[0].data+" already defined")
            exit(1)
    _processes[tok[0]] = n
    return n

def _create_prefix(string, loc, tok):
    log_pa("Tokens: "+str( len(tok) ))
    if len(tok) > 1:
        log_pa("Left token: "+tok[0].data)
        log_pa("Right token: "+tok[2].data)
        n = PrefixNode(".", "prefix")
        lhs = tok[0]
        rhs = tok[2]
        n.left = lhs
        n.right = rhs
        return n
    else:
        log_pa("Token: "+tok[0].data)
        return tok[0]

def _create_choice(string,loc,tok):
    log_pa("Start")
    log_pa("Tokens: "+str( len(tok) ))
    if not tok[0] is None:
        if len(tok) <3:
            log_pa("Token: "+tok[0].data)
            return tok[0]
        else:
            log_pa("Left token: "+tok[0].data)
            log_pa("Right token: "+tok[2].data)

            n = ChoiceNode("+", "choice")
            n.left = tok[0]
            n.right = tok[2]
            return n


def _create_coop(string, loc, tok):
    if not tok[0] is None:
        if len(tok) <3:
            log_pa("Token: "+tok[0].data)
            return tok[0]
        else:
            log_pa("Number of tokens" + str(len(tok)))
            log_pa("Left token: "+tok[0].data)
            if tok[1].actionset is not None:
                n = CoopNode("<"+str(tok[1].actionset)+">", "coop")
                n.cooptype = "sync"
                n.actionset = tok[1].actionset
                log_pa(n.actionset)
            else:
                n = CoopNode("||", "coop")
                n.cooptype = "par"
            if type(tok[2]).__name__ == "str":
                log_pa("String: "+tok[2])
            else:
                log_pa("Right token: "+tok[2].data)
            n.left = tok[0]
            n.right= tok[2]
            return n

def _create_sync_set(string, loc, tok):
    if tok[0] != "||" and tok[0] != "<>":
        log_pa("Non empty synset: " + str(tok))
        n = SyncsetNode("<>", "syncset")
        n.actionset = tok
    else:
        log_pa("Parallel")
        n = SyncsetNode("||", "syncset")
        n.actionset = None
    return n

def _create_subtree_aggregation(num, procname):
    """ Transforms Process[num] into AST subtree """
    first = CoopNode("||", "coop")
    first.cooptype = "par"
    last = first
    for i in list(range(2, num+1)):
        nl = ProcdefNode(procname, "procdef")
        if i == num:
            nr = ProcdefNode(procname, "procdef")
            last.right = nr
        else:
            nr = CoopNode("||", "coop")
            nr.cooptype = "par"
            last.right = nr
        last.left = nl
        last = nr
    return first

def _create_process(string, loc, tok):
    log_pa("Start")
    if tok[0].left is not None or tok[0].right is not None:
        log_pa("Token: "+tok[0].data)
        log_pa("Non terminal - passing")
        return tok[0]
    else:
        if tok[0].asttype == "procdef":
            n = ProcdefNode(tok[0].data, tok[0].asttype)
            # TODO create subtree
            if tok[0].aggregation == True:
                n.aggregation = True
                n.aggr_num = tok[0].aggr_num
                n = _create_subtree_aggregation(tok[0].aggr_num, tok[0].data)
                n.asttype = "coop"
                n.data = "||"
                n.cooptype = "par"
                n.actionset = None
        elif tok[0].asttype == "activity":
            n = ActivityNode(tok[0].data, tok[0].asttype)
            n.rate = tok[0].rate
            n.action = tok[0].action
        else:
            log_pa("ERRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRROR")
        log_pa("Terminal - creating Node ->" + tok[0].asttype)
        log_pa("Token: "+tok[0].data)
    return n


def _create_system_equation(string, loc, tok):
    log_pa("Creating system EQ")
    _systemeq = tok[0]


def assign_var(toks):
    _var_stack[toks[0]] = toks[2]

def _check_var(str,loc,tok):
    try:
        # just a number
        float(tok[0])
    except:
        try:
            if tok[0] not in ("infty", "T", "tau"):
                _var_stack[tok[0]]
        except:
            error("Rate " + tok[0]+ " not defined")
            exit(1)

def gramma():
## Tokens
    point = Literal('.')
    prefix_op = Literal('.')
    choice_op = Literal('+')
    parallel = Literal("||") | Literal("<>")
#ident = Word(alphas, alphanums+'_')
    ratename = Word(alphas.lower(),alphanums+"_")
    lpar = Literal('(').suppress()
    rpar = Literal(')').suppress()
    lsqpar = Literal('[').suppress()
    rsqpar = Literal(']').suppress()

    define = Literal('=')
    semicol = Literal(';').suppress()
    col = Literal(',').suppress()
    number = Word(nums)
    integer = number
    floatnumber = Combine( integer + Optional( point + Optional(number)))
    passiverate = Word('infty') | Word('T')
    internalrate = Word('tau')
    pound = Literal('#').suppress()
    percent = Literal('%').suppress()
    peparate = (ratename | floatnumber | internalrate | passiverate).setParseAction(_check_var)
    peparate_indef = floatnumber | internalrate | passiverate
    sync = Word('<').suppress() + ratename + ZeroOrMore(col + ratename) + Word('>').suppress()
    coop_op = (parallel | sync).setParseAction(_create_sync_set)
    activity = (ratename + col + peparate).setParseAction(_create_activity)
    procdef = (Word(alphas.upper(), alphanums+"_") + Optional(lsqpar + peparate_indef + rsqpar)).setParseAction(_create_procdef)
## RATES Definitions
    ratedef = (Optional(percent)+ratename + define + peparate_indef).setParseAction(assign_var) + semicol

    prefix = Forward()
    choice = Forward()
    coop = Forward()

    process = ( activity
             | procdef
             | lpar + coop + rpar
            ).setParseAction(_create_process)
    prefix  << (process + ZeroOrMore(prefix_op + prefix)).setParseAction( _create_prefix)
    choice << (prefix + ZeroOrMore(choice_op + choice)).setParseAction(_create_choice)
    coop << (choice + ZeroOrMore(coop_op + coop)).setParseAction(_create_coop)
    rmdef = (Optional(pound) + procdef + define + coop + semicol).setParseAction(_create_definition)
    system_eq =  Optional(pound) + coop
    pepa = ZeroOrMore(ratedef)  + ZeroOrMore(rmdef) + system_eq.setParseAction(_create_system_equation)
    pepacomment = '//' + restOfLine
    pepa.ignore(pepacomment)
    return pepa

def parse(string):
    gramma().parseString(string)
    return (_processes, _var_stack, _systemeq)



