import numpy

def file_len(f):
    for i, l in enumerate(f):
        pass
    return i + 1

def get_ss_size(filename):
    with open(filename, "r") as f:
        f.seek(0,2)
        fsize = f.tell()
        f.seek (max (fsize-1024, 0), 0)
        lines = f.readlines()
    last_line = lines[-1:][0]
    return int( last_line.split(',')[0] )

def pepa_ss_parser(filename):
    sssize = get_ss_size(filename)
    f = open(filename, 'r')
    # create matrix lnum x lnum
    Q = numpy.zeros( (sssize, sssize), dtype=numpy.float64)
    last_seen_state = 1
    rowsum = 0.0
    for line in f:
       row = line.split(',')
       from_state = int(row[0])
       to_state = int(row[1])
       rate = float(row[2])
       Q[ from_state-1 , to_state-1 ] = rate
       if last_seen_state != from_state:
           Q[ last_seen_state-1 , last_seen_state-1] = -rowsum
           rowsum = 0.0
       rowsum += rate
       last_seen_state = from_state
    Q[ last_seen_state-1 , last_seen_state-1] = -rowsum
    return Q

