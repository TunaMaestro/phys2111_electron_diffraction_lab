#align(center, text(1.5em)[
  *PHYS2111 Electron Diffraction --- Lab 1*
])

#set document(title: [PHYS2111 Electron Diffraction --- Lab 1],
  author: read("author.txt"))

#align(center)[
  Feburary 2025
]
#align(center)[
  #read("author.txt")
]


= Introduction

This experiment investigates the wave properties of electrons. Electrons, having momentum, have a De Broglie wavelength which we can observe through the wave proprty diffraction. Electrons are emitted from a cathode, then accelerated through a high voltage towards a screen. The electrons pass through a graphite powder, diffracting in the crystal lattice. The angle of deviation then results in a ring image on the screen.

= Aim

To observe electron diffraction and measure distances of graphite's latice spacing.

= Acknowledgements

Thanks Lukas.

= Theory

#set math.equation(numbering: "(1)")

NB: Mostly taken from the student notes.

The De Broglie wavlength equation is
$
  lambda = h / p.
$ <debroglie>

The momentum of an electron can be derived from its kinetic energy:

$
 "KE" = 1/2 m v^2 = p^2 / (2m) = e U_a.
$ <ke>

Using @debroglie and @ke we get:
$
  lambda = h / (sqrt(2 m e U_a)).
$

The Bragg condition for constructive interference gives maxima at:
$
  2 d sin theta = n lambda #h(1em)  ("for" n = 1, 2...).
$ <bragg>

Then, knowing that the angle of deviation, $alpha = 2 theta$ and using the small angle approximation, we can derive an expression for r:
$
  sin 2 alpha = r / R, \ 
  sin a = r / 2R, \
  sin theta = r / (4 R), \
$
$
  r = (2 R) / d n lambda.
$ <r_lambda>

To analyse the relationship we wish to plot a linear graph between voltage and radius.


$
  r = (2 n R) / d  h / sqrt(2 m e U_a)
$

Let our constant coefficient be $k = (2 n R h) / sqrt(2 m e)$ for each series of radii.

We could plot $r$ against $1/sqrt(U_a)$ but since $sqrt(U_a)$ is non-linear, we will instead square both sides. The reasoning is related to the inline resitor and is discussed later.
Therefore
$
  r^(-2) = 1/k^2   d^2  U_a.
$ <squared_with_k>

= Uncertainty Analysis

#let error(k) = {
  [$(Delta #k) / #k$]
}

=== Accelerating voltage

The accelerating voltage is plotted and analysed in such a way so that systematic errors (such as the inline resistor or other calibration errors) will not influence the final result. The error is not specified on the data sheet, so will be assumed to be 2%.

The voltage readout displays 1 decimal place, so the the uncertainty must be at least 0.05kV, which is within 2% for the voltage range in use.

=== Ring measurement

An inner and outer diameter were recorded for the maxima. The points of the diameter were eyeballed to be the closest area of dark screen to the ring. The radius was then derived from the average of the inner and outer diameter. The two diameter measurements were used to avoid the innacuracy due to the undefined nature of the centre of the ring. Diameter must be used instead of radii measurements as the centre of the ring, although illuminated by the central electron beam, can move around, and is itself an amorphous region. (Depending on the G4 focus voltage it can be sharp or large and blobby)

With these measures, it is reasonable to expect the diameter measurement is accurate to 2mm, and therefore the radius measurement to 1mm.

The radius of the apparatus $R approx 65"mm"$ will be taken as accurate to 1mm.

Therefore we have $error(d) = sqrt(error(R)^2 + error(r)^2 + error(U_a)^2) approx 5.6%$.

=== Statistical Uncertainty

The statistical uncertainty of $d$ was derived from the 95% confidence interval of each gradient.

= Analysis

See #link(<appendix>)[Appendix] for data table.

To plot a line of best fit, we can plot @squared_with_k as $y = m x + b$, where $x = U_a$ and $y = 1/r^2$, giving us
$
  d = sqrt(m k^2).
$

#grid(
columns: (50%, 50%),
inset:0pt,
figure(image("../plots/raw.png")),
figure(image("../plots/analysis.png"))
)

