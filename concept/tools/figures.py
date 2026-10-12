"""Character figures for the battle board, second pass.

Local space: feet at (0, 0), a human stands ~125 units tall. Heroes are
seen from a 3/4 back view (they face the burning city, so their backs are
in shadow and their silhouettes catch the fire); enemies face the camera
and are backlit the same way, with fel light as their accent.
"""
import random

from paint import FEL, FLAME, FROST, GLOW, INK, OATH_RED, RUNE, brush_strokes, particles, path, poly, shadow


def limb(points, col, w, ink=INK, edge=2.6):
    """Outlined, round-capped limb along a polyline (two strokes)."""
    d = "M" + " L".join(f"{x},{y}" for x, y in points)
    return (f'<path d="{d}" fill="none" stroke="{ink}" stroke-width="{w + edge}" stroke-linecap="round" stroke-linejoin="round"/>'
            f'<path d="{d}" fill="none" stroke="{col}" stroke-width="{w}" stroke-linecap="round" stroke-linejoin="round"/>')


def curve_limb(d, col, w, ink=INK, edge=2.6):
    return (f'<path d="{d}" fill="none" stroke="{ink}" stroke-width="{w + edge}" stroke-linecap="round"/>'
            f'<path d="{d}" fill="none" stroke="{col}" stroke-width="{w}" stroke-linecap="round"/>')


def folds(ds, col, w=1.4, op=0.7):
    return "".join(f'<path d="{d}" fill="none" stroke="{col}" stroke-width="{w}" stroke-linecap="round" opacity="{op}"/>' for d in ds)


def legs_back(trou, boot, spread=7, stride=4, hip=-58, thick=9):
    """Two legs, the left one stepping slightly forward (up the screen)."""
    return (limb([(-spread, hip), (-spread - 1, -30), (-spread - 2 + stride * 0.3, -6 - stride)], trou, thick)
            + limb([(spread, hip), (spread + 1, -30), (spread + 2, -6)], trou, thick)
            + path(f"M{-spread-7+stride*0.3},{-16-stride} L{-spread+4+stride*0.3},{-16-stride} L{-spread+4+stride*0.3},{-3-stride} L{-spread-9+stride*0.3},{-2-stride} Z", boot)
            + path(f"M{spread-4},-16 L{spread+7},-16 L{spread+9},0 L{spread-5},0 Z", boot))


# ------------------------------------------------------------------ heroes
def rhen():
    """Oathguard: broad and shield-led, mail and oath-red cloak, spear."""
    s = [shadow(34, 11)]
    s.append(legs_back("#3a2c24", "#191009", spread=8, stride=6))
    # cloak behind everything, blown to the left by the fire wind
    s.append(path("M-24,-104 C-36,-80 -44,-50 -58,-14 C-48,-18 -42,-12 -36,-8 C-30,-14 -22,-12 -14,-4 "
                  "C-6,-12 4,-10 12,-14 C18,-40 22,-80 22,-104 Q0,-112 -24,-104 Z", OATH_RED))
    s.append(folds(["M-14,-98 C-22,-70 -30,-40 -42,-14", "M-2,-98 C-6,-66 -8,-38 -14,-8",
                    "M10,-98 C10,-70 8,-40 6,-14"], "#3e0b07", 2.2, 0.9))
    s.append(folds(["M-24,-102 C-36,-78 -44,-50 -56,-16"], FLAME, 1.6, 0.75))
    # mail mantle over the shoulders
    s.append(path("M-27,-104 Q0,-120 26,-104 L22,-92 Q0,-102 -23,-92 Z", "#6a645e"))
    s.append(folds(["M-20,-100 Q0,-110 20,-100", "M-21,-96 Q0,-106 21,-96"], "#3a3632", 1.1, 0.8))
    # spear arm (right) and spear
    s.append(curve_limb("M22,-100 C30,-90 32,-78 30,-66", "#4a3a30", 8))
    s.append(path("M28,-30 L44,-196", "none", "#2a1a10", 3.6))
    s.append(path("M44,-196 L40,-216 L48,-197 Z", "#d8cab4", INK, 1.3))
    s.append(path("M42,-176 L46,-176", "none", OATH_RED, 3))
    s.append(f'<circle cx="31" cy="-64" r="5" fill="#4a3a30" stroke="{INK}" stroke-width="1.6"/>')
    # helm and coif
    s.append(path("M-10,-110 C-12,-126 -8,-134 0,-135 C8,-134 12,-126 10,-110 Q0,-106 -10,-110 Z", "#7a7068"))
    s.append(path("M-11,-114 L11,-114 L11,-110 L-11,-110 Z", "#3c3631"))
    s.append(folds(["M-6,-131 C-2,-134 4,-133 7,-128"], GLOW, 1.6, 0.9))
    # round shield on the left arm, painted with the oath sun
    s.append('<g transform="translate(-32,-72) rotate(-14)">')
    s.append(f'<ellipse rx="19" ry="30" fill="#8b6a3e" stroke="{INK}" stroke-width="2.2"/>')
    s.append(f'<ellipse rx="15" ry="25.5" fill="{OATH_RED}"/>')
    s.append('<path d="M0,-24 L4,-5 L0,0 L-4,-5 Z M0,24 L4,5 L0,0 L-4,5 Z M-14,0 L-3,3 L0,0 L-3,-3 Z M14,0 L3,3 L0,0 L3,-3 Z" fill="#dcc08a"/>')
    s.append(f'<ellipse rx="5" ry="7" fill="#c0ad90" stroke="{INK}" stroke-width="1.2"/>')
    s.append(f'<path d="M-12,-22 A19,30 0 0 1 10,-26" fill="none" stroke="{GLOW}" stroke-width="2" opacity="0.85"/>')
    s.append("</g>")
    return "\n".join(s)


