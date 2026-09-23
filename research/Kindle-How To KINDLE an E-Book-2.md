## Prototype 003 answer: what failed, and what replaces it

The practical rule now is:

> **Do not ask Kindle to preserve composed space. Ask Kindle to preserve reading flow, and give it plates wherever space carries meaning.**

Prototype 003 is failing in four specific places: duplicated page-breaking, long live background containers, live directional geometry, and multi-column relational navigation. The Kindle-native replacements are: **spine-start chapters with no first/last page-break rules; per-entry body fields or short color blocks, not long nested panels; atomic PNG plates for spatial meaning; and one-row-per-link navigation.**

---

# 1. Blank pages before new spine entries

## Diagnosis

The blank page is most likely a **double pagination request**:

1. The next chapter/entry is already a separate XHTML spine item.
2. Its first element, wrapper, or heading may also carry `break-before`, `page-break-before`, `break-before: right`, or `page-break-before: always`.
3. Or the previous spine item ends with `break-after` / `page-break-after`.
4. Or the new opener is wrapped in a large `break-inside: avoid` block, so Kindle moves the whole opener forward and leaves the current page empty.

Amazon documents that Kindle Enhanced Typesetting supports `break-before`, `break-after`, `break-inside`, and the legacy `page-break-*` forms with `always`, `auto`, and `avoid`, and that Kindle checks these properties when deciding page breaks. Amazon does **not** document a special “double blank page” bug, so the exact blank-page mechanism remains empirical; the supported-property interaction is official. ([Kindle Direct Publishing][1])

## Build rule

Yes: **remove all first-element page-break declarations from any XHTML file that is already its own spine item.**

Also remove final-element `break-after/page-break-after` rules from the previous spine item unless you have a tested reason to keep one.

Use this pattern instead:

```html
<body class="bht-entry bht-entry-11">
  <article id="entry-11" epub:type="chapter">
    <h1>See What Has Become Possible</h1>

    <p class="threshold">
      Short live threshold prose begins here.
    </p>

    <p>Live prose continues normally.</p>
  </article>
</body>
```

```css
html,
body {
  margin: 0;
  padding: 0;
}

body.bht-entry {
  margin: 0;
  padding: 0;
}

article {
  margin: 0;
  padding: 1em 0 0 0;
}

h1 {
  margin: 0 0 0.85em 0;
  padding: 0;
  text-align: left;
  line-height: 1.2;
}

/* Critical: absent on first elements in split spine files */
h1,
article,
.bht-entry-start {
  break-before: auto;
  page-break-before: auto;
}

/* Critical: absent at the end of split spine files */
.bht-entry-end {
  break-after: auto;
  page-break-after: auto;
}
```

Do **not** use this on a first heading in a split spine item:

```css
h1 {
  page-break-before: always;
  break-before: always;
}
```

Do **not** use this on the final block of the previous entry:

```css
.last-block {
  page-break-after: always;
  break-after: always;
}
```

Do **not** wrap the whole chapter opener like this:

```css
.chapter-opener {
  break-inside: avoid;
  page-break-inside: avoid;
  min-height: 80vh;
}
```

That combination is exactly how you invite giant whitespace.

---

# 2. Long colored fields drifting away from prose

## Diagnosis

Amazon officially supports `background-color` and related background properties in Enhanced Typesetting, and Enhanced Typesetting can adjust font color for contrast over background colors. But Amazon also warns against forced body text colors/backgrounds as a general reading experience problem and requires testing reflowable books in white, black, mint, and sepia background modes. ([Kindle Direct Publishing][2])

What Amazon does **not** document clearly is how a long `div` background is painted when the block fragments across several Kindle pages. Your screenshot symptom—background and prose getting vertically out of phase—is therefore best treated as an **undocumented fragmentation behavior**, not a mistake to outsmart with more CSS.

## Replacement mechanism

Use one of these, in this order:

| Field type                                          | Kindle-native replacement                                                                           |
| --------------------------------------------------- | --------------------------------------------------------------------------------------------------- |
| Whole entry is a color-world                        | Put the entry in its own XHTML file and apply the field to `body`/`article`, with minimal wrappers. |
| Short threshold / callout / source boundary         | Use a short bounded live block with padding and background color.                                   |
| Long multi-page field whose exact start/end matters | Split it into its own spine entry, or make the field/diagram an image plate.                        |
| Gradient/bloom/atmosphere                           | Bake it into a plate.                                                                               |
| Background meaning depends on alignment with prose  | Do not leave it as a long live wrapper.                                                             |

