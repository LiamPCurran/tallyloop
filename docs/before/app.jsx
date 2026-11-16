// Generated-style SPA: everything renders client-side after content.json loads.
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