def hakon():
    """Gor un Saga Reaver: huge, horned, fur-mantled, great axe on shoulder."""
    s = [shadow(40, 13)]
    s.append(legs_back("#3c2c20", "#170f09", spread=11, stride=8, hip=-66, thick=13))
    s.append(path("M-30,-122 C-36,-98 -36,-76 -32,-58 Q0,-50 32,-58 C36,-78 36,-100 30,-122 Z", "#5d412c"))
    s.append(path("M-30,-66 Q0,-58 30,-66 L32,-56 Q0,-48 -32,-56 Z", "#2d1e14"))
    s.append(f'<rect x="-6" y="-66" width="12" height="9" rx="2" fill="#a88a5a" stroke="{INK}" stroke-width="1.2"/>')
    # fur mantle with ragged hem
    s.append(path("M-38,-126 Q-44,-108 -40,-92 L-33,-96 L-30,-86 L-21,-95 L-13,-84 L-4,-95 L5,-84 L13,-95 L22,-85 L30,-95 L38,-88 "
                  "Q44,-110 38,-128 Q0,-146 -38,-126 Z", "#8b7158"))
    s.append(brush_strokes(random.Random(4), 70, (-38, -138, 38, -90), ["#d0b391", "#5b4635", "#a88e70"], (4, 12), (1, 2.2), (1.2, 1.9), (0.35, 0.8)))
    # bare arms: left hangs, right raised to the axe haft
    s.append(curve_limb("M-36,-116 C-48,-100 -50,-84 -46,-66", "#a06d4d", 12))
    s.append(curve_limb("M34,-118 C48,-128 58,-140 62,-152", "#a06d4d", 12))
    s.append(folds(["M-44,-110 C-50,-96 -50,-84 -48,-72", "M38,-122 C50,-132 56,-142 60,-150"], GLOW, 1.6, 0.7))
    s.append('<path d="M-44,-92 l8,-2 M-45,-86 l8,-2" stroke="#3b2318" stroke-width="2"/>')  # war paint
    # head and curling horns
    s.append(f'<ellipse cx="0" cy="-142" rx="14" ry="15" fill="#3d2619" stroke="{INK}" stroke-width="2"/>')
    s.append(path("M-12,-150 C-34,-160 -42,-136 -30,-124 C-30,-138 -24,-146 -14,-140 Z", "#d6c3a0"))
    s.append(path("M12,-150 C34,-160 42,-136 30,-124 C30,-138 24,-146 14,-140 Z", "#d6c3a0"))
    s.append(folds(["M-14,-152 C-30,-158 -38,-146 -36,-134", "M14,-152 C30,-158 38,-146 36,-134"], GLOW, 1.6, 0.9))
    s.append(path("M-6,-128 C-8,-112 -4,-100 -8,-90", "none", "#2a1a10", 4))  # braid
    # great axe resting over the right shoulder
    s.append(path("M64,-154 L-10,-196", "none", "#2a1a10", 5))
    s.append(path("M-8,-196 C-20,-224 -48,-226 -56,-208 C-42,-206 -32,-194 -28,-176 C-20,-186 -14,-192 -8,-196 Z", "#bdb5aa"))
    s.append(path("M-54,-208 C-42,-206 -32,-194 -28,-176", "none", GLOW, 2, 'opacity="0.95"'))
    return "\n".join(s)


