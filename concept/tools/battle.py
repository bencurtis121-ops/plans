"""Concept painting: The Last Patrol, the bridge at Daeroth's outer ward.

Writes concept/art/battle.svg. The UI is layered on top in HTML so its
text stays crisp; this file paints only the world.
"""
import json
import math
import random
import sys
from pathlib import Path

from paint import *  # noqa: F401,F403
from figures import FIGURES

W, H = 1600, 900
TW, TH = 150, 75
OX, OY = 800, 58
N = 12
HORIZON = 250
SCALE = 1.45

rng = random.Random(1912)


def V(c, r):
    """Grid vertex (tile corner) to screen."""
    return (OX + (c - r) * TW / 2, OY + (c + r) * TH / 2)


def C(c, r):
    """Tile centre to screen."""
    return V(c + 0.5, r + 0.5)


def tile(c, r, inset=0.0):
    i = inset
    return [V(c + i, r + i), V(c + 1 - i, r + i), V(c + 1 - i, r + 1 - i), V(c + i, r + 1 - i)]


RIVER = (4, 6)  # river occupies rows r in [4, 6)
BRIDGE_C = 5
heroes = {"rhen": (5, 5), "hakon": (7, 6), "yrsa": (6, 7), "apprentice": (5, 8), "astrid": (3, 7)}
enemies = {"shieldA": (5, 4), "shieldB": (6, 3), "harpoon": (4, 2), "adept": (7, 2)}
ENGINE = (8, 1)  # top-left tile of its 2x2 footprint
TELEGRAPH = [(5, 7), (4, 7), (6, 7), (5, 6), (5, 8)]
RUNE_TILE = (5, 3)
props = {"cart": (9, 7), "rocks": (7, 3), "rocks2": (2, 3), "brazier": (3, 2),
         "tree": (1, 8), "banner": (3, 8), "stakes": (2, 6), "stakes2": (4, 10)}


def is_river(c, r):
    return RIVER[0] <= r < RIVER[1] and c != BRIDGE_C


def blocked(c, r):
    occ = set(heroes.values()) | set(enemies.values()) | set(props.values())
    occ |= {(ENGINE[0] + i, ENGINE[1] + j) for i in (0, 1) for j in (0, 1)}
    return (c, r) in occ or is_river(c, r) or not (0 <= c < N and 0 <= r < N)


def move_range(start, steps):
    seen = {start: 0}
    frontier = [start]
    while frontier:
        nxt = []
        for (c, r) in frontier:
            for dc, dr in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                t = (c + dc, r + dr)
                if t in seen or blocked(*t):
                    continue
                seen[t] = seen[(c, r)] + 1
                if seen[t] < steps:
                    nxt.append(t)
                elif seen[t] == steps:
                    pass
        frontier = nxt
    seen.pop(start)
    return [t for t in seen]


# ---------------------------------------------------------------- sky
def sky():
    return """
  <linearGradient id="skyG" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="#0c0706"/>
    <stop offset="0.35" stop-color="#2a130c"/>
    <stop offset="0.75" stop-color="#8a3a17"/>
    <stop offset="1" stop-color="#e3843a"/>
  </linearGradient>
  <radialGradient id="fireG" cx="0.5" cy="1" r="0.6">
    <stop offset="0" stop-color="#ffd27a" stop-opacity="0.95"/>
    <stop offset="0.35" stop-color="#f08a34" stop-opacity="0.55"/>
    <stop offset="1" stop-color="#f08a34" stop-opacity="0"/>
  </radialGradient>
  <radialGradient id="billow" cx="0.45" cy="0.4" r="0.6" fx="0.5" fy="0.85">
    <stop offset="0" stop-color="#2a1810"/><stop offset="0.7" stop-color="#1a0f0b"/><stop offset="1" stop-color="#140b08"/>
  </radialGradient>
  <radialGradient id="billowHot" cx="0.5" cy="0.5" r="0.6" fx="0.5" fy="0.95">
    <stop offset="0" stop-color="#d06a2a"/><stop offset="0.55" stop-color="#5a2a16"/><stop offset="1" stop-color="#1c100b"/>
  </radialGradient>
  <linearGradient id="groundG" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="#8a6a54"/>
    <stop offset="0.2" stop-color="#7c6c68"/>
    <stop offset="0.6" stop-color="#4e5260"/>
    <stop offset="1" stop-color="#1c1e28"/>
  </linearGradient>
  <filter id="snowTex" x="0" y="0" width="100%" height="100%">
    <feTurbulence type="fractalNoise" baseFrequency="0.008 0.016" numOctaves="4" seed="14" result="n"/>
    <feColorMatrix in="n" type="matrix" values="0 0 0 0 0.93  0 0 0 0 0.86  0 0 0 0 0.78  0 0 0 3.2 -1.55"/>
    <feComposite in2="SourceAlpha" operator="in"/>
  </filter>
  <filter id="mudTex" x="0" y="0" width="100%" height="100%">
    <feTurbulence type="fractalNoise" baseFrequency="0.012 0.024" numOctaves="4" seed="40" result="n"/>
    <feColorMatrix in="n" type="matrix" values="0 0 0 0 0.12  0 0 0 0 0.09  0 0 0 0 0.09  0 0 0 3.4 -1.9"/>
    <feComposite in2="SourceAlpha" operator="in"/>
  </filter>
  <radialGradient id="gridFade" cx="0.5" cy="0.55" r="0.5">
    <stop offset="0.55" stop-color="#fff"/><stop offset="1" stop-color="#000"/>
  </radialGradient>
  <mask id="gridMask" maskUnits="userSpaceOnUse" x="0" y="0" width="1600" height="900">
    <ellipse cx="820" cy="520" rx="760" ry="330" fill="url(#gridFade)"/>
  </mask>"""


