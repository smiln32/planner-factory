---
name: Planner Studio
description: A professional working atelier for building customer-ready planner sets.
colors:
  ink: "#343a38"
  ink-soft: "#4d4d4d"
  canvas: "#ececec"
  surface: "#ffffff"
  border: "#606864"
  rule: "#aeb7b2"
  sage: "#b2c6b1"
  sage-soft: "#dfe9df"
  lavender: "#c6b5c8"
  lavender-soft: "#e8dfea"
  slate: "#7b9fb3"
  slate-soft: "#dce8ee"
  blush: "#e6d7d3"
  blush-soft: "#f0e6e2"
typography:
  display:
    fontFamily: "Georgia, Times New Roman, serif"
    fontSize: "23px"
    fontWeight: 700
    lineHeight: 1.05
    letterSpacing: "-0.25px"
  body:
    fontFamily: "Aptos, Helvetica Neue, Arial, sans-serif"
    fontSize: "16px"
    fontWeight: 400
    lineHeight: 1.5
  title:
    fontFamily: "Aptos, Helvetica Neue, Arial, sans-serif"
    fontSize: "18px"
    fontWeight: 700
    lineHeight: 1.25
  label:
    fontFamily: "Aptos, Helvetica Neue, Arial, sans-serif"
    fontSize: "14px"
    fontWeight: 700
    lineHeight: 1.3
rounded:
  control: "8px"
  container: "10px"
  panel: "12px"
spacing:
  xs: "4px"
  sm: "8px"
  md: "14px"
  lg: "24px"
  xl: "32px"
components:
  button-primary:
    backgroundColor: "{colors.ink}"
    textColor: "{colors.surface}"
    rounded: "{rounded.control}"
    padding: "10px 16px"
  button-secondary:
    backgroundColor: "{colors.surface}"
    textColor: "{colors.ink}"
    rounded: "{rounded.control}"
    padding: "10px 16px"
  input:
    backgroundColor: "{colors.surface}"
    textColor: "{colors.ink}"
    rounded: "{rounded.control}"
    padding: "10px 12px"
  planner-block:
    backgroundColor: "{colors.surface}"
    textColor: "{colors.ink}"
    rounded: "{rounded.container}"
    padding: "11px 13px"
---

# Design System: Planner Studio

## Overview

**Creative North Star: "The Working Atelier"**

Planner Studio is a professional work surface with the calm, material clarity of a well-run creative studio. The interface stays restrained so customer content and printable page previews remain visually dominant; color identifies tools, selection, page roles, and validation state rather than decorating empty space.

The product should feel deliberate without becoming precious. Dense editing controls are allowed when they accelerate real work, but the interface must progressively reveal advanced choices and keep the active page understandable at a glance. It explicitly rejects generic AI-generator styling, interchangeable dashboard decoration, unexplained automatic choices, and template-first experiences that erase the creator's judgment.

**Key Characteristics:**

- Restrained application chrome around a true-to-size planner preview.
- Precise 14px layout rhythm carried from the page system into the editor.
- Professional controls with creative color used for orientation and selection.
- Flat, print-aware surfaces with strong borders and no decorative effects.
- Immediate, accessible feedback for every edit and validation result.

## Colors

The Working Atelier palette pairs charcoal working ink with muted studio colors borrowed directly from the generated planner pages.

### Primary

- **Working Ink** (`ink`): Primary actions, active tool labels, and high-contrast text.
- **Studio Sage** (`sage`, `sage-soft`): Current selection, successful validation, and calm page themes.

### Secondary

- **Proof Lavender** (`lavender`, `lavender-soft`): Alternate page roles and secondary selection groups.
- **Layout Slate** (`slate`, `slate-soft`): Structural tools, guides, and information states.

### Tertiary

- **Review Blush** (`blush`, `blush-soft`): Gentle review prompts and non-critical attention states; never use it as the sole error signal.

### Neutral

- **Canvas Gray** (`canvas`): Workspace outside pages and panels.
- **True Surface** (`surface`): Editor panels, fields, and printable pages.
- **Structural Border** (`border`): Interactive boundaries and page-block outlines.
- **Quiet Rule** (`rule`): Writing lines, separators, and inactive guides.

**The Orientation Rule.** Color groups and orients; it never fills space merely to make the interface feel creative.

**The One Dominant Theme Rule.** A planner page carries one dominant theme color and only restrained supporting fills.

