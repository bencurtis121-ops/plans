"""Shared SVG painting helpers for The Meldstone War concept art.

Look: Banner Saga's flat, outlined, layered shapes (Eyvind Earle lineage)
lit like a Frank Frazetta canvas: umber darkness, a single hot light
source, rim-lit silhouettes, smoke, and visible brush texture.
"""
import math
import random

# ---------------------------------------------------------------- palette
INK = "#140b08"        # outline / deepest dark
UMBER = "#2a1810"
UMBER2 = "#3d2416"
SIENNA = "#7a3e1d"
EMBER = "#e0742a"
FLAME = "#f4a24a"
GLOW = "#ffd99a"
SNOW_LIT = "#d9c3a3"
SNOW_MID = "#9c8f86"
SNOW_SHADE = "#4b5262"
SNOW_DEEP = "#2b3040"
FEL = "#35d6c3"
FEL_DARK = "#0d3a37"
RUNE = "#ffb84a"
FROST = "#b8e2ff"
OATH_RED = "#7d1d14"


def defs_common():
    """Filters every painting shares."""
    return f"""
  <filter id="brush" x="-5%" y="-5%" width="110%" height="110%">
    <feTurbulence type="fractalNoise" baseFrequency="0.035" numOctaves="3" seed="7" result="n"/>
    <feDisplacementMap in="SourceGraphic" in2="n" scale="6" xChannelSelector="R" yChannelSelector="G"/>
  </filter>
  <filter id="brushFine" x="-5%" y="-5%" width="110%" height="110%">
    <feTurbulence type="fractalNoise" baseFrequency="0.09" numOctaves="2" seed="3" result="n"/>
    <feDisplacementMap in="SourceGraphic" in2="n" scale="2.5" xChannelSelector="R" yChannelSelector="G"/>
  </filter>
  <filter id="rim" x="-20%" y="-20%" width="140%" height="140%">
    <feOffset in="SourceAlpha" dx="1" dy="3" result="off"/>
    <feComposite in="SourceAlpha" in2="off" operator="out" result="edge"/>
    <feGaussianBlur in="edge" stdDeviation="0.5" result="edgeb"/>
    <feFlood flood-color="#ffb35c" result="c"/>
    <feComposite in="c" in2="edgeb" operator="in" result="rimc"/>
    <feMerge><feMergeNode in="SourceGraphic"/><feMergeNode in="rimc"/></feMerge>
  </filter>
  <filter id="rimFel" x="-20%" y="-20%" width="140%" height="140%">
    <feOffset in="SourceAlpha" dx="-1" dy="3" result="off"/>
    <feComposite in="SourceAlpha" in2="off" operator="out" result="edge"/>
    <feGaussianBlur in="edge" stdDeviation="0.5" result="edgeb"/>
    <feFlood flood-color="#ff9a48" result="c"/>
    <feComposite in="c" in2="edgeb" operator="in" result="rimc"/>
    <feMerge><feMergeNode in="SourceGraphic"/><feMergeNode in="rimc"/></feMerge>
  </filter>
  <filter id="castShadow" x="-50%" y="-50%" width="200%" height="200%">
    <feFlood flood-color="#0a0605"/><feComposite in2="SourceAlpha" operator="in"/>
    <feGaussianBlur stdDeviation="2.2"/>
  </filter>
  <filter id="white" x="-50%" y="-50%" width="200%" height="200%">
    <feFlood flood-color="#fff"/><feComposite in2="SourceAlpha" operator="in"/>
  </filter>
  <linearGradient id="shadeDown" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="#000" stop-opacity="0"/>
    <stop offset="0.45" stop-color="#0a0605" stop-opacity="0.05"/>
    <stop offset="1" stop-color="#0a0605" stop-opacity="0.75"/>
  </linearGradient>
  <linearGradient id="shadeSide" x1="0" y1="0" x2="1" y2="0">
    <stop offset="0" stop-color="#0a0605" stop-opacity="0.35"/>
    <stop offset="0.5" stop-color="#0a0605" stop-opacity="0"/>
    <stop offset="1" stop-color="#0a0605" stop-opacity="0.3"/>
  </linearGradient>
  <filter id="glow" x="-100%" y="-100%" width="300%" height="300%">
    <feGaussianBlur stdDeviation="6" result="b"/>
    <feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge>
  </filter>
  <filter id="bigGlow" x="-100%" y="-100%" width="300%" height="300%">
    <feGaussianBlur stdDeviation="22"/>
  </filter>
  <filter id="soft" x="-50%" y="-50%" width="200%" height="200%">
    <feGaussianBlur stdDeviation="3"/>
  </filter>
  <filter id="smoke" x="-20%" y="-50%" width="140%" height="200%">
    <feTurbulence type="fractalNoise" baseFrequency="0.006 0.018" numOctaves="4" seed="21" result="n"/>
    <feColorMatrix in="n" type="matrix" values="0 0 0 0 0.09  0 0 0 0 0.05  0 0 0 0 0.035  0 0 0 2.6 -1.15" result="s"/>
    <feComposite in="s" in2="SourceAlpha" operator="in"/>
  </filter>
  <filter id="grain" x="0" y="0" width="100%" height="100%">
    <feTurbulence type="fractalNoise" baseFrequency="0.85" numOctaves="2" seed="2" result="n"/>
    <feColorMatrix in="n" type="matrix" values="0 0 0 0 0.5  0 0 0 0 0.42  0 0 0 0 0.33  0 0 0 0.9 -0.32"/>
    <feComposite in2="SourceAlpha" operator="in"/>
  </filter>
  <filter id="canvasTex" x="0" y="0" width="100%" height="100%">
    <feTurbulence type="turbulence" baseFrequency="0.012 0.05" numOctaves="3" seed="9" result="n"/>
    <feColorMatrix in="n" type="matrix" values="0 0 0 0 0.12  0 0 0 0 0.07  0 0 0 0 0.04  0 0 0 1.4 -0.5"/>
    <feComposite in2="SourceAlpha" operator="in"/>
  </filter>
"""


