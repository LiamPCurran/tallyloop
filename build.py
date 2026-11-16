"""Build both versions of the Tallyloop concept site.

before/ = how AI site builders often ship it: a client-rendered single-page app
          (React + in-browser Babel from a CDN), hash routes, one generic title,
          no meta/canonical/OG, no real headings, click-handler 'links', no
          sitemap/robots, oversized PNG without alt text, render-blocking fonts.
after/  = the rescue: static, pre-rendered pages, same look and copy, fully
          indexable, fast.

Usage: python build.py [BASE_URL]   (BASE_URL of the after/ version)
"""
import json, shutil, sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).parent
BASE = (sys.argv[1] if len(sys.argv) > 1 else "https://USERNAME.github.io/tallyloop").rstrip("/")
TODAY = date.today().isoformat()

C = {
    "tagline": "Time tracking and invoicing for freelancers who'd rather be working",
    "lede": "Start a timer, turn your hours into a professional invoice in two clicks, and let Tallyloop chase late payments for you.",
    "features": [
        ("One-click timer", "Track time from the browser or your phone. Forgot to start it? Add hours later in seconds."),
        ("Hours → invoice in two clicks", "Pick a client and a date range. Tallyloop builds the invoice from your tracked time and your rates."),
        ("Polite payment reminders", "Overdue invoices get friendly automatic reminders, so you don't have to write awkward emails."),
        ("Online card payments", "Clients pay by card straight from the invoice. You see the payment the moment it lands."),
        ("Project budgets", "Set hours or dollar budgets per project and get a heads-up at 80%, before you go over."),
        ("Tax-time exports", "Export income and invoices by year or quarter as CSV or PDF for your accountant."),
    ],
    "steps": [
        ("Track", "Hit start when you begin a task. Tag it to a client and project."),
        ("Invoice", "At month-end, turn tracked hours into a branded invoice and send it."),
        ("Get paid", "Clients pay online. Tallyloop sends reminders if they don't."),
    ],
    "plans": [
        ("Free", "$0", "forever", ["1 active client", "Unlimited time tracking", "3 invoices per month"], False),
        ("Solo", "$9", "/month", ["Unlimited clients and invoices", "Online card payments", "Automatic reminders", "Project budgets"], True),
        ("Studio", "$19", "/month", ["Everything in Solo", "Up to 5 team members", "Team timesheets and approvals", "Tax-time exports"], False),
    ],
    "faqs": [
        ("Is there a free plan?", "Yes. The Free plan covers one active client with unlimited time tracking and three invoices a month. Upgrade only when you need more."),
        ("Can my clients pay online?", "Yes. On Solo and Studio, every invoice has a pay-by-card button. Card processing fees are charged by the payment provider."),
        ("Can I import my existing time entries?", "You can import time entries from a CSV file, which most time trackers can export."),
        ("Can I cancel any time?", "Yes. Plans are month-to-month, and you can export all your data before you leave."),
    ],
    "about": [
        "Tallyloop started as a spreadsheet. Its founder was freelancing as a designer, tracking hours in one app, building invoices in another and chasing payments by email. Every month-end took an afternoon.",
        "We built Tallyloop to make that afternoon take five minutes. It does three things well: tracks time, turns that time into invoices and gets those invoices paid. That's it. No project-management suite, no CRM, no fifty-tab settings page.",
        "We're a small, independent team, and we answer support emails ourselves.",
    ],
}