## Typography

**Display Font:** Georgia (with Times New Roman and serif fallbacks)
**Body Font:** Aptos (with Helvetica Neue, Arial, and sans-serif fallbacks)

**Character:** Georgia gives planner titles an authored, printable voice. Aptos keeps the editing interface practical, compact, and familiar. No third family is introduced.

### Hierarchy

- **Display** (700, 23px, 1.05): Planner-page titles inside the true-size preview only.
- **Headline** (700, 20px, 1.2): Primary workspace and flow headings.
- **Title** (700, 18px, 1.25): Panel and page-editor headings.
- **Body** (400, 16px, 1.5): Instructions and descriptive copy, capped near 70 characters per line.
- **Label** (700, 14px, 1.3): Form labels, tool names, and validation categories in sentence case.

**The Two-Family Rule.** Georgia belongs to planner artifacts; Aptos belongs to the product interface. Never use Georgia for buttons, fields, navigation, or status text.

**The Sentence-Case Rule.** Avoid tracked uppercase scaffolding. Short all-caps text is reserved for existing table headers where scan speed genuinely improves.

## Elevation

The system is flat by design. Depth comes from surface color, complete borders, adjacency, and sticky positioning—not shadows, gradients, glass, texture, or decorative blur. A selected draggable block may use a crisp focus outline, but it never floats on an ambient shadow.

**The Flat Workshop Rule.** If a panel needs a wide soft shadow to feel separate, its hierarchy or boundary is wrong.

## Components

### Buttons

- **Shape:** Compact working controls with gently curved corners (8px).
- **Primary:** Working Ink background, True Surface text, and 10px × 16px padding.
- **Hover / Focus:** Hover darkens the ink slightly; focus uses a 3px Layout Slate outline with 2px offset. Active state moves no more than 1px and never bounces.
- **Secondary:** True Surface background, Working Ink text, and a complete Structural Border.

### Chips

- **Style:** Used for page-pattern categories and active filters, with an 8px corner rather than exaggerated pills.
- **State:** Unselected chips use True Surface and Structural Border; selected chips use Studio Sage Soft plus a Working Ink checkmark and text.

### Cards / Containers

- **Corner Style:** Complete 10–12px corners.
- **Background:** True Surface against Canvas Gray.
- **Shadow Strategy:** None; see the Flat Workshop Rule.
- **Border:** Full 1–1.2px Structural Border where containment must be explicit.
- **Internal Padding:** 14px for compact tools, 24px for major panels.

### Inputs / Fields

- **Style:** White field, complete Structural Border, 8px corners, and a persistent visible label.
- **Focus:** 2px Layout Slate outline with 2px offset; never rely on border color alone.
- **Error / Disabled:** Errors include a text explanation and icon; disabled fields remain legible and explain why when the reason is not obvious.

### Navigation

A compact workspace header holds project identity, undo/redo, save state, preview, and export. Page navigation is a labeled sequence rather than anonymous thumbnails. Active items combine Studio Sage Soft, Working Ink, and a clear current-page indicator. On narrow screens, editing panels move below the preview instead of shrinking controls below usable sizes.

### Planner Canvas and Blocks

The preview preserves the exact 816 × 1056 proportion. Blocks snap to a 3-unit grid with 14px gutters and remain inside x=28–788 and y=104–1030. Selection uses a crisp Layout Slate outline and visible move handle. Dragging announces the destination to assistive technology; keyboard users can move blocks between named grid slots and undo every change.

## Do's and Don'ts

### Do:

- **Do** keep the planner preview visually dominant and the application chrome restrained.
- **Do** use 14px as the core layout rhythm and preserve exact printable safe areas.
- **Do** pair every color-coded state with text, shape, or an icon.
- **Do** explain recommendations and validation findings in creator language.
- **Do** provide complete hover, focus-visible, active, disabled, loading, error, success, and empty states.

### Don't:

- **Don't** create generic AI-generator styling, interchangeable dashboard decoration, or unexplained automatic choices.
- **Don't** let template-first experiences erase the creator's judgment.
- **Don't** use shadows, gradients, glassmorphism, textures, clipped decoration, or decorative grid backgrounds.
- **Don't** use colored side-stripe borders, gradient text, giant rounded cards, or identical card grids as visual scaffolding.
- **Don't** allow drag interactions to create overlap, off-page content, invalid gutters, or inaccessible pointer-only workflows.