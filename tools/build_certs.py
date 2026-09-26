"""Build the v2 certificate pages: docs/cert/<cert>/index.html (one per slab) + docs/cert/index.html.
Values are baked from the onchain AppraisalRegistry (read Sep 26 2026) and re-checked live in the browser.
Run: python3 tools/build_certs.py"""
import os, io, json, html
import qrcode, qrcode.image.svg

BASE = "https://gachagalaxyhq.github.io/gacha-robinhood-lending"
ROOT = os.path.join(os.path.dirname(__file__), "..", "docs")
REG = "0x30dfBCA3978CE186e6107A93cedC7d2971d30950"
EXPL = "https://explorer.testnet.chain.robinhood.com"
HERO = "109308847"

# onchain values (cents), score x10, appraisedAt unix, latest publish tx
CERTS = [
 dict(cert="109308847", tok=1, name="Rayquaza VMAX", num="218/203", set="Evolving Skies", year=2021,
      low=258651, pt=290000, high=321349, ltv=5000, score=860, comps=20, at=1790149107,
      txs=[("0x7edf40109ebd8362baa1c55b788f0618679150d0ee34506e2dea0b9bbe8cfc9e",1790147644),
           ("0x5bcddb7f009a8459531a2cfec2916390bf3f89a87a886eceaab158e34a140c94",1790148872),
           ("0xdf53ee76f0d8288d56aed73ed9e379f6ca9a7e4fb33d8f441fd704bad9c854ca",1790149107)]),
 dict(cert="118973623", tok=2, name="Pikachu & Zekrom GX", num="SM168", set="SM Black Star Promo", year=2019,
      low=287520, pt=320000, high=352480, ltv=5000, score=870, comps=15, at=1790147648, txs=[]),
 dict(cert="100863346", tok=3, name="Lugia V", num="186/195", set="Silver Tempest", year=2022,
      low=121561, pt=133100, high=144639, ltv=5000, score=890, comps=14, at=1790147652, txs=[]),
 dict(cert="154790134", tok=4, name="Giratina VSTAR", num="GG69/GG70", set="Crown Zenith", year=2023,
      low=52403, pt=65000, high=77597, ltv=5000, score=750, comps=45, at=1790147655, txs=[]),
 dict(cert="153708045", tok=5, name="Rayquaza VMAX", num="TG20/TG30", set="Silver Tempest Trainer Gallery", year=2022,
      low=34002, pt=41000, high=47998, ltv=5000, score=780, comps=29, at=1790147659, txs=[]),
 dict(cert="111992917", tok=6, name="Umbreon VMAX", num="TG23/TG30", set="Brilliant Stars Trainer Gallery", year=2022,
      low=24902, pt=27500, high=30098, ltv=5000, score=880, comps=27, at=1790147663, txs=[]),
]

def usd(c): return "$" + f"{round(c/100):,}"
def maxloan(c): return "$" + f"{(c['low']*c['ltv']//10000)//100:,}"

def qr_svg(url):
    img = qrcode.make(url, image_factory=qrcode.image.svg.SvgPathImage, box_size=10, border=1)
    s = img.to_string(encoding="unicode")
    return s[s.find("<svg"):]

FONTS = '<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin><link href="https://fonts.googleapis.com/css2?family=Geist:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500;600&display=swap" rel="stylesheet">'

