"""
Critical current vs magnetic field for a 2-nanowire SQUID.

Each wire is modelled with a linear (triangular) current-phase relation,
I(psi) = Ic * psi / psi_c, valid while |psi| < psi_c. The two wires share one
loop, so their phases are tied together by fluxoid quantisation with an integer
vorticity n.
"""

import math;
import numpy as np
import matplotlib.pyplot as plt


def two_nanowire_model(cric1=2, cric2=1, crip1=2 * math.pi, crip2=math.pi, save_as=None):
    # Loop through different fluxon states (vorticity)
    for n in range(-4, 4):
        blist = [];
        ilist_max = [];
        ilist_min = [];

        # outer loop is to trace through the magnetic field
        for b in np.linspace(-5, 5, 1000):
            current_max = 0;
            current_min = 0;
            valid_found = False;
            first_point = True;

            # inner loop is to trace through the psi values
            for psi1 in np.linspace(-crip1, crip1, 1000):
                psi2 = psi1 + (2 * math.pi * b) - (2 * math.pi * n);

                # adding continue like Cliff said
                if abs(psi2) >= crip2:
                    continue

                # If we are here, both wires are superconducting
                valid_found = True;
                total = ((cric1) * (psi1/crip1)) + ((cric2) * (psi2/crip2))

                # NEW: Initialize the max/min with the first valid total found
                if first_point:
                    current_max = total
                    current_min = total
                    first_point = False

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
        plt.plot(blist, ilist_max)
        plt.plot(blist, ilist_min)

    plt.xlabel("B field")
    plt.ylabel("Critical Current")
    plt.grid()
    if save_as:
        plt.savefig(save_as, dpi=130)
    else:
        plt.show()


if __name__ == "__main__":
    two_nanowire_model()
