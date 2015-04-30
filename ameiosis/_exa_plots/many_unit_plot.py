import time
from itertools import cycle

import numpy
import matplotlib.pyplot as plt

from lanchester.model import LanchesterSquareAllies
from lanchester.model.side import Engagement, Battalion, Faction


if __name__ == "__main__":
    # Just some sides.
    b1 = Battalion(10000, .01)
    #b2 = Battalion(10000, .01)
    b2 = [Battalion(1000, .01) for _ in range(10)]

    # Now they have chosen sides.
    f1 = Faction('a', b1)
    f2 = Faction('b', *b2)

    # The battle begins.
    engagement = Engagement(b1, *b2, alg=LanchesterSquareAllies())

    # Do the simulation and rotate the matrix for plotting.
    t1 = time.time()
    mat = numpy.matrix(list(engagement.iterate_engagement(1000)))
    mat = numpy.rot90(mat)
    print("took: %0.4f" % (time.time() - t1))

    # plot it

    mat_list = mat.tolist()
    for matrix, ls, col in zip(mat_list,
                        cycle(['--', ':']),
                        cycle(['r', 'm', 'b', 'g', 'y', 'k'])):

        plt.plot(matrix, col+ls)
    plt.show()