import sys, os

def is_ascii_file(path):
    try:
        with open(path, 'rb') as f:
            data = f.read()
        data.decode('ascii')
        return True
    except Exception:
        return False

bad = []
for root, _, files in os.walk('.'):
    for fn in files:
        p = os.path.join(root, fn)
        if '.git' in p:
            continue
        if not is_ascii_file(p):
            bad.append(p)

if bad:
    print('Non-ASCII files detected:')
    for b in bad:
        print(b)
    sys.exit(1)
print('ASCII guard OK')
