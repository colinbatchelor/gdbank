import sys
with open(sys.argv[1]) as f, open(sys.argv[2], 'w') as g:
    for line in f:
        if not line.startswith('#'):
            g.write(line)
        
