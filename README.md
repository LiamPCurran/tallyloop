# Tallyloop: website rescue (before & after)

**Concept project by Liam Curran. Tallyloop is a fictional product. Customer names, quotes and figures are illustrative.**

- After (fixed): https://liampcurran.github.io/tallyloop/
- Before (as a quick SPA export often ships it): https://liampcurran.github.io/tallyloop/before/

Same design, same copy, two builds. Both are generated from the same page content by `build.py`, so the only difference is how the site is delivered. The layout follows patterns from leading time-tracking and invoicing SaaS sites: an announcement pill, a product screenshot hero with floating UI cards, a customer logo strip, a three-step "how it works", alternating feature panels with UI mockups, a feature grid, a stats band, testimonials, pricing, an FAQ and a final call to action.

**Before:** a client-rendered single-page app.
- React (development build) and in-browser Babel loaded from a CDN, with all content fetched from JSON after load
- Hash routes, one generic `<title>`, no `lang`, and no meta description, canonical or Open Graph tags
- `<div>`s instead of headings, click-handler "links" crawlers can't follow, no landmarks and no form labels
- An oversized PNG without alt text or dimensions, render-blocking Google Fonts, and no sitemap or robots.txt

**After:** static, pre-rendered pages, one per route.
- Real headings, links, landmarks and labelled forms; unique titles and descriptions; canonical and OG tags
- `SoftwareApplication`, `Organization`, `FAQPage` and breadcrumb schema, plus a sitemap
- A responsive, preloaded WebP hero image; one self-hosted variable font; no JavaScript framework

| Lighthouse (mobile) | Performance | Accessibility | Best Practices | SEO |
|---|---|---|---|---|
| Before | 43 | 77 | 96 | 82 |
| After | 100 | 100 | 100 | 100 |

Page weight went from about 1.5 MB to 130 KB. (Measured locally on Nov 17, 2026 with Lighthouse 12. Live numbers are in the portfolio case study.)

## Build

```
# render mockup/dashboard.html to mockup/dashboard-2400.png with headless Chrome at 2x (1200x750 viewport)
python make_images.py
python build.py https://liampcurran.github.io/tallyloop
```

Font: Inter (SIL Open Font License).