# ======================= BEFORE (the flawed AI-builder version) =======================
B = ROOT / "docs" / "before"
(B / "assets").mkdir(parents=True, exist_ok=True)
shutil.copy(ROOT / "style.css", B / "assets" / "index-4f9a1c2e.css")
(B / "content.json").write_text(json.dumps(C, ensure_ascii=False, indent=1), encoding="utf-8")
(B / "index.html").write_text('''<!doctype html>
<html>
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Tallyloop</title>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@100;200;300;400;500;600;700;800;900&family=Poppins:wght@300;400;500;600;700;800&family=Roboto:wght@300;400;500;700&display=block" rel="stylesheet">
<link rel="stylesheet" href="assets/index-4f9a1c2e.css">
<script src="https://unpkg.com/react@18.3.1/umd/react.development.js"></script>
<script src="https://unpkg.com/react-dom@18.3.1/umd/react-dom.development.js"></script>
<script src="https://unpkg.com/@babel/standalone@7.24.7/babel.js"></script>
</head>
<body>
<div id="root"></div>
<script type="text/babel" src="app.jsx"></script>
</body>
</html>
''', encoding="utf-8")
(B / "app.jsx").write_text('''// Generated-style SPA: everything renders client-side after content.json loads.
const { useState, useEffect } = React;

function useRoute() {
  const [r, setR] = useState(window.location.hash.replace("#/", "") || "home");
  useEffect(() => { const f = () => setR(window.location.hash.replace("#/", "") || "home"); window.addEventListener("hashchange", f); return () => window.removeEventListener("hashchange", f); }, []);
  return r;
}
const go = (r) => { window.location.hash = "/" + r; window.scrollTo(0, 0); };

function Header() {
  return (<div className="site-header" style={{borderBottom: "1px solid #e4e1f2"}}><div className="wrap" style={{display:"flex",alignItems:"center",justifyContent:"space-between",minHeight:68}}>
    <div className="brand" onClick={() => go("home")}><i></i>Tallyloop</div>
    <div className="main" style={{display:"flex",gap:24}}>
      <span style={{fontWeight:600,cursor:"pointer"}} onClick={() => go("features")}>Features</span>
      <span style={{fontWeight:600,cursor:"pointer"}} onClick={() => go("pricing")}>Pricing</span>
      <span style={{fontWeight:600,cursor:"pointer"}} onClick={() => go("about")}>About</span>
      <span style={{fontWeight:600,cursor:"pointer"}} onClick={() => go("contact")}>Contact</span>
    </div>
    <div className="btn" onClick={() => go("pricing")}>Start free</div>
  </div></div>);
}

function Footer() {
  return (<div className="site" style={{background:"#151229",color:"#b9b4d9",padding:"40px 0 24px"}}><div className="wrap">
    <div>© Tallyloop</div>
    <div className="concept">Concept project by Liam Curran – fictional product. This is the deliberately flawed "before" version.</div>
  </div></div>);
}

function Features({ c }) {
  return (<div className="block"><div className="wrap"><div className="h2 center">Everything between "start timer" and "paid"</div>
    <div className="grid c3">{c.features.map(([t, d]) => <div className="card" key={t}><div className="h3">{t}</div><div>{d}</div></div>)}</div></div></div>);
}

function Pricing({ c }) {
  return (<div className="block alt"><div className="wrap"><div className="h2 center">Simple pricing</div>
    <div className="grid c3">{c.plans.map(([n, p, per, items, f]) => <div className={"card" + (f ? " featured" : "")} key={n}>
      <div className="h3">{n}</div><div className="price">{p} <span>{per}</span></div>
      <ul>{items.map(i => <li key={i}>{i}</li>)}</ul><div className="btn">Choose {n}</div></div>)}</div></div></div>);
}

function Faq({ c }) {
  return (<div className="block"><div className="wrap faq"><div className="h2">Questions</div>
    {c.faqs.map(([q, a]) => <details key={q}><summary>{q}</summary><p>{a}</p></details>)}</div></div>);
}

function Home({ c }) {
  return (<>
    <div className="hero"><div className="wrap">
      <div className="h1">{c.tagline}</div>
      <div className="lede">{c.lede}</div>
      <div className="ctas"><div className="btn" onClick={() => go("pricing")}>Start free</div><div className="btn ghost" onClick={() => go("features")}>See features</div></div>
      <div className="shot"><img src="assets/dashboard-screenshot-final-v3.png" /></div>
    </div></div>
    <Features c={c} />
    <div className="block alt"><div className="wrap"><div className="h2 center">How it works</div>
      <div className="grid c3">{c.steps.map(([t, d], i) => <div className="card" key={t}><div className="h3">{i + 1}. {t}</div><div>{d}</div></div>)}</div></div></div>
    <Faq c={c} />
  </>);
}

function About({ c }) {
  return (<div className="block"><div className="wrap prose"><div className="h1">About us</div>{c.about.map((p, i) => <p key={i}>{p}</p>)}</div></div>);
}

function Contact() {
  return (<div className="block"><div className="wrap"><div className="h1">Contact</div><p>Email us at hello@example.com</p></div></div>);
}

function App() {
  const [c, setC] = useState(null);
  const route = useRoute();
  useEffect(() => { fetch("content.json").then(r => r.json()).then(setC); }, []);
  if (!c) return <div style={{padding:80,textAlign:"center"}}>Loading...</div>;
  return (<>
    <Header />
    {route === "home" && <Home c={c} />}
    {route === "features" && <Features c={c} />}
    {route === "pricing" && <Pricing c={c} />}
    {route === "about" && <About c={c} />}
    {route === "contact" && <Contact />}
    <Footer />
  </>);
}

ReactDOM.createRoot(document.getElementById("root")).render(<App />);
''', encoding="utf-8")
(B / ".nojekyll").write_text("", encoding="utf-8")