For a whole-entry color field:

```html
<body class="bht-entry field-west">
  <article id="west">
    <h1>West</h1>

    <p class="threshold">
      Live threshold language.
    </p>

    <p>Live prose continues across as many Kindle pages as needed.</p>
  </article>
</body>
```

```css
body.field-west {
  margin: 0;
  padding: 0;
  background-color: #221b28;
  color: #f4efe8;
}

body.field-west article {
  margin: 0;
  padding: 1em 0;
  background-color: transparent;
}

body.field-west p,
body.field-west h1 {
  color: inherit;
}
```

But this must be tested in **white, black, mint, and sepia** modes. Amazon explicitly includes those background modes in its QA checklist. ([Kindle Direct Publishing][3])

For a short colored live block:

```html
<section class="field-note">
  <p>This short field can stay live because it does not span multiple pages.</p>
</section>
```

```css
.field-note {
  margin: 1em 0;
  padding: 0.8em 0.9em;
  background-color: #eee5d6;
}

.field-note p {
  margin: 0;
}
```

Avoid long wrappers like:

```html
<section class="giant-color-field">
  <!-- five pages of prose -->
</section>
```

Kindle-native replacement: **body field if the whole entry is colored; short blocks if local; plate if spatial/atmospheric.**

---

# 3. Atomic plates: Western Tellings and Jules

## Diagnosis

Western Tellings worked because Kindle had almost nothing spatial to recompute. The title, prose, source boundary, caption, and navigation remained live; the relational field became one image. That matches Amazon’s image guidance better than the live Grid/absolute attempts: Amazon recommends block images, `display:block; width:100%; object-fit:contain`, live captions, alt text, and special care that text-bearing diagrams/maps remain legible. It specifically recommends that images containing letters, numbers, or symbols occupy at least **80% of screen width** on smaller devices. ([Kindle Direct Publishing][4])

So yes: **live frame + atomic relational plate is now the default BHT pattern for composed meaning.**

## Plate format

For BHT diagrams with typography, flat color, nodes, labels, and relation geometry:

| Format                   |              Use? | Reason                                                                                                                                                                                                                                   |
| ------------------------ | ----------------: | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **PNG**                  |       **Default** | Best practical choice for flat color, labels, hard edges, and predictable appearance.                                                                                                                                                    |
| JPEG                     | No, except photos | Compression can blur type/lines.                                                                                                                                                                                                         |
| External SVG via `<img>` |         Test-only | Amazon says computer-generated visuals are well represented as SVG, but warns SVG tags can cause errors and recommends using the image tag; Enhanced Typesetting also flags SVG namespace-prefix issues. ([Kindle Direct Publishing][4]) |
| Inline SVG               |             Avoid | Too many unsupported/ignored SVG/CSS edge cases; harder to diagnose.                                                                                                                                                                     |
| Transparent PNG          |  Avoid for fields | Amazon says images with transparent areas are not supported and transparent backgrounds are converted to white. ([Kindle Direct Publishing][4])                                                                                          |

## Plate CSS

Yes: critical plates should generally be this simple:

```css
figure.plate {
  margin: 1.2em 0;
  padding: 0;
  text-align: center;
}

figure.plate img {
  display: block;
  width: 100%;
  height: auto;
  object-fit: contain;
  margin: 0 auto;
}

figure.plate figcaption {
  margin: 0.5em 0 0 0;
  text-align: center;
  text-indent: 0;
  font-size: 0.9em;
}
```

Do **not** put the plate inside an aspect-ratio frame, `min-height`, `max-height`, `vh`, or `break-inside: avoid` wrapper unless a specific test proves it helps.

## Plate size

Amazon gives a percentage target, not a universal pixel width: **text-bearing diagrams should occupy at least 80% of screen width**. It does not publish a current “BHT-style diagram must be N pixels wide” rule. ([Kindle Direct Publishing][4])

Practical BHT source sizes:

| Target                     | Practical source width | Notes                                               |
| -------------------------- | ---------------------: | --------------------------------------------------- |
| Small e-ink / phone stress |           1400–1600 px | Minimum for label-bearing plates.                   |
| Paperwhite-class           |           1600–2000 px | Good default.                                       |
| Scribe / tablet            |           2200–2600 px | Use for plates with many labels.                    |
| Very dense relational maps |      Split or simplify | Do not solve density only by making one huge plate. |

