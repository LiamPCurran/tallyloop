"""Build both versions of the Tallyloop concept site from the SAME page content.

after/  (docs/)        = the rescue: static, pre-rendered, indexable, fast.
before/ (docs/before/) = the same pages as a typical quick-export SPA: React + in-browser Babel
          from a CDN, content fetched client-side from JSON, hash routes, one generic <title>,
          no meta/canonical/OG, <div> "headings", click-handler "links" crawlers can't follow,
          no landmarks, an oversized PNG without alt text, render-blocking Google Fonts,
          and no sitemap/robots.

Usage: python build.py [BASE_URL]   (BASE_URL of the after/ version)
Run make_images.py first.
"""
import json, re, shutil, sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).parent
BASE = (sys.argv[1] if len(sys.argv) > 1 else "https://liampcurran.github.io/tallyloop").rstrip("/")
TODAY = date.today().isoformat()
A = ROOT / "docs"
B = A / "before"


def ico(path):
    return f'<svg class="i" viewBox="0 0 24 24" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">{path}</svg>'


I = {
    "timer": ico('<circle cx="12" cy="13" r="8"/><path d="M12 9v4l2 2M9 2h6M12 2v3"/>'),
    "invoice": ico('<path d="M6 2h9l5 5v15H6z"/><path d="M14 2v6h6M9 13h6M9 17h4"/>'),
    "bell": ico('<path d="M6 8a6 6 0 0 1 12 0c0 7 3 9 3 9H3s3-2 3-9"/><path d="M10.3 21a1.9 1.9 0 0 0 3.4 0"/>'),
    "card": ico('<rect x="2" y="5" width="20" height="14" rx="2"/><path d="M2 10h20M6 15h4"/>'),
    "target": ico('<circle cx="12" cy="12" r="9"/><circle cx="12" cy="12" r="5"/><circle cx="12" cy="12" r="1"/>'),
    "export": ico('<path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4M7 10l5 5 5-5M12 15V3"/>'),
    "check": ico('<path d="M20 6 9 17l-5-5"/>'),
    "arrow": ico('<path d="M5 12h14M13 6l6 6-6 6"/>'),
    "zap": ico('<path d="M13 2 3 14h9l-1 8 10-12h-9z"/>'),
    "heart": ico('<path d="M20.8 4.6a5.5 5.5 0 0 0-7.8 0L12 5.7l-1-1.1a5.5 5.5 0 0 0-7.8 7.8L12 21.2l8.8-8.8a5.5 5.5 0 0 0 0-7.8z"/>'),
    "lock": ico('<rect x="4" y="11" width="16" height="10" rx="2"/><path d="M8 11V7a4 4 0 0 1 8 0v4"/>'),
    "mail": ico('<rect x="2" y="4" width="20" height="16" rx="2"/><path d="m22 6-10 7L2 6"/>'),
    "chat": ico('<path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/>'),
    "book": ico('<path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20V2H6.5A2.5 2.5 0 0 0 4 4.5z"/><path d="M4 19.5V22h16"/>'),
}
STAR = '<svg class="i" viewBox="0 0 24 24" aria-hidden="true"><path fill="currentColor" d="m12 2 3.1 6.3 6.9 1-5 4.9 1.2 6.8L12 17.8 5.8 21l1.2-6.8-5-4.9 6.9-1z"/></svg>'
STARS = '<span class="stars" role="img" aria-label="Rated 4.8 out of 5">' + STAR * 5 + "</span>"
LOGO = '<svg class="logo" viewBox="0 0 32 32" aria-hidden="true"><defs><linearGradient id="lg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#8b6cff"/><stop offset="1" stop-color="#5b3df0"/></linearGradient></defs><rect width="32" height="32" rx="8" fill="url(#lg)"/><path d="M9 16a7 7 0 1 0 7-7" fill="none" stroke="#fff" stroke-width="3" stroke-linecap="round"/><path d="M16 5l3 4-4 2" fill="none" stroke="#fff" stroke-width="2.5" stroke-linejoin="round"/></svg>'