# ======================= AFTER (the rescue) =======================
A = ROOT / "docs"
(A / "assets").mkdir(parents=True, exist_ok=True)
shutil.copy(ROOT / "style.css", A / "assets" / "style.css")
(A / "assets" / "logo.svg").write_text('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32"><rect width="32" height="32" rx="8" fill="#7c5cff"/><path d="M9 16a7 7 0 1 0 7-7" fill="none" stroke="#fff" stroke-width="3" stroke-linecap="round"/><path d="M16 5l3 4-4 2" fill="none" stroke="#fff" stroke-width="2.5" stroke-linejoin="round"/></svg>', encoding="utf-8")

NAV = [("index.html", "Home"), ("features.html", "Features"), ("pricing.html", "Pricing"), ("about.html", "About"), ("contact.html", "Contact")]
ORG = {"@context": "https://schema.org", "@type": "Organization", "@id": BASE + "/#org", "name": "Tallyloop",
       "url": BASE + "/", "logo": BASE + "/assets/logo.svg", "email": "hello@example.com"}
APP = {"@context": "https://schema.org", "@type": "SoftwareApplication", "name": "Tallyloop",
       "applicationCategory": "BusinessApplication", "operatingSystem": "Web, iOS, Android",
       "description": C["lede"], "publisher": {"@id": BASE + "/#org"},
       "offers": [{"@type": "Offer", "name": n, "price": p.strip("$"), "priceCurrency": "USD"} for n, p, *_ in C["plans"]]}


def ld(o):
    return '<script type="application/ld+json">' + json.dumps(o, ensure_ascii=False, separators=(",", ":")) + "</script>"


def crumbs(items):
    return {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": i + 1, "name": n, "item": BASE + "/" + u} for i, (u, n) in enumerate(items)]}


def faq_ld():
    return {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in C["faqs"]]}


def page_hero(path, label, h1, lede=""):
    return (f'<section class="page-hero"><div class="wrap"><div class="crumbs"><a href="index.html">Home</a> › {label}</div>'
            f'<h1>{h1}</h1>' + (f'<p class="muted" style="font-size:1.15rem">{lede}</p>' if lede else "") + '</div></section>')


def features_html(level="h2"):
    cards = "".join(f'<div class="card"><h3>{t}</h3><p>{d}</p></div>' for t, d in C["features"])
    return f'<section class="block"><div class="wrap"><{level} class="center">Everything between "start timer" and "paid"</{level}><div class="grid c3">{cards}</div></div></section>'