Keep plate height moderate. A plate that is too tall will be scaled down to fit a page and can become unreadable. Amazon’s QA checklist says large pictures should scale to fit the page and display in their entirety on one screen, which means a tall plate will likely be shrunk, not split. ([Kindle Direct Publishing][3])

Practical BHT height rule:

| Plate ratio                                   | Recommendation                           |
| --------------------------------------------- | ---------------------------------------- |
| Up to ~4:3 or 3:4                             | Usually safe.                            |
| Tall portrait field, ~1:1.4                   | Test carefully.                          |
| Taller than ~1:1.6                            | Split into two plates or redesign.       |
| Contains text under ~18–22 px at source scale | Too small; increase label size or split. |

## Image + caption

Use live caption immediately after the image. Amazon explicitly says not to raster the caption into the image and gives a `figure > img + figcaption` sample with `figure { width:100%; } img { display:block; width:100%; object-fit:contain; }`. ([Kindle Direct Publishing][4])

Do **not** force a giant keep-together block around image + caption. Let the image remain atomic; let the caption sit close through normal flow. If a caption occasionally lands on the next page, that is better than a full blank page caused by `break-inside: avoid`.

---

# 4. Family compass / directional geometry

## Direct answer

No: there is no live Kindle technique I would trust for:

```text
        North

West — Jules — East

        South
```

when the directional relation is part of the meaning.

Amazon’s Enhanced Typesetting support table lists `display:flex`, `inline flex`, `table cell`, `block`, `inline`, and related values, but it does **not** list CSS Grid. Grid also returned no match in the support table. ([Kindle Direct Publishing][2])

## Technique comparison

| Technique                | Kindle status                                                                                                                                                                                             | BHT decision                                                |
| ------------------------ | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------- |
| CSS Grid                 | Unsupported / not documented                                                                                                                                                                              | Do not use.                                                 |
| Flexbox                  | Supported in the table, but not geometry-safe                                                                                                                                                             | Do not use for compass meaning.                             |
| HTML table               | Can preserve a rough 3×3 arrangement                                                                                                                                                                      | Semantically wrong unless the content is genuinely tabular. |
| Absolute-positioned HTML | Not a safe reflowable mechanism; `position` is not in the supported list, and Amazon’s own internal-error examples include `position:absolute` plus inherited dimensions. ([Kindle Direct Publishing][2]) | Do not use.                                                 |
| External SVG via `<img>` | Worth one experiment for simple lines/shapes                                                                                                                                                              | Secondary option only.                                      |
| PNG plate                | Most predictable                                                                                                                                                                                          | Default.                                                    |

A table is accessible and Kindle-smart when it is actually tabular. Amazon recommends HTML tables for tabular content because they paginate and can be exposed to screen readers, but warns that image tables are not accessible and that wide tables are poor UX. A compass relation is not a data table; using a table only to force geometry creates false semantics. ([Kindle Direct Publishing][5])

So yes: **plate all five family-compass diagrams if directional geometry is meaning.** Preserve interpretation with live heading, caption, alt, and extended description.

---

# 5. Navigation: replace crushed multi-column maps

## Safest Kindle markup

Use one-column lists. One link per row. No Grid, no columns, no side-by-side pairing.

```html
<nav aria-label="Entry questions" class="bht-rel-nav">
  <ol>
    <li>
      <a href="entry-03.xhtml">
        <span class="question">What happened?</span>
        <span class="destination">03 · Gravity</span>
      </a>
    </li>
    <li>
      <a href="entry-04.xhtml">
        <span class="question">What changed?</span>
        <span class="destination">04 · The Shape Begins</span>
      </a>
    </li>
  </ol>
</nav>
```

```css
.bht-rel-nav {
  margin: 1.2em 0;
  padding: 0;
}

.bht-rel-nav ol {
  margin: 0;
  padding: 0;
}

.bht-rel-nav li {
  list-style-type: none;
  margin: 0 0 0.65em 0;
  padding: 0;
}

.bht-rel-nav a {
  display: block;
  padding: 0.55em 0;
  text-decoration: none;
  border-top: 0.05em solid currentColor;
}

.bht-rel-nav .question,
.bht-rel-nav .destination {
  display: block;
}

.bht-rel-nav .question {
  font-weight: bold;
}

.bht-rel-nav .destination {
  margin-top: 0.15em;
}
```

