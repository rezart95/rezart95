"""Generate the profile banner and the project dock.

Usage (from anywhere):
    pip install -r tools/banner/requirements.txt
    python tools/banner/generate.py

Writes assets/banner.svg and assets/dock/<id>.svg in the repo root.

- Banner: name and title on the left; on the right a 3D feed-forward neural
  network (layers 3-6-6-3) spinning on its flow axis with a forward-pass
  pulse, inside three tilted orbits. Each satellite carries one keyword
  (edit ORBITS). Satellites are evenly spaced, move at a constant angular
  rate and grow/brighten on the near half of their orbit.
- Dock: dark tiles joined under the banner. The label tile is 16% wide and
  each app tile 14%, so label + 6 apps = the banner width. Adding or
  removing an app means changing those percentages in README.md (and the
  tile widths LW/AW here) so the row still sums to 100%.
- prefers-reduced-motion: motion hidden, a static frame with the same
  composition shown instead.
- Fonts: Geist and Geist Mono (SIL OFL, see fonts/OFL.txt), instanced,
  subset and embedded as WOFF so the SVGs render the same everywhere.
"""
import base64, io, math, os, sys
from fontTools import subset
from fontTools.ttLib import TTFont
from fontTools.varLib import instancer
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
FONT_DIR = os.path.join(HERE, 'fonts')
ICONS = os.path.join(HERE, 'icons')
REPO = os.path.abspath(os.path.join(HERE, '..', '..'))


def font_uri(path, axes, text):
    f = instancer.instantiateVariableFont(TTFont(path, recalcTimestamp=False), axes)  # stable output: no build timestamp
    o = subset.Options(); o.flavor = 'woff'; o.layout_features = ['kern']; o.name_IDs = ['*']; o.drop_tables += ['meta']
    s = subset.Subsetter(o); s.populate(text=text); s.subset(f)
    b = io.BytesIO(); f.flavor = 'woff'; f.save(b)
    return 'data:font/woff;base64,' + base64.b64encode(b.getvalue()).decode()


CH = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789 ·/-'
sans_l = font_uri(f'{FONT_DIR}/Geist.ttf', {'wght': 300}, CH)
sans_m = font_uri(f'{FONT_DIR}/Geist.ttf', {'wght': 500}, CH)
mono = font_uri(f'{FONT_DIR}/GeistMono.ttf', {'wght': 400}, CH)

BG, BG2, DOT, LINE, DIM, GOLD, GOLD_HI, INK, SUB = (
    '#07080C', '#121726', '#2B3142', '#C9CFDC', '#5B6273', '#D2B072', '#F4E6C4', '#F1F2F5', '#9AA1B0')
PANEL = '#0A0C12'

