from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from check_markdown import check_markdown, findings
from test_pstack_sync import commit, initialize, write


class MarkdownTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name) / "repo"
        initialize(self.root)

    def test_unchanged_caller_detects_deleted_target_and_baselines_old_errors(self):
        write(self.root, "README.md", "[Target](docs/target.md)\n[Existing placeholder](url)\n")
        write(self.root, "docs/target.md", "# Target\n")
        commit(self.root)
        (self.root / "docs/target.md").unlink()
        report = check_markdown(self.root)
        self.assertEqual(len(report["errors"]), 1)
        self.assertIn("docs/target.md", report["errors"][0])
        self.assertEqual(report["existing_errors"], 1)

    def test_code_and_examples_allow_legitimate_markdown_syntax(self):
        text = """# Guide

```markdown
CONFLICT_EXAMPLE
# Repeated
# Repeated
[Example](missing.md)
```

    [Indented example](missing.md)
`[Inline example](missing.md)`

## First
### Run
## Second
### Run
""".replace("CONFLICT_EXAMPLE", "<" * 7 + " example")
        errors, warnings = findings({"README.md": text}, lambda _: False)
        self.assertFalse(errors)
        self.assertFalse(warnings)

    def test_conflicts_fail_but_duplicate_headings_are_review_notices(self):
        write(self.root, "README.md", "# Guide\n")
        commit(self.root)
        write(self.root, "README.md", "# Guide\n## Step 4\nFirst\n## Step 4\nAgain\n<<<<<<< local\n")
        report = check_markdown(self.root)
        self.assertEqual(len(report["errors"]), 1)
        self.assertIn("conflict marker", report["errors"][0])
        self.assertEqual(len(report["warnings"]), 1)

    def test_changed_code_is_reported_without_failing(self):
        write(self.root, "README.md", "# Example\n```sh\necho old\n```\n")
        commit(self.root)
        write(self.root, "README.md", "# Example\n```sh\necho new\n```\n")
        report = check_markdown(self.root)
        self.assertFalse(report["errors"])
        self.assertEqual(report["code_blocks_changed"], ["README.md"])

    def test_relative_reference_image_and_encoded_links(self):
        write(self.root, "README.md", "# Guide\n")
        write(self.root, "docs/a (b).md", "# Target\n")
        commit(self.root)
        write(self.root, "README.md", '[Nested](docs/a%20(b).md)\n[Spaced](<docs/a (b).md>)\n[ref]: docs/a%20%28b%29.md "Title"\n![Missing](missing.png)\n[External](https://example.invalid/file)\n')
        report = check_markdown(self.root)
        self.assertEqual(len(report["errors"]), 1)
        self.assertIn("missing.png", report["errors"][0])

    def test_new_untracked_document_is_checked(self):
        write(self.root, "README.md", "# Guide\n")
        commit(self.root)
        write(self.root, "new.md", "[Broken](absent.md)\n")
        self.assertEqual(len(check_markdown(self.root)["errors"]), 1)


if __name__ == "__main__":
    unittest.main()