def pricing_html(level="h2"):
    cards = "".join(
        f'<div class="card{" featured" if f else ""}">' + ('<span class="tag">Most popular</span>' if f else "") +
        f'<h3>{n}</h3><p class="price">{p} <span>{per}</span></p><ul>' + "".join(f"<li>{i}</li>" for i in items) +
        f'</ul><a class="btn{"" if f else " ghost"}" href="contact.html">Choose {n}</a></div>' for n, p, per, items, f in C["plans"])
    return f'<section class="block alt"><div class="wrap"><{level} class="center">Simple pricing in USD. Cancel any time.</{level}><div class="grid c3">{cards}</div></div></section>'


def faq_html():
    return ('<section class="block"><div class="wrap faq"><h2>Common questions</h2>' +
            "".join(f"<details><summary>{q}</summary><p>{a}</p></details>" for q, a in C["faqs"]) + "</div></section>")


CTA = ('<section class="cta-band"><div class="wrap"><h2>Get your month-end afternoon back</h2>'
       '<p>Free for your first client. No card needed.</p><a class="btn" href="pricing.html">Start free</a></div></section>')

pages = []


def page(path, title, desc, body, schemas=()):
    canon = BASE + "/" + ("" if path == "index.html" else path)
    nav = "".join(f'<a href="{h}"' + (' aria-current="page"' if h == path else "") + (' class="hide-m"' if h in ("index.html", "about.html") else "") + f'>{l}</a>' for h, l in NAV)
    html = f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="{canon}">
<meta property="og:type" content="website"><meta property="og:site_name" content="Tallyloop">
<meta property="og:title" content="{title}"><meta property="og:description" content="{desc}">
<meta property="og:url" content="{canon}"><meta property="og:image" content="{BASE}/assets/og.png">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="assets/logo.svg" type="image/svg+xml">
<link rel="stylesheet" href="assets/style.css">
{chr(10).join(ld(s) for s in schemas)}
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
<header class="site"><div class="wrap">
<a class="brand" href="index.html"><i></i>Tallyloop</a>
<nav class="main" aria-label="Main">{nav}</nav>
<a class="btn" href="pricing.html">Start free</a>
</div></header>
<main id="main">
{body}
</main>
<footer class="site"><div class="wrap">
<div class="cols"><div><strong style="color:#fff">Tallyloop</strong><p>Time tracking and invoicing for freelancers.</p></div>
<ul><li><a href="features.html">Features</a></li><li><a href="pricing.html">Pricing</a></li></ul>
<ul><li><a href="about.html">About</a></li><li><a href="contact.html">Contact</a></li></ul></div>
<p class="concept">Concept project by Liam Curran – fictional product. This is the fixed "after" version of an AI-built site rescue demo.</p>
</div></footer>
</body>
</html>
'''
    (A / path).write_text(html, encoding="utf-8")
    pages.append(path)


steps = "".join(f'<div class="card"><h3>{i + 1}. {t}</h3><p>{d}</p></div>' for i, (t, d) in enumerate(C["steps"]))
page("index.html", "Tallyloop | Time Tracking & Invoicing Software for Freelancers",
     "Track time, turn hours into invoices in two clicks and get paid faster with automatic reminders. Free plan for your first client.",
     f'''<section class="hero"><div class="wrap">
<h1>{C["tagline"]}</h1>
<p class="lede">{C["lede"]}</p>
<div class="ctas"><a class="btn" href="pricing.html">Start free</a><a class="btn ghost" href="features.html">See features</a></div>
<small>Free plan for your first client. No card needed.</small>
<div class="shot"><img src="assets/dashboard-1200.webp" srcset="assets/dashboard-640.webp 640w, assets/dashboard-1200.webp 1200w"
 sizes="(max-width: 1040px) 100vw, 1000px" width="1200" height="750" fetchpriority="high"
 alt="Tallyloop dashboard showing hours tracked this week, unbilled amount, an hours-by-day chart and recent invoices"></div>
