# Audit existing tests

Use this workflow when the task asks to find or remove low-value tests. Discovery stays read-only until there is evidence for a specific candidate. Optimize for confidence, not a deletion count.

Inspect the complete test, the production entry point and owner, non-test callers, sibling implementations, overlapping tests, CI routing, and relevant history. If a dependency's behavior matters, inspect its source or types. Prefer a few high-confidence candidates in one coherent owner area over a large speculative inventory.

For each candidate, record:

- Its exact name and location, and the failure it can actually detect.
- The production path or test-support seam it exercises, including non-test callers.
- The stronger remaining proof at the owning boundary, or why the contract needs no retained test.
- The history that explains why it exists, plus any risk of removing it.
- The edit it enables and the focused validation command.

A missing answer means the candidate is not ready for deletion. A failing retained test may expose a product bug; reproduce that failure before deciding what to remove. Keep a test that independently guards a public API, protocol, config, migration, storage, security, platform, generated artifact, package, or release contract, even when it looks static. Source inspection can be appropriate when it is the cheapest independent guard and survives behavior-preserving refactors.

Edit one owning area at a time. Remove obsolete test-only production seams when they have no production callers. If a weak test is the only useful proof of a real contract, replace it at the owning boundary before deleting it. Do not add a substitute that repeats the same implementation detail. Run focused owner and sibling checks, any executable command that replaces a source-only assertion, and the repository's required changed-file checks. Report retained false positives, the evidence for removals, and production versus test changes.