Amazon’s navigation guidance requires clickable HTML links, says not to build a table of contents with table tags because tables are for tabular data rather than layout, says no page numbers, and supports only two levels of Kindle navigation nesting. ([Kindle Direct Publishing][6])

For in-book relational maps, I would use ordinary lists or a shallow `<nav aria-label="...">`. Avoid nested content-level `<nav>` if it makes the file harder to reason about. The formal package/navigation document can remain the real EPUB nav; in-book maps can simply be linked lists.

Yes, `display:block` on `<a>` is a safe current property because `display:block` is in the Enhanced Typesetting supported display values. ([Kindle Direct Publishing][2])

---

# 6. Jules and similar fields

## Should diagram labels remain live?

No, not if label placement is part of the diagram’s meaning.

For Jules-style fields, put **geometry + internal labels** inside the plate. Keep outside the plate:

* semantic live heading;
* governing statement;
* source/editorial boundary;
* caption;
* extended description;
* navigation.

Do **not** rasterize the entire chapter opening unless the title/prose itself is spatially inseparable. Amazon’s accessibility guidance says to use real text rather than images of text where possible, but it also permits meaningful images with alt text and surrounding description; the practical distinction is whether the text can be separated from the art without destroying the meaning. ([Kindle Direct Publishing][4])

## Plate extent decision

| Component                              | Treatment                                         |
| -------------------------------------- | ------------------------------------------------- |
| Semantic heading                       | Live.                                             |
| Governing statement                    | Live unless it is physically part of the diagram. |
| Diagram geometry                       | Plate.                                            |
| Internal labels whose position matters | Plate.                                            |
| Caption                                | Live.                                             |
| Extended explanation                   | Live.                                             |
| Navigation                             | Live.                                             |

For complex diagrams, concise alt + caption is **not** enough. Use concise alt, live caption, and a visible extended description. Amazon says meaningful images need text alternatives or surrounding text; Amazon’s detail-page accessibility language recognizes alt text, extended descriptions, transcripts, and captions as textual alternatives. ([Kindle Direct Publishing][7])

---

# 7. Typography and reader settings

## What readers can change

Current Kindle reading environments expose user controls for font, font size, boldness, line/paragraph/word/character spacing, margins, orientation, alignment, themes/background, and saved theme settings, though exact controls vary by device/model. Amazon’s e-reader help says the Aa menu includes font, size, bold, layout spacing, margin size, portrait/landscape, alignment, themes, and background color; KDP’s own Previewer page says Previewer can test device type, orientation, font type, and font size. ([Amazon DigPRJ Survey][8])

## BHT typography rule

Body prose should remain reader-controlled. Amazon says body text in reflowable Kindle books must use defaults, should not force font size/line-height, should not impose book-wide font color, should not force margins/padding, and should not force body font face in a way that prevents reader font selection. ([Kindle Direct Publishing][1])

Use display typography only for:

* headings;
* short standing language;
* captions;
* source/editorial labels;
* plates.

Embedded fonts may be used for headings/display if they are licensed and necessary to convey intent. Amazon supports OTF/TTF fonts, says publishers are responsible for license rights, and recommends Kindle defaults unless embedded fonts are necessary. ([Kindle Direct Publishing][1])

---

# 8. Vertical pacing

## Safe pacing primitives

| Primitive                          |                                   Use? | Notes                                                                    |
| ---------------------------------- | -------------------------------------: | ------------------------------------------------------------------------ |
| `margin-top/bottom` in modest `em` |                                    Yes | Best for breathing space.                                                |
| `padding`                          |                 Yes, short blocks only | Good for colored callouts, not page simulation.                          |
| `break-before/page-break-before`   | Only inside a multi-section XHTML file | Not on first element of split spine item.                                |
| `break-after/page-break-after`     |                                   Rare | Not on final element before next spine file.                             |
| `break-inside: avoid`              |                      Small blocks only | Use for small image+caption or heading+one paragraph, not giant openers. |
| empty paragraphs                   |                                     No | Fragile and semantically dirty.                                          |
| `min-height`, `height`, `vh`, `vw` |                                  Avoid | Especially in text-containing blocks.                                    |

Amazon recommends `margin-top`/`margin-bottom` for paragraph spacing, `em` values for top/bottom spacing, percentages for left/right margins, and says never use `height` to control text-containing elements because overlap can occur. It also says fixed values like points/pixels should be avoided for CSS sizing/spacing. ([Kindle Direct Publishing][1])

