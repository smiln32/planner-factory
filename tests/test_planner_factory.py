import json
import tempfile
import unittest
from pathlib import Path

import planner_factory

ROOT = Path(__file__).resolve().parents[1]


class PlannerFactoryTests(unittest.TestCase):
    def load_example(self):
        return json.loads((ROOT / "examples" / "basic" / "spec.json").read_text(encoding="utf-8-sig"))

    def test_example_has_no_validation_findings(self):
        self.assertEqual(planner_factory.validate(self.load_example()), [])

    def test_render_uses_exact_letter_canvas_and_page_count(self):
        spec = self.load_example()
        html = planner_factory.render(spec)
        self.assertIn("width:816px;height:1056px", html)
        self.assertEqual(html.count('data-document-role="page"'), len(spec["pages"]))

    def test_duplicate_concepts_are_errors(self):
        spec = self.load_example()
        spec["pages"][0]["concept"] = "Daily focus"
        spec["pages"][1]["concept"] = "Daily focus"
        findings = planner_factory.validate(spec)
        self.assertTrue(any("repeat the same concept" in finding for finding in findings))

    def test_overlapping_blocks_are_errors(self):
        spec = self.load_example()
        spec["pages"][0]["blocks"][1].update(x=28, y=104, w=300, h=200)
        findings = planner_factory.validate(spec)
        self.assertTrue(any("overlap" in finding for finding in findings))

    def test_invalid_geometry_is_an_error(self):
        cases = [
            {"x": 28, "y": 104, "w": 179, "h": 200},
            {"x": 27, "y": 104, "w": 760, "h": 200},
            {"x": 28, "y": 103, "w": 760, "h": 200},
            {"x": 28, "y": 104, "w": 760, "h": 927},
            {"x": "bad", "y": 104, "w": 760, "h": 200},
        ]
        for geometry in cases:
            with self.subTest(geometry=geometry):
                spec = self.load_example()
                spec["pages"][0]["blocks"] = [{**geometry, "content": {"type": "lines"}}]
                self.assertTrue(any(finding.startswith("ERROR:") for finding in planner_factory.validate(spec)))

    def test_titles_and_prompts_are_checked_independently(self):
        spec = self.load_example()
        first, second = spec["pages"][0]["blocks"][:2]
        first["title"] = second["title"] = "Repeated section"
        first["content"]["prompt"] = "First unique prompt"
        second["content"]["prompt"] = "Second unique prompt"
        findings = planner_factory.validate(spec)
        self.assertTrue(any("repeats section title" in finding for finding in findings))

        second["title"] = "Unique section"
        second["content"]["prompt"] = "First unique prompt"
        findings = planner_factory.validate(spec)
        self.assertTrue(any("repeats prompt" in finding for finding in findings))

    def test_rendered_output_is_substantial_html(self):
        html = planner_factory.render(self.load_example())
        self.assertTrue(html.startswith("<!doctype html>"))
        self.assertGreater(len(html), 1000)

    def test_starter_spec_is_valid_and_topic_aware(self):
        spec = planner_factory.starter_spec("Morning Routine")
        self.assertEqual(planner_factory.validate(spec), [])
        self.assertIn("Morning Routine", spec["set_title"])
        self.assertEqual(len(spec["pages"]), 1)

    def test_version_is_semantic(self):
        self.assertRegex(planner_factory.VERSION, r"^\d+\.\d+\.\d+$")

if __name__ == "__main__":
    unittest.main()
