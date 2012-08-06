#!/usr/bin/env python
"""
PEPA Parser
"""

from pyparsing import Word, Literal, alphas, alphanums, nums, Combine, Optional, ZeroOrMore, Forward, restOfLine
from PEPAAst import *
import sys


class PEPAParser(object):
    """
    TODO: change all to private fields...
    """

    logging = False
    logging_pa = False
    varStack = {}
    processes = {}
    rates = {}
    systemeq = None

    def __init__(self, logging_pa = False):
        self.logging_pa = logging_pa

    def log_pa(self, string, msg="", prepend="[PARSEACT]"):
        fname = sys._getframe(1).f_code.co_name
        if self.logging_pa:  print(prepend + "[" + fname + "]", msg, string)

    def log(self, string, msg="", prepend="log"):
        if logging:  print(prepend,msg,string)

    def error(self,string):
        print("SYNTAX ERROR: ", string)


    def _createActivity(self,str,loc,tok):
        self.log_pa("Token: "+tok[0])
        n = ActivityNode("(" + tok[0] + "," + tok[1] + ")", "activity")
        n.action = tok[0]
        n.rate = tok[1]
        return n

    def _create_procdef(self,str,loc,tok):
        self.log_pa("Token: "+tok[0])
        n = ProcdefNode(tok[0], "procdef")
        n.name = tok[0]
        return n

    def _create_definition(self,str,loc, tok):
        self.log_pa("Left token: "+tok[0].data)
        self.log_pa("Right token: "+tok[2].data)
        n = DefNode("=", "definition")
        n.left = tok[0]
        n.right = tok[2]
        n.process = tok[0].data
        for key in self.processes.keys():
            if self.processes[key].process == tok[0].data:
                self.error("Process "+tok[0].data+" already defined")
                exit(1)
        self.processes[tok[0]] = n
        return n

    def _create_prefix(self,string, loc, tok):
        self.log_pa("Tokens: "+str( len(tok) ))
        if len(tok) > 1:
            self.log_pa("Left token: "+tok[0].data)
            self.log_pa("Right token: "+tok[2].data)
            n = PrefixNode(".", "prefix")
            lhs = tok[0]
            rhs = tok[2]
            n.left = lhs
            n.right = rhs
            return n
        else:
            self.log_pa("Token: "+tok[0].data)
            return tok[0]

    def _create_choice(self,string,loc,tok):
        self.log_pa("Start")
        self.log_pa("Tokens: "+str( len(tok) ))
        if not tok[0] is None:
            if len(tok) <3:
                self.log_pa("Token: "+tok[0].data)
                return tok[0]
            else:
                self.log_pa("Left token: "+tok[0].data)
                self.log_pa("Right token: "+tok[2].data)

                n = ChoiceNode("+", "choice")
                n.left = tok[0]
                n.right = tok[2]
                return n


    def createCoop(self,string, loc, tok):
        if not tok[0] is None:
            if len(tok) <3:
                self.log_pa("Token: "+tok[0].data)
                return tok[0]
            else:
                self.log_pa("Number of tokens" + str(len(tok)))
                self.log_pa("Left token: "+tok[0].data)
                if tok[1].actionset is not None:
                    n = CoopNode("<"+str(tok[1].actionset)+">", "coop")
                    n.cooptype = "sync"
                    n.actionset = tok[1].actionset
                    self.log_pa(n.actionset)
                else:
                    n = CoopNode("||", "coop")
                    n.cooptype = "par"
                if type(tok[2]).__name__ == "str":
                    self.log_pa("String: "+tok[2])
                else:
                    self.log_pa("Right token: "+tok[2].data)
                n.left = tok[0]
                n.right= tok[2]
                return n

    def createSyncSet(self,string, loc, tok):
        if tok[0] != "||" and tok[0] != "<>":
            self.log_pa("Non empty synset: " + str(tok))
            n = SyncsetNode("<>", "syncset")
            n.actionset = tok
        else:
            self.log_pa("Parallel")
            n = SyncsetNode("||", "syncset")
            n.actionset = None
        return n


    def createProcess(self,string, loc, tok):
        self.log_pa("Start")
        if tok[0].left is not None or tok[0].right is not None:
            self.log_pa("Token: "+tok[0].data)
            self.log_pa("Non terminal - passing")
            return tok[0]
        else:
            if tok[0].asttype == "procdef":
                n = ProcdefNode(tok[0].data, tok[0].asttype)
            elif tok[0].asttype == "activity":
                n = ActivityNode(tok[0].data, tok[0].asttype)
                n.rate = tok[0].rate
                n.action = tok[0].action
            else:
                self.log_pa("ERRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRROR")
            self.log_pa("Terminal - creating Node ->" + tok[0].asttype)
            self.log_pa("Token: "+tok[0].data)
        return n


    def createSystemEQ(self, string, loc, tok):
        self.log_pa("Creating system EQ")
        self.systemeq = tok[0]


    def assignVar(self,toks):
        self.varStack[toks[0]] = toks[2]

    def checkVar(self,str,loc,tok):
        try:
            # just a number
            float(tok[0])
        except:
            try:
                if tok[0] not in ("infty", "T", "tau"):
                    self.varStack[tok[0]]
            except:
                self.error("Rate " + tok[0]+ " not defined")
                exit(1)

    def gramma(self):
## Tokens
        point = Literal('.')
        prefix_op = Literal('.')
        choice_op = Literal('+')
        parallel = Literal("||") | Literal("<>")
#ident = Word(alphas, alphanums+'_')
        ratename = Word(alphas.lower(),alphanums+"_")
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
        percent = Literal('%').suppress()
        peparate = (ratename | floatnumber | internalrate | passiverate).setParseAction(self.checkVar)
        peparate_indef = floatnumber | internalrate | passiverate
        sync = Word('<').suppress() + ratename + ZeroOrMore(col + ratename) + Word('>').suppress()
        coop_op = (parallel | sync).setParseAction(self.createSyncSet)
        activity = (ratename + col + peparate).setParseAction(self._createActivity)
        procdef = Word(alphas.upper(), alphanums+"_").setParseAction(self._create_procdef)
## RATES Definitions
        ratedef = (Optional(percent)+ratename + define + peparate_indef).setParseAction(self.assignVar) + semicol

        prefix = Forward()
        choice = Forward()
        coop = Forward()

        process = ( activity
                 | procdef
                 | lpar + coop + rpar
                ).setParseAction(self.createProcess)
        prefix  << (process + ZeroOrMore(prefix_op + prefix)).setParseAction(self. _create_prefix)
        choice << (prefix + ZeroOrMore(choice_op + choice)).setParseAction(self. _create_choice)
        coop << (choice + ZeroOrMore(coop_op + coop)).setParseAction(self.createCoop)
        rmdef = (Optional(pound) + procdef + define + coop + semicol).setParseAction(self._create_definition)


        system_eq =  Optional(pound) + coop

        pepa = ZeroOrMore(ratedef)  + ZeroOrMore(rmdef) + system_eq.setParseAction(self.createSystemEQ)


        pepacomment = '//' + restOfLine
        pepa.ignore(pepacomment)
        return pepa

    def parse(self,string):
            self.gramma().parseString(string)
            return (self.processes, self.varStack, self.systemeq)



