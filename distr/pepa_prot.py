import  cPickle as pickle
import struct

PROT_VERSION = 1
PICKLE_PROTOCOL = 2


def extract_data(y):
    data = pickle.loads(y)
    return data

def extract_header(y):
    head = struct.unpack('!lb', y)
    return head

def prepare_to_send(y):
    x = pickle.dumps(y,pickle.HIGHEST_PROTOCOL)
    return struct.pack('!lb',len(x),PROT_VERSION) + x

def check_version(ver):
    if ver != PROT_VERSION:
        return False
    return True