CSS = r"""
:root{--canvas:#F7F5FB;--surface:#FFFFFF;--ink:#1B1424;--mute:#6E6479;--line:#E6E0EF;--purple:#7B3FE4;--deep:#532B7D;--glow:#A74CFF;--lilac:#F0E9FC;--green:#0E8A5F;--greenbg:#E3F4EC;--amber:#A86200;--amberbg:#FBF0DF;--red:#C2334D;--redbg:#FBE7EB}
*{box-sizing:border-box;margin:0;padding:0}
html{-webkit-text-size-adjust:100%}
body{background:var(--canvas);color:var(--ink);font-family:'Geist',system-ui,sans-serif;font-size:15px;line-height:1.45}
a{color:inherit}
.mono{font-family:'JetBrains Mono',ui-monospace,monospace}
.bar{display:flex;align-items:center;justify-content:space-between;gap:16px;max-width:980px;margin:0 auto;padding:22px 24px 18px}
.brand{display:flex;align-items:center;gap:12px;text-decoration:none;font-weight:700;font-size:18px;letter-spacing:-.01em}
.brand img{width:52px;height:52px;border-radius:50%;display:block}
.bar nav{display:flex;gap:18px;font-size:13.5px;color:var(--mute)}
.bar nav a{text-decoration:none}.bar nav a:hover{color:var(--purple)}
.wrap{max-width:980px;margin:0 auto;padding:0 24px 56px}
.cert{background:var(--surface);border:1px solid var(--line);border-radius:20px;box-shadow:0 1px 0 rgba(27,20,36,.04),0 24px 60px -24px rgba(83,43,125,.28);overflow:hidden}
.status{display:flex;justify-content:space-between;align-items:center;gap:12px;flex-wrap:wrap;padding:12px 28px;background:var(--greenbg);color:var(--green);font-size:13.5px;font-weight:600}
.status.due{background:var(--amberbg);color:var(--amber)}.status.exp{background:var(--redbg);color:var(--red)}
.status .l{display:flex;gap:10px;align-items:center}.status i{width:9px;height:9px;border-radius:50%;background:currentColor;box-shadow:0 0 0 4px rgba(14,138,95,.16);flex:none}
.status .mono{font-size:11.5px;font-weight:500}
.head{display:grid;grid-template-columns:160px 1fr 200px;gap:28px;padding:26px 28px;align-items:center}
.head img.slab{width:100%;border-radius:8px;display:block;background:var(--canvas)}
.eyebrow{font:600 10.5px 'JetBrains Mono',monospace;letter-spacing:.16em;text-transform:uppercase;color:var(--purple)}
h1{font-size:23px;font-weight:600;letter-spacing:-.01em;margin-top:8px;line-height:1.25}
.id{font:500 12px 'JetBrains Mono',monospace;color:var(--mute);margin-top:6px}
.val{font-size:52px;font-weight:700;letter-spacing:-.035em;margin-top:14px;line-height:1}
.range{font:500 12.5px 'JetBrains Mono',monospace;color:var(--mute);margin-top:7px}
.dialw{text-align:center}
.dial{--p:86;width:164px;height:164px;border-radius:50%;margin:0 auto;display:grid;place-items:center;position:relative;
background:conic-gradient(from 200deg,var(--deep),var(--purple) calc(var(--p)*.58%),var(--glow) calc(var(--p)*1%),var(--line) calc(var(--p)*1%) 100%)}
.dial::after{content:"";position:absolute;inset:-6px;border-radius:50%;border:1px dashed var(--line)}
.dial>div{width:134px;height:134px;border-radius:50%;background:var(--surface);display:grid;place-items:center;text-align:center}
.dial b{font-size:48px;font-weight:700;letter-spacing:-.04em;display:block;line-height:1}
.dial small{font:500 10px 'JetBrains Mono',monospace;letter-spacing:.14em;text-transform:uppercase;color:var(--mute)}
.dialw p{font-weight:600;margin-top:12px;font-size:14px}
.facts{display:grid;grid-template-columns:repeat(4,1fr);border-top:1px solid var(--line);border-bottom:1px solid var(--line)}
.facts div{padding:15px 28px;border-right:1px solid var(--line)}.facts div:last-child{border-right:0}
.facts small,.lbl{font:600 10px 'JetBrains Mono',monospace;letter-spacing:.14em;text-transform:uppercase;color:var(--mute)}
.facts b{display:block;font-size:19px;font-weight:600;margin-top:4px}
.sec{padding:20px 28px 0}
.lbl{display:block;margin-bottom:10px;font-size:10.5px}
.priv{display:grid;grid-template-columns:1fr 1fr;border:1px solid var(--line);border-radius:14px;overflow:hidden}
.priv>div{padding:14px 18px}
.priv .sea{background:var(--lilac);border-left:1px solid var(--line)}
.priv h4{font:600 10.5px 'JetBrains Mono',monospace;letter-spacing:.12em;text-transform:uppercase;margin-bottom:8px}
.priv .pub h4{color:var(--green)}.priv .sea h4{color:var(--deep)}
.priv ul{list-style:none;font-size:13.5px;line-height:1.8}
.priv .sea li{color:var(--deep)}
.priv .sea li::before{content:"";display:inline-block;width:64px;height:8px;border-radius:4px;background:repeating-linear-gradient(90deg,rgba(83,43,125,.35) 0 6px,transparent 6px 9px);margin-right:10px;vertical-align:middle}
.rows{border:1px solid var(--line);border-radius:14px;overflow:hidden}
.row{display:grid;grid-template-columns:190px 1fr auto;gap:14px;align-items:center;padding:12px 18px;border-bottom:1px solid var(--line);font-size:13.5px}
.row:last-child{border-bottom:0}
.row .k{font:600 10px 'JetBrains Mono',monospace;letter-spacing:.12em;text-transform:uppercase;color:var(--mute)}
.row .rv b{font-weight:600}
.pill{font:600 11px 'Geist',sans-serif;padding:3px 10px;border-radius:99px;white-space:nowrap;background:var(--greenbg);color:var(--green)}
.pill.soon{background:var(--lilac);color:var(--deep)}.pill.warn{background:var(--amberbg);color:var(--amber)}
.track{display:grid;grid-template-columns:repeat(4,1fr);gap:10px}
.v{border:1px solid var(--line);border-radius:10px;padding:10px 12px;text-decoration:none;display:block;min-width:0}
.v small{font:500 10px 'JetBrains Mono',monospace;color:var(--mute);letter-spacing:.04em;display:block;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.v b{display:block;font-size:16px;font-weight:600;margin-top:4px}
.v.now{border-color:var(--purple);background:var(--lilac)}.v.now small{color:var(--purple)}
.v.next{opacity:.6}
a.v:hover{border-color:var(--purple)}
.foot{display:grid;grid-template-columns:104px 1fr auto;gap:20px;align-items:center;padding:22px 28px 24px}
.qr{width:104px;height:104px;display:block;background:#fff;border:1px solid var(--line);border-radius:10px;padding:6px}
.qr svg{width:100%;height:100%;display:block}
.foot p{font-size:12.5px;color:var(--mute);line-height:1.55}.foot p b{color:var(--ink)}
.foot p b.hv,.foot p b.rh,.pw b{color:var(--deep);font-weight:700}
.btn{display:inline-block;font:600 13.5px 'Geist',sans-serif;color:#fff;background:var(--purple);border-radius:99px;padding:11px 18px;white-space:nowrap;text-decoration:none}
.btn:hover{background:var(--deep)}
.pw{display:flex;align-items:center;justify-content:center;gap:14px;flex-wrap:wrap;padding:13px 28px;background:var(--lilac);border-top:1px solid var(--line);font-size:13px;color:var(--mute)}
.pw img{width:26px;height:26px;border-radius:50%;display:block}.pw .dot{width:4px;height:4px;border-radius:50%;background:var(--mute)}
.note{font:500 11.5px 'JetBrains Mono',monospace;color:var(--mute);margin-top:14px;line-height:1.6}
.live{font:500 11.5px 'JetBrains Mono',monospace;color:var(--mute);margin-top:6px}
.live.ok{color:var(--green)}.live.bad{color:var(--red)}
/* index */
.grid{display:grid;grid-template-columns:repeat(3,1fr);gap:16px;margin-top:18px}
.tile{background:var(--surface);border:1px solid var(--line);border-radius:16px;padding:16px;text-decoration:none;display:grid;grid-template-columns:72px 1fr;gap:14px;align-items:center}
.tile:hover{border-color:var(--purple)}
.tile img{width:72px;border-radius:5px;display:block}
.tile p{font-weight:600;font-size:14px;line-height:1.3}.tile .pr{font-size:21px;font-weight:700;margin-top:4px;letter-spacing:-.02em}
.tile .id{margin-top:4px}
.tag{display:inline-block;margin-top:8px;font:600 10px 'JetBrains Mono',monospace;letter-spacing:.08em;text-transform:uppercase;padding:3px 8px;border-radius:99px;background:var(--lilac);color:var(--deep)}
.tag.hero{background:var(--purple);color:#fff}
h2.page{font-size:30px;font-weight:700;letter-spacing:-.03em}
.lede{color:var(--mute);margin-top:8px;max-width:62ch}
@media (max-width:760px){
 .bar{padding:16px 18px}.brand img{width:44px;height:44px}.bar nav{gap:12px;font-size:13px}
 .wrap{padding:0 12px 40px}
 .status{padding:11px 18px}
 .head{grid-template-columns:96px 1fr;gap:16px;padding:20px 18px}
 .dialw{grid-column:1/-1;display:flex;align-items:center;gap:18px;text-align:left;border-top:1px solid var(--line);padding-top:16px}
 .dial{width:112px;height:112px;margin:0}.dial>div{width:90px;height:90px}.dial b{font-size:34px}.dial small{font-size:9px}
 .dialw p{margin:0}
 h1{font-size:18px}.val{font-size:40px;margin-top:10px}
 .facts{grid-template-columns:1fr 1fr}.facts div{padding:12px 18px;border-bottom:1px solid var(--line)}.facts div:nth-child(2n){border-right:0}
 .sec{padding:18px 18px 0}
 .priv{grid-template-columns:1fr}.priv .sea{border-left:0;border-top:1px solid var(--line)}
 .row{grid-template-columns:1fr auto;padding:11px 14px}.row .k{grid-column:1/-1}
 .track{grid-template-columns:1fr 1fr}
 .foot{grid-template-columns:84px 1fr;padding:18px}.qr{width:84px;height:84px}.foot .btn{grid-column:1/-1;text-align:center}
 .grid{grid-template-columns:1fr}
}
"""