Yes: remove `min-height` from all text-containing Kindle blocks. Amazon’s own Enhanced Typesetting documentation is internally tense here: `min-height` appears in the supported list, but also appears in the ignored attributes list. When a property is both “supported” and “ignored” in official docs, do not make it carry design meaning. ([Kindle Direct Publishing][2])

Practical BHT spacing limits:

```css
h1 {
  margin-top: 0;
  margin-bottom: 0.85em;
}

.part-opener {
  margin-top: 1.5em;
  margin-bottom: 1.2em;
}

.section-breath {
  margin-top: 1.2em;
  margin-bottom: 1.2em;
}
```

Avoid chapter-opening vertical space above about **2em** unless a specific Previewer test passes at large font sizes.

---

# 9. Per-entry spine architecture

Keep the 22 entry XHTML files plus front matter.

Amazon’s import restrictions are far above this: each HTML file must be under 30 MB, and the ebook must contain fewer than 300 HTML files. Amazon also explicitly asks publishers to review for missing content and to flip through the whole book. Your empirical ending fix is therefore not explained by an official size limit, but the fix is production-sensible and well within Amazon’s formal limits. ([Kindle Direct Publishing][3])

## TOC targeting

Use:

```html
<li><a href="entry-11.xhtml">See What Has Become Possible</a></li>
```

rather than:

```html
<li><a href="entry-11.xhtml#entry-11-title">See What Has Become Possible</a></li>
```

when the heading is the first substantial element.

Keep fragments for interior links:

```html
<a href="entry-11.xhtml#give-it-a-home">Give it a home</a>
```

Amazon documents TOC errors when targets point to hidden elements or IDs placed on `body`, and gives a workaround of moving IDs from `body` to child elements. For top-level TOC targets, document-level links avoid one entire category of fragment failure. ([Kindle Direct Publishing][2])

The first substantial element in each entry should be a real heading:

```html
<article id="entry-11">
  <h1>See What Has Become Possible</h1>
  ...
</article>
```

Do not put the TOC target on `body`.

---

# 10. Source splitting and CSS

## Stylesheet structure

Use:

1. `bht-kindle-reset.css`
2. `bht-kindle-components.css`
3. limited entry classes on `body`

Avoid dozens of per-entry stylesheets unless a specific entry truly needs its own field class. Amazon supports one CSS file and different CSS files/media-query strategies, but the lowest-risk Kindle branch is simpler: one reset, one component sheet, limited body classes. ([Kindle Direct Publishing][9])

## Remove dead retail CSS and hidden helper markup

Yes: remove retail-only CSS and dead geometry. Do not merely hide it.

Amazon documents a conversion error when more than 10,000 characters are hidden with `display:none`, and it also documents TOC failures when a TOC link points to `display:none` or `visibility:hidden`. ([Kindle Direct Publishing][2])

Pseudo-elements should not carry meaning. Amazon’s current supported/ignored tables do not give enough confidence to let `::before/::after` produce meaningful text, blooms, markers, or labels. Use real HTML for text and plates for visual fields.

---

# 11. Dark mode and color

Enhanced Typesetting can adapt font colors for contrast over background colors or reader themes, but that also means publisher color behavior is not fully yours. Amazon’s Enhanced Typesetting page says font colors adapt automatically for contrast with reader-selected device themes or page-level backgrounds. ([Kindle Direct Publishing][10])

## BHT dark-mode rules

| Component                    | Rule                                                                  |
| ---------------------------- | --------------------------------------------------------------------- |
| Live body prose              | Let reader theme win.                                                 |
| Short colored callouts       | Use mid-tone colors; test all modes.                                  |
| Dark North/South/West plates | Bake the background into the plate.                                   |
| Transparent PNGs             | Do not use. Transparency becomes white.                               |
| SVG                          | Test; do not trust for critical dark fields.                          |
| Body background field        | Use only for intentional per-entry field chapters and test all modes. |

Yes: keep dark live sections short when possible, then return to the reader’s normal page background.

---

# 12. SVG policy

## Resolve the contradiction

Amazon’s guidance is not actually “SVG is safe.” It is:

* computer-generated visuals are well represented by SVG;
* SVG tags can cause errors;
* use the HTML image tag for images;
* SVG namespace prefixes are unsupported;
* some KDP language pages say Enhanced Typesetting supports GIF/JPEG/PNG but does not support SVG images, with partial SVG rasterization. ([Kindle Direct Publishing][4])

## Minimal SVG subset worth testing

