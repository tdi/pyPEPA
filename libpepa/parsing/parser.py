#!/usr/bin/env python
"""
PEPA Parser
"""
from pyparsing import Word, Literal, alphas, alphanums, nums, Combine, Optional, ZeroOrMore, Forward, restOfLine
import sys
from libpepa.parsing.pepa_ast import *
from libpepa.logger import init_log

class PEPAParser(object):
    """
    TODO: change to dicts
    """

    def __init__(self):
        self.log_pa = init_log()
        self._processes = {}
        self._var_stack = {}
        self.systemeq = None


    def error(self,string):
        print("SYNTAX ERROR: ", string)


    def _create_activity(self, string, loc,tok):
        self.log_pa.info("Token: "+tok[0])
        n = ActivityNode("(" + tok[0] + "," + tok[1] + ")", "activity")
        n.action = tok[0]
        n.rate = tok[1]
        return n

    def _create_procdef(self, s, loc, toks):
        self.log_pa.info("Token: "+toks[0])
        n = ProcdefNode(toks[0], "procdef")
        if len(toks) > 1:
            n.aggregation = True
            if toks[1] in self._var_stack:
                n.aggr_num = int(self._var_stack[toks[1]])
            else:
                n.aggr_num = int(toks[1])
        n.name = toks[0]
        return n

    def _create_definition(self, string, loc, tok):
        self.log_pa.info("Left token: "+tok[0].data)
        self.log_pa.info("Right token: "+tok[2].data)
        n = DefNode("=", "definition")
        n.left = tok[0]
        n.right = tok[2]
        n.process = tok[0].data
        for key in self._processes.keys():
            if self._processes[key].process == tok[0].data:
                self.error("Process "+tok[0].data+" already defined")
                exit(1)
        self._processes[tok[0]] = n
        return n

    def _create_prefix(self,string, loc, tok):
        self.log_pa.info("Tokens: "+str( len(tok) ))
        if len(tok) > 1:
            self.log_pa.info("Left token: "+tok[0].data)
            self.log_pa.info("Right token: "+tok[2].data)
            n = PrefixNode(".", "prefix")
            lhs = tok[0]
            rhs = tok[2]
            n.left = lhs
            n.right = rhs
            return n
        else:
            self.log_pa.info("Token: "+tok[0].data)
            return tok[0]

    def _create_choice(self,string,loc,tok):
        self.log_pa.info("Start")
        self.log_pa.info("Tokens: "+str( len(tok) ))
        if not tok[0] is None:
            if len(tok) <3:
                self.log_pa.info("Token: "+tok[0].data)
                return tok[0]
            else:
                self.log_pa.info("Left token: "+tok[0].data)
                self.log_pa.info("Right token: "+tok[2].data)

                n = ChoiceNode("+", "choice")
                n.left = tok[0]
                n.right = tok[2]
                return n


    def _create_coop(self,string, loc, tok):
        if not tok[0] is None:
            if len(tok) <3:
                self.log_pa.info("Token: "+tok[0].data)
                return tok[0]
            else:
                self.log_pa.info("Number of tokens" + str(len(tok)))
                self.log_pa.info("Left token: "+tok[0].data)
                if tok[1].actionset is not None:
                    n = CoopNode("<"+str(tok[1].actionset)+">", "coop")
                    n.cooptype = "sync"
                    n.actionset = tok[1].actionset
                    self.log_pa.info(n.actionset)
                else:
                    n = CoopNode("||", "coop")
                    n.cooptype = "par"
                if type(tok[2]).__name__ == "str":
                    self.log_pa.info("String: "+tok[2])
                else:
                    self.log_pa.info("Right token: "+tok[2].data)
                n.left = tok[0]
                n.right= tok[2]
                return n

    def _create_sync_set(self,string, loc, tok):
        if tok[0] != "||" and tok[0] != "<>":
            self.log_pa.info("Non empty synset: " + str(tok))
            n = SyncsetNode("<>", "syncset")
            n.actionset = tok
        else:
            self.log_pa.info("Parallel")
            n = SyncsetNode("||", "syncset")
            n.actionset = None
        return n

    def _create_subtree_aggregation(self, num, procname):
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

    def _create_process(self,string, loc, tok):
        self.log_pa.info("Start")
        if tok[0].left is not None or tok[0].right is not None:
            self.log_pa.info("Token: "+tok[0].data)
            self.log_pa.info("Non terminal - passing")
            return tok[0]
        else:
            if tok[0].asttype == "procdef":
                n = ProcdefNode(tok[0].data, tok[0].asttype)
                # TODO create subtree
                if tok[0].aggregation == True:
                    n.aggregation = True
                    n.aggr_num = tok[0].aggr_num
                    n = self._create_subtree_aggregation(tok[0].aggr_num, tok[0].data)
                    n.asttype = "coop"
                    n.data = "||"
                    n.cooptype = "par"
                    n.actionset = None
            elif tok[0].asttype == "activity":
                n = ActivityNode(tok[0].data, tok[0].asttype)
                n.rate = tok[0].rate
                n.action = tok[0].action
            else:
                self.log_error("This situation should not take place")
            self.log_pa.info("Terminal - creating Node ->" + tok[0].asttype)
            self.log_pa.info("Token: "+tok[0].data)
        return n


    def _create_system_equation(self, string, loc, tok):
        self.log_pa.info("Creating system EQ")
        self._systemeq = tok[0]


    def _assign_var(self,toks):
        self._var_stack[toks[0]] = toks[2]

    def _check_var(self,str,loc,tok):
        try:
            # just a number
            float(tok[0])
        except:
            try:
                if tok[0] not in ("infty", "T", "tau"):
                    self._var_stack[tok[0]]
            except:
                self.error("Rate " + tok[0]+ " not defined")
                exit(1)

    def gramma(self):