def billow(cx, base, height, spread, seed):
    """A smoke column built from stacked flat cloud lobes, dark with a fire-lit underside."""
    r = random.Random(seed)
    out = []
    n = 9
    for i in range(n):
        t = i / (n - 1)
        y = base - t * height
        x = cx - t * t * spread + r.uniform(-12, 12)
        rad = 26 + t * 70
        lit = max(0.0, 0.75 - t * 1.1)
        for k in range(3):
            xx = x + r.uniform(-rad * 0.7, rad * 0.7)
            yy = y + r.uniform(-rad * 0.3, rad * 0.3)
            rr = rad * r.uniform(0.6, 0.9)
            grad = "billowHot" if t < 0.35 else "billow"
            out.append(f'<circle cx="{xx:.0f}" cy="{yy:.0f}" r="{rr:.0f}" fill="url(#{grad})" opacity="{0.92 - t*0.25:.2f}"/>')
    return "".join(out)


def clouds():
    return (f'<rect x="-50" y="-40" width="1700" height="260" fill="#000" filter="url(#smoke)" opacity="0.95"/>'
            f'<rect x="-50" y="-60" width="1700" height="180" fill="#000" filter="url(#smoke)" opacity="0.8" transform="translate(220,10)"/>')


def city():
    """Daeroth's outer ward burning on the far ridge: flat layered silhouettes."""
    s = []
    s.append(path("M0,236 C120,200 220,214 330,190 C430,170 520,204 640,180 C760,160 880,196 1000,180 "
                  "C1130,162 1240,200 1380,182 C1480,168 1560,190 1600,184 L1600,280 L0,280 Z", "#3a1c12", "none", 0))
    r = random.Random(77)
    x = 300
    d = "M280,250 L280,214 "
    towers = []
    while x < 1340:
        w = r.uniform(30, 70)
        d += f"L{x:.0f},{214 - r.uniform(0, 8):.0f} "
        if r.random() < 0.5:
            towers.append((x, w * 0.5, r.uniform(30, 80)))
        x += w
    d += "L1340,214 L1340,250 Z"
    s.append(path(d, "#170c09", "none", 0))
    for (tx, tw, th) in towers:
        s.append(poly([(tx, 216), (tx, 214 - th), (tx + tw / 2, 214 - th - tw * 1.1), (tx + tw, 214 - th), (tx + tw, 216)], "#140a08", "none", 0))
        for k in range(r.randint(0, 2)):
            s.append(f'<rect x="{tx + tw/2 - 2:.0f}" y="{214 - th*r.uniform(0.3,0.8):.0f}" width="3" height="6" fill="{FLAME}"/>')
    s.append(poly([(770, 218), (782, 110), (800, 40), (818, 110), (830, 218)], "#100806", "none", 0))
    s.append(poly([(744, 218), (750, 140), (850, 140), (856, 218)], "#130907", "none", 0))
    s.append(f'<rect x="796" y="120" width="8" height="14" fill="{GLOW}" filter="url(#glow)"/>')
    # flames: several licking tongues per fire
    for fx in (420, 560, 700, 920, 1040, 1180, 1290):
        h = r.uniform(28, 64)
        s.append(f'<ellipse cx="{fx}" cy="206" rx="{h*2.2:.0f}" ry="{h*1.2:.0f}" fill="#ff8a30" opacity="0.4" filter="url(#bigGlow)"/>')
        tongues = []
        for k in range(5):
            ox = r.uniform(-18, 18)
            th = h * r.uniform(0.5, 1.0)
            lean = r.uniform(-14, 4)
            tongues.append(f"M{fx+ox-9:.0f},216 C{fx+ox-8:.0f},{216-th*0.5:.0f} {fx+ox+lean:.0f},{216-th*0.7:.0f} {fx+ox+lean-4:.0f},{216-th:.0f} "
                           f"C{fx+ox+6:.0f},{216-th*0.6:.0f} {fx+ox+10:.0f},{216-th*0.4:.0f} {fx+ox+9:.0f},216 Z")
        s.append(f'<path d="{" ".join(tongues)}" fill="{FLAME}" opacity="0.95"/>')
        s.append(f'<path d="M{fx-8},216 C{fx-6},{216-h*0.35:.0f} {fx-2},{216-h*0.45:.0f} {fx},{216-h*0.6:.0f} C{fx+3},{216-h*0.4:.0f} {fx+8},{216-h*0.3:.0f} {fx+8},216 Z" fill="{GLOW}"/>')
    return "\n".join(s)


