# Canva Planner Factory: How It Works

## Overview

Canva Planner Factory is a small Python-based system for creating polished, printable planner pages from structured JSON files.

You describe a planner set in JSON: its title, page concepts, section positions, prompts, writing areas, checklists, choices, and tables. The factory validates that description and converts it into a self-contained HTML document. Each generated page is exactly 816 × 1056 pixels, representing an 8.5 × 11-inch US Letter page.

The output uses ordinary HTML text, borders, lines, checkboxes, and tables instead of flattened images. This makes the pages suitable for browser review, printing, and import into Canva, where supported elements can remain editable.

## What the factory does

The factory can:

- Generate one-page or multi-page planner sets
- Produce exact US Letter page dimensions
- Create writing lines, checklists, choices, callouts, tables, split sections, and custom HTML areas
- Apply consistent typography, colors, borders, margins, spacing, and footers
- Detect blocks outside the page or below the safe printing area
- Detect overlapping blocks
- Warn when a page does not use enough of the available sheet
- Detect repeated page concepts and repeated prompt wording
- Create a ready-to-edit starter specification for any topic
- Validate a specification without generating output

It does not automatically upload files to Canva. Canva import and final visual verification remain separate human-reviewed steps.

## How it works

The workflow has five stages:

1. **Choose a topic and purpose.** Decide who the planner is for and what each page should help the user do.
2. **Create a JSON specification.** Define the planner set, pages, concepts, positioned blocks, and response formats.
3. **Validate the specification.** The factory checks geometry, page use, overlap, repeated concepts, and repeated wording.
4. **Generate HTML.** Valid JSON is rendered as one self-contained HTML document containing all planner pages.
5. **Review and import.** Open the HTML in a browser, inspect it at full and print size, correct any issues, and optionally import it into Canva.

```text
Topic and audience
        ↓
JSON planner specification
        ↓
Layout and content validation
        ↓
Editable US Letter HTML pages
        ↓
Browser review → Canva import → final verification
```

## What is needed

### Required

- Windows, macOS, or Linux
- Python 3.9 or newer
- The files in this repository
- A modern web browser such as Edge, Chrome, Firefox, or Safari
- A text editor for editing JSON

The generator uses only the Python standard library. No third-party Python packages are required.

### Optional

- A Canva account, if you want to import and continue editing the generated pages in Canva
- Git, if you want to clone the repository or track your changes
- An AI assistant, if you want help planning page concepts or drafting a JSON specification

## Download or clone the project

Download the repository as a ZIP from GitHub and extract it, or clone it with Git:

```bash
git clone https://github.com/smiln32/planner-pages-factory.git
cd planner-pages-factory
```

Because the repository is private, cloning requires GitHub access to the repository.

## Confirm Python is available

Run one of these commands:

```bash
python --version
```

or:

```bash
python3 --version
```

The reported version should be 3.9 or newer. On systems where the command is `python3`, substitute `python3` for `python` in the examples below.

## Fastest first run

Create a starter specification for a topic:

```bash
python planner_factory.py --init my-planner.json --topic "Morning Routine"
```

This creates `my-planner.json` with one complete example page. The topic is inserted into its title and footer.

Validate it:

```bash
python planner_factory.py my-planner.json my-planner.html --validate-only
```

Generate the planner:

```bash
python planner_factory.py my-planner.json my-planner.html
```

Open `my-planner.html` in a web browser. You should see a full US Letter planner page with four editable-content sections.

## Available commands

### Show the version

```bash
python planner_factory.py --version
```

### Create a starter specification

```bash
python planner_factory.py --init FILE.json --topic "TOPIC"
```

### Validate without generating

```bash
python planner_factory.py SPEC.json OUTPUT.html --validate-only
```

The output filename is still supplied for command consistency, but no HTML file is written in validation-only mode.

### Generate planner HTML

```bash
python planner_factory.py SPEC.json OUTPUT.html
```

## Understanding the JSON specification

A specification contains set-level information and an ordered list of pages:

```json
{
  "set_title": "Morning Routine Planner",
  "footer_label": "Simplify to Glorify | Morning Routine Planner",
  "pages": [
    {
      "concept": "Choose one realistic morning priority",
      "title": "My Morning Focus",
      "subtitle": "Begin with one useful next step.",
      "theme": "#b2c6b1",
      "blocks": []
    }
  ]
}
```

Each block has exact page coordinates and a content definition. For example:

```json
{
  "x": 28,
  "y": 104,
  "w": 760,
  "h": 260,
  "title": "What matters today",
  "color": "sage",
  "content": {
    "type": "lines",
    "prompt": "A few words are enough.",
    "rows": 7
  }
}
```

The complete field-by-field format is documented in [`SPECIFICATION.md`](SPECIFICATION.md).

## Supported response formats

