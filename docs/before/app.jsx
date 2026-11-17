// Generated-style SPA: every page renders client-side after content.json loads.
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