def smoke_columns():
    s = []
    for i, (fx, h, sp) in enumerate(((560, 300, 160), (920, 380, 260), (1180, 320, 200), (420, 220, 120))):
        s.append(billow(fx, 196, h, sp, i))
    return f'<g filter="url(#brush)" opacity="0.95">' + "".join(s) + "</g>"


def far_bank():
    """Snow ridge with dark pines that hides the horizon behind the board."""
    s = []
    d = "M-20,300 "
    x = -20
    r = random.Random(3)
    while x < 1640:
        x += r.uniform(40, 90)
        d += f"L{x:.0f},{r.uniform(236, 262):.0f} "
    d += "L1640,330 L-20,330 Z"
    s.append(path(d, "#7b6152", INK, 2))
    s.append(brush_strokes(r, 120, (0, 236, 1600, 300), ["#e7b98a", "#c48a5c", "#4b3a34"], (14, 40), (2, 5), (-0.1, 0.1), (0.2, 0.5)))
    # stylised pines (Banner Saga stacked triangles), backlit
    for _ in range(46):
        px = r.uniform(-20, 1620)
        if 560 < px < 1250 and r.random() < 0.75:
            continue  # keep the city visible above the bridge
        ph = r.uniform(50, 120)
        py = r.uniform(250, 280)
        tri = []
        for k in range(4):
            yy = py - ph * k / 4
            ww = ph * 0.32 * (1 - k / 5)
            tri.append(f"M{px-ww:.0f},{yy:.0f} L{px:.0f},{yy - ph*0.42:.0f} L{px+ww:.0f},{yy:.0f} Z")
        s.append(f'<path d="{" ".join(tri)}" fill="#160d0a" stroke="{INK}" stroke-width="1"/>')
        s.append(f'<path d="M{px:.0f},{py - ph*1.17:.0f} L{px + ph*0.12:.0f},{py - ph*0.9:.0f}" stroke="{FLAME}" stroke-width="1.5" opacity="0.6"/>')
    return "\n".join(s)


def ground_layer():
    s = [f'<rect x="0" y="{HORIZON+20}" width="{W}" height="{H-HORIZON}" fill="url(#groundG)"/>']
    s.append(f'<ellipse cx="860" cy="{HORIZON+60}" rx="900" ry="200" fill="#e09050" opacity="0.30" filter="url(#bigGlow)"/>')
    s.append(f'<rect x="0" y="{HORIZON+20}" width="{W}" height="{H-HORIZON}" fill="#000" filter="url(#snowTex)" opacity="0.28"/>')
    s.append(f'<rect x="0" y="{HORIZON+20}" width="{W}" height="{H-HORIZON}" fill="#000" filter="url(#mudTex)" opacity="0.7"/>')
    # trodden roads to the bridge
    road = [V(4.55, -3), V(6.45, -3), V(6.5, 3.5), V(4.5, 3.5)]
    s.append(poly(road, "#4a3428", "none", 0, 'opacity="0.55" filter="url(#brush)"'))
    road2 = [V(4.5, 6.5), V(6.5, 6.5), V(6.8, 15), V(4.2, 15)]
    s.append(poly(road2, "#2f2830", "none", 0, 'opacity="0.55" filter="url(#brush)"'))
    # fat isometric dabs, both diagonals, like a loaded brush dragged over wet paint
    dab_rng = random.Random(8)
    out = []
    for _ in range(900):
        x = dab_rng.uniform(0, W)
        y = dab_rng.uniform(HORIZON + 30, H)
        t = (y - HORIZON) / (H - HORIZON)
        warm = dab_rng.random() > t * 1.1
        col = dab_rng.choice(["#e9c9a0", "#d7a676", "#b49480"] if warm else ["#9aa2b6", "#6f7790", "#c2bcc0", "#3a3f50"])
        ang = 26.6 if dab_rng.random() < 0.7 else -26.6
        rx = dab_rng.uniform(30, 90)
        out.append(f'<ellipse cx="{x:.0f}" cy="{y:.0f}" rx="{rx:.0f}" ry="{dab_rng.uniform(2.5,6):.1f}" '
                   f'fill="{col}" opacity="{dab_rng.uniform(0.06, 0.18):.2f}" transform="rotate({ang} {x:.0f} {y:.0f})"/>')
    s.append("<g>" + "".join(out) + "</g>")
    return "\n".join(s)


