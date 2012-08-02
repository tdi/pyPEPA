#!/usr/bin/env python
from pprint import pprint
from colorama import Fore, Back

class StateSpace():
    operators = []
    components = []
    comp_ss = None
    STAN = ['(getm1,g_times_p).(use,m1).(relm1,r).P1+(getm2,g_times_1_minus_p).(use,m2).(relm2,r).P2', 'Bus', 'M1', 'M2']

    def __init__(self):
        self.max_length = 0


    def _combine_states(self, states):
        combined_states = []
        to_del = []
        to_states = [i.to_s for i in states]
        # TODO FIX OFFSETS
        for i in list( range(0, len(to_states))):
            if to_states[i] is None: continue
            for j in list (range(0, len(to_states))):
                if i!=j and to_states[i] == to_states[j]:
                    states[i].action += "," + states[j].action
                    to_del.append(j)
                    to_states[j] = None
                    combined_states.append(states[i])
        to_states = [i for i in to_states if i is not None]
        for tod in to_del:
            states.pop(tod)


    def derive(self):
        initial_state = []
        queue = []
        visited = []
        for oper in self.operators:
            oper.update_offset()
        for comp in self.components:
            initial_state.append(comp.name)
        queue.append(initial_state)
        #TODO: dodawac stan nowy, a nie stary
        #print(self.components)
        while(queue):
            state = queue.pop(0)
            if self._gs_to_string(state) in visited:
              continue
            if state == self.STAN:
                print("STATE " + str(state))
            visited.append(self._gs_to_string(state))
            # update components table (same refs are in operators)
            for i in list( range(0, len( state ),1)):
#                if not self.components[i].name == state[i]:
                self.components[i].update( state[i] )
            for x in list(range(0,self.max_length+1,1)):
                for op in self.operators:
                    if op.length == x:
                        if self.max_length == op.length:
                            new_states = []
                            new_states = op.compose(self.comp_ss, state, True)
                            if not new_states:
                                print("DEADLOCK in " + str(state))
                                exit(1)
                            self._combine_states(new_states)
                            for news in new_states:
                                # aggregate
                                if len(news.to_s) < self.max_length:
                                    new_state = state[:]
                                    new_state[news.offset] = news.to_s[0]
                                    news.to_s = new_state
                                if state==self.STAN:
                                    print(Fore.GREEN + "\t " + news.action + Fore.RESET + "\t"+ str(news.to_s))
                                if self._gs_to_string(news.to_s) not in visited:
                                    #print(self._gs_to_string(news.to_s) + " ", end="" )
                                    queue.append(news.to_s)
                        else:
                            op.compose(self.comp_ss , state , False)
        else:
            print( str( len(visited)))
    def _gs_to_string(self, gs_list):
        return ','.join( map( str, gs_list ) )



class Component():
    length = None
    offset = None
    name = None
    ss = None
    data = None

    def update(self, name):
        """
        Update with new name
        """
        self.name = name
        self.data = name #TODO: wyjebac
        self.derivatives = []
        # if self.name=="Bus":
        #     print("AAA")
        #     for trr in self.ss[self.name].transitions:
        #         print(trr.to)
        #     print("ZZZ")
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

class Derivative():

    def __init__(self, from_s, to_s, action, rate, offset,shared=False):
        self.from_s = from_s
        self.to_s = to_s
        self.action = action
        self.rate = rate
        self.shared = shared
        self.offset = offset

    def __str__(self):
        return " T:" + str(self.to_s) \
                + " Act:"+self.action+" R:"+self.rate+" O:"+str(self.offset)+" Sh:"+str(self.shared)

class Operator(Component):
    length = None
    offset = 0
    actionset = []
    lhs = None
    rhs = None
    STAN = ['(getm1,g_times_p).(use,m1).(relm1,r).P1+(getm2,g_times_1_minus_p).(use,m2).(relm2,r).P2', 'Bus', 'M1', 'M2']

    def __init__(self):
        self.actionset = []
        self.derivatives = []

    def update_offset(self):
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
        ddd = Derivative(state, to_state,tran_l.action,tran_l.rate,self.offset,True)
        return ddd



    def compose(self,ss, state, topop=False):
        self.derivatives =  []
        if state == self.STAN:
            print(Fore.BLUE + "OPERATOR" + str(self) + Fore.RESET)
        for tran_l in self.lhs.get_derivatives():
            # UNSHARED
            if tran_l.action not in self.actionset:
                self.derivatives.append(tran_l)
                new_state = state[:]
                new_state[tran_l.offset] = tran_l.to_s[0]
        #        print("\t/ "+str(tran_l))
        #        print("\tPS "+str(new_state))
            else:
                for tran_r in self.rhs.get_derivatives():
                    #FIXME: TU SIE KURWI
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
                        if state == self.STAN: print(Back.BLUE + "S H A R E D " + Back.RESET + str(tran_l))
                        if state == self.STAN: print(Back.CYAN + "S H A R E D " + Back.RESET + str(tran_r))
                        ddd = self._create_shared_trans(state, tran_l, tran_r)
#                        new_state[tran_r.offset] = tran_r.to_s[0]
#                        new_state[tran_l.offset] = tran_l.to_s[0]
                        if state == self.STAN: print(Back.MAGENTA + "S H A R E D OUT" + Back.RESET + str(ddd))
                        self.derivatives.append(ddd)
        for tran_r in self.rhs.get_derivatives():
            if tran_r.action not in self.actionset:
                self.derivatives.append(tran_r)
                #print("\t \\"+str(tran_r))
          #      print("\t PS "+str(new_state))
        if state==self.STAN:
            print(Fore.RED + "DERIVATIVES" + Fore.RESET)
            for ddd in self.derivatives:
                print("\t"+str(ddd))
        if topop == True:
            return self.derivatives




