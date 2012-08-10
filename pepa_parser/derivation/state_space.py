#!/usr/bin/env python
from colorama import Fore, Back

class StateSpace():
    operators = []
    components = []
    comp_ss = None
    STATE = "['Robot', 'Belt', '(ready_to_pick,xi).(ready_to_pick,infty).Table', 'Press', 'DBelt_1', 'Crane']"


    def __init__(self):
        self.max_length = 0

    def _combine_states(self, states):
        """ When more than one transition leads to the same state,
            the function combines these transitions into one with actions rewritten
        """
        for i in list( range(0, len(states))):
            #FIXME: if None then exception
            if states[i] is not None and len(states[i].to_s) == 1:
                continue
            if states[i] is not None:
                for j in list (range(i+1, len(states))):
                    if states[j] is not None:
                        if states[i].to_s == states[j].to_s:
                            states[i].actions = {}
                            states[i].actions[states[i].action] = states[i].rate
                            states[i].combined = True
                            states[i].action += "," + states[j].action
                            states[i].rate =  float(states[i].rate) + float(states[j].rate)
                            states[i].actions[states[j].action] = float(states[j].rate)
                            states[j] = None
        states = [i for i in states if i is not None]
        return states


    def derive(self):
        """ Derives the whole state space according to BU"""
        initial_state = []
        queue = []
        visited = []
        resulting_states = {}
        actions_to_state = {}
        state_num = 0
        for x in list(range(0,self.max_length+1,1)):
            for op in self.operators:
                if op.length == x:
                    op.update_offset()
        for comp in self.components:
            initial_state.append(comp.name)
        #print(list(filter(lambda x: print(x), self.operators)))
        queue.append(initial_state)
        while(queue):
            state = queue.pop(0)
            if self._gs_to_string(state) in visited:
              continue
            state_num = state_num + 1
            #print("in{}".format(state_num))
            #print("{} STATE {}".format(state_num, state))
            resulting_states[self._gs_to_string(state)] = ([],state_num)
            visited.append(self._gs_to_string(state))
            # update components table (same refs are in operators)
            for i in list( range(0, len( state ),1)):
                self.components[i].update( state[i] )
            # if self.STATE == str(state):
                # print(list(filter(lambda x: print(x), self.components)))
            for x in list(range(0,self.max_length+1,1)):
                for op in self.operators:
                    if op.length == x:
                        if self.max_length == op.length:
                            new_states = []
                            new_states = op.compose(self.comp_ss, state, True)
#                            if self.STATE == str(state):
#                                for n in new_states:
#                                    print(n)
                            if not new_states:
                                print("DEADLOCK in {}".format(state))
                                exit(1)
                            #dostaje w tej samej i combinuje
                            new_states = self._combine_states(new_states[:])
                            for news in new_states:
                                # aggregate
                                if len(news.to_s) < self.max_length:
                                    new_state = state[:]
                                    new_state[news.offset] = news.to_s[0]
                                    news.to_s = new_state
                                #print(Fore.GREEN + "\t " + news.action + " " + Back.WHITE + Fore.BLACK  + str(news.rate) + Back.RESET + Fore.RESET + "\t"+ str(news.to_s))
                                resulting_states[self._gs_to_string(state)][0].append( (news.rate, self._gs_to_string(news.to_s)))
                                #handle combines actions, not very elegant so to be changed
                                if news.combined:
                                    for act in news.actions:
                                        self._add_to_actions_set(act, news.actions[act], actions_to_state, state_num)
                                else:
                                    self._add_to_actions_set(news.action, news.rate, actions_to_state, state_num)

                                if self._gs_to_string(news.to_s) not in visited:
                                    queue.append(news.to_s)
                        else:
                            op.compose(self.comp_ss , state , False)
        return (resulting_states, actions_to_state)

    def _add_to_actions_set(self, action, rate,actions_to_state, state_num):
        if rate == "infty":
            print("Resulting rate cannot be infty in {} in state {}".format(action, state_num))
            exit(1)
        if (action,state_num) not in actions_to_state:
            actions_to_state[ (action, state_num) ] = float(rate)
        else:
            #check if the same stateand action, so we add rates
            actions_to_state[ (action, state_num) ] += float(rate)

    def _gs_to_string(self, gs_list):
        """ TODO: wywalic do osobnych toolsow """
        return ','.join( map( str, gs_list ) )