def pts(points):
    return " ".join(f"{x:.1f},{y:.1f}" for x, y in points)


def poly(points, fill, stroke=INK, sw=1.6, extra=""):
    return f'<polygon points="{pts(points)}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}" stroke-linejoin="round" {extra}/>'


def path(d, fill, stroke=INK, sw=1.6, extra=""):
    return f'<path d="{d}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}" stroke-linejoin="round" stroke-linecap="round" {extra}/>'


def brush_strokes(rng, n, region, colors, length=(10, 40), width=(2, 6),
                  angle=(-0.3, 0.3), opacity=(0.08, 0.3), inside=None):
    """Scatter semi-transparent elongated dabs, like loose oil strokes."""
    x0, y0, x1, y1 = region
    out = []
    for _ in range(n):
        x = rng.uniform(x0, x1)
        y = rng.uniform(y0, y1)
        if inside and not inside(x, y):
            continue
        L = rng.uniform(*length)
        a = rng.uniform(*angle)
        dx, dy = math.cos(a) * L / 2, math.sin(a) * L / 2
        c = rng.choice(colors)
        out.append(
            f'<line x1="{x-dx:.1f}" y1="{y-dy:.1f}" x2="{x+dx:.1f}" y2="{y+dy:.1f}" '
            f'stroke="{c}" stroke-width="{rng.uniform(*width):.1f}" stroke-linecap="round" '
            f'opacity="{rng.uniform(*opacity):.2f}"/>'
        )
    return "\n".join(out)


def particles(rng, n, region, color, r=(0.6, 2.2), opacity=(0.3, 0.9), glow=False):
    x0, y0, x1, y1 = region
    f = ' filter="url(#glow)"' if glow else ""
    out = [f"<g{f}>"]
    for _ in range(n):
        out.append(
            f'<circle cx="{rng.uniform(x0,x1):.1f}" cy="{rng.uniform(y0,y1):.1f}" '
            f'r="{rng.uniform(*r):.1f}" fill="{color}" opacity="{rng.uniform(*opacity):.2f}"/>'
        )
    out.append("</g>")
    return "\n".join(out)