def river():
    s = []
    r0, r1 = RIVER
    top = [V(c, r0 + 0.08 * math.sin(c * 2.1)) for c in [x * 0.5 for x in range(-12, 32)]]
    bot = [V(c, r1 + 0.1 * math.sin(c * 1.7 + 1)) for c in [x * 0.5 for x in range(31, -13, -1)]]
    pts_ = top + bot
    s.append('<clipPath id="riverClip"><polygon points="' + pts(pts_) + '"/></clipPath>')
    s.append(f'<g filter="url(#brushFine)">')
    s.append(poly(pts_, "#6f7f92", INK, 2))
    s.append(f'<g clip-path="url(#riverClip)">')
    s.append(brush_strokes(rng, 500, (0, 200, W, 900), ["#a9bccd", "#c7d4de", "#56677c", "#e7a463", "#f3c27c"],
                           (20, 90), (2, 6), (0.40, 0.55), (0.12, 0.4)))
    # open dark water pools
    for (c, r, w) in ((1.5, 4.6, 0.9), (8.6, 5.1, 1.1), (10.6, 4.4, 0.8), (3.2, 5.4, 0.5)):
        x, y = V(c, r)
        L = w * 90
        d = (f"M{x-L:.0f},{y-L*0.5:.0f} C{x-L*0.4:.0f},{y-L*0.62:.0f} {x+L*0.3:.0f},{y-L*0.1:.0f} {x+L:.0f},{y+L*0.5:.0f} "
             f"C{x+L*0.4:.0f},{y+L*0.42:.0f} {x-L*0.2:.0f},{y+L*0.1:.0f} {x-L:.0f},{y-L*0.5:.0f} Z")
        s.append(f'<path d="{d}" fill="#121822" opacity="0.9"/>')
        s.append(f'<path d="M{x-L*0.5:.0f},{y-L*0.3:.0f} C{x-L*0.1:.0f},{y-L*0.32:.0f} {x+L*0.2:.0f},{y-L*0.05:.0f} {x+L*0.5:.0f},{y+L*0.2:.0f}" '
                 f'fill="none" stroke="{FLAME}" stroke-width="2" opacity="0.45"/>')
    # cracks
    cr = random.Random(5)
    for _ in range(26):
        c = cr.uniform(-2, 13)
        r = cr.uniform(r0 + 0.2, r1 - 0.2)
        x, y = V(c, r)
        d = f"M{x:.0f},{y:.0f}"
        for _ in range(4):
            x += cr.uniform(-32, 32)
            y += cr.uniform(-12, 14)
            d += f" L{x:.0f},{y:.0f}"
        s.append(f'<path d="{d}" fill="none" stroke="#2a3342" stroke-width="1.2" opacity="0.7"/>')
    # cut face of the far bank, lit from behind so it reads dark
    face = top + [(x, y + 26) for (x, y) in reversed(top)]
    s.append(poly(face, "#2e2620", "none", 0, 'opacity="0.85"'))
    s.append('</g></g>')
    # snow lip on the near bank
    lip = " ".join(f"L{x:.1f},{y:.1f}" for (x, y) in bot)
    s.append(f'<path d="M{bot[0][0]:.1f},{bot[0][1]:.1f} {lip}" fill="none" stroke="#d8cbbf" stroke-width="6" opacity="0.6" filter="url(#brush)"/>')
    return "\n".join(s)