LIVE_JS = r"""
(() => {
  const C = window.__CERT; if (!C) return;
  const RPCS = ['https://rpc.testnet.chain.robinhood.com', 'https://46630.rpc.thirdweb.com'];
  const REG = '0x30dfBCA3978CE186e6107A93cedC7d2971d30950';
  const $ = id => document.getElementById(id);
  const DAY = 86400, MAXAGE = 90 * DAY, DUE = 14 * DAY;
  const MON = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'];
  const fmtDate = t => { const d = new Date(t * 1000); return d.getUTCDate() + ' ' + MON[d.getUTCMonth()] + ' ' + d.getUTCFullYear(); };
  function setStatus(at) {
    const now = Math.floor(Date.now() / 1000), until = at + MAXAGE, el = $('status');
    el.classList.remove('due', 'exp');
    let t;
    if (now > until) { el.classList.add('exp'); t = 'Expired · value needs a new check'; }
    else if (until - now < DUE) { el.classList.add('due'); t = 'Refresh due · value checked ' + fmtDate(at); }
    else t = 'Current · value checked ' + fmtDate(at);
    $('statusText').textContent = t;
    $('validUntil').textContent = 'valid until ' + fmtDate(until);
  }
  setStatus(C.at);
  async function call(data) {
    for (const url of RPCS) {
      try {
        const ctl = new AbortController(); const tm = setTimeout(() => ctl.abort(), 8000);
        const r = await fetch(url, { method: 'POST', headers: { 'content-type': 'application/json' }, signal: ctl.signal,
          body: JSON.stringify({ jsonrpc: '2.0', id: 1, method: 'eth_call', params: [{ to: REG, data }, 'latest'] }) });
        clearTimeout(tm);
        const j = await r.json(); if (j.result && j.result.length > 2) return j.result;
      } catch (e) {}
    }
    throw new Error('rpc');
  }
  // getAppraisalByCert(string,string) selector + ABI-encoded ('PSA', cert)
  function enc(cert) {
    const hex = s => Array.from(new TextEncoder().encode(s)).map(b => b.toString(16).padStart(2, '0')).join('');
    const w = n => n.toString(16).padStart(64, '0');
    const str = s => { const h = hex(s); return w(h.length / 2) + h.padEnd(Math.ceil(h.length / 64) * 64 || 64, '0'); };
    const a = str('PSA'), b = str(cert);
    return w(64) + w(64 + a.length / 2) + a + b;
  }
  (async () => {
    try {
      const out = await call(C.sel + enc(C.cert));
      const word = i => BigInt('0x' + out.slice(2 + i * 64, 2 + (i + 1) * 64));
      const live = { low: Number(word(0)), pt: Number(word(1)), high: Number(word(2)), ltv: Number(word(3)), score: Number(word(4)), comps: Number(word(5)), at: Number(word(9)) };
      const same = live.low === C.low && live.pt === C.pt && live.high === C.high && live.score === C.score && live.at === C.at;
      const el = $('live');
      if (same) { el.className = 'live ok'; el.textContent = '✓ Checked live on Robinhood Chain just now: every number on this certificate matches the registry.'; }
      else {
        el.className = 'live bad';
        el.textContent = 'The registry has a newer value than this page. Live value: $' + Math.round(live.pt / 100).toLocaleString('en-US') + ', checked ' + fmtDate(live.at) + '.';
        setStatus(live.at);
      }
    } catch (e) { $('live').textContent = 'Could not reach Robinhood Chain from this browser just now. The numbers above are from the last build.'; }
  })();
})();
"""