Only test external SVG via `<img>`:

```html
<img src="../images/family-compass.svg"
     alt="Compass relation with North, East, South, and West around Jules." />
```

Safe-ish SVG subset for experiment:

* `viewBox`
* simple `path`
* `circle`
* `line`
* `rect`
* simple `fill`
* simple `stroke`
* no embedded fonts
* no filters
* no blur
* no masks
* no CSS animations
* no namespace prefixes
* no tiny SVG text relied on for accessibility

For BHT, SVG only has a meaningful advantage if it renders vector-sharp **and** keeps file size small **and** survives every Previewer target. Otherwise high-resolution PNG wins.

---

# 13. Conversion diagnostics

Amazon’s current Previewer page says Kindle Previewer previews device type, orientation, font, images/lists/tables, and auto-advance; it also shows Enhanced Typesetting support in Book Information. KDP QA says the Conversion Log shows errors/warnings from Kindle conversion, and older Previewer user-guide material documents CLI commands including `-convert`, `-qualitychecks`, `-showpreview`, and `-log`. ([Kindle Direct Publishing][11])

What you **cannot** get, officially, is a clean post-conversion source tree that lists every removed CSS rule, every image recompression, and every KFX layout rewrite.

## Practical QA path

Use:

```powershell
kindlepreviewer input.epub -convert -output out -qualitychecks
kindlepreviewer input.epub -log -output out-log
```

Then inspect:

* GUI Conversion Log;
* `out/Logs/`;
* Previewer Quality Report;
* every TOC target;
* every in-book map;
* all pages with images;
* all pages with colored backgrounds;
* final-entry sentinel phrase.

No official tool was found that automatically proves every source paragraph survived conversion. Build your own paragraph sentinel check before conversion, then manually verify the converted Previewer output at the ending and any previously missing zones.

---

# 14. Disappearing ending

I did not find current official Amazon documentation for “content silently disappears near the end of a large XHTML flow while conversion succeeds.” Amazon does, however, explicitly tells publishers to check for missing content and to flip through every page, and sets a formal per-HTML-file limit of 30 MB, far larger than your failed 1.2 MB monolith. ([Kindle Direct Publishing][3])

The closest production-aligned explanation is: the large XHTML file created a converter/location-map/pathology below the formal size limit. Your workaround—one top-level entry per XHTML—matches long-standing production advice to split large source HTML into smaller chapter files. BB eBooks’ older KindleGen-era tutorial recommended splitting large files at chapters and keeping files around 300 KB because older devices were slow parsers; that 300 KB rule is historical, but the chapter-splitting habit remains useful. ([BB eBooks][12])

Keep the split. Treat “complete ending present” as a release gate.

---

# 15. Decision table for BHT components

| BHT component                     | Treatment                            | Reason                                                      |
| --------------------------------- | ------------------------------------ | ----------------------------------------------------------- |
| Ordinary prose                    | Live                                 | Kindle handles this well; reader settings matter.           |
| Headings                          | Live                                 | Semantic navigation/accessibility.                          |
| Source/editorial standing         | Live                                 | Preserves distinction and accessibility.                    |
| Western Tellings relational field | PNG plate                            | Proven successful; spatial meaning.                         |
| Jules bearing                     | PNG plate                            | Proven superior to live geometry.                           |
| Family compass                    | PNG plate                            | Directional geometry is meaning.                            |
| Five-place/family diagrams        | PNG plate                            | Do not ask Kindle to recompute compass space.               |
| Multi-column story nav            | One-column live links                | Tap targets and reflow safety.                              |
| 7–20 link maps                    | One link per row                     | Avoid crush.                                                |
| Long colored chapter world        | Per-entry body/background experiment | Only if whole entry is the field.                           |
| Local colored note                | Short live block                     | Safe if it does not span pages.                             |
| Bloom/gradient/atmosphere         | Plate                                | CSS gradient/bloom unreliable; linear gradient unsupported. |
| Real data tables                  | HTML table                           | Accessible/paginates.                                       |
| Relational non-table layout       | Plate or one-column prose            | Tables would lie semantically.                              |
| SVG diagrams                      | Test candidate only                  | Not default for critical fields.                            |
| Hidden helper geometry            | Remove                               | `display:none` and hidden targets cause problems.           |
| Retail CSS Grid                   | Remove                               | Not supported/documented.                                   |
| Absolute positioning              | Remove for meaning                   | Not safe in reflow.                                         |

---