C = {
    "tagline": "Time tracking and invoicing for freelancers who'd rather be working",
    "lede": "Start a timer, turn your hours into a professional invoice in two clicks, and let Tallyloop chase late payments for you.",
    "features": [
        ("timer", "One-click timer", "Track time from the browser, desktop or phone. Forgot to start it? Add hours later in seconds."),
        ("invoice", "Hours to invoice in two clicks", "Pick a client and a date range. Tallyloop builds the invoice from your tracked time and rates."),
        ("bell", "Polite payment reminders", "Overdue invoices get friendly automatic reminders, so you never write an awkward email again."),
        ("card", "Online card payments", "Clients pay by card straight from the invoice. You see the payment the moment it lands."),
        ("target", "Project budgets", "Set hour or dollar budgets per project and get a heads-up at 80%, before you go over."),
        ("export", "Tax-time exports", "Export income and invoices by year or quarter as CSV or PDF for your accountant."),
    ],
    "plans": [
        ("Free", "$0", "forever", "For trying it out with your first client.", ["1 active client", "Unlimited time tracking", "3 invoices per month"], False),
        ("Solo", "$9", "/month", "For full-time freelancers.", ["Unlimited clients and invoices", "Online card payments", "Automatic reminders", "Project budgets"], True),
        ("Studio", "$19", "/month", "For small studios and duos.", ["Everything in Solo", "Up to 5 team members", "Team timesheets and approvals", "Tax-time exports"], False),
    ],
    "faqs": [
        ("Is there a free plan?", "Yes. The Free plan covers one active client with unlimited time tracking and three invoices a month. Upgrade only when you need more."),
        ("Can my clients pay online?", "Yes. On Solo and Studio, every invoice has a pay-by-card button. Card processing fees are charged by the payment provider."),
        ("Can I import my existing time entries?", "You can import time entries from a CSV file, which most time trackers can export."),
        ("Can I cancel any time?", "Yes. Plans are month-to-month, and you can export all your data before you leave."),
        ("Is my data secure?", "Data is encrypted in transit and at rest, and card payments are handled by a PCI-compliant payment provider. We never see card numbers."),
    ],
    "reviews": [
        ("Month-end used to eat my whole Friday afternoon. Now I click two buttons and go for a run.", "Maya Chen", "Brand designer", "#6a48f0"),
        ("The automatic reminders alone paid for it. Two clients who always paid late now pay within a week.", "Jordan Okafor", "Developer, Okafor &amp; Lee", "#0ea5e9"),
        ("It does exactly three things and does them really well. I don't miss my old 40-tab setup.", "Priya Natarajan", "Copywriter", "#f97316"),
    ],
}
CLIENTS = [("Northfield Studio", "w1"), ("Okafor &amp; Lee", "w2"), ("Brightside Co.", "w3"), ("Juniper Labs", "w4"), ("Pixelwell", "w5"), ("Marlow Copy", "w6")]
NAV = [("features.html", "Features"), ("pricing.html", "Pricing"), ("about.html", "About"), ("contact.html", "Contact")]


# ------------------------------------------------------------------ shared page parts
def header(path):
    nav = "".join(f'<a href="{h}"' + (' aria-current="page"' if h == path else "") + f'>{l}</a>' for h, l in NAV)
    return f'''<header class="site-header"><div class="wrap">
<a class="brand" href="index.html">{LOGO}<span>Tallyloop</span></a>
<nav class="nav" aria-label="Main">{nav}</nav>
<div class="h-cta"><a class="login" href="contact.html">Log in</a><a class="btn" href="pricing.html">Start free</a></div>
</div></header>'''


FOOTER = f'''<footer class="site-footer"><div class="wrap">
<div class="f-grid">
<div><a class="brand light" href="index.html">{LOGO}<span>Tallyloop</span></a><p>Time tracking and invoicing for freelancers and small studios.</p></div>
<div><p class="f-h">Product</p><ul><li><a href="features.html">Features</a></li><li><a href="pricing.html">Pricing</a></li><li><a href="features.html#reminders">Payment reminders</a></li></ul></div>
<div><p class="f-h">Company</p><ul><li><a href="about.html">About</a></li><li><a href="contact.html">Contact</a></li></ul></div>
<div><p class="f-h">Get started</p><p>Free for your first client. No card needed.</p><a class="btn btn-sm" href="pricing.html">Start free</a></div>
</div>
<p class="concept">Concept project by Liam Curran: a fictional product. Customer names, quotes and figures are illustrative. <span class="ver">This is the fixed "after" version of a website rescue demo.</span></p>
</div></footer>'''


