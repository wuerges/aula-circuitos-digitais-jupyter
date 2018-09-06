from BDD import *


x = BDD('x', ZERO, ONE)
y = BDD('y', ZERO, ONE)

z = x.land(y)

print(simplify(z))
