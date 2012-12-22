import socket
import sys
import gevent
import pepa_prot
from cmd import Cmd
import time
from math import ceil
rid = 1

workers = [ ('localhost', 6000),
            ('192.168.1.23', 6000) ]

config = {"timing":1}

class CLI(Cmd):

    prompt = "(PEPA) "
    intro = "Welcome to the PEPA client"

    def do_list_workers(self, arg):
        for worker in workers:
            print("%d %s" % ( workers.index(worker), worker) )

    def do_check(self, arg):
        for worker in workers:
            try:
                send_recv(worker, {"cmd" : "chk"} )
                print("%s:%s OK" % worker)
            except:
                print("%s:%s FAILED" % worker)


    def do_list_models(self, arg):
        """ list_models WORKER_NUM """
        args = self._parse(arg)
        if len(args) != 1:
            print("Wrong arguments")
            return
        if args[0] == "all":
            jobs = []
            for i in workers:
                rid = rid + 1
                dat = {"cmd": "list_models" , "rid": rid}
                jobs.append(gevent.spawn(send_recv, i, dat))
            gevent.joinall(jobs)
            print("All done")
            return
        try:
            workers[int(args[0])]
        except:
            print("No such worker")
            return
        global rid
        rid = rid + 1
        dat = {"cmd": "list_models" , "rid": rid}
        try:
            data = send_recv( workers[int(args[0])], dat)
        except:
            print("Connection error")
        for mod in data["data"]:
            print("%s" % mod)

    def do_solve_th(self, arg):
        """ solve_th MODEL WORKER """
        global rid
        args = self._parse(arg)
        if len(args) != 2:
            print("Wrong arguments")
            return
        if args[1] == "all":
            jobs = []
            for i in workers:
                rid = rid + 1
                dat = {"cmd": "solve_th", "data" : args[0], "rid" :rid, "ret": "th"}
                jobs.append(gevent.spawn(send_recv, i, dat))
            gevent.joinall(jobs)
            print("All done")
            return

        try:
            workers[int(args[1])]
        except:
            print("No such worker")
            return
        rid = rid + 1
        dat = {"cmd": "solve_th", "data" : args[0], "rid" :rid}
        data = send_recv( workers[int(args[1])], dat)
        print(data["data"])

    def do_exp(self, arg):
        """ exp MODEL ACTION RATE VALUES WORKER """
        global rid
        args = self._parse(arg)
        rid = rid + 1
        if args[4] == "map":
            vals = [i for i in range(1,200)]
            cpus = len(workers)
            tasks = _carousel(vals, cpus)
            jobs = []
            if "timing" in config:
                start = time.time()
            for w in workers:
                job = tasks.pop(0)
                dat = {"cmd": "exp", "data" : args[0], "rid" :rid, "action": "use", "ret": "th", "rate":"userate","values":job, "map":1}
                jobs.append(gevent.spawn(send_recv, w, dat))
            gevent.joinall(jobs)
            if "timing" in config:
                stop = time.time() - start
                print("Time %s" % stop)
            print("All done")
            return
        vals = [i for i in range(1,200)]
        dat = {"cmd": "exp", "data" : args[0], "rid" :rid, "action": "use", "ret": "th", "rate":"userate","values":vals, "map":1}
        if "timing" in config:
            start = time.time()
        data = send_recv( workers[int(args[4])], dat)
        if "timing" in config:
            stop = time.time() - start
            print("Time %s" % stop)
        print(len(data["data"]))

    def do_solve_ss(self, arg):
        """ solve_ss MODEL WORKER """
        args = self._parse(arg)
        if len(args) != 2:
            print("Wrong arguments")
            return
        try:
            workers[int(args[1])]
        except:
            print("No such worker")
            return
        global rid
        rid = rid + 1
        dat = {"cmd": "solve_ss", "data" : args[0], "rid" :rid, "ret": "ss"}
        data = send_recv( workers[int(args[1])], dat)
        print(data["data"])


    def do_quit(self,arg):
        exit(1)

    def _parse(self,arg):
        return tuple(map(str, arg.split()))


def send_recv( address, dat):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        sock.connect(address)
    except Exception as e:
        raise
    tos = pepa_prot.prepare_to_send(dat)
    sock.send(tos)
    header_bytes = sock.recv(5)
    header = pepa_prot.extract_header(header_bytes)
    if not pepa_prot.check_version(header[1]):
        print("Protocol mismatch")
        exit(1)
    #TODO: zmienic w petelke
    data_bytes = sock.recv(header[0])
    sock.shutdown(socket.SHUT_RDWR)
    sock.close()
    return pepa_prot.extract_data(data_bytes)

def _carousel(sequence, m):
    if len(sequence) < m:
        m = len(sequence)
    n = float(len(sequence))
    return [sequence[((i+0)*int(n/m)):((i+1)*int(ceil(n/m)))] for i in range(m)]



# prepare_to_send = lambda x: struct.pack('!l',len(x)) + x


# def callback(socket, address):
#     print("Received callback from %s:%s" % address)
#     data = socket.recv(5)
#     print(data)
# 
if __name__ == "__main__":
    cli = CLI()
    loop = cli.cmdloop()
    gevent.spawn(loop)
    # server = StreamServer( ('0.0.0.0', 6001), callback)
    # address = ('localhost', 6000)
    # # dat = {"cmd": "solve_ss", "data":"resource.pepa","rid": rid, "ret":"ss"}
    # dat = {"cmd": "list_models" , "rid": rid}
    # try:
    #     sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #     sock.connect(address)
    # except Exception as e:
    #     print("Cannot connect to %s:%s" % address)
    #     exit(1)
    # print("Sending CMD:%s" % dat["cmd"])
    # tos = pepa_prot.prepare_to_send(dat)
    # sock.send(tos)
    # print("Answer")
    # header_bytes = sock.recv(5)
    # header = pepa_prot.extract_header(header_bytes)

    # print ("Length of data %i, protocol version %i" %(header[0], header[1]))
    # if not pepa_prot.check_version(header[1]):
    #     print("Protocol mismatch")
    # #TODO: zmienic w petelke
    # data_bytes = sock.recv(header[0])
    # data = pepa_prot.extract_data(data_bytes)
    # print(data)

    # server.serve_forever()
