# Tallyloop: AI-built site rescue (before & after)

**Concept project by Liam Curran. Tallyloop is a fictional product.**

- After (fixed): https://liampcurran.github.io/tallyloop/
- Before (as an AI site builder might ship it): https://liampcurran.github.io/tallyloop/before/

Same design, same copy, two builds.

**Before:** a client-rendered single-page app, typical of quick AI-builder exports.
- React and in-browser Babel loaded from a CDN, with content fetched after load
- Hash routes, one generic `<title>` and no meta description, canonical or Open Graph tags
- Styled `<div>`s instead of real headings, and click-handler "links" crawlers can't follow
- No sitemap or robots.txt, an oversized PNG without alt text, render-blocking font requests

**After:** static, pre-rendered pages, one per route.
- Real headings and links, unique titles and descriptions, canonical and OG tags
- `SoftwareApplication`, `Organization`, `FAQPage` and breadcrumb schema, plus a sitemap
- Responsive WebP images with alt text and no JavaScript framework

| Lighthouse (mobile) | Performance | Accessibility | Best Practices | SEO |
|---|---|---|---|---|
| Before | 34 | 71 | 96 | 82 |
| After | 100 | 100 | 100 | 100 |

Largest Contentful Paint on mobile went from 9.8 s to 1.1 s, and page weight from about 1.3 MB to 36 KB. (Measured locally on Nov 16, 2026 with Lighthouse 12.)

## Build

```
python make_images.py
python build.py https://liampcurran.github.io/tallyloop
```
