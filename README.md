Thu 14 Apr 15:14:29 BST 2022

This repository contains some small tests generating perceptual
colour palettes for Grafana. These were intended for use in the
IRIS Accounting Portal. Currently there is a tool compile the 
Grafana colour mapping config from a set of fixed colours generated
by some web service. The idea was to automate the palette generator
with a local script, and to have that script generate more accessible
colours. 

The tool attempts to select colours which are equidistant in the
human perceptual space (using CIELAB) for any number of colours, 
therefore making them more distinguishable. It is possible to
pick a set of colours in HSV, H being the "colour" equally spaced
around a circle, but these vary in brightness and distinguishability
depending on the wavelength. It is not as easy to pick a set of
equidistant colours in a nonparametric space (CIELAB), so an optimiser
is used to nudge the colours as far away as possible from each other
as would be seen by a person.

Currently the tool is *not very useful* when compared to the simpler
approach of using a web tool to optimise the colours. But it does
mean that it still needs to be handled manually when new data fields 
are added to the palette. 

This repository acts to archive the attempts made and you are encouraged
to pick up the work if it becomes relevant again.






