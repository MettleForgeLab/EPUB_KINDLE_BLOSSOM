# Platform-native review card

Use this after internal package audit and standards validation.

A clean validator does not replace platform review. A good renderer pass does not replace exact-file validation.

## Record first

- artifact filename;
- SHA-256;
- byte size;
- source/policy identity;
- platform application and version;
- device/profile;
- orientation;
- text size;
- theme;
- margins where available;
- reviewer;
- date.

## Shared whole-book pass

Review beginning to end.

Check:

- cover and front matter;
- TOC / Go To behavior;
- direct major-entry destinations;
- reading order;
- headings and quiet starts;
- duplicate or missing content;
- unexplained blank pages;
- captions and description links;
- external links;
- enlarged text;
- dark/light behavior;
- final transitions and ending;
- no platform adaptation louder than the book.

## Apple / non-Kindle emphasis

Check:

- actual page measure rather than outer window width;
- one-page and two-page behavior;
- fragmentation through entry wrappers;
- any `overflow` clipping;
- live CSS/HTML graphics;
- live SVG/CSS graphics;
- gutter intrusion;
- dedicated cover behavior;
- Apple external cover versus in-book cover roles.

Do not import Kindle plates merely because they exist.

## Kindle emphasis

Check:

- conversion/ingestion result;
- Jules `Presence → Startup & Settle` split;
- Western `Present Recognition → Human authority and family → Human` split;
- forward/backward traversal through both boundaries;
- plate scaling and label clarity;
- dark-field foreground/background pairing;
- Spot crack;
- closing edge light;
- page-turn separation before the final declaration;
- phone, tablet, and e-reader profiles where available;
- portrait/landscape where available;
- light/dark themes where available.

Do not remove renderer-stability splits merely because the source is semantically continuous.

## Graphic review

For each platform-specific representation:

- relation preserved;
- crop;
- spatial hierarchy;
- negative space;
- label legibility;
- banding/ringing;
- caption remains live where intended;
- alt/description/caption relationship;
- no stale sibling-platform asset.

## Blank-space decision

Ask:

- Is content missing?
- Is content duplicated?
- Is navigation broken?
- Is the renderer unstable?
- Or is the space carrying pace, pause, or page-turn meaning?

Do not repair quiet space by reflex.

## Result vocabulary

- `PASS`
- `REVISE`
- `OPEN`
- `NOT EVALUATED`

Record the exact artifact hash with the result.

## Freeze rule

After platform review and standards validation both pass:

- make a byte-identical release copy;
- verify the release hash;
- record candidate → release relation;
- prohibit mutation after freeze;
- create a new candidate for any later change.