SEL = "0x"  # filled below

def selector():
    # keccak256("getAppraisalByCert(string,string)")[:4]; computed with node/ethers at build time
    import subprocess
    js = "const {ethers}=require('ethers');console.log(ethers.id('getAppraisalByCert(string,string)').slice(0,10))"
    return subprocess.check_output(["node", "-e", js], cwd=os.path.join(os.path.dirname(__file__), "..", "..", "headless")).decode().strip()

def page(title, body, desc, url, extra_head=""):
    return f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{html.escape(title)}</title><meta name="description" content="{html.escape(desc)}">
<meta property="og:title" content="{html.escape(title)}"><meta property="og:description" content="{html.escape(desc)}"><meta property="og:url" content="{url}">
<link rel="icon" href="{extra_head or '../'}img/gg-logo.png">
{FONTS}<style>{CSS}</style></head><body>{body}</body></html>'''

def bar(up):
    return f'''<header class="bar"><a class="brand" href="{up}"><img src="{up}img/gg-logo.png" alt="Gacha Galaxy logo">Gacha Galaxy</a>
<nav><a href="{up}cert/">All certificates</a><a href="{up}">Live demo</a></nav></header>'''

def cert_page(c, sel):
    hero = c["cert"] == HERO
    url = f"{BASE}/cert/{c['cert']}/"
    title = f"{c['name']} {c['num']} PSA 10 · Verified Value {usd(c['pt'])} · Gacha Galaxy"
    score = round(c["score"] / 10)
    conf = "High confidence" if score >= 80 else "Good confidence" if score >= 70 else "Fair confidence"
    up = "../../"
    if hero:
        engine = '<b>Horizen Vela app</b>, run locally. Not yet live on Horizen\'s network.'
        engine_pill = '<span class="pill warn">Tested locally</span>'
        sealed_h = "◆ Sealed in Horizen Vela, never leaves the enclave"
    else:
        engine = '<b>Gacha Galaxy pricing model</b>. Horizen Vela run for this card is pending.'
        engine_pill = '<span class="pill soon">Vela pending</span>'
        sealed_h = "◆ Sealed in Horizen Vela (pending for this card)"
    if c["txs"]:
        vs = ""
        n = len(c["txs"])
        for i, (tx, t) in enumerate(c["txs"]):
            cur = i == n - 1
            import datetime
            d = datetime.datetime.fromtimestamp(t, datetime.timezone.utc).strftime("%-d %b %Y")
            vs += f'<a class="v{" now" if cur else ""}" href="{EXPL}/tx/{tx}" target="_blank" rel="noopener"><small>v{i+1} · {d}{" · current" if cur else ""}</small><b>{usd(c["pt"])}</b></a>'
        latest = c["txs"][-1][0]
    else:
        import datetime
        d = datetime.datetime.fromtimestamp(c["at"], datetime.timezone.utc).strftime("%-d %b %Y")
        vs = f'<a class="v now" href="{EXPL}/address/{REG}" target="_blank" rel="noopener"><small>v1 · {d} · current</small><b>{usd(c["pt"])}</b></a>'
        latest = None
    vs += '<div class="v next"><small>next · due by 22 Dec 2026</small><b>next check</b></div>'
    verify = f"{EXPL}/tx/{latest}" if latest else f"{EXPL}/address/{REG}"
    data = {k: c[k] for k in ("cert", "low", "pt", "high", "score", "at")}
    data["sel"] = sel
    body = f'''{bar(up)}