def astrid():
    """Elementalist: tall and narrow, long braid, frost staff raised mid-cast."""
    s = [shadow(28, 9)]
    s.append(legs_back("#2f2a2c", "#150f0c", spread=6, stride=5, hip=-56, thick=8))
    s.append(path("M-19,-104 C-30,-74 -38,-40 -48,-2 C-36,-6 -24,-2 -14,2 C-4,-4 8,-2 18,0 C14,-36 16,-74 17,-104 Q0,-112 -19,-104 Z", "#3c4757"))
    s.append(folds(["M-8,-98 C-14,-66 -20,-34 -26,-4", "M6,-98 C4,-66 4,-34 4,-2"], "#232a35", 2.2, 0.9))
    s.append(folds(["M-19,-102 C-30,-74 -38,-40 -46,-6"], FLAME, 1.5, 0.7))
    s.append(path("M-18,-106 Q0,-116 18,-106 L15,-96 Q0,-104 -15,-96 Z", "#5b6676"))
    # head, long copper braid down the back
    s.append(f'<ellipse cx="0" cy="-116" rx="9" ry="10.5" fill="#a96a35" stroke="{INK}" stroke-width="1.8"/>')
    s.append(curve_limb("M-1,-108 C-5,-92 3,-78 -2,-58", "#a96a35", 5.5, edge=2))
    s.append('<path d="M-1,-104 l3,3 M-1,-96 l3,3 M0,-88 l3,3 M-1,-80 l3,3 M-1,-72 l3,3 M-2,-64 l3,3" stroke="#5a3214" stroke-width="1.2"/>')
    s.append(folds(["M-6,-124 C-2,-127 4,-126 7,-121"], GLOW, 1.5, 0.9))
    # raised casting arm and staff
    s.append(curve_limb("M15,-102 C24,-118 30,-132 34,-148", "#3c4757", 7))
    s.append(path("M20,-60 L44,-196", "none", "#3a2a1c", 3.2))
    s.append('<g filter="url(#glow)">')
    s.append(path("M44,-196 L37,-214 L45,-232 L53,-213 Z", FROST, "#f0faff", 1.2))
    s.append("</g>")
    s.append(f'<circle cx="45" cy="-212" r="30" fill="{FROST}" opacity="0.25" filter="url(#soft)"/>')
    s.append(particles(random.Random(12), 16, (20, -250, 75, -180), FROST, (0.6, 1.8), (0.5, 1.0), glow=True))
    return "\n".join(s)


def yrsa():
    """Dwarven Rune Smith: short and very broad, hooded, rune hammer, amber runes."""
    s = [shadow(34, 11)]
    s.append(legs_back("#3a2c22", "#170f09", spread=10, stride=3, hip=-40, thick=12))
    s.append(path("M-30,-86 C-36,-64 -36,-42 -32,-24 Q0,-16 32,-24 C36,-44 36,-66 30,-86 Q0,-96 -30,-86 Z", "#5e4b34"))
    s.append(path("M-26,-44 Q0,-38 26,-44 L28,-22 Q0,-14 -28,-22 Z", "#3a2b1d"))
    for x in (-18, -6, 6, 18):
        s.append(f'<path d="M{x-3},-38 l3,6 l-3,6 l3,4" fill="none" stroke="{RUNE}" stroke-width="1.6" filter="url(#glow)"/>')
    s.append(curve_limb("M-30,-80 C-40,-66 -40,-52 -36,-42", "#5e4b34", 11))
    s.append(curve_limb("M30,-80 C38,-92 42,-104 42,-114", "#5e4b34", 11))
    # gauntlet with glowing rune channel
    s.append(f'<circle cx="42" cy="-116" r="7" fill="#6e6a64" stroke="{INK}" stroke-width="1.6"/>')
    # hood
    s.append(path("M-20,-84 Q-24,-112 0,-116 Q24,-112 20,-84 Q0,-92 -20,-84 Z", "#4c5c3a"))
    s.append(folds(["M-14,-108 Q0,-116 14,-108"], GLOW, 1.6, 0.85))
    # hammer over the shoulder
    s.append(path("M42,-116 L18,-150", "none", "#2a1a10", 4.4))
    # heavy two-faced hammer head, end-on to us
    s.append(path("M4,-164 L18,-170 L32,-164 L32,-144 L18,-138 L4,-144 Z", "#5e5a56"))
    s.append(path("M18,-170 L18,-138", "none", "#2c2826", 1.6))
    s.append(path("M4,-164 L18,-170 L32,-164", "none", GLOW, 1.8, 'opacity="0.9"'))
    s.append(f'<path d="M8,-158 l4,6 l-4,6 M24,-158 l4,6 l-4,6" fill="none" stroke="{RUNE}" stroke-width="1.8" filter="url(#glow)"/>')
    # bag of runestones
    s.append(f'<ellipse cx="-34" cy="-34" rx="10" ry="12" fill="#6b5338" stroke="{INK}" stroke-width="1.6"/>')
    return "\n".join(s)