- `lines` — open writing space
- `checklist` — labeled and blank checkbox rows
- `choices` — radio-style or checkbox-style options
- `callout` — short guidance with optional writing space
- `table` — repeated-row trackers and logs
- `split` — two related response areas
- `custom_html` — trusted custom markup for advanced cases

Prefer the standard types. They are easier to validate and keep visually consistent.

## Validation results

The factory returns one of three exit codes:

- `0` — generation succeeded or validation passed cleanly
- `1` — validation completed with advisory warnings
- `2` — invalid input or a validation error

Typical findings include:

- A block extends outside the 816 × 1056 page
- A block enters the header or footer area
- Two blocks overlap
- The content stops too high and leaves an accidental empty lower section
- Two pages use the same concept
- A prompt or section title is repeated

Correct errors before generating or publishing. Review warnings rather than automatically ignoring them.

## Design and content guidance

Three documents guide planner quality:

- [`DESIGN_STANDARD.md`](DESIGN_STANDARD.md) defines the grid, spacing, typography, colors, safe areas, and visual checks.
- [`CONTENT_GUIDE.md`](CONTENT_GUIDE.md) explains how to write supportive, specific, non-repetitive prompts.
- [`SPECIFICATION.md`](SPECIFICATION.md) documents the JSON format and all supported content types.

Give every page one distinct concept. A page should help the user notice, choose, plan, track, reflect, or act on one focused idea. Avoid repeating the same prompt, response format, and layout silhouette throughout a set.

## Reviewing generated pages

Before importing or publishing:

1. Open the generated HTML in a modern browser.
2. Review every page at 100% zoom.
3. Check the browser's print preview at US Letter size.
4. Confirm headings and prompts are not clipped.
5. Confirm writing areas are large enough to use.
6. Confirm boxes do not overlap and their corners are complete.
7. Confirm content reaches the lower portion of the page without entering the footer.
8. Read every prompt for usefulness, tone, repetition, and safety.

A file that generates successfully is not automatically a finished planner. Visual and editorial review are required.

## Canva workflow

After the browser review:

1. Create or open a US Letter design in Canva.
2. Import the generated HTML using the Canva workflow available to your account.
3. Confirm the expected page count.
4. Inspect every imported page rather than relying only on thumbnails.
5. Verify that text, lines, boxes, checkboxes, and tables remain editable where expected.
6. Correct any font substitution, clipping, alignment, or import changes.
7. Save or duplicate the verified Canva design before making experimental edits.

Canva import behavior can change, so the actual imported design must always be checked.

## Project structure

```text
planner_factory.py             Generator and validator
planner_spec_template.json     Reusable specification template
SPECIFICATION.md               Complete JSON reference
DESIGN_STANDARD.md             Visual and layout rules
CONTENT_GUIDE.md               Prompt and content guidance
NEW_CHAT_STARTER_PROMPT.md      AI-assisted creation workflow
examples/basic/                Small two-page example
examples/depression/           Full multi-page example
examples/adhd/                 ADHD PDF example
prompts/                       Reusable ideation prompts
assets/                        Repository preview images
tests/                         Automated unit tests
.github/workflows/             GitHub Actions validation
```

## Running the automated tests

From the repository root:

```bash
python -m unittest discover -s tests -v
```

The test suite checks example validation, exact page structure, overlap detection, duplicate concepts, starter-file behavior, and semantic version formatting.

GitHub Actions runs these checks automatically after every push to `main` and for pull requests. It also validates the basic and full depression specifications and exercises the CLI starter workflow.

## Troubleshooting

### `python` is not recognized

Install Python 3.9 or newer from the official Python website or your operating system's package manager. On macOS or Linux, try `python3`.

### JSON cannot be read

Check for missing commas, unmatched braces, invalid quotation marks, or non-JSON comments. Start from `planner_spec_template.json` or generate a new starter file.

### Validation returns warnings

Read each warning in the terminal. A warning usually indicates an underfilled page or another layout concern that needs human review.

### Validation returns an error

Correct invalid coordinates, page bounds, overlaps, missing pages, repeated concepts, or other reported errors. Error exit code `2` means the specification should not be treated as ready.

### The Canva import looks different

Check for font substitution and altered spacing. Compare the imported design with the browser-rendered HTML and adjust the specification or Canva design as needed.

## Mental-health and wellness planners

The factory can structure supportive reflection, but it is not a clinical tool and does not provide diagnosis, treatment, crisis care, or medical advice.

Health-related planners require careful human review. Content involving mental health, trauma, disability, medication, or crisis topics should be reviewed by an appropriately qualified professional before publication. Never use a planner as a substitute for emergency or professional support.

## Summary

To use Canva Planner Factory successfully, you need Python, a JSON specification, and a browser. The factory turns the JSON into precise US Letter HTML pages, validates common layout and repetition problems, and supports a human-reviewed path into Canva. The design, content, and specification guides provide the standards needed to turn generated output into a polished planner set.
