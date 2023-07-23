# Validation

By default datachef supports three types of validation.

- Simple selection assertions (`assert_one()`, `assert_len()`, `assert_single_row()`, `assert_single_clumn()`
- Validation via the `<selection>.valdiation()` method.
- Validation via the `Column(validation=)` keyword.

This section contains some simple examples of using a mixture of these approaches. To do this we're going to add validation _to example provided elsewhere in the documentation_.

## Important

These techniques have a place because they _give you contextual information_ on where the issue is.

Neverthless if you're going to be using datachef in any sort of productionized ETL system further external checks would be typical and probably wise.

## Data Disclaimer

Precisely how to correctly extract, dimension and categorize extracted data is an art all of its own and _very dependent on domain expertise_ and _very subject to contrary opinions_, as such I'm not even going to try and make no claims whatsoever as to whether or to what extent any of the examples are "correctly" represented after extraction from their original sources.

To put it another way these are purely examples of **how** to extract data with code, the correct/best/ideal structure and categorization for any and all examples I leave to others to debate as it has no bearing on our goal of teaching people how to use these tools.