# ------------------------------------------------------------- figures
# Each figure is drawn in local space with the feet at (0, 0) and wrapped
# in a translate/scale group. Heroes are seen from behind (3/4 back) because
# the fire that lights them is in front of them; enemies face the camera.

def shadow(rx=26, ry=8):
    # tagged so the scene can draw the ground shadow outside the rim filter
    return f'<!--SH--><ellipse cx="0" cy="0" rx="{rx}" ry="{ry}" fill="#000" opacity="0.55" filter="url(#soft)"/><!--/SH-->'


def legs(trou, boot, spread=9, top=-40):
    return (
        poly([(-spread - 2, top), (-1, top), (-2, -2), (-spread - 3, -1)], trou)
        + poly([(1, top), (spread + 2, top), (spread + 3, -1), (2, -2)], trou)
        + poly([(-spread - 3, -13), (-2, -13), (-2, 0), (-spread - 6, 0)], boot)
        + poly([(2, -13), (spread + 3, -13), (spread + 6, 0), (2, 0)], boot)
    )


def figure_rhen():
    """Oathguard: broad, shield-led, oath-red cloak, spear. Back view."""
    s = [shadow(28, 9)]
    s.append(legs("#3a2a22", "#1c120d"))
    # cloak blown left by the fire wind
    s.append(path("M-17,-84 C-30,-60 -36,-30 -44,-8 L-30,-12 L-22,-4 L-6,-14 L8,-8 L16,-30 C18,-55 18,-72 15,-84 Z", OATH_RED))
    s.append(path("M-12,-80 C-20,-55 -24,-32 -30,-14", "none", "#4b0f0a", 3, 'opacity="0.8"'))
    s.append(path("M2,-80 C2,-55 0,-35 -4,-16", "none", "#4b0f0a", 3, 'opacity="0.7"'))
    # mail shoulders and helm
    s.append(path("M-19,-80 Q0,-92 19,-80 L15,-72 Q0,-80 -15,-72 Z", "#5d5650"))
    s.append(path("M-8,-88 Q-9,-103 0,-104 Q9,-103 8,-88 Z", "#6b635b"))
    s.append(path("M-9,-89 L9,-89 L9,-86 L-9,-86 Z", "#3b3530"))
    # spear in right hand
    s.append(path("M20,-40 L34,-150", "none", "#2b1b12", 3.2))
    s.append(path("M34,-150 L31,-164 L37,-151 Z", "#c9b8a0", INK, 1.2))
    s.append(path("M15,-58 Q22,-52 22,-40 L17,-38 Q16,-50 11,-54 Z", "#3a2a22"))
    # round shield on left arm, seen at an angle: painted oath sun
    s.append('<g transform="translate(-24,-56) rotate(-12)">')
    s.append(f'<ellipse rx="15" ry="24" fill="#8b6a3e" stroke="{INK}" stroke-width="1.8"/>')
    s.append(f'<ellipse rx="11.5" ry="19.5" fill="{OATH_RED}" stroke="none"/>')
    s.append(f'<path d="M0,-19 L3,-4 L0,0 L-3,-4 Z M0,19 L3,4 L0,0 L-3,4 Z M-11,0 L-2,2 L0,0 L-2,-2 Z" fill="#d9b880"/>')
    s.append(f'<ellipse rx="4" ry="5.5" fill="#b9a68a" stroke="{INK}" stroke-width="1"/>')
    s.append("</g>")
    return "\n".join(s)


