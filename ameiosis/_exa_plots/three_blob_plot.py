import time
import numpy
import matplotlib.pyplot as plt


from lanchester import LanchesterSquare, LanchesterSquareAllies
from ameiosis.simulation import Blob, Faction, Engagement


if __name__ == "__main__":
    # Just some blobs.
    b1 = Blob(1500, .01)
    b2 = Blob(700, .01)
    b3 = Blob(500, .01)
    b4 = Blob(300, .01)

    # Now they have chosen sides.
    f1 = Faction('a', b1)
    f2 = Faction('b', b2, b3, b4)

    # The battle begins.
    engagement = Engagement(b1, b2, b3, b4, alg=LanchesterSquareAllies())

    # Do the simulation and rotate the matrix for plotting.
    t1 = time.time()
    mat = numpy.matrix(list(engagement.iterate_engagement(1000)))
    mat = numpy.rot90(mat)
    print("took: %0.4f" % (time.time() - t1))

    # plot it
    from itertools import cycle
    mat_list = mat.tolist()
    for matrix, ls, col in zip(mat_list,
                        cycle(['--', ':']),
                        cycle(['r', 'm', 'b', 'g', 'y', 'k'])):

        plt.plot(matrix, col+ls)
    plt.show()