def page_hero(label, h1, lede=""):
    return (f'<section class="page-hero"><div class="wrap center"><p class="eyebrow">{label}</p>'
            f'<h1>{h1}</h1>' + (f'<p class="lede">{lede}</p>' if lede else "") + '</div></section>')


def mock_timer():
    rows = [("Homepage redesign", "Northfield Studio", "1:24:37", True), ("Brand guidelines", "Juniper Labs", "2:10:00", False),
            ("Client call", "Okafor &amp; Lee", "0:45:00", False), ("Blog illustrations", "Pixelwell", "3:05:00", False)]
    r = "".join(f'<li class="{"run" if run else ""}"><span><strong>{t}</strong><small>{c}</small></span><span class="dur">{d}</span>'
                f'<span class="play{" stop" if run else ""}"></span></li>' for t, c, d, run in rows)
    return f'<div class="mock mock-timer" aria-hidden="true"><div class="mh"><strong>Today</strong><span>7h 24m</span></div><ul>{r}</ul></div>'


def mock_invoice():
    return '''<div class="mock mock-inv" aria-hidden="true">
<div class="inv-top"><span class="inv-logo"></span><div><strong>Invoice #1043</strong><small>Due Dec 1 · Northfield Studio</small></div><span class="badge sent">Sent</span></div>
<div class="inv-rows"><div><span>Homepage redesign · 18.5 h × $85</span><b>$1,572.50</b></div>
<div><span>Design review calls · 3 h × $85</span><b>$255.00</b></div>
<div><span>Stock photo licence</span><b>$49.00</b></div></div>
<div class="inv-total"><span>Total (CAD)</span><b>$1,876.50</b></div>
<div class="inv-pay">Pay by card</div></div>'''


def mock_remind():
    return '''<div class="mock mock-remind" aria-hidden="true">
<div class="mail"><div class="mh"><strong>Friendly reminder: Invoice #1040</strong><span>Auto · 3 days overdue</span></div>
<p>Hi Alex, just a quick nudge that invoice #1040 for $960 was due on Nov 14. You can pay by card in a few seconds using the link below. Thanks!</p>
<span class="mail-btn">View &amp; pay invoice</span></div>
<div class="toast"><span class="ok"></span><div><strong>Payment received</strong><small>Brightside Co. paid $960.00</small></div></div></div>'''


PANELS = [
    ("timer", "Track", "A timer that stays out of your way", "Start tracking from any device in one click, tag the client and project, and get back to work. Tallyloop remembers your rates for each client.",
     ["Browser, desktop and mobile apps", "Add or edit time after the fact", "Idle detection, so a coffee break isn't billed"], mock_timer),
    ("invoices", "Invoice", "From hours to a polished invoice in two clicks", "Pick a client and date range. Tallyloop pulls in every tracked hour, applies your rates and builds a branded invoice ready to send.",
     ["Your logo, colours and payment terms", "Hourly, fixed-fee and expense lines", "Multi-currency for international clients"], mock_invoice),
    ("reminders", "Get paid", "Late payments chase themselves", "Clients pay by card straight from the invoice. If they don't, Tallyloop sends polite, automatic reminders on a schedule you set.",
     ["Reminders at 3, 7 and 14 days overdue", "Card payments land in days, not weeks", "See who's opened, viewed and paid"], mock_remind),
]