def figure_hakon():
    """Gor un Saga Reaver: huge, fur mantle, curled horns, great axe."""
    s = [shadow(34, 11)]
    s.append(legs("#3b2c20", "#1a110c", spread=12, top=-46))
    s.append(path("M-24,-92 C-30,-70 -32,-50 -28,-36 L28,-36 C32,-52 30,-74 24,-92 Z", "#5a3f2c"))
    # fur mantle
    s.append(path("M-30,-96 Q-36,-80 -32,-66 L-26,-70 L-22,-62 L-14,-70 L-6,-60 L2,-70 L10,-61 L18,-70 L26,-63 L30,-72 Q36,-84 30,-98 Q0,-112 -30,-96 Z", "#8a6f55"))
    s.append(brush_strokes(random.Random(4), 40, (-30, -104, 30, -64), ["#c2a383", "#5b4635"], (4, 10), (1, 2), (1.2, 1.9), (0.3, 0.7)))
    # bare arms
    s.append(path("M-30,-86 Q-42,-70 -40,-52 L-33,-50 Q-33,-66 -24,-80 Z", "#9a6b4e"))
    s.append(path("M30,-86 Q44,-96 52,-112 L46,-117 Q36,-102 24,-92 Z", "#9a6b4e"))
    # head and horns
    s.append(f'<ellipse cx="0" cy="-108" rx="12" ry="12" fill="#3a2418" stroke="{INK}" stroke-width="1.6"/>')
    s.append(path("M-9,-114 C-24,-120 -30,-106 -22,-98 C-24,-108 -18,-112 -10,-108 Z", "#cbb796"))
    s.append(path("M9,-114 C24,-120 30,-106 22,-98 C24,-108 18,-112 10,-108 Z", "#cbb796"))
    # great axe resting over shoulder
    s.append(path("M50,-116 L-6,-150", "none", "#2a1a10", 4))
    s.append(path("M-4,-150 C-14,-170 -34,-170 -40,-158 C-30,-156 -22,-146 -20,-134 C-14,-142 -8,-146 -4,-150 Z", "#b8b0a6"))
    s.append(path("M-38,-158 C-30,-156 -22,-146 -20,-134", "none", GLOW, 1.4, 'opacity="0.9"'))
    return "\n".join(s)


def figure_astrid():
    """Elementalist: tall, braided, frost staff raised, storm-grey cloak."""
    s = [shadow(24, 8)]
    s.append(legs("#2e2a2c", "#18120f", spread=7, top=-38))
    s.append(path("M-15,-80 C-24,-56 -30,-26 -36,-2 L-18,-6 L-6,0 L8,-4 L20,-2 C16,-30 16,-58 14,-80 Z", "#3f4a5a"))
    s.append(path("M-6,-76 C-10,-50 -14,-26 -18,-8", "none", "#262d38", 3))
    s.append(path("M-14,-82 Q0,-90 14,-82 L12,-74 Q0,-80 -12,-74 Z", "#55606e"))
    # head with long braid
    s.append(f'<ellipse cx="0" cy="-90" rx="7.5" ry="8.5" fill="#b0763e" stroke="{INK}" stroke-width="1.5"/>')
    s.append(path("M-1,-84 C-4,-70 2,-58 -2,-44", "none", "#b0763e", 4.2))
    s.append(path("M-1,-84 C-4,-70 2,-58 -2,-44", "none", INK, 0.8, 'stroke-dasharray="2 3"'))
    # raised arm + staff with frost crystal
    s.append(path("M12,-78 Q24,-96 30,-118 L25,-120 Q19,-100 8,-84 Z", "#3f4a5a"))
    s.append(path("M18,-60 L36,-150", "none", "#3a2a1c", 2.8))
    s.append(f'<g filter="url(#glow)"><path d="M36,-150 L31,-164 L37,-176 L43,-163 Z" fill="{FROST}" stroke="#e9f6ff" stroke-width="1"/></g>')
    s.append(f'<circle cx="37" cy="-160" r="22" fill="{FROST}" opacity="0.22" filter="url(#soft)"/>')
    return "\n".join(s)


def figure_yrsa():
    """Dwarven Rune Smith: short, very broad, hood, rune hammer, amber runes."""
    s = [shadow(28, 9)]
    s.append(legs("#3a2c22", "#1a110c", spread=11, top=-30))
    s.append(path("M-24,-64 C-28,-44 -28,-24 -26,-10 L26,-10 C28,-26 28,-46 24,-64 Z", "#5c4a33"))
    s.append(path("M-20,-34 L20,-34 L22,-10 L-22,-10 Z", "#3c2c1e"))
    for i, x in enumerate((-14, -4, 6, 14)):
        s.append(f'<path d="M{x},-30 l3,6 l-3,6" fill="none" stroke="{RUNE}" stroke-width="1.4" filter="url(#glow)"/>')
    # hood
    s.append(path("M-14,-62 Q-16,-84 0,-86 Q16,-84 14,-62 Q0,-68 -14,-62 Z", "#4a5a3a"))
    # hammer on shoulder
    s.append(path("M18,-40 L30,-96", "none", "#2a1a10", 3.4))
    s.append(path("M20,-98 L42,-104 L44,-90 L22,-84 Z", "#7c766e"))
    s.append(f'<path d="M26,-96 l4,6 l4,-7 l4,6" fill="none" stroke="{RUNE}" stroke-width="1.5" filter="url(#glow)"/>')
    # runestone bag
    s.append(f'<ellipse cx="-24" cy="-26" rx="8" ry="10" fill="#6b5338" stroke="{INK}" stroke-width="1.4"/>')
    return "\n".join(s)


