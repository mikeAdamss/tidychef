Work in progress pet/passion project. A ground up rewrite of the functionality of (excellent but getting a bit old): https://github.com/sensiblecodeio/databaker. Full credit and acknowlagments will be given.

Aiming for:

- A more object orientated extensible design with exhaustive test coverage.
- Stand alone app rather than wrapper to avoid the depreciated dependency issues plaguing databaker at the moment.
- Minimise dependendencies and keep any of the format parsing libraries (pyexcel etc) as optional and on-demand.
- Create some awareness of a DSD with the stretch goal of two way transformations, possible creation of simple csvws.
- Enable the ability to implement (without necesserily doing so) the tracking of provenance information as part of transforms.
- Enable the concept of "engines" for resolving topic to observation relationships, allow simple updates to or variations of these resolving classes to allow optimisation for different use cases/shapes.
- Support creation of spreadsheet from tidy data as well as tidy data from spreadsheet.
- Decouple inputs as well as "selectors" so you can chop and change inputs sources and input selection methods relatively easily without touching the principle code base.
- Enable pivoting of some of the more obvious formats databaker does not do: csv, ODF, google sheets, html tables
- Avoid using pandas directly, as anyone using this will also almost certainly be using some variation of pandas but not always the latest, we don't want to be constantly fighting unnecessary versioning battles.
- Enable detailed doc strings, documentation and examples.
- We eventually want C bindings to speed up the more low level comparative operations. To begin with break up the process enough that these operations happen in distinct decoupled places (so we can drop in C code later without restructuring).
- Decide whether pivoter is a good name or a stupid one.