def panels_html(level="h2"):
    out = []
    for i, (pid, kicker, title, desc, bullets, mock) in enumerate(PANELS):
        b = "".join(f"<li>{I['check']}<span>{x}</span></li>" for x in bullets)
        out.append(f'''<div class="panel{" rev" if i % 2 else ""}" id="{pid}"><div class="panel-copy">
<p class="eyebrow">{i + 1:02d} · {kicker}</p><{level}>{title}</{level}><p>{desc}</p><ul class="ticks">{b}</ul>
<a class="link-arrow" href="pricing.html">Start free {I['arrow']}</a></div><div class="panel-mock">{mock()}</div></div>''')
    return '<section class="section"><div class="wrap panels">' + "".join(out) + "</div></section>"


def bento_html(title="Everything between “start timer” and “paid”"):
    cards = "".join(f'<div class="feat"><span class="f-ico">{I[k]}</span><h3>{t}</h3><p>{d}</p></div>' for k, t, d in C["features"])
    return f'''<section class="section tint"><div class="wrap"><div class="sec-head center"><p class="eyebrow">Features</p><h2>{title}</h2>
<p class="lede">Three jobs, done well: track time, invoice it, get paid. No project-management suite, no fifty-tab settings page.</p></div>
<div class="feat-grid">{cards}</div></div></section>'''


def pricing_cards():
    return "".join(
        f'<div class="plan{" featured" if f else ""}">' + ('<span class="tag">Most popular</span>' if f else "") +
        f'<h3>{n}</h3><p class="plan-sub">{sub}</p><p class="price">{p}<span>{per}</span></p>'
        f'<a class="btn btn-block{"" if f else " ghost"}" href="contact.html">{"Start free" if n == "Free" else "Try " + n + " free for 14 days"}</a>'
        f'<ul class="ticks">' + "".join(f"<li>{I['check']}<span>{x}</span></li>" for x in items) + "</ul></div>"
        for n, p, per, sub, items, f in C["plans"])


def pricing_section(level="h2", head=True):
    h = (f'<div class="sec-head center"><p class="eyebrow">Pricing</p><{level}>Simple pricing that starts at free</{level}>'
         f'<p class="lede">Prices in USD. Month-to-month, cancel any time.</p></div>') if head else f'<{level} class="sr-only">Plans</{level}>'
    return f'<section class="section"><div class="wrap">{h}<div class="plans">{pricing_cards()}</div></div></section>'


def faq_section():
    items = "".join(f"<details><summary>{q}</summary><p>{a}</p></details>" for q, a in C["faqs"])
    return f'''<section class="section"><div class="wrap faq-split"><div><p class="eyebrow">FAQ</p><h2>Common questions</h2>
<p>Something else? <a href="contact.html">Ask a human</a>. We reply within one business day.</p></div><div class="faq">{items}</div></div></section>'''


def reviews_section():
    cards = "".join(f'''<figure class="review">{STARS}<blockquote>“{q}”</blockquote><figcaption><span class="av" style="background:{c}">{n[0]}</span>
<span><strong>{n}</strong><small>{r}</small></span></figcaption></figure>''' for q, n, r, c in C["reviews"])
    return f'''<section class="section"><div class="wrap"><div class="sec-head center"><p class="eyebrow">Loved by freelancers</p>
<h2>Month-end, minus the afternoon</h2><p class="rating-line">{STARS} <strong>4.8 / 5</strong> from 1,200+ reviews</p></div>
<div class="reviews">{cards}</div></div></section>'''


CTA = f'''<section class="cta"><div class="wrap"><div class="cta-box">
<h2>Get your month-end afternoon back</h2><p>Free for your first client. No card needed. Set up in under five minutes.</p>
<div class="ctas center"><a class="btn btn-lg light" href="pricing.html">Start free</a><a class="btn btn-lg ghost-light" href="features.html">See all features</a></div>
</div></div></section>'''

STATS = '''<section class="stats"><div class="wrap">
<div><strong>9,000+</strong><span>freelancers and studios</span></div><div><strong>2.4M</strong><span>hours tracked</span></div>
<div><strong>$310M</strong><span>invoiced through Tallyloop</span></div><div><strong>11 days</strong><span>faster payment on average</span></div>
</div></section>'''

