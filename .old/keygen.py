import sys, random
import pprint

name, threshold = sys.argv
MAX = 1024

threshold = int(threshold)

coeff = {}
for i in range(threshold):
    coeff[i] = random.randint(0, MAX)

def make_poly(coeff: dict):

    def f(x):
        sum = 0
        for n, p in coeff.items():
            sum += p*x**n
        return sum

    return f

def probe(poly, x):
    out = {}
    for val in x:
        out[val] = poly(val)
    return out

def choise(population: list, k):
    copy = population.copy()
    out = []
    for _ in range(k):
        c = random.choice(copy)
        copy.remove(c)
        out.append(c)
    return out
pprint.pprint(coeff)
poly = make_poly(coeff)



linspace = list(range(1, threshold + 1))

atoms = probe(poly, linspace)


shared = choise(list(atoms.keys()), k = int(len(atoms) * .20))
shared_atoms = {}
for x in shared:
    shared_atoms[x] = atoms.pop(x)


pprint.pprint(atoms)

one = choise(list(atoms.keys()), k = int(len(atoms) * .50))
print(one)
one_atoms = {}
for x in one:
    one_atoms[x] = atoms.pop(x)

pprint.pprint(shared_atoms)
pprint.pprint(one_atoms)
pprint.pprint(atoms)