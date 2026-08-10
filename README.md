# Nanowire SQUID Critical Current Model

Numerical model of critical current versus magnetic field for superconducting
nanowire SQUIDs, for 2-wire and 3-wire geometries. Written as part of the
nanowire qubit work in the Bezryadin group.

## The model

Each nanowire is treated with a linear (triangular) current-phase relation
rather than the usual sinusoidal Josephson relation:

```
I(psi) = Ic * (psi / psi_c)     valid while |psi| < psi_c
```

Once the phase drop across a wire exceeds its critical phase `psi_c`, that wire
is no longer superconducting and the configuration is discarded.

The wires share a loop, so their phases are not independent. Fluxoid
quantisation ties them together through the applied field `b` (in units of the
flux quantum) and an integer vorticity index. For a given field, the code sweeps
the phase across the first wire, derives the remaining phases from the
quantisation condition, throws out any configuration where a wire has gone
normal, and records the largest and smallest total current over what survives.
Each vorticity index traces out its own branch, and stacking the branches gives
the full interference pattern.

## Scripts

### `two_nanowire_squid.py`

Two wires, one loop, one vorticity index `n`:

```
psi2 = psi1 + 2*pi*b - 2*pi*n
```

Run it directly, or import and call `two_nanowire_model()`. Default parameters
are `cric1 = 2`, `cric2 = 1`, `crip1 = 2*pi`, `crip2 = pi`.

The envelope caps at the sum of the critical currents, so `+/- 3` with these
defaults, and the pattern repeats with period 1 in `b`.

![2 nanowire result](figures/two_nanowire.png)

### `three_nanowire_squid.py`

Three wires means two independent loops, so a second vorticity index `m` is
needed. Both `psi2` and `psi3` are referenced back to `psi1`:

```
psi2 = psi1 + pi*b     - 2*pi*n
psi3 = psi1 + 2*pi*b   - 2*pi*(n + m)
```

The factor of two between the two flux terms is the physical assumption in this
version. It says the wire1-wire2 loop encloses half the flux of the wire1-wire3
loop, which corresponds to wire 2 sitting at the midpoint between wires 1 and 3.
For unevenly spaced wires this ratio would need to change to match the actual
enclosed areas.

Run it directly, or import and call `three_nanowire_model()`. Defaults are all
three critical currents set to 1, with `crip1 = 2*pi`, `crip2 = pi`,
`crip3 = 2*pi`. The envelope caps at `+/- 3` as expected.

![3 nanowire result](figures/three_nanowire.png)

## Running

```
pip install -r requirements.txt
python two_nanowire_squid.py
python three_nanowire_squid.py
```

Both functions take an optional `save_as` argument to write the figure to a file
instead of opening a window:

```python
from three_nanowire_squid import three_nanowire_model
three_nanowire_model(save_as="figures/three_nanowire.png")
```

## Notes

The 3-wire model is slower than the 2-wire one, since it sweeps 81 combinations
of `(n, m)` instead of 8 values of `n`. The grid is 500 x 500 there and
1000 x 1000 in the 2-wire case.

Parameter values in both scripts are placeholders chosen to make the structure
of the pattern clear. They are not fitted to a measured device.
