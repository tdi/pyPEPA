# PEPA Parser
# Version: 0.1
# Date: 26.05.2012
# Author: Dariusz Dwornikowski dariusz.dwornikowski@cs.put.poznan.pl
# Licence: Poznań University of Technology

from pyparsing import *
from CSPAst import *
import sys


class PEPAParser(object):

    logging = False
    logging_pa = False
    varStack = {}

    def __init__(self, logging_pa = False):
        self.model = Model()
        self.logging_pa = logging_pa

    def log_pa(self,string, msg="",prepend="[PARSEACT]"):
        fname = sys._getframe(1).f_code.co_name
        if self.logging_pa:  print(prepend+"["+fname+"]",msg,string)

    def log(self,string, msg="",prepend="log"):
        if logging:  print(prepend,msg,string)

    def error(self,string):
        print("SYNTAX ERROR: ", string)


    def createActivity(self,str,loc,tok):
        self.log_pa("Token: "+tok[0])
        n = Node( "("+tok[0]+","+tok[1]+")", "activity")
        n.activity = tok[0]
        n.rate = tok[1]
        return n

    def createProcdef(self,str,loc,tok):
        self.log_pa("Token: "+tok[0])
        n = Node(tok[0], "procdef")
        return n

    def createDefinition(self,str,loc, tok):
        self.log_pa("Start")
        self.log_pa("Left token: "+tok[0].data)
        self.log_pa("Right token: "+tok[2].data)
        n = DefNode("=", "definition")
        n.left = tok[0]
        n.right = tok[2]
        n.lhs = tok[0].data
        for key in self.model.processes.keys():
            if self.model.processes[key].lhs == tok[0].data:
                self.error("Process "+tok[0].data+" already defined")
                exit(1)
        self.model.processes[tok[0]] = n
        return n

    def createPrefix(self,string, loc, tok):
        self.log_pa("Start<<<")
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

    def createChoice(self,string,loc,tok):
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
                self.log_pa("Left token: "+tok[0].data)
                if tok[1].actions is not None:
                    n = Node("<"+str(tok[1].actions)+">", "coop")
                else:
                    n = Node("||", "coop")
                if type(tok[2]).__name__ == "str":
                    self.log_pa("String: "+tok[2])
                else:
                    self.log_pa("Right token: "+tok[2].data)
                n.left = tok[0]
                n.right= tok[2]
                return n

    def createSyncSet(self,string, loc, tok):
        if len(tok) >1:
            self.log_pa("Non empty synset: "+str(tok))
            n = Node(tok, "syncset")
            n.actions = tok
        else:
            self.log_pa("Parallel")
            n = Node("||", "syncset")
        return n


    def createProcess(self,string, loc, tok):
        self.log_pa("Start")
        if tok[0].left is not None or tok[0].right is not None:
            self.log_pa("Token: "+tok[0].data)
            self.log_pa("Non terminal - passing")
            return tok[0]
        else:
            n = Node(tok[0].data, tok[0].asttype)
            self.log_pa("Terminal - creating Node")
            self.log_pa("Token: "+tok[0].data)
        return n


    def createSystemEQ(self, string, loc, tok):
        self.log_pa("Creating system EQ")
        self.model.systemeq = tok[0]


    def createRates(self,string, loc, tok):
        self.model.rates = self.varStack


    def assignVar(self,toks):
        self.log_pa("VAR"+toks[0])
        self.varStack[toks[0]] = toks[2]

    def checkVar(self,str,loc,tok):
        try:
            if tok[0] not in ("infty", "T", "tau"):
                self.varStack[tok[0]]
        except:
            self.error(tok[0]+" Rate not defined")
            exit(1)

    def gramma(self):
## Tokens
        point = Literal('.')
        prefix_op = Literal('.')
        choice_op = Literal('+')
        parallel = Literal("||") | Literal("<>")
#ident = Word(alphas, alphanums+'_')
        ratename = Word(alphas.lower(),alphanums.lower()+"_")
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
        activity = (ratename + col + peparate).setParseAction(self.createActivity)
        procdef = Word(alphas.upper(), alphanums+"_").setParseAction(self.createProcdef)
## RATES Definitions
        ratedef = (Optional(percent)+ratename + define + peparate_indef).setParseAction(self.assignVar) + semicol

        expression = Forward()
        prefix = Forward()
        choice = Forward()
        coop = Forward()

        process = ( activity
                 | procdef
                 | lpar + coop + rpar
                ).setParseAction(self.createProcess)
        prefix  << (process + ZeroOrMore(prefix_op + prefix)).setParseAction(self.createPrefix)
        choice << (prefix + ZeroOrMore(choice_op + choice)).setParseAction(self.createChoice)
        coop << (choice + ZeroOrMore(coop_op + coop)).setParseAction(self.createCoop)
        rmdef = (Optional(pound) + procdef + define + coop + semicol).setParseAction(self.createDefinition)


        system_eq =  Optional(pound) + coop

        pepa = (ZeroOrMore(ratedef)  + ZeroOrMore(rmdef)
                + system_eq.setParseAction(self.createSystemEQ)
                ).setParseAction(self.createRates)

        pepacomment = '//' + restOfLine
        pepa.ignore(pepacomment)
        return pepa

    def PEPAparse(self,string):
            self.gramma().parseString(string)
            return self.model



if __name__=="__main__":
   with open("test_files/comparison.pepa","r") as f:
         try:
             tokens = pepa.parseString(f.read())
             print("============= >> SEQ Procs TREE << ===============")
             for key in model.processes.keys():
                 tree_walker(model.processes[key])
             print("============= >> System EQ TREE << ===============")
             tree_walker(model.systemeq)
         except ParseException as e:
            error(e)
