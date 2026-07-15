# Canva Planner Factory

Canva Planner Factory is a specification-driven toolkit for creating polished, printable planner pages for nearly any topic. It converts structured JSON into editable, Canva-importable HTML sized precisely for US Letter pages.

The project combines a consistent visual system with guidance for writing supportive, useful, and non-repetitive prompts. Each planner page is designed around one clear concept, with response formats and layouts chosen to match its purpose.

## What it provides

- Exact 816 × 1056 px US Letter pages
- Editable HTML text, writing lines, checkboxes, tables, and section containers
- Consistent typography, spacing, margins, borders, and color roles
- Validation for page bounds, underfilled layouts, overlapping blocks, repeated concepts, and repeated prompts
- Content guidance for encouraging reflection without shame, pressure, forced positivity, or unnecessary repetition
- Reusable JSON specifications for producing complete planner sets
- Example specifications and approved visual references

## Requirements

- Python 3.9 or newer
- A modern web browser for reviewing generated HTML
- A Canva account if you want to import and edit the finished pages in Canva

No third-party Python packages are required.

## Quick start

1. Clone or download this repository.
2. Read [`CONTENT_GUIDE.md`](CONTENT_GUIDE.md) for prompt-writing and page-uniqueness guidance.
3. Read [`DESIGN_STANDARD.md`](DESIGN_STANDARD.md) for the required visual and layout system.
4. Copy [`planner_spec_template.json`](planner_spec_template.json) and replace the sample content with your planner topic and pages.
5. Give every page a distinct `concept` and define its content blocks.
6. Validate the specification, generate the HTML, and inspect every page before importing it into Canva.

Generate a planner:

```bash
python planner_factory.py planner_spec.json output.html
```

Validate without creating an output file:

```bash
python planner_factory.py planner_spec.json output.html --validate-only
```

Validation messages are written to the terminal. Errors must be corrected before publication; layout warnings should be reviewed rather than ignored.

## Specification overview

A planner specification contains set-level information and a list of pages. Each page includes a title, subtitle, theme color, unique concept, and positioned content blocks.

```json
{
  "set_title": "My Planner",
  "footer_label": "My Brand | My Planner",
  "pages": [
    {
      "concept": "Choose one realistic priority",
      "title": "A Gentle Priority",
      "subtitle": "Make today smaller and more workable.",
      "theme": "#b2c6b1",
      "blocks": []
    }
  ]
}
```

See [`planner_spec_template.json`](planner_spec_template.json) and the [`examples`](examples) directory for complete examples.

## Supported content types

- `lines` — open writing space
- `checklist` — predefined and blank checklist items
- `choices` — radio-style or checkbox-style choices
- `callout` — short guidance followed by optional writing lines
- `table` — structured trackers and logs
- `split` — two related response areas
- `custom_html` — an advanced escape hatch for layouts not covered by the standard types

Use `custom_html` sparingly. Standard content types are easier to validate and keep visually consistent.

## Design principles

Every page should:

- Focus on one useful concept
- Ask specific, answerable questions
- Match the response format to the mental effort required
- Provide practical writing space
- Avoid repeating wording or composition from nearby pages
- Move gently from noticing toward a choice, support, or feasible next step
- Remain legible and editable after Canva import

The full visual requirements are documented in [`DESIGN_STANDARD.md`](DESIGN_STANDARD.md).

## Using the project with an AI assistant

[`NEW_CHAT_STARTER_PROMPT.md`](NEW_CHAT_STARTER_PROMPT.md) contains a reusable prompt for asking an AI assistant to create a new planner specification with this toolkit. Provide the desired topic, audience, page count, and outcomes.

AI-generated planner content and layouts still require human review. Inspect wording, usefulness, visual balance, cultural fit, accessibility, and every rendered page before publishing or selling a set.

## Mental-health and wellness content

This project can help structure supportive reflection, but it is not a clinical tool and does not provide diagnosis, treatment, crisis care, or medical advice.

Planners addressing mental health, trauma, disability, medication, or other sensitive health subjects should be reviewed by an appropriately qualified professional before publication. Crisis-related products should direct users to suitable local emergency or crisis resources and trusted human support.

## Canva workflow

The generator creates ordinary HTML elements rather than flattened page images. After generation:

1. Review the HTML at full size and print scale.
2. Correct clipping, overflow, cramped writing areas, or weak visual hierarchy.
3. Import the finished HTML into a US Letter Canva design.
4. Confirm the page count and inspect every imported page.
5. Verify that text and structural elements remain editable.

Canva import behavior may change over time, so always test the actual imported design before treating it as finished.

## Repository structure

```text
planner_factory.py             HTML generator and validator
planner_spec_template.json     Reusable planner specification template
CONTENT_GUIDE.md               Prompt, safety, and uniqueness guidance
DESIGN_STANDARD.md             Typography, spacing, color, and layout rules
NEW_CHAT_STARTER_PROMPT.md      Reusable AI-assisted creation workflow
examples/                      Small example specifications and outputs
reference/                     Approved visual references
```

## Contributing

Contributions that improve validation, accessibility, Canva editability, documentation, content types, or layout precision are welcome. Keep changes consistent with the content and design standards and include a representative example when introducing a new content type.

## License

This project is available under the [MIT License](LICENSE).
