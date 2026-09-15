from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from check_docs import check_tree


class LinkChecks(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)

    def write(self, name, content=""):
        path = self.root / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
        return path

    def test_relative_links_images_and_directories(self):
        self.write("docs/page.md", "[home](../README.md) ![map](assets/map.png) [dir](assets/)")
        self.write("README.md")
        self.write("docs/assets/map.png")
        result = check_tree(self.root)
        self.assertEqual((result.documents, result.local, result.errors), (2, 3, []))

    def test_missing_document_and_asset(self):
        self.write("README.md", "[doc](missing.md) ![asset](missing.png)")
        result = check_tree(self.root)
        self.assertEqual(len(result.errors), 2)
        self.assertTrue(all("target does not exist" in error for error in result.errors))

    def test_encoded_unicode_spaces_query_and_fragment(self):
        self.write("README.md", "[doc](<docs/한 글.md#section>) ![x](assets/a%20b.png?v=1#x)")
        self.write("docs/한 글.md")
        self.write("assets/a b.png")
        self.assertEqual(check_tree(self.root).errors, [])

    def test_reference_style_collapsed_shortcut_and_nested_parentheses(self):
        self.write("README.md", '[full][a] ![a][] [a] [nested](a(b).png "title")\n\n[a]: a(b).png\n')
        self.write("a(b).png")
        result = check_tree(self.root)
        self.assertEqual((result.local, result.errors), (4, []))

    def test_html_links_and_assets(self):
        self.write("README.md", '<a href="page.md">page</a>\n<img src="a.png" />\n<video src="missing.mp4"></video>')
        self.write("page.md")
        self.write("a.png")
        result = check_tree(self.root)
        self.assertEqual((result.local, len(result.errors)), (3, 1))

    def test_external_urls_are_not_requested(self):
        self.write("README.md", "[a](https://unreachable.invalid/x) [b](http://invalid.test) [c](mailto:a@example.test) ![d](data:image/png;base64,AA) [e](//example.test/x)")
        result = check_tree(self.root)
        self.assertEqual((result.external, result.local, result.errors), (5, 0, []))

    def test_code_and_comments_are_not_references(self):
        self.write("README.md", '`[x](missing.md)`\n\n```md\n![x](missing.png)\n```\n\n<!-- <img src="missing.png"> -->\n\n    [code](missing.md)\n')
        result = check_tree(self.root)
        self.assertEqual((result.local, result.errors), (0, []))

    def test_same_document_fragment_is_not_anchor_validation(self):
        self.write("README.md", "[section](#not-checked) [query](?mode=demo)")
        self.assertEqual(check_tree(self.root).errors, [])

    def test_absolute_paths_and_escape_fail(self):
        self.write("README.md", "[a](/tmp/a) [b](../escape.md) [c](file:///tmp/a) [d](C:/a.png)")
        self.assertEqual(len(check_tree(self.root).errors), 4)

    def test_symlink_cannot_escape_root(self):
        with tempfile.TemporaryDirectory() as outside:
            external = Path(outside) / "asset.png"
            external.write_text("fixture")
            (self.root / "asset.png").symlink_to(external)
            self.write("README.md", "![x](asset.png)")
            self.assertIn("escapes repository", check_tree(self.root).errors[0])

    def test_dependencies_and_generated_directories_are_excluded(self):
        self.write("README.md")
        for folder in [
            "node_modules", ".git", ".venv", "build", ".next",
            "test-results", "playwright-report", ".local-data", ".local-assets",
        ]:
            self.write(f"{folder}/README.md", "[x](missing.md)")
        result = check_tree(self.root)
        self.assertEqual((result.documents, result.errors), (1, []))

    def test_cli_failure_then_recovery_from_another_directory(self):
        self.write("README.md", "![x](missing.png)")
        script = Path(__file__).resolve().parents[1] / "check_docs.py"
        args = [sys.executable, str(script), "--root", str(self.root)]
        failed = subprocess.run(args, cwd=self.temp.name, capture_output=True, text=True)
        self.assertEqual(failed.returncode, 1)
        self.assertIn("README.md:1", failed.stdout)
        self.write("missing.png")
        passed = subprocess.run(args, cwd=self.temp.name, capture_output=True, text=True)
        self.assertEqual(passed.returncode, 0)
        self.assertIn("PASS", passed.stdout)


if __name__ == "__main__":
    unittest.main()