# 16. Proposed BHT Kindle reset stylesheet

```css
/* BHT Kindle Reset — reflow-first, plate-ready */

html,
body {
  margin: 0;
  padding: 0;
}

body {
  font-family: serif;
  font-size: 1em;
  line-height: normal;
  text-align: left;
}

article,
section,
div,
figure,
figcaption,
nav,
ol,
ul,
li,
p,
h1,
h2,
h3,
blockquote {
  margin-left: 0;
  margin-right: 0;
  padding-left: 0;
  padding-right: 0;
}

h1,
h2,
h3 {
  text-indent: 0;
  text-align: left;
  line-height: 1.2;
  break-before: auto;
  page-break-before: auto;
  break-after: auto;
  page-break-after: auto;
}

h1 {
  margin-top: 0;
  margin-bottom: 0.85em;
  font-size: 1.45em;
}

h2 {
  margin-top: 1.2em;
  margin-bottom: 0.55em;
  font-size: 1.2em;
}

h3 {
  margin-top: 1em;
  margin-bottom: 0.4em;
  font-size: 1em;
}

p {
  margin-top: 0;
  margin-bottom: 0.8em;
  text-indent: 0;
}

blockquote,
.standing,
.threshold,
.source-boundary {
  margin: 1em 5%;
  padding: 0;
  text-indent: 0;
}

.short-field {
  margin: 1em 0;
  padding: 0.8em 0.9em;
}

.short-field p {
  margin: 0 0 0.6em 0;
}

.short-field p:last-child {
  margin-bottom: 0;
}

figure.plate {
  margin: 1.2em 0;
  padding: 0;
  text-align: center;
}

figure.plate img {
  display: block;
  width: 100%;
  height: auto;
  object-fit: contain;
  margin: 0 auto;
}

figure.plate figcaption {
  margin: 0.5em 0 0 0;
  text-align: center;
  text-indent: 0;
  font-size: 0.9em;
}

.bht-rel-nav {
  margin: 1.2em 0;
  padding: 0;
}

.bht-rel-nav ol,
.bht-rel-nav ul {
  margin: 0;
  padding: 0;
}

.bht-rel-nav li {
  list-style-type: none;
  margin: 0 0 0.65em 0;
  padding: 0;
}

.bht-rel-nav a {
  display: block;
  padding: 0.55em 0;
  text-decoration: none;
  border-top: 0.05em solid currentColor;
}

.bht-rel-nav .question,
.bht-rel-nav .destination {
  display: block;
}

.bht-rel-nav .question {
  font-weight: bold;
}

.bht-rel-nav .destination {
  margin-top: 0.15em;
}

/* Explicitly neutralize desktop/retail carryover */
.no-kindle-grid,
.no-kindle-absolute,
.retail-only,
.desktop-only {
  display: none;
}
```

Use the `.retail-only` rule only while migrating. Final Kindle files should remove retail-only markup entirely because Kindle has documented limits and conversion hazards around hidden content. ([Kindle Direct Publishing][2])

---

# 17. Chapter-opening recipe

```html
<body class="bht-entry bht-entry-07">
  <article id="entry-07" epub:type="chapter">
    <h1>Cultivate Rather Than Fire</h1>

    <p class="threshold">
      A short live threshold statement belongs here.
    </p>

    <figure class="plate">
      <img
        src="../images/entry-07-field.png"
        alt="Relational field for Cultivate Rather Than Fire." />
      <figcaption>
        Cultivation field. The image preserves spatial relation; the prose remains live.
      </figcaption>
    </figure>

    <p>Live prose begins here.</p>
  </article>
</body>
```

```css
body.bht-entry {
  margin: 0;
  padding: 0;
}

body.bht-entry article {
  margin: 0;
  padding: 1em 0 0 0;
}

body.bht-entry h1 {
  margin: 0 0 0.85em 0;
  padding: 0;
  text-align: left;
  line-height: 1.2;
  break-before: auto;
  page-break-before: auto;
}

body.bht-entry article > *:last-child {
  break-after: auto;
  page-break-after: auto;
}
```

---

# 18. Plate recipe

```html
<section id="jules-bearing">
  <h2>Jules Bearing</h2>

  <p class="standing">
    Live standing language introduces the relation without being trapped in the image.
  </p>

  <figure class="plate">
    <img
      src="../images/jules-bearing.png"
      alt="Bearing diagram arranging Jules in relation to surrounding directional fields." />
    <figcaption>
      Jules bearing field.
      <a href="../backmatter/extended-descriptions.xhtml#desc-jules-bearing">
        Extended description
      </a>
    </figcaption>
  </figure>
</section>
```