def bridge_back():
    """Deck and far parapet: drawn under the figures."""
    s = []
    c0, c1 = BRIDGE_C, BRIDGE_C + 1
    a, b = 3.3, 6.7
    deck = [V(c0, a), V(c1, a), V(c1, b), V(c0, b)]
    # visible near side face with the arch over the ice
    face = [V(c1, 3.8), V(c1, 6.2), (V(c1, 6.2)[0], V(c1, 6.2)[1] + 44), (V(c1, 3.8)[0], V(c1, 3.8)[1] + 44)]
    s.append(poly(face, "#3a302c", INK, 2))
    ax0, ay0 = V(c1, 4.2)
    ax1, ay1 = V(c1, 5.8)
    s.append(f'<path d="M{ax0:.0f},{ay0+44:.0f} Q{(ax0+ax1)/2 - 4:.0f},{(ay0+ay1)/2 - 2:.0f} {ax1:.0f},{ay1+44:.0f} Z" fill="#0f0c0c" stroke="{INK}" stroke-width="1.5"/>')
    for i in range(7):
        t = 3.9 + i * 0.36
        x, y = V(c1, t)
        s.append(f'<line x1="{x:.0f}" y1="{y+2:.0f}" x2="{x:.0f}" y2="{y+12:.0f}" stroke="#1e1816" stroke-width="1"/>')
    s.append(poly(deck, "#7d6d63", INK, 2))
    # flagstones
    for i in range(1, 10):
        t = a + (b - a) * i / 10
        p0, p1 = V(c0, t), V(c1, t)
        s.append(f'<line x1="{p0[0]:.0f}" y1="{p0[1]:.0f}" x2="{p1[0]:.0f}" y2="{p1[1]:.0f}" stroke="#4a3d36" stroke-width="1.2" opacity="0.8"/>')
    s.append(brush_strokes(rng, 80, (min(V(c0, b)[0], V(c0, a)[0]), V(c0, a)[1], V(c1, a)[0], V(c1, b)[1]),
                           ["#c9a27a", "#e5c39a", "#4e4038"], (6, 20), (1.5, 4), (0.40, 0.55), (0.15, 0.4),
                           inside=lambda x, y: True))
    # far parapet (c = c0 line)
    for t in (a, b - 0.6):
        pass
    p0, p1 = V(c0, a), V(c0, b)
    par = [p0, p1, (p1[0], p1[1] - 20), (p0[0], p0[1] - 20)]
    s.append(poly(par, "#5a4c44", INK, 1.8))
    s.append(f'<line x1="{p0[0]:.0f}" y1="{p0[1]-20:.0f}" x2="{p1[0]:.0f}" y2="{p1[1]-20:.0f}" stroke="{FLAME}" stroke-width="1.6" opacity="0.7"/>')
    return f'<g filter="url(#brushFine)">' + "\n".join(s) + "</g>"


def parapet_near_segment(r_from, r_to):
    c1 = BRIDGE_C + 1
    p0, p1 = V(c1, r_from), V(c1, r_to)
    par = [p0, p1, (p1[0], p1[1] - 18), (p0[0], p0[1] - 18)]
    return (poly(par, "#6a5a50", INK, 1.8, 'filter="url(#brushFine)"')
            + f'<line x1="{p0[0]:.0f}" y1="{p0[1]-18:.0f}" x2="{p1[0]:.0f}" y2="{p1[1]-18:.0f}" stroke="{FLAME}" stroke-width="1.4" opacity="0.6"/>')


def light_pools():
    bx, by = C(*props["brazier"])
    ex, ey = V(ENGINE[0] + 1, ENGINE[1] + 1)
    tx, ty = C(*TELEGRAPH[0])
    rx_, ry_ = C(*heroes["rhen"])
    return f"""<linearGradient id="horizonFade" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0.45" stop-color="#000"/><stop offset="1" stop-color="#000" stop-opacity="0"/></linearGradient>
    <mask id="lightMask" maskUnits="userSpaceOnUse" x="0" y="0" width="{W}" height="{H}">
      <rect width="{W}" height="{H}" fill="#fff"/>
      <ellipse cx="{bx:.0f}" cy="{by:.0f}" rx="260" ry="130" fill="#000" filter="url(#bigGlow)"/>
      <ellipse cx="{rx_:.0f}" cy="{ry_ - 20:.0f}" rx="300" ry="150" fill="#000" filter="url(#bigGlow)"/>
      <ellipse cx="{ex:.0f}" cy="{ey:.0f}" rx="200" ry="110" fill="#333" filter="url(#bigGlow)"/>
      <ellipse cx="{tx:.0f}" cy="{ty:.0f}" rx="150" ry="80" fill="#444" filter="url(#bigGlow)"/>
      <rect y="0" width="{W}" height="{HORIZON + 140}" fill="url(#horizonFade)"/>
    </mask>
    <rect width="{W}" height="{H}" fill="#120b0a" opacity="0.55" mask="url(#lightMask)"/>
    <ellipse cx="{ex:.0f}" cy="{ey:.0f}" rx="170" ry="80" fill="{FEL}" opacity="0.12" filter="url(#bigGlow)"/>
    <ellipse cx="{bx:.0f}" cy="{by:.0f}" rx="170" ry="80" fill="#ff9a40" opacity="0.18" filter="url(#bigGlow)"/>"""


def grid():
    s = ['<g opacity="0.45" mask="url(#gridMask)">']
    for i in range(-2, N + 3):
        a, b = V(i, -2), V(i, N + 2)
        s.append(f'<line x1="{a[0]:.0f}" y1="{a[1]:.0f}" x2="{b[0]:.0f}" y2="{b[1]:.0f}" stroke="#1a1210" stroke-width="1"/>')
        a, b = V(-2, i), V(N + 2, i)
        s.append(f'<line x1="{a[0]:.0f}" y1="{a[1]:.0f}" x2="{b[0]:.0f}" y2="{b[1]:.0f}" stroke="#1a1210" stroke-width="1"/>')
    s.append("</g>")
    return "\n".join(s)


