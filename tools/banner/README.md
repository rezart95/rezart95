# Banner generator

Builds the animated profile banner (`assets/banner.svg`) and the project dock
tiles (`assets/dock/*.svg`) used in the profile README.

```sh
pip install -r tools/banner/requirements.txt
python tools/banner/generate.py
```

Common edits, all in `generate.py`:

- **Keywords on the satellites:** `ORBITS`. Each orbit lists its satellites as
  `(keyword, gold)`; satellites are spaced evenly, so adding one re-spaces the rest.
- **Add or remove an app:** add its square icon to `icons/<id>.png`, add it to
  `PROJECTS`, then add the matching `<a><img></a>` to the README dock line. Keep
  the dock widths summing to 100% (label 16% + apps), and keep the dock line free
  of spaces or line breaks between tiles so they join edge to edge.
- **Name or title:** the two `<text>` lines under `# identity`.

Icon sources: each app's own PWA icon (Footbolski, MiredheLire, FashionPricing
`icon-512.png`; My Finances `icon-maskable-512.png`; LegalHub
`apple-touch-icon.png`; Almanac rendered from its `maskable-icon.svg`).

Fonts: Geist and Geist Mono, SIL Open Font License 1.1 (`fonts/OFL.txt`).
