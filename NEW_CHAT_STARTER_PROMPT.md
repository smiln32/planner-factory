# New Chat Starter Prompt — Canva Planner Factory

Upload this folder, then paste the request below with your topic and desired page count.

---

Create a complete, editable Canva planner set about: **[TOPIC]**.

Read `CONTENT_GUIDE.md`, then `DESIGN_STANDARD.md`, then inspect the approved reference HTML. Treat those files as requirements.

Before writing the JSON, make a private page blueprint. Give every page one sharply defined `concept`, one intended benefit, one mental task, one response form, and one composition. Remove semantic duplicates. Do not show me generic approval checkpoints; make sound decisions and complete the set.

Content requirements:

- Use supportive, specific, non-judgmental language. Never diagnose, prescribe, promise outcomes, force disclosure, or use toxic positivity.
- Keep each page focused on one concept and give it a small arc: arrive, notice, choose, act, close.
- Match response effort to the user’s likely capacity. Use bounded choices for low-energy moments and generous writing space for reflection.
- Where useful, translate intention into an if-then plan or one feasible next step.
- Do not repeat page concepts, prompts, section titles, interaction patterns, or adjacent layout silhouettes. Track wording across the whole set before finalizing.
- For health or mental-health topics, include appropriate scope/support language and flag the set for professional review before publication.

Design requirements:

- Exactly 816 x 1056 px per page, full safe-area use, precise aligned geometry, harmonious 14 px gutters, and no overlaps.
- Use the typography and palette in `DESIGN_STANDARD.md`; sentence-case section labels; no decorative clutter.
- Keep all content editable after Canva import. Use supported content types before `custom_html`.
- Write a complete JSON spec from `planner_spec_template.json`, run validation, generate HTML, and correct every error, collision, overflow, underfill, and repetition warning.
- Visually inspect every rendered page at full size and print scale. Then import to Canva and verify page count, clipping, editability, and complete corners.
- Give me the Canva edit link first when Canva access is available. Otherwise provide the finished HTML and JSON and state exactly what remains to import.

Set details:

- Page count: [COUNT]
- Audience/context: [AUDIENCE]
- Desired pages or outcomes: [LIST]
- Brand/footer: Simplify to Glorify | [TOPIC] Planner