</div></section>
{features_html()}
<section class="block alt"><div class="wrap"><h2 class="center">How it works</h2><div class="grid c3">{steps}</div></div></section>
{faq_html()}
{CTA}''', [ORG, APP, faq_ld()])

page("features.html", "Features: Timer, Invoicing & Payment Reminders | Tallyloop",
     "See how Tallyloop's one-click timer, hours-to-invoice builder, automatic payment reminders and project budgets save freelancers hours every month.",
     page_hero("features.html", "Features", "Features built for solo freelancers", "Three jobs, done well: track time, invoice it, get paid.")
     + features_html("h2").replace('<h2 class="center">Everything between "start timer" and "paid"</h2>', '<h2 class="center">What\'s included</h2>') + CTA,
     [crumbs([("", "Home"), ("features.html", "Features")])])

page("pricing.html", "Pricing: Free, Solo & Studio Plans | Tallyloop",
     "Tallyloop pricing: Free for one client, Solo at $9/month, Studio at $19/month for small teams. Month-to-month, cancel any time.",
     page_hero("pricing.html", "Pricing", "Pricing that starts at free")
     + pricing_html() + faq_html(), [crumbs([("", "Home"), ("pricing.html", "Pricing")]), APP, faq_ld()])

page("about.html", "About Tallyloop | Built by a Freelancer, for Freelancers",
     "Tallyloop started as a freelancer's month-end spreadsheet. Meet the small, independent team behind simple time tracking and invoicing.",
     page_hero("about.html", "About", "Built because month-end took an afternoon")
     + '<section class="block"><div class="wrap prose">' + "".join(f"<p>{p}</p>" for p in C["about"]) + "</div></section>" + CTA,
     [crumbs([("", "Home"), ("about.html", "About")]), ORG])

page("contact.html", "Contact Tallyloop Support",
     "Questions about Tallyloop? Email hello@example.com or send a message. A real person on our small team will reply within one business day.",
     page_hero("contact.html", "Contact", "Talk to a human", "We reply within one business day.")
     + '''<section class="block"><div class="wrap"><form class="contact" id="contact" onsubmit="event.preventDefault();document.getElementById('m').classList.add('show');this.reset();">
<div><label for="n">Name</label><input id="n" name="name" autocomplete="name" required></div>
<div><label for="e">Email</label><input id="e" name="email" type="email" autocomplete="email" required></div>
<div><label for="q">Message</label><textarea id="q" name="message" rows="5" required></textarea></div>
<button class="btn" type="submit">Send message</button>
<p class="form-msg" id="m" role="status">Thanks! This is a concept site, so nothing was sent.</p>
<p>Or email <a href="mailto:hello@example.com">hello@example.com</a>.</p></form></div></section>''',
     [crumbs([("", "Home"), ("contact.html", "Contact")])])

(A / "404.html").write_text('<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>Page not found | Tallyloop</title><meta name="robots" content="noindex"><link rel="stylesheet" href="/tallyloop/assets/style.css"></head><body><main class="block"><div class="wrap"><h1>Page not found</h1><p><a href="/tallyloop/">Back to Tallyloop</a></p></div></main></body></html>', encoding="utf-8")
(A / "sitemap.xml").write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">' + "".join(
    f"<url><loc>{BASE}/{'' if p == 'index.html' else p}</loc><lastmod>{TODAY}</lastmod></url>" for p in pages) + "</urlset>\n", encoding="utf-8")
(A / "robots.txt").write_text(f"User-agent: *\nAllow: /\n\nSitemap: {BASE}/sitemap.xml\n", encoding="utf-8")
(A / ".nojekyll").write_text("", encoding="utf-8")
print("before/ and after/ built;", len(pages), "pages in after/, base", BASE)
