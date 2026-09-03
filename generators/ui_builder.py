import os
def w(p, t):
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, chr(119), encoding=chr(117)+chr(116)+chr(102)+chr(45)+chr(56)) as f: f.write(t)
    print(chr(87)+chr(114)+chr(111)+chr(116)+chr(101)+chr(58), p)
