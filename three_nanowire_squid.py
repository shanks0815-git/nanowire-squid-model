"""
Critical current vs magnetic field for a 3-nanowire SQUID.

Same linear current-phase relation as the 2-wire case, extended to three wires.
There are now two independent loops, so two vorticity indices (n and m) are
needed. psi2 and psi3 are both referenced to psi1: psi2 picks up half the flux
of psi3, which assumes wire 2 sits at the midpoint between wires 1 and 3.
"""

import math
import numpy as np
import matplotlib.pyplot as plt


def three_nanowire_model(cric1=1, cric2=1, cric3=1,
                         crip1=2 * math.pi, crip2=math.pi, crip3=2 * math.pi,
                         save_as=None):
    #there is two vortices now so have to loop through both
    for n in range(-4, 5):

        for m in range(-4, 5):
            blist = [];
            ilist_max = [];
            ilist_min = [];

            # outer loop is to trace through the magnetic field
            for b in np.linspace(-5, 5, 500):
                current_max = 0;
                current_min = 0;
                valid_found = False;
                first_point = True;

                # inner loop is to trace through the psi values
                for psi1 in np.linspace(-crip1, crip1, 500):
                    psi2 = psi1 + (math.pi * b) - (2 * math.pi * n);
                    psi3 = psi1 + (2 * math.pi * b) - (2 * math.pi * (n + m));

                    # adding continue like Cliff said
                    if abs(psi1) >= crip1 or abs(psi2) >= crip2 or abs(psi3) >= crip3:
                        continue

                    # If we are here, both wires are superconducting
                    valid_found = True;
                    total = ((cric1) * (psi1/crip1)) + ((cric2) * (psi2/crip2)) + ((cric3) * (psi3/crip3))

                    # NEW: Initialize the max/min with the first valid total found
                    if first_point:
                        current_max = total;
                        current_min = total;
                        first_point = False;

                    # Tracking both the max and min
                    if total > current_max:
                        current_max = total
                    if total < current_min:
                        current_min = total

                # only plotting the values that are valid and exist
                if valid_found:
                    blist.append(b)
                    ilist_max.append(current_max)
                    ilist_min.append(current_min)

            # Plot each diamond within the n-loop
            plt.plot(blist, ilist_max, 'b', alpha=0.1)
            plt.plot(blist, ilist_min, 'r', alpha=0.1)

    plt.xlabel("B field")
    plt.ylabel("Critical Current")
    plt.grid()
    if save_as:
        plt.savefig(save_as, dpi=130)
    else:
        plt.show()


if __name__ == "__main__":
    three_nanowire_model()