def apprentice():
    """Civilian escort: small, hooded, clutching a satchel of records."""
    s = [shadow(22, 7)]
    s.append(legs_back("#4a3a2c", "#1a120c", spread=5, stride=2, hip=-36, thick=7))
    s.append(path("M-16,-70 C-22,-50 -24,-30 -22,-16 Q0,-10 20,-16 C20,-32 18,-52 14,-70 Q0,-76 -16,-70 Z", "#6e5b45"))
    s.append(path("M-14,-68 Q-15,-90 0,-92 Q15,-90 14,-68 Q0,-74 -14,-68 Z", "#5a4a38"))
    s.append(folds(["M-10,-86 Q0,-92 10,-86"], GLOW, 1.4, 0.8))
    s.append(f'<rect x="-22" y="-48" width="20" height="16" rx="2" fill="#8b5a2b" stroke="{INK}" stroke-width="1.5"/>')
    s.append(f'<path d="M-20,-44 h16 M-20,-40 h12" stroke="#e8d8b0" stroke-width="1" opacity="0.8"/>')
    return "\n".join(s)


# ------------------------------------------------------------------ enemies
def shieldbearer():
    """Eludin shield crew: tall, finned helm, tower shield set with a fel crystal."""
    s = [shadow(32, 10)]
    s.append(limb([(-8, -60), (-10, -30), (-12, -6)], "#1f1c1e", 9) + limb([(8, -60), (10, -30), (12, -6)], "#1f1c1e", 9))
    s.append(path("M-18,-16 L-5,-16 L-4,0 L-22,0 Z M5,-16 L18,-16 L22,0 L4,0 Z", "#0d0a0a"))
    s.append(path("M-20,-120 C-24,-100 -26,-80 -28,-56 Q0,-48 28,-56 C26,-80 24,-100 20,-120 Z", "#2d2b2e"))
    s.append(path("M-26,-124 Q0,-134 26,-124 L22,-112 Q0,-120 -22,-112 Z", "#5d4630"))
    # finned helm with glowing slit
    s.append(path("M-11,-124 C-12,-138 -9,-148 0,-152 C9,-148 12,-138 11,-124 Z", "#6e5538"))
    s.append(path("M0,-152 L6,-178 L13,-148 Z", "#3a2b1e"))
    s.append(f'<path d="M-7,-138 L7,-138" stroke="{FEL}" stroke-width="2.4" filter="url(#glow)"/>')
    s.append(folds(["M-8,-148 C-2,-153 6,-152 10,-146", "M2,-174 L6,-178 L12,-150"], FLAME, 1.4, 0.8))
    # spear
    s.append(path("M20,-40 L-8,-196", "none", "#1c130e", 3.4))
    s.append(path("M-8,-196 L-14,-216 L-3,-198 Z", "#c4baa8", INK, 1.3))
    # tower shield, front-facing, slightly turned
    s.append(path("M-36,-124 L8,-130 L10,-18 L-34,-12 Z", "#6e5130"))
    s.append(path("M-31,-117 L3,-122 L5,-26 L-29,-21 Z", "#4c3622", "none"))
    s.append(path("M-14,-92 L-6,-78 L-14,-60 L-22,-78 Z", FEL, "#c4fbf2", 1.2, 'filter="url(#glow)"'))
    s.append(path("M-34,-72 L8,-76", "none", "#2c1f13", 2.4))
    s.append(path("M-36,-124 L8,-130", "none", FLAME, 1.8, 'opacity="0.8"'))
    return "\n".join(s)