def overlays():
    s = []
    # movement range for the active hero
    for (c, r) in move_range(heroes["rhen"], 4):
        if (c, r) in TELEGRAPH:
            continue
        s.append(poly(tile(c, r, 0.06), "#f1e3c6", "#f1e3c6", 1.2, 'fill-opacity="0.16" stroke-opacity="0.55"'))
    # engine telegraph: fel hatch, the strike lands at the end of the round
    s.append(f"""<pattern id="hatch" patternUnits="userSpaceOnUse" width="12" height="12" patternTransform="rotate(30)">
      <rect width="12" height="12" fill="{FEL}" opacity="0.12"/><line x1="0" y1="0" x2="0" y2="12" stroke="{FEL}" stroke-width="3.5" opacity="0.5"/></pattern>""")
    for (c, r) in TELEGRAPH:
        s.append(poly(tile(c, r, 0.04), "url(#hatch)", FEL, 2, 'stroke-opacity="0.9" filter="url(#glow)"'))
    cx, cy = C(*TELEGRAPH[0])
    s.append(f'<circle cx="{cx:.0f}" cy="{cy:.0f}" r="16" fill="none" stroke="{FEL}" stroke-width="2" filter="url(#glow)"/>')
    s.append(f'<path d="M{cx-26:.0f},{cy:.0f} h52 M{cx:.0f},{cy-13:.0f} v26" stroke="{FEL}" stroke-width="1.5" opacity="0.8"/>')
    # rune glyph placed by Yrsa on the north abutment
    gx, gy = C(*RUNE_TILE)
    s.append(f'<g filter="url(#glow)" transform="translate({gx:.0f},{gy:.0f}) scale(1.45,0.72)">'
             f'<circle r="26" fill="none" stroke="{RUNE}" stroke-width="2.4"/>'
             f'<circle r="20" fill="{RUNE}" opacity="0.12"/>'
             f'<path d="M0,-18 L0,18 M0,-18 L12,-6 M0,0 L-12,-12 M0,0 L12,12" stroke="{RUNE}" stroke-width="3" fill="none"/></g>')
    # attack target and active hero markers
    s.append(poly(tile(*enemies["shieldA"], 0.04), "#e0562a", "#ff8a4a", 2.4, 'fill-opacity="0.22" filter="url(#glow)"'))
    s.append(poly(tile(*heroes["rhen"], 0.04), "#ffd27a", GLOW, 2.4, 'fill-opacity="0.18" filter="url(#glow)"'))
    return "\n".join(s)