def figure_apprentice():
    """Civilian escort: small, hooded, clutching a satchel of records."""
    s = [shadow(18, 6)]
    s.append(path("M-12,-50 C-16,-32 -18,-14 -16,0 L14,0 C16,-14 14,-32 10,-50 Z", "#6d5a44"))
    s.append(path("M-10,-48 Q-11,-64 0,-66 Q11,-64 10,-48 Q0,-52 -10,-48 Z", "#5a4a38"))
    s.append(f'<rect x="-14" y="-34" width="16" height="12" rx="2" fill="#8b5a2b" stroke="{INK}" stroke-width="1.3"/>')
    s.append(f'<path d="M-12,-30 h12" stroke="{GLOW}" stroke-width="1" opacity="0.7"/>')
    return "\n".join(s)


def figure_shieldbearer():
    """Eludin shield crew: tall, finned helm, tower shield set with a fel crystal."""
    s = [shadow(26, 8)]
    s.append(legs("#1f1c1d", "#0e0b0b", spread=8, top=-44))
    s.append(path("M-16,-92 L16,-92 L22,-44 L-22,-44 Z", "#2b2a2c"))
    s.append(path("M-20,-94 Q0,-102 20,-94 L18,-84 L-18,-84 Z", "#5b4630"))
    # finned helm with glowing slit
    s.append(path("M-9,-96 L-8,-114 L0,-120 L8,-114 L9,-96 Z", "#6b5236"))
    s.append(path("M0,-120 L4,-140 L10,-118 Z", "#3a2b1e"))
    s.append(f'<path d="M-6,-108 L6,-108" stroke="{FEL}" stroke-width="2" filter="url(#glow)"/>')
    # spear
    s.append(path("M16,-30 L-6,-150", "none", "#1c130e", 3))
    s.append(path("M-6,-150 L-11,-166 L-2,-152 Z", "#b9b0a0", INK, 1.2))
    # tower shield, front-facing, slightly turned
    s.append(path("M-28,-96 L6,-100 L8,-14 L-26,-10 Z", "#6e5130"))
    s.append(path("M-24,-90 L2,-93 L4,-20 L-22,-17 Z", "#4c3622", "none"))
    s.append(path("M-10,-70 L-4,-60 L-10,-46 L-16,-60 Z", FEL, "#bff8ef", 1, 'filter="url(#glow)"'))
    s.append(path("M-26,-56 L6,-58", "none", "#2c1f13", 2))
    return "\n".join(s)


def figure_harpooner():
    """Eludin harpoon raider: lean, coiled rope, barbed harpoon cocked to throw."""
    s = [shadow(22, 7)]
    s.append(legs("#2a2420", "#110c0a", spread=9, top=-42))
    s.append(path("M-13,-88 L13,-88 L16,-42 L-16,-42 Z", "#3a3029"))
    s.append(path("M-18,-90 Q0,-98 18,-90 L14,-80 L-14,-80 Z", "#7a6650"))
    s.append(f'<ellipse cx="0" cy="-99" rx="8" ry="9" fill="#2b2421" stroke="{INK}" stroke-width="1.5"/>')
    s.append(f'<path d="M-5,-100 L5,-100" stroke="{FEL}" stroke-width="1.8" filter="url(#glow)"/>')
    # coiled rope on hip
    s.append(f'<ellipse cx="-12" cy="-52" rx="9" ry="7" fill="none" stroke="#a88a5c" stroke-width="2.4"/>')
    s.append(f'<ellipse cx="-12" cy="-52" rx="5" ry="4" fill="none" stroke="#a88a5c" stroke-width="2"/>')
    # harpoon raised overhead
    s.append(path("M12,-86 Q20,-104 22,-118 L17,-118 Q14,-104 6,-90 Z", "#3a3029"))
    s.append(path("M52,-120 L-30,-112", "none", "#2a1c12", 2.8))
    s.append(path("M-30,-112 L-46,-110 L-34,-106 L-38,-112 L-34,-117 Z", "#c0b6a6", INK, 1.2))
    s.append(path("M52,-120 C64,-100 40,-80 -10,-54", "none", "#a88a5c", 1.2, 'opacity="0.8"'))
    return "\n".join(s)


