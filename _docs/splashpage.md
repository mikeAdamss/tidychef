## installation

Datachef can be installed from pypi via `pip install datachef`

_note: not true (yet) at time of writing_.

You can run datacheck via any python interpreter you want to, but the examples and documentation will tend to use Jupyter notebooks/labs/books as its html rendering works particularly well with the datachef preview functionality. 


## the datachef book

The "datachef book" is a series jupyter book (connected and organised jupyter notebooks) designed to gradually introduce a new user to the full functionality of datachef via well documented, contextualised examples.

- [see the example (opens a new window)](./example.html) to get an idea what datachef does and if it satisfies your use case(s) 
- [view the book (opens a new window)](./example.html) 

_# note: both the above links are just to a holding file for now._


## real life use cases

A repository of data transformation examples using datachef. These are all real life use cases showing the transformation of messy open data to well strcutured machine readable data.

[TODO - link wont work!]()

_note: as a interim during development, if you open any of the py files in `./datachef/scenarios` with a jupyter notebook or lab and run them, you should get an idea of the functionality we're building out here_.

## development

In addition to the API documentation (see "Submodules" in the left hand menu) the [datachef github repo](https://github.com/mikeAdamss/datachef) also contains details on design choices, guidelines for contributing and an explanation of how datachef can be extended and customised. 


## test strategy

We have two rounds of testing that new builds of the codebase must pass.

**1.) Unit Tests**

100% test coverage is required before a build will succeed.

**2.) Scenarios**

Optional tests of more complex interactions. Uses jupyter notebooks to confirm that the output under each new code release remains as expected. This serves as both a primitive form of regression and behavioural testing.

Each "scenario" consists of:

- A `.py` representation of a notebook stored in `./scenarios/scenarios`
- The expected html output of said notebook once ran stored in `./scenarios/expected`

The comparisson will be triggered using pytest but as a separate test stage, so code coverage will not be effected. This is _supplementary_ to the standard unit tests, not instead of.