def harpooner():
    """Eludin harpoon raider: lean, coiled rope, barbed harpoon cocked to throw."""
    s = [shadow(26, 8)]
    s.append(limb([(-7, -56), (-12, -30), (-18, -6)], "#2a2420", 8) + limb([(7, -56), (10, -30), (14, -6)], "#2a2420", 8))
    s.append(path("M-24,-14 L-12,-14 L-12,0 L-28,0 Z M8,-14 L18,-14 L22,0 L6,0 Z", "#0f0b09"))
    s.append(path("M-16,-112 C-20,-94 -20,-74 -20,-56 Q0,-50 20,-56 C20,-74 20,-94 16,-112 Z", "#3a3029"))
    s.append(path("M-22,-116 Q0,-126 22,-116 L18,-104 Q0,-110 -18,-104 Z", "#7a6650"))
    s.append(f'<ellipse cx="0" cy="-126" rx="10" ry="11.5" fill="#2b2421" stroke="{INK}" stroke-width="1.8"/>')
    s.append(f'<path d="M-6,-127 L6,-127" stroke="{FEL}" stroke-width="2.2" filter="url(#glow)"/>')
    s.append(f'<ellipse cx="-16" cy="-66" rx="11" ry="8.5" fill="none" stroke="#a88a5c" stroke-width="2.8"/>')
    s.append(f'<ellipse cx="-16" cy="-66" rx="6" ry="4.5" fill="none" stroke="#a88a5c" stroke-width="2.2"/>')
    s.append(curve_limb("M16,-110 C24,-126 28,-140 30,-152", "#3a3029", 7))
    s.append(curve_limb("M-16,-110 C-24,-100 -26,-88 -22,-78", "#3a3029", 7))
    s.append(path("M70,-156 L-44,-144", "none", "#2a1c12", 3.2))
    s.append(path("M-44,-144 L-64,-142 L-48,-136 L-54,-144 L-48,-151 Z", "#c8beae", INK, 1.3))
    s.append(path("M70,-156 C84,-128 52,-100 -14,-70", "none", "#a88a5c", 1.4, 'opacity="0.8"'))
    s.append(folds(["M-22,-116 Q0,-126 22,-116", "M70,-157 L-44,-145"], FLAME, 1.3, 0.7))
    return "\n".join(s)


def adept():
    """Eludin cinder adept: hooded robe, fel brazier staff venting teal cinders."""
    s = [shadow(28, 9)]
    s.append(path("M-18,-112 C-26,-78 -30,-36 -32,0 L30,0 C28,-36 24,-78 18,-112 Z", "#262024"))
    s.append(path("M-32,0 L-24,-8 L-15,0 L-6,-8 L4,0 L13,-8 L22,0 L30,0", "none", "#0c0a0a", 1.8))
    s.append(folds(["M-8,-100 C-12,-66 -14,-32 -16,-4", "M8,-100 C10,-66 12,-32 14,-4"], "#120e10", 2, 0.9))
    s.append(path("M-16,-110 Q-19,-140 0,-146 Q19,-140 16,-110 Q0,-118 -16,-110 Z", "#352c2e"))
    s.append(f'<ellipse cx="0" cy="-126" rx="8" ry="9" fill="#050404"/>')
    s.append(f'<circle cx="-3" cy="-127" r="1.6" fill="{FEL}" filter="url(#glow)"/>')
    s.append(f'<circle cx="3" cy="-127" r="1.6" fill="{FEL}" filter="url(#glow)"/>')
    s.append(folds(["M-12,-138 Q0,-148 12,-138"], FLAME, 1.4, 0.8))
    s.append(curve_limb("M-16,-104 C-24,-96 -30,-86 -32,-76", "#262024", 8))
    s.append(path("M-26,-10 L-34,-180", "none", "#1a1412", 3.2))
    s.append(path("M-44,-180 L-24,-180 L-28,-200 L-40,-200 Z", "none", "#6e5a3e", 2))
    s.append(f'<circle cx="-34" cy="-190" r="9" fill="{FEL}" filter="url(#glow)" opacity="0.95"/>')
    s.append(f'<circle cx="-34" cy="-192" r="32" fill="{FEL}" opacity="0.2" filter="url(#soft)"/>')
    s.append(particles(random.Random(8), 18, (-52, -260, -16, -200), FEL, (0.6, 1.8), (0.4, 0.95), glow=True))
    return "\n".join(s)


FIGURES = {
    "rhen": rhen, "hakon": hakon, "yrsa": yrsa, "apprentice": apprentice, "astrid": astrid,
    "shieldA": shieldbearer, "shieldB": shieldbearer, "harpoon": harpooner, "adept": adept,
}