W, H = 1000, 440
CX, CY = 700, 220
o = []
a = o.append
a(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-labelledby="t d">')
a('<title id="t">Rezart Abazi, Senior AI Engineer</title>')
a('<desc id="d">A three-dimensional neural network at the centre of three orbits. Satellites travel around it, each '
  'named after a part of agentic AI work: agents, MCP, evals, guardrails, RAG, tools, fine-tuning, memory, context, embeddings.</desc>')
a('<style>'
  f'@font-face{{font-family:GL;src:url({sans_l}) format("woff")}}@font-face{{font-family:GM;src:url({mono}) format("woff")}}'
  '.n{font-family:GL,"Segoe UI",Helvetica,sans-serif;font-weight:300;letter-spacing:-.015em}'
  '.c{font-family:GM,ui-monospace,Consolas,monospace;letter-spacing:.14em}'
  '.st{display:none}'
  '@keyframes fp{0%,100%{opacity:.55}12%{opacity:1}30%{opacity:.55}}'
  '.L0,.L1,.L2,.L3{animation:fp 3.2s ease-in-out infinite}.L1{animation-delay:.35s}.L2{animation-delay:.7s}.L3{animation-delay:1.05s}'
  '@media (prefers-reduced-motion:reduce){.mv{display:none}.st{display:inline}.L0,.L1,.L2,.L3{animation:none}}'
  '</style>')
a('<defs>'
  f'<radialGradient id="atm" cx="{CX/W:.3f}" cy="{CY/H:.3f}" r="0.62"><stop offset="0" stop-color="{BG2}"/><stop offset="1" stop-color="{BG}"/></radialGradient>'
  f'<radialGradient id="fade" cx="{CX/W:.3f}" cy="0.5" r="0.55"><stop offset="0" stop-color="#fff" stop-opacity="1"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></radialGradient>'
  f'<mask id="m"><rect width="{W}" height="{H}" fill="url(#fade)"/></mask>'
  f'<pattern id="dots" width="22" height="22" patternUnits="userSpaceOnUse"><circle cx="11" cy="11" r="0.9" fill="{DOT}"/></pattern>'
  f'<radialGradient id="aura"><stop offset="0" stop-color="{GOLD}" stop-opacity=".18"/><stop offset="1" stop-color="{GOLD}" stop-opacity="0"/></radialGradient>'
  '</defs>')
SHAPE = f'M18 0H{W-18}A18 18 0 0 1 {W} 18V{H}H0V18A18 18 0 0 1 18 0Z'
a(f'<path d="{SHAPE}" fill="url(#atm)"/>')
a(f'<path d="{SHAPE}" fill="url(#dots)" mask="url(#m)"/>')

# instrument ring
R = 200
for k in range(0, 360, 3):
    long = k % 30 == 0
    r1, r2 = R, R + (9 if long else 4)
    t = math.radians(k)
    a(f'<line x1="{CX + r1*math.cos(t):.1f}" y1="{CY + r1*math.sin(t):.1f}" x2="{CX + r2*math.cos(t):.1f}" '
      f'y2="{CY + r2*math.sin(t):.1f}" stroke="{DIM}" stroke-opacity="{.7 if long else .3}"/>')

# orbits: rx, ry, tilt, seconds per turn, first phase, base radius, satellites (keyword, gold?)
ORBITS = [
    (266, 102, -12, 80, 0.03, 4.6, [('AGENTS', True), ('MCP', False), ('EVALS', False), ('GUARDRAILS', False)]),
    (194, 78, 13, 54, 0.20, 4.0, [('RAG', False), ('TOOLS', False), ('FINE-TUNING', False)]),
    (126, 54, -6, 34, 0.42, 3.5, [('MEMORY', False), ('CONTEXT', False), ('EMBEDDINGS', False)]),
]


def pt(rx, ry, tilt, u):
    ct, stt = math.cos(math.radians(tilt)), math.sin(math.radians(tilt))
    x, y = rx * math.cos(u), ry * math.sin(u)
    return CX + x*ct - y*stt, CY + x*stt + y*ct


def depth(u):
    return (1 + math.sin(u)) / 2


for rx, ry, tilt, *_ in ORBITS:
    p0, p1 = pt(rx, ry, tilt, 0), pt(rx, ry, tilt, math.pi)
    a(f'<path d="M{p1[0]:.1f} {p1[1]:.1f} A{rx} {ry} {tilt} 0 1 {p0[0]:.1f} {p0[1]:.1f}" fill="none" stroke="{LINE}" stroke-opacity=".13"/>')
    a(f'<path d="M{p0[0]:.1f} {p0[1]:.1f} A{rx} {ry} {tilt} 0 1 {p1[0]:.1f} {p1[1]:.1f}" fill="none" stroke="{LINE}" stroke-opacity=".34"/>')

# ---- core: 3D neural network spinning on its flow axis
LAYERS = [(-56, 3, 15, 60), (-19, 6, 31, 0), (19, 6, 31, 30), (56, 3, 15, 0)]   # x, nodes, ring radius, offset deg
NODES = [(li, x, r, math.radians(off + 360 * k / n)) for li, (x, n, r, off) in enumerate(LAYERS) for k in range(n)]
EDGES = [(i, j) for i, A in enumerate(NODES) for j, B in enumerate(NODES) if B[0] == A[0] + 1]
YAW, PITCH, FOC, SC = math.radians(28), math.radians(-12), 340, 1.0


def project(x, y, z):
    x1, z1 = x*math.cos(YAW) + z*math.sin(YAW), -x*math.sin(YAW) + z*math.cos(YAW)
    y2, z2 = y*math.cos(PITCH) - z1*math.sin(PITCH), y*math.sin(PITCH) + z1*math.cos(PITCH)
    p = FOC / (FOC - z2)
    return CX + x1*p*SC, CY - y2*p*SC, z2


def nframe(s):
    return [project(x, r*math.cos(t + s), r*math.sin(t + s)) for _, x, r, t in NODES]


NF, CDUR = 24, 15                                 # 120 degrees is a full symmetry cycle
FR = [nframe(math.radians(120) * k / NF) for k in range(NF + 1)]
zs = [p[2] for F in FR for p in F]
ZMIN, ZMAX = min(zs), max(zs)
dn = lambda z: (z - ZMIN) / (ZMAX - ZMIN)
epath = lambda F: 'M' + 'M'.join(f'{F[i][0]:.1f} {F[i][1]:.1f}L{F[j][0]:.1f} {F[j][1]:.1f}' for i, j in EDGES)
ES = f'fill="none" stroke="{GOLD}" stroke-opacity=".24" stroke-width=".7"'
a(f'<circle cx="{CX}" cy="{CY}" r="104" fill="url(#aura)"/>')
for x, n, r, off in LAYERS:   # each layer as a ring; spinning on its own axis leaves the ring in place
    ring = [project(x, r*math.cos(2*math.pi*i/60), r*math.sin(2*math.pi*i/60)) for i in range(61)]
    a(f'<path d="M' + 'L'.join(f'{q[0]:.1f} {q[1]:.1f}' for q in ring) + f'" fill="{GOLD}" fill-opacity=".05" stroke="{GOLD}" stroke-opacity=".55" stroke-width=".8"/>')
a(f'<g class="mv"><path {ES} d="{epath(FR[0])}"><animate attributeName="d" dur="{CDUR}s" repeatCount="indefinite" '
  f'values="{";".join(epath(F) for F in FR)}"/></path>')
for li in range(len(LAYERS)):
    a(f'<g class="L{li}">')
    for ni, nd in enumerate(NODES):
        if nd[0] != li:
            continue
        xs = ';'.join(f'{F[ni][0]:.1f}' for F in FR); ys = ';'.join(f'{F[ni][1]:.1f}' for F in FR)
        rs = ';'.join(f'{1.8 + 1.9 * dn(F[ni][2]):.2f}' for F in FR); ops = ';'.join(f'{.4 + .6 * dn(F[ni][2]):.2f}' for F in FR)
        f0 = FR[0][ni]
        a(f'<circle cx="{f0[0]:.1f}" cy="{f0[1]:.1f}" r="2" fill="{GOLD_HI}">'
          f'<animate attributeName="cx" dur="{CDUR}s" repeatCount="indefinite" values="{xs}"/>'
          f'<animate attributeName="cy" dur="{CDUR}s" repeatCount="indefinite" values="{ys}"/>'
          f'<animate attributeName="r" dur="{CDUR}s" repeatCount="indefinite" values="{rs}"/>'
          f'<animate attributeName="opacity" dur="{CDUR}s" repeatCount="indefinite" values="{ops}"/></circle>')
    a('</g>')
a('</g>')
a(f'<g class="st"><path {ES} d="{epath(FR[0])}"/>')
for ni, nd in enumerate(NODES):
    f0 = FR[0][ni]
    a(f'<circle cx="{f0[0]:.1f}" cy="{f0[1]:.1f}" r="{1.8 + 1.9 * dn(f0[2]):.2f}" fill="{GOLD_HI}" opacity="{.4 + .6 * dn(f0[2]):.2f}"/>')
a('</g>')

# ---- satellites with keywords
N, M = 72, 12
for rx, ry, tilt, dur, ph, br, sats in ORBITS:
    n = len(sats)
    for j, (word, gold) in enumerate(sats):
        u0 = 2 * math.pi * (ph + j / n)
        P = [pt(rx, ry, tilt, u0 + 2 * math.pi * i / N) for i in range(N + 1)]
        x0, y0 = P[0]
        seg = [math.dist(P[i], P[i + 1]) for i in range(N)]
        tot, acc, kp = sum(seg), 0, ['0']
        for s in seg:
            acc += s; kp.append(f'{acc / tot:.4f}')
        kp[-1] = '1'
        kt = ';'.join(f'{i / N:.4f}' for i in range(N + 1))
        path = 'M0 0 ' + ' '.join(f'L{x - x0:.1f} {y - y0:.1f}' for x, y in P[1:])
        dv = [depth(u0 + 2 * math.pi * i / M) for i in range(M + 1)]
        rv = ';'.join(f'{br * (0.68 + 0.55 * d):.2f}' for d in dv)
        ov = ';'.join(f'{0.42 + 0.58 * d:.2f}' for d in dv)
        dkt = ';'.join(f'{i / M:.4f}' for i in range(M + 1))
        fill = GOLD if gold else INK
        tfill = GOLD if gold else SUB
        tag = (f'<text x="{x0:.1f}" y="{y0 - br - 8:.1f}" class="c" font-size="9.5" fill="{tfill}" text-anchor="middle">{word}</text>')
        a(f'<g class="mv"><g><animateMotion dur="{dur}s" repeatCount="indefinite" calcMode="linear" '
          f'keyPoints="{";".join(kp)}" keyTimes="{kt}" path="{path}"/>'
          f'<animate attributeName="opacity" dur="{dur}s" repeatCount="indefinite" values="{ov}" keyTimes="{dkt}"/>'
          f'<circle cx="{x0:.1f}" cy="{y0:.1f}" r="{br * 2.6:.1f}" fill="{fill}" opacity=".12"/>'
          f'<circle cx="{x0:.1f}" cy="{y0:.1f}" r="{br}" fill="{fill}">'
          f'<animate attributeName="r" dur="{dur}s" repeatCount="indefinite" values="{rv}" keyTimes="{dkt}"/></circle>{tag}</g></g>')
        d0 = depth(u0)
        a(f'<g class="st" opacity="{0.42 + 0.58 * d0:.2f}"><circle cx="{x0:.1f}" cy="{y0:.1f}" r="{br * 2.6:.1f}" fill="{fill}" opacity=".12"/>'
          f'<circle cx="{x0:.1f}" cy="{y0:.1f}" r="{br * (0.68 + 0.55 * d0):.2f}" fill="{fill}"/>{tag}</g>')

# identity
a(f'<text x="64" y="212" class="n" font-size="40" fill="{INK}">Rezart Abazi</text>')
a(f'<text x="66" y="248" class="c" font-size="12.5" fill="{GOLD}" letter-spacing=".16em">SENIOR AI ENGINEER</text>')
a('</svg>')
open(f'{REPO}/assets/banner.svg', 'w', encoding='utf8').write(''.join(o))
print('banner', len(''.join(o)) // 1024, 'KB')

# ---------------------------------------------------------------- dock
# Icons: icons/<id>.png, one per app (square, 160px or larger). Order here is the order in the dock.
os.makedirs(f'{REPO}/assets/dock', exist_ok=True)
TH, RAD = 170, 18


def panel(w, left, right):
    """Tile background; outer corners rounded only at the ends of the dock."""
    rl, rr = (RAD if left else 0), (RAD if right else 0)
    return (f'<path d="M0 0H{w}V{TH - rr}' + (f'A{rr} {rr} 0 0 1 {w - rr} {TH}' if rr else '') + f'H{rl}'
            + (f'A{rl} {rl} 0 0 1 0 {TH - rl}' if rl else '') + f'Z" fill="{PANEL}"/>'
            + f'<path d="M0 .5H{w}" stroke="#FFFFFF" stroke-opacity=".06"/>')


FONT_TILE = (f'<style>@font-face{{font-family:GMd;src:url({sans_m}) format("woff")}}@font-face{{font-family:GM;src:url({mono}) format("woff")}}'
             '.k{font-family:GMd,"Segoe UI",Helvetica,sans-serif;font-weight:500}'
             '.c{font-family:GM,ui-monospace,Consolas,monospace;letter-spacing:.16em}</style>')
LW = 160
lab = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{LW}" height="{TH}" viewBox="0 0 {LW} {TH}" role="img" aria-label="My work">'
       + FONT_TILE + panel(LW, True, False)
       + f'<text x="36" y="84" class="c" font-size="13" fill="{GOLD}">MY WORK</text>'
       + f'<path d="M36 100H140" stroke="{DIM}" stroke-opacity=".8"/><circle cx="142" cy="100" r="2.4" fill="{PANEL}" stroke="{SUB}"/></svg>')
open(f'{REPO}/assets/dock/my-work.svg', 'w', encoding='utf8').write(lab)

PROJECTS = [('footbolski', 'Footbolski'), ('miredhelire', 'MiredheLire'), ('fashionpricing', 'FashionPricing'),
            ('almanac', 'Almanac'), ('my-finances', 'My Finances'), ('legalhub', 'LegalHub')]
AW, IS = 140, 64
for k, (pid, name) in enumerate(PROJECTS):
    im = Image.open(f'{ICONS}/{pid}.png').convert('RGBA').resize((160, 160), Image.LANCZOS)
    buf = io.BytesIO(); im.save(buf, 'PNG', optimize=True)
    data = base64.b64encode(buf.getvalue()).decode()
    x0, y0 = (AW - IS) / 2, 34
    t = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{AW}" height="{TH}" viewBox="0 0 {AW} {TH}" role="img" aria-label="{name}">'
         + FONT_TILE + panel(AW, False, k == len(PROJECTS) - 1)
         + f'<path d="M.5 40V130" stroke="#FFFFFF" stroke-opacity=".07"/>'
         + f'<defs><clipPath id="c"><rect x="{x0}" y="{y0}" width="{IS}" height="{IS}" rx="15"/></clipPath></defs>'
         + f'<image href="data:image/png;base64,{data}" x="{x0}" y="{y0}" width="{IS}" height="{IS}" clip-path="url(#c)" preserveAspectRatio="xMidYMid slice"/>'
         + f'<rect x="{x0 + .5}" y="{y0 + .5}" width="{IS - 1}" height="{IS - 1}" rx="14.5" fill="none" stroke="rgba(230,237,243,.16)"/>'
         + f'<text x="{AW/2}" y="132" class="k" font-size="15" text-anchor="middle" fill="#E6EDF3">{name}</text></svg>')
    open(f'{REPO}/assets/dock/{pid}.svg', 'w', encoding='utf8').write(t)
print('dock done')