## Tokens
        point = Literal('.')
        prefix_op = Literal('.')
        choice_op = Literal('+')
        parallel = Literal("||") | Literal("<>")
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
        peparate = (ratename | floatnumber | internalrate | passiverate).setParseAction(self._check_var)
        peparate_indef = floatnumber | internalrate | passiverate
        sync = Word('<').suppress() + ratename + ZeroOrMore(col + ratename) + Word('>').suppress()
        coop_op = (parallel | sync).setParseAction(self._create_sync_set)
        activity = (ratename + col + peparate).setParseAction(self._create_activity)
        procdef = (Word(alphas.upper(), alphanums+"_"+"`"+"'") + Optional(lsqpar + peparate + rsqpar)).setParseAction(self._create_procdef)
## RATES Definitions
        ratedef = (Optional(percent)+ratename + define + peparate_indef).setParseAction(self._assign_var) + semicol

        prefix = Forward()
        choice = Forward()
        coop = Forward()

        process = ( activity
                 | procdef
                 | lpar + coop + rpar
                ).setParseAction(self._create_process)
        prefix  << (process + ZeroOrMore(prefix_op + prefix)).setParseAction(self. _create_prefix)
        choice << (prefix + ZeroOrMore(choice_op + choice)).setParseAction(self. _create_choice)
        coop << (choice + ZeroOrMore(coop_op + coop)).setParseAction(self._create_coop)
        rmdef = (Optional(pound) + procdef + define + coop + semicol).setParseAction(self._create_definition)
        system_eq =  Optional(pound) + coop
        pepa = ZeroOrMore(ratedef)  + ZeroOrMore(rmdef) + system_eq.setParseAction(self._create_system_equation)
        pepacomment = '//' + restOfLine
        pepa.ignore(pepacomment)
        return pepa

    def parse(self,string):
        self.gramma().parseString(string)
        return (self._processes, self._var_stack, self._systemeq)