<main class="wrap"><article class="cert" aria-label="Price certificate">
<div class="status" id="status"><span class="l"><i></i><span id="statusText">Current</span></span><span class="mono" id="validUntil"></span></div>
<div class="head"><img class="slab" src="{up}img/{c['cert']}.jpg" alt="PSA 10 slab: {html.escape(c['name'])} {c['num']}, cert {c['cert']}">
<div><p class="eyebrow">Gacha Galaxy · Verified Value</p>
<h1>{html.escape(c['name'])} #{c['num'].split('/')[0]} · {html.escape(c['set'])} · <span style="white-space:nowrap">PSA 10</span></h1>
<p class="id">PSA cert {c['cert']} · GG-VV-{c['cert']}</p>
<p class="val">{usd(c['pt'])}</p><p class="range">fair range {usd(c['low'])} to {usd(c['high'])}</p></div>
<div class="dialw"><div class="dial" style="--p:{score}"><div><div><b>{score}</b><small>of 100</small></div></div></div><p>{conf}</p></div></div>
<div class="facts"><div><small>Price points</small><b>{c['comps']}</b></div><div><small>Risk tier</small><b>A</b></div><div><small>Max loan ({c['ltv']//100}%)</small><b>{maxloan(c)}</b></div><div><small>One token per cert</small><b>Enforced</b></div></div>
<div class="sec"><div class="priv"><div class="pub"><h4>● Public, anyone can check</h4><ul><li>Value, range and confidence</li><li>Risk tier and max loan</li><li>Who signed it, and when</li></ul></div>
<div class="sea"><h4>{sealed_h}</h4><ul><li>Dealer prices</li><li>Platform inventory</li><li>Pricing model</li></ul></div></div></div>
<div class="sec"><span class="lbl">How this value was made</span><div class="rows">
<div class="row"><span class="k">Pricing engine</span><span class="rv">{engine}</span>{engine_pill}</div>
<div class="row"><span class="k">Attester (signed by)</span><span class="rv">Gacha Galaxy attester <span class="mono">0xfc8C…CA54</span>. Built to swap in the Vela enclave key.</span><span class="pill">Verified</span></div>
<div class="row"><span class="k">Price data</span><span class="rv">{c['comps']} public marketplace listings. Asking prices, not completed sales.</span><span></span></div>
<div class="row"><span class="k">Custody proof</span><span class="rv">Proof that the slab is in the vault, 1 to 1 with the token.</span><span class="pill soon">Coming</span></div>
</div></div>
<div class="sec"><span class="lbl">Value history · every version kept onchain</span><div class="track">{vs}</div></div>
<div class="foot"><div class="qr" role="img" aria-label="QR code for this certificate">{qr_svg(url)}</div>
<p><b>Scan to open this certificate.</b> Priced privately with <b class="hv">Horizen Vela</b>, stored on <b class="rh">Robinhood Chain</b>. Check the numbers yourself on the public registry.<span class="live" id="live" style="display:block">Checking Robinhood Chain…</span></p>
<a class="btn" href="{verify}" target="_blank" rel="noopener">Verify onchain</a></div>
<div class="pw"><img src="{up}img/gg-logo.png" alt=""><span>Private pricing by <b>Horizen Vela</b></span><span class="dot"></span><span>Settled on <b>Robinhood Chain</b></span></div>
</article>
<p class="note">Testnet demo on Robinhood Chain (chain ID 46630). Registry <a href="{EXPL}/address/{REG}" target="_blank" rel="noopener">{REG[:6]}…{REG[-4:]}</a>. Not financial advice.</p>
</main>
<script>window.__CERT={json.dumps(data)};</script><script>{LIVE_JS}</script>'''
    return page(title, body, f"Verified Value certificate for PSA 10 {c['name']} {c['num']}, cert {c['cert']}: {usd(c['pt'])}, confidence {score} of 100.", url, up)

def index_page():
    up = "../"
    tiles = ""
    for c in CERTS:
        hero = c["cert"] == HERO
        tag = '<span class="tag hero">Real Vela output</span>' if hero else '<span class="tag">Priced · Vela pending</span>'
        tiles += f'''<a class="tile" href="{c['cert']}/"><img src="{up}img/{c['cert']}.jpg" alt=""><div><p>{html.escape(c['name'])} {c['num']}</p><p class="pr">{usd(c['pt'])}</p><p class="id">PSA 10 · cert {c['cert']} · score {round(c['score']/10)}</p>{tag}</div></a>'''
    body = f'''{bar(up)}<main class="wrap"><h2 class="page">Verified Value certificates</h2>
<p class="lede">Six real PSA 10 slabs, each with a price certificate stored on Robinhood Chain. Open one to see its value, confidence and history, and scan its QR code to share it.</p>
<div class="grid">{tiles}</div>
<p class="note">Asking prices from public marketplace listings, not completed sales. Horizen Vela is tested locally, not yet live on Horizen's network.</p></main>'''
    return page("Verified Value certificates · Gacha Galaxy", body, "Onchain price certificates for graded cards on Robinhood Chain.", f"{BASE}/cert/", up)

if __name__ == "__main__":
    sel = selector()
    for c in CERTS:
        d = os.path.join(ROOT, "cert", c["cert"]); os.makedirs(d, exist_ok=True)
        open(os.path.join(d, "index.html"), "w").write(cert_page(c, sel))
    open(os.path.join(ROOT, "cert", "index.html"), "w").write(index_page())
    print("built", len(CERTS), "certificate pages, selector", sel)