HERO_IMG = ('<img class="shot-img" src="assets/dashboard-1200.webp" srcset="assets/dashboard-640.webp 640w, assets/dashboard-1200.webp 1200w" '
            'sizes="(max-width: 1100px) 100vw, 1060px" width="1200" height="750" fetchpriority="high" '
            'alt="Tallyloop dashboard showing hours tracked this week, unbilled time, an hours-by-day chart, recent invoices and project budgets">')

PAGES = []  # (path, title, desc, body, schemas)
ORG = {"@context": "https://schema.org", "@type": "Organization", "@id": BASE + "/#org", "name": "Tallyloop",
       "url": BASE + "/", "logo": BASE + "/assets/logo.svg", "email": "hello@example.com"}
APP = {"@context": "https://schema.org", "@type": "SoftwareApplication", "name": "Tallyloop",
       "applicationCategory": "BusinessApplication", "operatingSystem": "Web, iOS, Android",
       "description": C["lede"], "publisher": {"@id": BASE + "/#org"},
       "offers": [{"@type": "Offer", "name": n, "price": p.strip("$"), "priceCurrency": "USD"} for n, p, *_ in C["plans"]]}


def crumbs(items):
    return {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": i + 1, "name": n, "item": BASE + "/" + u} for i, (u, n) in enumerate(items)]}


FAQ_LD = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
    {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in C["faqs"]]}

logos = "".join(f'<span class="{c}">{n}</span>' for n, c in CLIENTS)
steps = [("timer", "Track", "Hit start when you begin a task. Tag it to a client and project."),
         ("invoice", "Invoice", "At month-end, turn tracked hours into a branded invoice and send it."),
         ("card", "Get paid", "Clients pay online. Tallyloop sends reminders if they don't.")]
steps_html = "".join(f'<li><span class="s-ico">{I[k]}</span><strong>{t}</strong><p>{d}</p></li>' for k, t, d in steps)

PAGES.append(("index.html", "Tallyloop | Time Tracking & Invoicing Software for Freelancers",
    "Track time, turn hours into invoices in two clicks and get paid faster with automatic reminders. Free plan for your first client.",
    f'''<section class="hero"><div class="wrap center">
<a class="announce" href="features.html#reminders"><span>New</span> Automatic late-payment reminders {I['arrow']}</a>
<h1>{C["tagline"]}</h1>
<p class="lede">{C["lede"]}</p>
<div class="ctas center"><a class="btn btn-lg" href="pricing.html">Start free</a><a class="btn btn-lg ghost" href="features.html">See how it works</a></div>
<ul class="micro"><li>{I['check']} Free plan for your first client</li><li>{I['check']} No card needed</li><li>{I['check']} Cancel any time</li></ul>
<div class="shot"><div class="shot-frame">{HERO_IMG}</div>
<div class="float f1" aria-hidden="true"><span class="dot-run"></span><div><strong>01:24:37</strong><small>Homepage redesign</small></div></div>
<div class="float f2" aria-hidden="true"><span class="ok"></span><div><strong>Invoice #1042 paid</strong><small>Northfield Studio · $2,400</small></div></div></div>
</div></section>
<section class="logos"><div class="wrap"><p>Trusted by 9,000+ freelancers and small studios</p><div class="logo-row">{logos}</div></div></section>
<section class="section"><div class="wrap"><div class="sec-head center"><p class="eyebrow">How it works</p><h2>Three steps from “start timer” to “paid”</h2></div>
<ol class="steps">{steps_html}</ol></div></section>
{panels_html()}
{bento_html()}
{STATS}
{reviews_section()}
{pricing_section()}
{faq_section()}
{CTA}''', [ORG, APP, FAQ_LD]))

PAGES.append(("features.html", "Features: Timer, Invoicing & Payment Reminders | Tallyloop",
    "See how Tallyloop's one-click timer, hours-to-invoice builder, automatic payment reminders and project budgets save freelancers hours every month.",
    page_hero("Features", "Built for freelancers, not for project managers", "Three jobs, done well: track time, invoice it, get paid.")
    + panels_html() + bento_html("Plus the details that save you time") + STATS + CTA,
    [crumbs([("", "Home"), ("features.html", "Features")])]))