def figure_adept():
    """Eludin cinder adept: hooded robe, fel brazier staff venting teal cinders."""
    s = [shadow(22, 7)]
    s.append(path("M-14,-88 C-20,-60 -24,-28 -26,0 L24,0 C22,-28 18,-60 14,-88 Z", "#241f22"))
    s.append(path("M-26,0 L-20,-6 L-12,0 L-4,-6 L4,0 L12,-6 L20,0 L24,0", "none", "#0c0a0a", 1.5))
    s.append(path("M-12,-86 Q-14,-110 0,-114 Q14,-110 12,-86 Q0,-92 -12,-86 Z", "#332b2c"))
    s.append(f'<ellipse cx="0" cy="-98" rx="6" ry="7" fill="#050404"/>')
    s.append(f'<circle cx="-2.5" cy="-99" r="1.3" fill="{FEL}" filter="url(#glow)"/>')
    s.append(f'<circle cx="2.5" cy="-99" r="1.3" fill="{FEL}" filter="url(#glow)"/>')
    # staff with cage brazier
    s.append(path("M-20,-10 L-26,-140", "none", "#1a1412", 2.8))
    s.append(path("M-34,-140 L-18,-140 L-22,-156 L-30,-156 Z", "none", "#6e5a3e", 1.8))
    s.append(f'<circle cx="-26" cy="-148" r="7" fill="{FEL}" filter="url(#glow)" opacity="0.9"/>')
    s.append(f'<circle cx="-26" cy="-150" r="26" fill="{FEL}" opacity="0.18" filter="url(#soft)"/>')
    s.append(particles(random.Random(8), 14, (-40, -200, -12, -156), FEL, (0.6, 1.6), (0.4, 0.9), glow=True))
    return "\n".join(s)


def _limb(a, b, w0, w1, fill):
    """Tapered armoured limb segment from a to b."""
    (x0, y0), (x1, y1) = a, b
    dx, dy = x1 - x0, y1 - y0
    L = math.hypot(dx, dy) or 1
    nx, ny = -dy / L, dx / L
    return poly([(x0 + nx * w0, y0 + ny * w0), (x1 + nx * w1, y1 + ny * w1),
                 (x1 - nx * w1, y1 - ny * w1), (x0 - nx * w0, y0 - ny * w0)], fill, INK, 2)