# ---------------------------------------------------------------- props
def prop(kind):
    if kind == "cart":
        out = [shadow(52, 15)]
        for (bx, by, h) in ((-26, -10, 44), (14, -18, 44), (-4, 10, 40)):
            out.append(path(f"M{bx-16},{by} L{bx-16},{by-h} A16,7 0 0 1 {bx+16},{by-h} L{bx+16},{by} A16,7 0 0 1 {bx-16},{by} Z", "#6a4a2e"))
            out.append(f'<ellipse cx="{bx}" cy="{by-h}" rx="16" ry="7" fill="#8a6640" stroke="{INK}" stroke-width="1.6"/>')
            for hy in (0.25, 0.75):
                out.append(f'<path d="M{bx-16},{by - h*hy:.0f} A16,7 0 0 0 {bx+16},{by - h*hy:.0f}" fill="none" stroke="#2a1c12" stroke-width="2.4"/>')
            out.append(f'<path d="M{bx-14},{by-h-3} A16,7 0 0 1 {bx+14},{by-h-3}" fill="none" stroke="{FLAME}" stroke-width="1.6" opacity="0.8"/>')
        # an abandoned shield leaning on the barrels
        out.append(f'<ellipse cx="34" cy="-14" rx="11" ry="18" fill="{OATH_RED}" stroke="#8b6a3e" stroke-width="3"/>')
        return "".join(out)
    if kind in ("rocks", "rocks2"):
        return (shadow(36, 11)
                + path("M-34,0 C-40,-20 -24,-38 -4,-36 C10,-46 30,-34 32,-18 C40,-10 34,2 22,4 Z", "#5b5450")
                + path("M-26,-24 C-14,-34 4,-36 10,-30", "none", FLAME, 2, 'opacity="0.55"')
                + path("M-6,-36 C0,-24 -2,-10 6,2", "none", "#2d2826", 1.4))
    if kind == "brazier":
        return (shadow(18, 6)
                + path("M-10,0 L-4,-26 M10,0 L4,-26 M0,2 L0,-26", "none", "#2a1c14", 2.4)
                + path("M-16,-26 L16,-26 L12,-36 L-12,-36 Z", "#3a2a1e")
                + f'<path d="M-12,-36 C-10,-52 -4,-58 0,-70 C4,-56 10,-52 12,-36 Z" fill="{FLAME}" filter="url(#glow)"/>'
                + f'<path d="M-5,-36 C-4,-46 0,-50 1,-58 C3,-48 6,-44 5,-36 Z" fill="{GLOW}"/>'
                + f'<circle cx="0" cy="-44" r="70" fill="#ff9a40" opacity="0.22" filter="url(#bigGlow)"/>')
    if kind == "tree":
        # weathered runestone: the old world's carved memory, half buried in snow
        return (shadow(30, 10)
                + path("M-24,4 C-30,-40 -26,-96 -10,-128 C0,-138 16,-134 22,-118 C30,-80 30,-30 26,4 Z", "#4d4844")
                + path("M-10,-128 C0,-138 16,-134 22,-118", "none", FLAME, 2.2, 'opacity="0.8"')
                + path("M10,-120 C18,-90 20,-40 18,0", "none", "#2c2826", 2)
                + f'<path d="M-8,-104 l8,-10 l8,10 M0,-114 v40 M-8,-66 l8,8 l8,-8 M0,-58 v30 M-8,-40 h16" fill="none" '
                  f'stroke="{RUNE}" stroke-width="2.2" opacity="0.55" filter="url(#glow)"/>'
                + path("M-30,4 C-20,-10 20,-12 32,4 Z", "#cfc2b4", "none", 0, 'opacity="0.8"'))
    if kind == "banner":
        return (shadow(14, 5)
                + path("M0,0 L0,-160", "none", "#2a1a12", 3.4)
                + path("M0,-156 L-56,-150 L-50,-128 L-60,-108 L-46,-112 L-34,-96 L-26,-114 L0,-118 Z", OATH_RED)
                + f'<circle cx="-26" cy="-134" r="9" fill="none" stroke="#d9b880" stroke-width="2"/>'
                + path("M0,-156 L-56,-150", "none", FLAME, 1.4, 'opacity="0.8"'))
    if kind in ("stakes", "stakes2"):
        out = [shadow(44, 12)]
        for i, x in enumerate(range(-36, 40, 12)):
            h = 34 + (i % 3) * 8
            out.append(path(f"M{x-4},{x*0.3+4:.0f} L{x+10},{x*0.3 - h:.0f} L{x+5},{x*0.3+4:.0f} Z", "#3a281c"))
            out.append(path(f"M{x+4},{x*0.3 - h*0.5:.0f} L{x+10},{x*0.3 - h:.0f}", "none", FLAME, 1.2, 'opacity="0.5"'))
        out.append(path("M-40,-10 L44,8", "none", "#3a2a1e", 3))
        return "".join(out)
    if kind == "crates":
        return (shadow(36, 11)
                + poly([(-30, -6), (0, -20), (28, -6), (0, 8)], "#5e4430")
                + poly([(-30, -6), (-30, -34), (0, -48), (0, -20)], "#7a5838")
                + poly([(0, -20), (0, -48), (28, -34), (28, -6)], "#4d3624")
                + poly([(-30, -34), (0, -48), (28, -34), (0, -20)], "#9a7448")
                + path("M-30,-34 L0,-48 L28,-34", "none", FLAME, 1.4, 'opacity="0.6"'))
    return ""


FIG = FIGURES
FIG_SCALE = 1.12
FLIP = {"shieldA": False, "shieldB": False, "harpoon": False, "adept": False}


FIGDEFS = []


def place(name, inner, x, y, sc, filt):
    """Draw a figure: ground shadow, rim-lit body, then a dark gradient
    masked to the silhouette so the feet sink into Frazetta shadow."""
    import re
    m = re.search(r"<!--SH-->(.*?)<!--/SH-->", inner, re.S)
    sh = m.group(1) if m else ""
    body = re.sub(r"<!--SH-->.*?<!--/SH-->", "", inner, flags=re.S)
    fid = f"fig_{name}"
    FIGDEFS.append(f'<g id="{fid}">{body}</g>')
    FIGDEFS.append(f'<mask id="m_{name}" maskUnits="userSpaceOnUse" x="-260" y="-330" width="520" height="400">'
                   f'<use href="#{fid}" filter="url(#white)"/></mask>')
    cast = (f'<g transform="scale(1,-0.42) skewX(-28)" opacity="0.5">'
            f'<use href="#{fid}" filter="url(#castShadow)"/></g>')
    return (f'<g transform="translate({x:.0f},{y:.0f}) scale({sc})">{cast}{sh}'
            f'<use href="#{fid}" filter="url(#{filt})"/>'
            f'<g mask="url(#m_{name})"><rect x="-260" y="-230" width="520" height="250" fill="url(#shadeDown)"/>'
            f'<rect x="-260" y="-330" width="520" height="350" fill="url(#shadeSide)"/></g></g>')


