### Design notes

Keep everything as stand along functions that operate on low level objects (typically `List[BaseCell]` or primitve objects.

The intention of this it to:

- Power the more obviously exposed methods that will make up most of a users selection methods.
- Also be availble to more oadvanced users for dealing with edge cases we have not yet accounted for.