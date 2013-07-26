#!/usr/bin/env python
from pyparsing import Word, Literal, alphas, alphanums, Combine, Optional,\
                      ZeroOrMore, Forward, restOfLine, nums, lineno, col, \
                      ParseException
from pypepa.parsing.pepa_ast import ActivityNode, ProcdefNode, DefNode, CoopNode, \
                                    PrefixNode, SyncsetNode
from pypepa.parsing.rate_parser import RateParser
from pypepa.logger import init_log
from pypepa.exceptions import VariableNotDefinedError, VariableAlreadyDefinedError, \
                               ProcessNotDefinedError, ProcessNotDefinedError, \
                               ProcessAlreadyDefinedError

class PEPAParser(object):

    def __init__(self):
        self.log_pa = init_log()
        self._processes = {}
        self._var_stack = {}
        self._actions = []
        self._seen = {}
        self.systemeq = None
        self.rate_parser = RateParser()

    def _create_activity(self, string, loc,tok):
        self.log_pa.debug("Token: "+tok[0])
        n = ActivityNode("(" + tok[0] + "," + tok[1] + ")")
        n.action = tok[0]
        self._actions.append(n.action)
        n.rate = tok[1]
        return n

    def _create_procdef(self, s, loc, toks):
        self.log_pa.debug("Token: "+toks[0])
        n = ProcdefNode(toks[0])
        self._seen[toks[0]] = (loc, s)
        if len(toks) > 1:
            n.aggregation = True
            if toks[1] in self._var_stack:
                n.aggr_num = int(self._var_stack[toks[1]])
            else:
                n.aggr_num = int(toks[1])
        n.name = toks[0]
        return n

    def _create_definition(self, string, loc, tok):
        self.log_pa.debug("Left token: "+tok[0].data)
        self.log_pa.debug("Right token: "+tok[2].data)
        n = DefNode("=")
        n.left = tok[0]
        n.right = tok[2]
        n.process = tok[0].data
        if n.process in self._processes:
            message = "Process "+n.process+" already defined"
            self.log_pa.error(message)
            raise ProcessAlreadyDefinedError(message)
        self._processes[n.process] = n
        return n

    def _create_prefix(self,string, loc, tok):
        self.log_pa.debug("Tokens: " + str(len(tok)))
        if len(tok) > 1:
            self.log_pa.debug("Left token: " + tok[0].data)
            self.log_pa.debug("Right token: "+ tok[2].data)
            n = PrefixNode(".")
            n.left = tok[0]
            n.right = tok[2]
            return n
        else:
            self.log_pa.debug("Token: " + tok[0].data)
            return tok[0]

    def _create_choice(self,string,loc,tok):
        self.log_pa.debug("Tokens: " + str(len(tok)))
        if not tok[0] is None:
            if len(tok) <3:
                self.log_pa.debug("Token: "+ tok[0].data)
                return tok[0]
            else:
                self.log_pa.debug("Left token: " + tok[0].data)
                self.log_pa.debug("Right token: " + tok[2].data)
                n = ChoiceNode("+")
                n.left = tok[0]
                n.right = tok[2]
                return n

    def _create_coop(self,string, loc, tok):
        if not tok[0] is None:
            if len(tok) <3:
                self.log_pa.debug("Token: "+tok[0].data)
                return tok[0]
            else:
                self.log_pa.debug("Number of tokens" + str(len(tok)))
                self.log_pa.debug("Left token: "+tok[0].data)
                if tok[1].actionset is not None:
                    n = CoopNode("<"+str(tok[1].actionset)+">")
                    n.cooptype = "sync"
                    n.actionset = tok[1].actionset
                    self.log_pa.debug(n.actionset)
                else:
                    n = CoopNode("||")
                    n.cooptype = "par"
                if type(tok[2]).__name__ == "str":
                    self.log_pa.debug("String: "+tok[2])
                else:
                    self.log_pa.debug("Right token: "+tok[2].data)
                n.left = tok[0]
                n.right= tok[2]
                return n

    def _create_sync_set(self,string, loc, tok):
        if tok[0] != "||" and tok[0] != "<>":
            self.log_pa.debug("Non empty synset: " + str(tok))
            n = SyncsetNode("<>")
            n.actionset = tok
        else:
            self.log_pa.debug("Parallel")
            n = SyncsetNode("||")
            n.actionset = None
        return n

    def _create_subtree_aggregation(self, num, procname):
        """ Transforms Process[num] into AST subtree """
        first = CoopNode("||")
        first.cooptype = "par"
        last = first
        for i in range(2, num+1):
            nl = ProcdefNode(procname)
            if i == num:
                nr = ProcdefNode(procname)
                last.right = nr
            else:
                nr = CoopNode("||")
                nr.cooptype = "par"
                last.right = nr
            last.left = nl
            last = nr
        return first

    def _create_process(self,string, loc, tok):
        self.log_pa.debug("Start")
        if tok[0].left is not None or tok[0].right is not None:
            self.log_pa.debug("Token: "+tok[0].data)
            self.log_pa.debug("Non terminal - passing")
            return tok[0]
        else:
            if tok[0].asttype == ProcdefNode.asttype:
                n = ProcdefNode(tok[0].data)
                if tok[0].aggregation == True and n.aggr_num > 1:
                    n.aggregation = True
                    n.aggr_num = tok[0].aggr_num
                    n = self._create_subtree_aggregation(tok[0].aggr_num, tok[0].data)
                    n.asttype = "coop"
                    n.data = "||"
                    n.cooptype = "par"
                    n.actionset = None
            elif tok[0].asttype == ActivityNode.asttype:
                n = ActivityNode(tok[0].data)
                n.rate = tok[0].rate
                n.action = tok[0].action
            else:
                self.log_pa.error("This situation should not take place")
            self.log_pa.debug("Terminal - creating Node ->" + tok[0].asttype)
            self.log_pa.debug("Token: "+tok[0].data)
        return n

    def _create_system_equation(self, string, loc, tok):
        self.log_pa.debug("Creating system EQ")
        self._systemeq = tok[0]

    def _assign_var(self,toks):
        result = self.rate_parser.parse_rate_expr("".join(toks))
        if toks[0] not in self._var_stack:
            self._var_stack[toks[0]] = str(result)
        else:
            raise VariableAlreadyDefinedError("Variable {} has been already defined".format(toks[0]))

    def _check_var(self,str,loc,tok):
        try:
            float(tok[0])
        except:
            pass
        else:
            return
        if tok[0] not in ("infty", "T"):
            if tok[0] not in self._var_stack:
                raise VariableNotDefinedError("Rate {} not defined in {}".format(tok[0], loc))

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
        pound = Literal('#').suppress()
        percent = Literal('%').suppress()
        peparate = (ratename | floatnumber | passiverate).setParseAction(self._check_var)
        sync = Word('<').suppress() + ratename + ZeroOrMore(col + ratename) + Word('>').suppress()
        coop_op = (parallel | sync).setParseAction(self._create_sync_set)
        activity = (ratename + col + peparate).setParseAction(self._create_activity)
        procdef = (Word(alphas.upper(), alphanums+"_"+"`"+"'") + Optional(lsqpar + peparate + rsqpar)).setParseAction(self._create_procdef)
## RATES Definitions
        ratedef = Optional(percent)+(self.rate_parser.grammar()).setParseAction(self._assign_var) + semicol

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
        try:
            self.gramma().parseString(string, parseAll=True)
        except ParseException as e:
            raise
        for seen, location_info in self._seen.items():
            if seen not in self._processes:
                line = lineno(*location_info)
                column = col(*location_info)
                message = "{} process not defined - possible deadlock, line {}, col {}".format(seen,line, column)
                raise ProcessNotDefinedError(message)
        return (self._processes, self._var_stack, self._systemeq, self._actions)