compare_rows = [("Active clients", "1", "Unlimited", "Unlimited"), ("Time tracking", "✓", "✓", "✓"), ("Invoices per month", "3", "Unlimited", "Unlimited"),
                ("Online card payments", "–", "✓", "✓"), ("Automatic reminders", "–", "✓", "✓"), ("Project budgets", "–", "✓", "✓"),
                ("Team members", "1", "1", "Up to 5"), ("Timesheet approvals", "–", "–", "✓"), ("Tax-time exports", "–", "–", "✓")]
compare = ("<div class=\"table-wrap\"><table class=\"compare\"><thead><tr><th scope=\"col\">Compare plans</th><th scope=\"col\">Free</th><th scope=\"col\">Solo</th><th scope=\"col\">Studio</th></tr></thead><tbody>"
           + "".join(f"<tr><th scope=\"row\">{r[0]}</th><td>{r[1]}</td><td>{r[2]}</td><td>{r[3]}</td></tr>" for r in compare_rows) + "</tbody></table></div>")
PAGES.append(("pricing.html", "Pricing: Free, Solo & Studio Plans | Tallyloop",
    "Tallyloop pricing: Free for one client, Solo at $9/month, Studio at $19/month for small teams. Month-to-month, cancel any time.",
    page_hero("Pricing", "Simple pricing that starts at free", "Prices in USD. Month-to-month. Cancel any time and take your data with you.")
    + pricing_section(head=False).replace('<section class="section">', '<section class="section pt0">')
    + f'<section class="section tint"><div class="wrap"><div class="sec-head center"><h2>Every plan, side by side</h2></div>{compare}</div></section>'
    + faq_section() + CTA,
    [crumbs([("", "Home"), ("pricing.html", "Pricing")]), APP, FAQ_LD]))

values = [("zap", "Fast by default", "Every screen loads quickly and every common task takes two clicks or fewer."),
          ("heart", "Small on purpose", "We build three things well instead of thirty things badly."),
          ("lock", "Your data is yours", "Export everything, any time, in plain CSV and PDF.")]
PAGES.append(("about.html", "About Tallyloop | Built by a Freelancer, for Freelancers",
    "Tallyloop started as a freelancer's month-end spreadsheet. Meet the small, independent team behind simple time tracking and invoicing.",
    page_hero("About", "Built because month-end took an afternoon")
    + '''<section class="section pt0"><div class="wrap narrow prose">
<p class="big">Tallyloop started as a spreadsheet. Its founder was freelancing as a designer, tracking hours in one app, building invoices in another and chasing payments by email. Every month-end took an afternoon.</p>
<p>We built Tallyloop to make that afternoon take five minutes. It does three things well: tracks time, turns that time into invoices and gets those invoices paid. That's it. No project-management suite, no CRM, no fifty-tab settings page.</p>
<p>We're a small, independent team, and we answer support emails ourselves.</p></div></section>'''
    + '<section class="section tint"><div class="wrap"><div class="sec-head center"><h2>What we believe</h2></div><div class="feat-grid three">'
    + "".join(f'<div class="feat"><span class="f-ico">{I[k]}</span><h3>{t}</h3><p>{d}</p></div>' for k, t, d in values)
    + "</div></div></section>" + STATS + CTA,
    [crumbs([("", "Home"), ("about.html", "About")]), ORG]))

PAGES.append(("contact.html", "Contact Tallyloop Support",
    "Questions about Tallyloop? Email hello@example.com or send a message. A real person on our small team will reply within one business day.",
    page_hero("Contact", "Talk to a human", "We reply within one business day, usually much sooner.")
    + f'''<section class="section pt0"><div class="wrap contact-grid">
<form class="contact-form" id="contact" novalidate>
<div><label for="n">Name</label><input id="n" name="name" autocomplete="name" required></div>
<div><label for="e">Email</label><input id="e" name="email" type="email" autocomplete="email" required></div>
<div><label for="t">Topic</label><select id="t" name="topic"><option>Question before signing up</option><option>Help with my account</option><option>Billing</option><option>Something else</option></select></div>
<div><label for="q">Message</label><textarea id="q" name="message" rows="5" required></textarea></div>
<button class="btn btn-lg" type="submit">Send message</button>
<p class="form-msg" role="status">Thanks! This is a concept site, so nothing was sent.</p></form>
<div class="contact-cards">
<div class="c-card">{I['mail']}<div><strong>Email</strong><p><a href="mailto:hello@example.com">hello@example.com</a></p></div></div>
<div class="c-card">{I['chat']}<div><strong>In-app chat</strong><p>Weekdays, 9am–5pm Eastern.</p></div></div>
<div class="c-card">{I['book']}<div><strong>Help centre</strong><p>Step-by-step guides for every feature.</p></div></div>
</div></div></section>''',
    [crumbs([("", "Home"), ("contact.html", "Contact")])]))