```css
figure.plate {
  margin: 1.2em 0;
  padding: 0;
  text-align: center;
}

figure.plate img {
  display: block;
  width: 100%;
  height: auto;
  object-fit: contain;
  margin: 0 auto;
}

figure.plate figcaption {
  margin: 0.5em 0 0 0;
  text-align: center;
  text-indent: 0;
}
```

---

# 19. One-column relational-navigation recipe

```html
<section class="relation-map" aria-labelledby="map-entry-questions">
  <h2 id="map-entry-questions">Questions this part can answer</h2>

  <ol class="bht-rel-nav">
    <li>
      <a href="entry-03.xhtml">
        <span class="question">What happened?</span>
        <span class="destination">03 · Gravity</span>
      </a>
    </li>

    <li>
      <a href="entry-04.xhtml">
        <span class="question">What became possible?</span>
        <span class="destination">04 · Opening Field</span>
      </a>
    </li>

    <li>
      <a href="entry-05.xhtml">
        <span class="question">Where does it live now?</span>
        <span class="destination">05 · Give It a Home</span>
      </a>
    </li>
  </ol>
</section>
```

```css
.bht-rel-nav {
  margin: 1.2em 0;
  padding: 0;
}

.bht-rel-nav li {
  list-style-type: none;
  margin: 0 0 0.65em 0;
  padding: 0;
}

.bht-rel-nav a {
  display: block;
  padding: 0.55em 0;
  border-top: 0.05em solid currentColor;
  text-decoration: none;
}

.bht-rel-nav span {
  display: block;
}
```

---

# 20. The next build checklist

For Prototype 004:

1. Keep the per-entry split.
2. Change top-level TOC links to `entry-XX.xhtml`.
3. Remove first-element `break-before/page-break-before`.
4. Remove final-element `break-after/page-break-after`.
5. Remove `min-height`, `height`, `vh`, `vw` from text blocks.
6. Plate Jules, Western Tellings, compass/family relations, and all atmosphere/bloom fields.
7. Convert multi-column navigation to one-column row links.
8. Replace long colored wrappers with either per-entry body fields or short live blocks.
9. Remove dead retail CSS/hidden geometry.
10. Run Previewer with e-reader, phone, tablet, portrait/landscape, large font, narrow margins, and all background modes.

The key decision is now settled: **there is no live alternative worth keeping for directional/relational geometry when direction is meaning. Plate it decisively, keep the interpretive frame live, and let Kindle do what it is actually good at: prose, headings, links, captions, and reader-controlled flow.**

[1]: https://kdp.amazon.com/en_US/help/topic/GH4DRT75GWWAGBTU "Text Guidelines - Reflowable"
[2]: https://kdp.amazon.com/en_US/help/topic/GB5GDY7WAJDN9GFK "Attributes and Tags Supported by Enhanced Typesetting"
[3]: https://kdp.amazon.com/en_US/help/topic/GGRXLC5USU4H67YM "QA Standards"
[4]: https://kdp.amazon.com/en_US/help/topic/G75V4YX5X8GRGXWV "Image Guidelines - Reflowable"
[5]: https://kdp.amazon.com/en_US/help/topic/GZ8BAXASXKB5JVML "Table Guidelines - Reflowable"
[6]: https://kdp.amazon.com/en_US/help/topic/GY3AD8C6C6GAG42N?utm_source=chatgpt.com "Navigation Guidelines"
[7]: https://kdp.amazon.com/en_US/help/topic/GF9Z3HLUMTRJ6QPL "Accessibility Guidelines"
[8]: https://digprjsurvey.amazon.com/csad/help/node/T5Y94BzSCGwm0vd75W?utm_source=chatgpt.com "Customize Your Kindle E-Reader Text Display"
[9]: https://kdp.amazon.com/en_US/help/topic/GR4KL488MXKPZ5BK "Media Queries"
[10]: https://kdp.amazon.com/en_US/help/topic/G202087570 "Enhanced Typesetting"
[11]: https://kdp.amazon.com/en_US/help/topic/G202131170 "Kindle Previewer"
[12]: https://bbebooksthailand.com/bb-epub-kindlegen-tutorial.html?utm_source=chatgpt.com "BB eBooks – EPUB and KindleGen Tutorial"