/**
Uncertainty outputs:
  Uncertainty for n=1
          Fitted Parameters: m = 1.350 ± 0.057, c = 461.957 ± 271.621
          Chi-Squared: 15.177, Reduced Chi-Squared: 0.843
          R-Squared: 0.979
          95% Confidence Interval for m: ±0.119, for c: ±570.655
          Relative uncertainty for m: 0.08824396296325338
  Uncertainty for n=2
          Fitted Parameters: m = 0.486 ± 0.019, c = -15.594 ± 89.404
          Chi-Squared: 23.373, Reduced Chi-Squared: 1.299
          R-Squared: 0.975
          95% Confidence Interval for m: ±0.040, for c: ±187.831
          Relative uncertainty for m: 0.08166575088325519
*/

The statistic uncertainties for each series are: \
$sigma_"1 stat" = 8.8%$ \
$sigma_"2 stat" = 8.2%$.

#par(
[From the gradients, we get: \
  $d_1 = 184 plus.minus 15_"stat" plus.minus 10_"sys" "pm" = 184 plus.minus 18 "pm"$, \
  $d_2 = 110 plus.minus 9.0_"stat" plus.minus 6.2_"sys" "pm" = 110 plus.minus 10.9 "pm"$.
]  
)

= Discussion

== In-series Resistor

There is a 10M Ohm resistor, '$"R"$', in series with the high voltage supply to limit current and protect the Wehnelt circuitry. This results in a voltage drop over $"R"$, making the display voltage $V_"src"$ unequal to the accelerating voltage. However, since $V_"src" = U_a + V_R$, we can rewrite @squared_with_k in terms of $V_"src"$ and a constant factor. Therefore the voltage drop does not influence the slope $m$, and hence $d$ is independent of the resistor.

$
  r^(-2) &= 1/k^2 d^2 (V_"src" - V_R) \
         &= 1/k^2 d^2 V_"src" + C \
         &= m x + C.
$

== Expected values

The expected values were sourced from this diagram of graphite's crystal structure.
#grid(
  columns: (50%, 50%),
  figure(
    image("graphite-lattice-student-notes.png"),
    caption: [Graphite planes for first two interference rings. #cite(<student_notes>)]
  ),
  figure(
    image("graphite-lattice-diagram.png"),
    caption: [Crystal structure of graphite. #cite(<carbon_geometry>)]
  )
)

Applying some geometry, this gives values $d_1 = 213"pm"$ and $d_2 = 123"pm"$.

This gives errors:
$
  error(d_1) = -13% "and" error(d_2) = -11%
$.

The errors are just outside the range of consistency for the calculated lattice spacings. This could indicates that there is a systematic error in the experiment, but more data would be required to evaluate the consistency of the approx. -12% error.
This could be due to Bragg's law being an insufficient model for electron diffraction. The factor could also be due to unnacounted for relativistic effects. The velocity of a 10keV electron is approximately 0.19c, but the equations used (@ke) use classical kinetic energy. The lorentz factor at this value is only around 2% so this is probably not a large component of the error.

== Diffraction effects

#table(
  stroke: (thickness: 0.1pt),
  columns: 3,
  [Voltage (kV)], [Wavelength (pm)], [Observation],
  [1.4], [32.8pm], [No diffraction effects],
  [1.7], [29.7pm], [Appear extremely faintly],
  [2.2], [26.1pm], [Appear strongly],
  [8.0], [13.7pm], [Appear strongly],
  [10.0], [12.3pm], [Appear strongly],
)

The electrons did not produce an interference at low voltages, and produces an image up until the highest tested voltage of 8kV.
The diffraction appears only within a certain band of wavelengths, but the range itself is unexpected. I had thought that diffraction mainly occured when the wavelength was within the order of the grating distances.
When there are no diffraction effects, the electrons behave as particles and travel straight from the sample to the centre of the screen.

= Conclusion

+ Electrons diffract under some conditions i.e. within a specific momentum range and
+ electrons therefore exhibit wave properties.
+ That a straight electron beam causes an image with maxima and minima demonstrates well that interference is occuring.


#pagebreak()
= Appendix <appendix>

== Measurements

#let results = csv("../data.csv")
#set table.cell(inset: (y: 3pt))
#table(
  stroke: (thickness: 0.1pt),
  columns: 4,
  [*Order*], [*Voltage (kV)*], [*Inner Diameter (mm)*], [*Outer Diameter (mm)*],
  ..results.flatten()
)

#bibliography("bib.bib", style: "american-physics-society")