FORM_JS = '''document.querySelectorAll("form.contact-form").forEach(function(f){f.addEventListener("submit",function(e){e.preventDefault();
if(!f.reportValidity())return;f.querySelector(".form-msg").classList.add("show");f.reset();});});'''

# ------------------------------------------------------------------ AFTER
if A.exists():
    for p in A.iterdir():
        if p.name not in ("assets", "before"):
            p.unlink() if p.is_file() else shutil.rmtree(p)
(A / "assets").mkdir(parents=True, exist_ok=True)
shutil.copy(ROOT / "style.css", A / "assets" / "style.css")
shutil.copy(ROOT.parent / "_fonts" / "inter-latin-wght-normal.woff2", A / "assets" / "inter.woff2")
(A / "assets" / "logo.svg").write_text(LOGO.replace('class="logo" ', 'xmlns="http://www.w3.org/2000/svg" ').replace(' aria-hidden="true"', ""), encoding="utf-8")


def ld(o):
    return '<script type="application/ld+json">' + json.dumps(o, ensure_ascii=False, separators=(",", ":")) + "</script>"


for path, title, desc, body, schemas in PAGES:
    canon = BASE + "/" + ("" if path == "index.html" else path)
    pre = ('<link rel="preload" as="image" href="assets/dashboard-1200.webp" imagesrcset="assets/dashboard-640.webp 640w, assets/dashboard-1200.webp 1200w" imagesizes="(max-width: 1100px) 100vw, 1060px" fetchpriority="high">\n'
           if path == "index.html" else "")
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
<meta name="theme-color" content="#6a48f0">
<link rel="icon" href="assets/logo.svg" type="image/svg+xml">
<link rel="preload" href="assets/inter.woff2" as="font" type="font/woff2" crossorigin>
{pre}<link rel="stylesheet" href="assets/style.css">
{chr(10).join(ld(s) for s in schemas)}
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
{header(path)}
<main id="main">
{body}
</main>
{FOOTER}
<script>{FORM_JS}</script>
</body>
</html>
'''
    (A / path).write_text(html, encoding="utf-8")

(A / "404.html").write_text('<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>Page not found | Tallyloop</title><meta name="robots" content="noindex"><link rel="stylesheet" href="/tallyloop/assets/style.css"></head><body><main class="section"><div class="wrap center"><h1>Page not found</h1><p><a class="btn" href="/tallyloop/">Back to Tallyloop</a></p></div></main></body></html>', encoding="utf-8")
(A / "sitemap.xml").write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">' + "".join(
    f"<url><loc>{BASE}/{'' if p == 'index.html' else p}</loc><lastmod>{TODAY}</lastmod></url>" for p, *_ in PAGES) + "</urlset>\n", encoding="utf-8")
(A / "robots.txt").write_text(f"User-agent: *\nAllow: /\n\nSitemap: {BASE}/sitemap.xml\n", encoding="utf-8")
(A / ".nojekyll").write_text("", encoding="utf-8")


# ------------------------------------------------------------------ BEFORE (same pages, flawed delivery)
def degrade(html):
    """Turn the clean markup into what a quick SPA export typically ships."""
    def heading(m):
        tag, attrs = m.group(1), m.group(2) or ""
        if 'class="' in attrs:
            attrs = attrs.replace('class="', f'class="{tag} ', 1)
        else:
            attrs += f' class="{tag}"'
        return f"<div{attrs}>"
    html = re.sub(r"<(h[1-4])(\s[^>]*)?>", heading, html)
    html = re.sub(r"</h[1-4]>", "</div>", html)
    # links -> click-handler spans (not crawlable, not keyboard-focusable)
    def link(m):
        attrs = m.group(1)
        href = re.search(r'href="([^"]*)"', attrs).group(1)
        attrs = re.sub(r'\s*href="[^"]*"', "", attrs)
        route = href.split("#")[0].replace(".html", "") or "index"
        return f'<span data-go="{route}"{attrs}>'
    html = re.sub(r"<a(\s[^>]*)>", link, html)
    html = html.replace("</a>", "</span>")
    # landmarks and labelled controls -> plain divs
    for t in ("header", "nav", "main", "footer", "section", "figure", "figcaption", "blockquote"):
        html = re.sub(fr"<{t}(\s[^>]*)?>", lambda m: "<div" + (m.group(1) or "") + ">", html)
        html = html.replace(f"</{t}>", "</div>")
    html = re.sub(r'\s(aria-[a-z]+|role|scope|for|autocomplete)="[^"]*"', "", html)
    html = re.sub(r"<label>|<label\s[^>]*>", "<div class=\"lbl\">", html).replace("</label>", "</div>")
    # the hero image: one oversized PNG, no dimensions, no alt
    html = html.replace(HERO_IMG, '<img class="shot-img" src="assets/dashboard-screenshot-final-v3.png">')
    return html


(B / "assets").mkdir(parents=True, exist_ok=True)
# Same stylesheet, minus the self-hosted font (the "before" pulls fonts from Google instead).
before_css = [l for l in (ROOT / "style.css").read_text(encoding="utf-8").splitlines() if not l.startswith("@font-face")]
(B / "assets" / "index-4f9a1c2e.css").write_text(chr(10).join(before_css), encoding="utf-8")
before_footer = FOOTER.replace('<span class="ver">This is the fixed "after" version of a website rescue demo.</span>',
                               '<span class="ver">This is the deliberately flawed "before" version.</span>')
routes = {p.replace(".html", ""): degrade(body) for p, _, _, body, _ in PAGES}
content = {"header": {p.replace(".html", ""): degrade(header(p)) for p, *_ in PAGES}, "footer": degrade(before_footer), "routes": routes}
(B / "content.json").write_text(json.dumps(content, ensure_ascii=False), encoding="utf-8")
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
(B / "app.jsx").write_text('''// Generated-style SPA: every page renders client-side after content.json loads.
const { useState, useEffect } = React;

