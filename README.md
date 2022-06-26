# datachef

> :warning: This software is a **work in progress**.

Datachef is a pet/passion project to create a ground up rewrite and extension of the functionality of https://github.com/sensiblecodeio/databaker

Databaker is a great tool, but it's getting a bit old and is wrapping some libraries that are now depreciated, making interoperation with other data related tools (notably pandas) quite challenging. There's also a lot of functionality I want to add that will be difficult it not impossible to add to the existing codebase. This includes things like docstrings, type hinting, api documentation and auto completion that have become much more the expected standard since databaker was first envisioned.

As much as possible I will support backwards compatibility with databaker scripts, likely with via importing a compatibility module (i.e wrap what will look and act like the databaker api around the datachef api).

The api signature will be extremely familiar to anyone familiar with databaker, though under the hood the code will be completely different, working in a much more modular and easily extensibly/configurable way.

There will also a be significant amount of additional functionality to deal with more complex use cases than were orginally envisioned or considered for databaker.

_Note - this page will be replaced with a more standard "this is what the software does" README when datachef is closer to release. If you're reading this we ain't there yet._