class Component():
    length = None
    offset = None
    name = None
    ss = None
    data = None
    STATE = "['Robot', 'Belt', '(ready_to_pick,xi).(ready_to_pick,infty).Table', 'Press', 'DBelt_1', 'Crane']"

    def update(self, name):
        """
        Update with new name
        """
        self.name = name
        self.data = name #TODO: wyjebac
        self.derivatives = []
        for der in self.ss[self.name].transitions:
            self.derivatives.append(Derivative(self.name, [der.to], der.action, der.rate, self.offset))


    def __init__(self, ss, name,offset):
        self.name = name
        self.ss = ss
        self.offset = offset
        self.derivatives = []
        for der in self.ss[self.name].transitions:
            self.derivatives.append(Derivative(self.name, [der.to], der.action, der.rate, self.offset))

    def get_derivatives(self):
        return self.derivatives

    def __str__(self):
        return self.name


class Derivative():

    def __init__(self, from_s, to_s, action, rate, offset,shared=False):
        self.from_s = from_s
        self.to_s = to_s
        self.action = action
        self.rate = rate
        self.shared = shared
        self.offset = offset
        self.combined = False

    def __str__(self):
        return " T:" + str(self.to_s) \
                + " Act:"+self.action+" R:"+self.rate+" O:"+str(self.offset)+" Sh:"+str(self.shared)

class Operator(Component):
    length = None
    offset = 0
    actionset = []
    lhs = None
    rhs = None
    STATE = "['Robot', 'Belt', '(ready_to_pick,xi).(ready_to_pick,infty).Table', 'Press', 'DBelt_1', 'Crane']"

    def __init__(self):
        self.actionset = []
        self.derivatives = []

    def update_offset(self):
        print("updating {} with {}".format(self, self.lhs.offset))
        if self.lhs is not None:
            self.offset = self.lhs.offset

    def get_derivatives(self):
        return self.derivatives

    def __str__(self):
        return "<" + str( self.actionset ) + ">"

    def _create_shared_trans(self, state, tran_l, tran_r):
        to_state = state[:]
        for i in list(range(0, self.lhs.length)):
            to_state[self.lhs.offset + i] = tran_l.to_s[self.lhs.offset + i]
        for i in list(range(0, self.rhs.length)):
            to_state[self.rhs.offset + i] = tran_r.to_s[self.rhs.offset + i]
#            to_state[i] = tran_r.to_s[i]
        new_rate = self._min(tran_r.rate, tran_l.rate)
        ddd = Derivative(state, to_state,tran_l.action,new_rate,self.offset,True)
        return ddd

    def _create_unshared_trans(self, state, tran):
        to_state = state[:]
        for i in list(range(0, self.lhs.length)):
            to_state[self.lhs.offset + i] = tran.to_s[self.lhs.offset + i]
        ddd = Derivative(state, to_state, tran.action, tran.rate, self.offset, False)
        return ddd


    def compose(self,ss, state, topop=False):
        self.derivatives =  []
        for tran_l in self.lhs.get_derivatives():
            # UNSHARED
            if tran_l.action not in self.actionset:
                new_state = state[:]
                new_state[tran_l.offset] = tran_l.to_s[0]
                self.derivatives.append(tran_l)
        #        print("\t/ "+str(tran_l))
        #        print("\tPS "+str(new_state))
            else:
                for tran_r in self.rhs.get_derivatives():
                    if tran_r.action == tran_l.action:
                        new_state = state[:]
                        if len(tran_r.to_s) == 1:
                            new_tran_s = new_state[:]
                            new_tran_s[tran_r.offset] = tran_r.to_s[0]
                            tran_r.to_s = new_tran_s
                        if len(tran_l.to_s) == 1:
                            new_tran_s = new_state[:]
                            new_tran_s[tran_l.offset] = tran_l.to_s[0]
                            tran_l.to_s = new_tran_s
                        ddd = self._create_shared_trans(state, tran_l, tran_r)
                        self.derivatives.append(ddd)
        for tran_r in self.rhs.get_derivatives():
            if tran_r.action not in self.actionset:
                self.derivatives.append(tran_r)
        if topop == True:
            return self.derivatives


    def _min(self,rate1, rate2):
        if rate1 == "infty":
            if rate2 == "infty":
                return "infty"
            else:
                return rate2
        if rate2 == "infty":
            if rate1 == "infty":
                return "infty"
            else:
                return rate1
        return min(rate1,rate2)