def base_ring(x, y, enemy, civilian):
    """Team plate under each unit (gold heroes, ember-red enemies, pale civilians)."""
    col = "#e0563a" if enemy else ("#e9e2cf" if civilian else "#f2c46a")
    return (f'<g transform="translate({x:.0f},{y + 2:.0f}) scale(1,0.5)" opacity="0.9">'
            f'<circle r="44" fill="none" stroke="#120a08" stroke-width="7" opacity="0.6"/>'
            f'<circle r="44" fill="none" stroke="{col}" stroke-width="2.6"/>'
            f'<circle r="38" fill="none" stroke="{col}" stroke-width="1" opacity="0.5" stroke-dasharray="4 5"/></g>')


def actors():
    items = []
    for name, (c, r) in {**heroes, **enemies}.items():
        items.append((c + r + 1, name, (c, r)))
    for name, (c, r) in props.items():
        items.append((c + r + 1, "prop:" + name, (c, r)))
    items.append((ENGINE[0] + ENGINE[1] + 2.01, "engine", ENGINE))
    for rr in range(3, 7):
        items.append((BRIDGE_C + 1 + rr + 0.5, f"par:{rr}", None))
    items.sort(key=lambda t: t[0])
    out = []
    for _, name, pos in items:
        if name.startswith("par:"):
            rr = int(name[4:])
            out.append(parapet_near_segment(max(3.3, rr), min(6.7, rr + 1)))
            continue
        if name == "engine":
            x, y = V(ENGINE[0] + 1, ENGINE[1] + 1)
            out.append(place("engine", spirit_engine(), x, y, 1.3, "rimFel"))
            continue
        x, y = C(*pos)
        if name.startswith("prop:"):
            out.append(f'<g transform="translate({x:.0f},{y:.0f}) scale({SCALE})" filter="url(#rim)">{prop(name[5:])}</g>')
            continue
        filt = "rimFel" if name in enemies else "rim"
        out.append(base_ring(x, y, name in enemies, name == "apprentice"))
        out.append(place(name, FIG[name](), x, y + 6, FIG_SCALE, filt))
    return "\n".join(out)


def atmosphere():
    s = []
    # drifting smoke low across the far bank
    s.append(f'<rect x="-100" y="{HORIZON-40}" width="{W+200}" height="160" fill="#000" filter="url(#smoke)" opacity="0.45"/>')
    # embers rising from the city, ash and snow falling over everything
    s.append(particles(rng, 120, (300, 60, 1400, 420), FLAME, (0.6, 2.0), (0.4, 1.0), glow=True))
    s.append(particles(rng, 260, (0, 0, W, H), "#e9e0d4", (0.6, 1.8), (0.25, 0.7)))
    # Frazetta darkness: heavy vignette with a warm core
    s.append(f"""<radialGradient id="vig" cx="0.52" cy="0.42" r="0.75">
      <stop offset="0.45" stop-color="#000" stop-opacity="0"/>
      <stop offset="0.85" stop-color="#0b0605" stop-opacity="0.65"/>
      <stop offset="1" stop-color="#050302" stop-opacity="0.92"/></radialGradient>""")
    s.append(f'<rect width="{W}" height="{H}" fill="url(#vig)"/>')
    s.append(f'<rect width="{W}" height="{H}" fill="#000" filter="url(#canvasTex)" opacity="0.55"/>')
    s.append(f'<rect width="{W}" height="{H}" fill="#000" filter="url(#grain)" opacity="0.35"/>')
    return "\n".join(s)


def build():
    parts = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">',
             "<defs>", defs_common(), sky(), "</defs>",
             f'<rect width="{W}" height="{H}" fill="url(#skyG)"/>',
             clouds(),
             f'<ellipse cx="860" cy="{HORIZON-30}" rx="820" ry="200" fill="url(#fireG)"/>',
             smoke_columns(),
             f'<g filter="url(#brush)">{city()}</g>',
             ground_layer(),
             f'<g filter="url(#brush)">{far_bank()}</g>',
             river(),
             light_pools(),
             grid(),
             bridge_back(),
             overlays(),
             actors(),
             atmosphere(),
             "</svg>"]
    # figure symbols and masks are collected while drawing the actors
    i = parts.index("</defs>")
    parts.insert(i, "\n".join(FIGDEFS))
    return "\n".join(parts)


if __name__ == "__main__":
    out = Path(sys.argv[1] if len(sys.argv) > 1 else "../art/battle.svg")
    out.write_text(build())
    # anchor points the HTML UI layer uses to pin nameplates over units
    anchors = {k: [round(v, 1) for v in C(*p)] for k, p in {**heroes, **enemies}.items()}
    anchors["engine"] = [round(v, 1) for v in V(ENGINE[0] + 1, ENGINE[1] + 1)]
    anchors["telegraph"] = [round(v, 1) for v in C(*TELEGRAPH[0])]
    print(json.dumps(anchors))
