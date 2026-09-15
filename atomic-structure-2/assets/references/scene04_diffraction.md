# Scene 4: moving waves and calculated diffraction

The opening uses light-field pulses and localized detector flashes.
The matter-wave graphs display real amplitude, with continuous phase motion;
they are not drawings of an electron following a sinusoidal trajectory.

The quantitative speed example uses k proportional to momentum and omega
proportional to k squared, with arbitrary slow playback time. The wavelength
bracket and numerical readout retain the existing de Broglie calculation.
Dense cricket-ball illustrations cap the displayed phase rate to prevent
temporal aliasing; the logarithmic ruler gives the actual length comparison.

The crystal is an illustrative 3 × 7 periodic array with elastic, coherent,
single-scattering amplitudes in the far-field approximation. Its amplitude is

A(theta) = exp[-0.5 (sin(theta)/0.65)^2]
           × mean_j exp[i (2 pi/lambda)
             ((1-cos(theta)) x_j - sin(theta) y_j)].

Drawing coordinates use transverse spacing 0.66 and wavelength 0.25.
They are schematic, not material-specific lattice measurements.
A smooth atomic envelope reduces scattering at large angles.
The image stretches the far-field angular distribution for readability:
moving crests show phase, while the angular amplitude envelope stays fixed.

Detector arrivals are sampled from |A(arctan(y/L))|². The displayed intensity
curve uses that same function. Three strong maxima emerge from the calculation;
weak subsidiary maxima are retained. No Gaussian band positions are prescribed.

The science audit checks unit forward intensity, symmetry, an exact
seven-row destructive-interference zero, and a nonzero first diffraction order.
These checks would fail if the complex amplitudes were replaced by incoherent
intensity addition.

Sources:
- [OpenStax: The Wave Nature of Matter](https://openstax.org/books/college-physics/pages/29-6-the-wave-nature-of-matter)
  explains electron diffraction and its connection to de Broglie wavelength.
- [OpenStax: Diffraction Gratings](https://openstax.org/books/university-physics-volume-3/pages/4-4-diffraction-gratings)
  explains the phase condition for constructive interference from periodic
  scatterers. The finite-array model above applies coherent phase summation
  to an illustrative two-dimensional lattice.

Scene 4 narration now explains A_j, amplitude addition and squared magnitude.
The chapter remains 150 seconds; all 19 narration exports match the source.
