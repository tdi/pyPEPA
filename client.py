import socket
import sys
import gevent
import pepa_prot
from cmd import Cmd

rid = 1

workers = [ ('localhost', 6000),
            ('localhost', 6001) ]


class CLI(Cmd):

    prompt = "(PEPA) "
    intro = "Welcome to the PEPA client"

    def do_list_workers(self, arg):
        for worker in workers:
            print("%d %s" % ( workers.index(worker), worker) )

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
            for mod in data["ret"]:
                print("%s" % mod)
        except:
            print("Connection error")

    def do_solve_th(self, arg):
        """ solve_th MODEL WORKER """
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
        dat = {"cmd": "solve_th", "data" : args[0], "rid" :rid, "ret": "th"}
        data = send_recv( workers[int(args[1])], dat)
        print(data["ret"])




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
        print(data["ret"])


    def do_quit(self,arg):
        exit(1)

    def _parse(self,arg):
        return tuple(map(str, arg.split()))


def send_recv( address, dat):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
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