function useRoute() {
  const get = () => window.location.hash.replace("#/", "") || "index";
  const [r, setR] = useState(get());
  useEffect(() => { const f = () => setR(get()); window.addEventListener("hashchange", f); return () => window.removeEventListener("hashchange", f); }, []);
  return r;
}

function App() {
  const [c, setC] = useState(null);
  const route = useRoute();
  useEffect(() => { fetch("content.json").then(r => r.json()).then(setC); }, []);
  useEffect(() => { window.scrollTo(0, 0); }, [route]);
  const onClick = (e) => {
    const el = e.target.closest("[data-go]");
    if (el) { window.location.hash = "/" + el.getAttribute("data-go"); }
    if (e.target.closest("button[type=submit]")) { e.preventDefault(); const m = document.querySelector(".form-msg"); if (m) m.classList.add("show"); }
  };
  if (!c) return <div style={{padding: 80, textAlign: "center"}}>Loading...</div>;
  const key = c.routes[route] ? route : "index";
  return (<div onClick={onClick}>
    <div dangerouslySetInnerHTML={{__html: c.header[key]}} />
    <div dangerouslySetInnerHTML={{__html: c.routes[key]}} />
    <div dangerouslySetInnerHTML={{__html: c.footer}} />
  </div>);
}

ReactDOM.createRoot(document.getElementById("root")).render(<App />);
''', encoding="utf-8")
(B / ".nojekyll").write_text("", encoding="utf-8")
print("built", len(PAGES), "pages in after/ and the before/ SPA; base", BASE)