def spirit_engine():
    """Eludin spirit engine artillery: an armoured siege spider carrying a
    crystal soul housing, with visible feed lines and a fel lens aimed at
    the heroes. Origin is the centre of its 2x2 footprint."""
    rng = random.Random(31)
    s = [shadow(130, 46)]
    hips = [(-60, -108), (-36, -96), (-6, -92), (24, -94), (52, -104), (34, -122)]
    knees = [(-138, -170), (-118, -120), (-56, -54), (78, -60), (130, -160), (100, -196)]
    feet = [(-120, 4), (-92, 34), (-30, 50), (46, 42), (110, 14), (78, -30)]

    def leg(i, near):
        h, k, f = hips[i], knees[i], feet[i]
        base = "#4a3420" if near else "#2c2018"
        out = [_limb(h, k, 9, 7, base), _limb(k, f, 7, 3, base)]
        out.append(f'<circle cx="{k[0]}" cy="{k[1]}" r="9" fill="#6e5030" stroke="{INK}" stroke-width="2"/>')
        out.append(f'<circle cx="{k[0]}" cy="{k[1]}" r="3" fill="{FEL}" filter="url(#glow)"/>')
        out.append(path(f"M{f[0]-9},{f[1]+2} L{f[0]},{f[1]-18} L{f[0]+9},{f[1]+2} Z", "#1e150e"))
        if near:
            out.append(path(f"M{h[0]},{h[1]-6} L{k[0]},{k[1]-8}", "none", FLAME, 1.6, 'opacity="0.6"'))
        return "".join(out)

    for i in (5, 0, 4):
        s.append(leg(i, False))
    # under-hull glow from the soul furnace
    s.append(f'<ellipse cx="0" cy="-70" rx="90" ry="30" fill="{FEL}" opacity="0.18" filter="url(#bigGlow)"/>')
    # layered hull plates
    s.append(path("M-92,-110 C-80,-160 70,-170 96,-118 L84,-82 C40,-62 -50,-62 -82,-80 Z", "#2a1e16"))
    s.append(path("M-84,-112 C-60,-150 60,-156 86,-116 L78,-100 C40,-120 -40,-122 -78,-98 Z", "#4d3826"))
    for k in range(-3, 4):
        x = k * 24
        s.append(path(f"M{x-10},{-86 - abs(k)*2} L{x},{-130 + abs(k)*5} L{x+10},{-86 - abs(k)*2}", "none", "#1a120c", 1.6))
    s.append(path("M-84,-112 C-60,-150 60,-156 86,-116", "none", "#b8864a", 2.4))
    s.append(path("M-84,-112 C-60,-150 60,-156 86,-116", "none", FLAME, 1.2, 'opacity="0.8"'))
    for x in range(-70, 80, 12):
        s.append(f'<circle cx="{x}" cy="{-96 - 14*math.cos(x/55):.1f}" r="2" fill="#c09050"/>')
    # crystal soul housing caged in bronze, trapped wisps inside
    s.append(f'<ellipse cx="0" cy="-176" rx="80" ry="70" fill="{FEL}" opacity="0.16" filter="url(#bigGlow)"/>')
    s.append('<g filter="url(#glow)">')
    s.append(path("M-30,-140 L-18,-196 L6,-206 L30,-146 L4,-130 Z", "#0f4a45", "#9ff6ea", 1.8, 'opacity="0.95"'))
    s.append(path("M-18,-196 L4,-130 M6,-206 L4,-130", "none", "#6fe8d8", 1, 'opacity="0.6"'))
    for _ in range(6):
        x = rng.uniform(-14, 14)
        y = rng.uniform(-190, -150)
        s.append(f'<path d="M{x:.1f},{y:.1f} q5,-7 0,-14 q-5,-6 3,-11" fill="none" stroke="#c9fff6" stroke-width="1.5" opacity="0.9"/>')
    s.append("</g>")
    s.append(path("M-36,-138 L-24,-200 M36,-144 L10,-212 M-24,-200 L10,-212 M-40,-136 L40,-142", "none", "#8a6a3a", 3))
    # feed lines snaking from housing to legs, carrying fel light
    for d in ("M-26,-140 C-80,-130 -96,-100 -80,-82", "M26,-142 C86,-134 98,-104 86,-84", "M0,-132 C-10,-110 10,-96 -4,-78"):
        s.append(path(d, "none", "#130e0b", 6))
        s.append(path(d, "none", FEL, 1.6, 'opacity="0.7" stroke-dasharray="8 6"'))
    # lens barrel aimed down-left at the bridge
    s.append(_limb((-60, -96), (-134, -60), 16, 12, "#3a2a1c"))
    s.append(path("M-70,-108 L-140,-74", "none", FLAME, 1.4, 'opacity="0.5"'))
    s.append(f'<ellipse cx="-134" cy="-60" rx="9" ry="14" fill="{FEL}" stroke="#e0fffa" stroke-width="1.5" filter="url(#glow)" transform="rotate(-28 -134 -60)"/>')
    s.append(f'<ellipse cx="-136" cy="-58" rx="34" ry="34" fill="{FEL}" opacity="0.3" filter="url(#soft)"/>')
    for i in (1, 2, 3):
        s.append(leg(i, True))
    return "\n".join(s)
