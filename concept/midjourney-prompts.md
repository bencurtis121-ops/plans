# The Meldstone War: Midjourney prompt pack

Art direction: **Frank Frazetta's lighting, color and drama painted over The
Banner Saga's flat shapes, clean linework and layered landscapes.** Umber
darkness, a single hot light source, rim-lit silhouettes, smoke and embers.
The Norse-inflected world is original.

## How to use this

1. **Make the style key first (section 0).** Generate it a few times, pick the
   image that best matches the look, and copy its URL. Every later prompt ends
   in `--sref STYLE_URL`; replace that with your URL so everything matches.
2. **Characters come in two passes.** First a full-body turnaround on a plain
   background (for the sprite artist or for me to cut out), then a portrait.
   Once you like a character, use that image as the character reference
   (`--oref URL` in V7, `--cref URL` in V6) for that character's other shots.
3. **Battle maps are empty terrain.** Midjourney can't draw a reliable tactics
   grid or place units on exact tiles, so generate the map with nobody on it.
   I overlay the grid, units and interface myself.
4. **Upload with these names** so I know what each image is:
   `stylekey_01.png`, `battle_lastpatrol_01.png`, `hero_rhen_body_01.png`,
   `hero_rhen_portrait_01.png`, `enemy_shieldcrew_01.png`, and so on.

Shared ending used below (`[STYLE]`); paste it in place of the token:

```
Frank Frazetta oil painting lighting and palette, The Banner Saga flat stylized shapes and clean ink linework, painterly brushwork, dramatic chiaroscuro, umber shadows, ember and firelight glow, Norse saga atmosphere --no text, watermark, signature, logo, UI
```

---

## 0. Style key

```
a lone shield guard in a red cloak standing on a stone bridge over a frozen river at dusk, a walled city burning on the far ridge, black smoke columns, embers in the wind, snowy pines silhouetted against the fire, [STYLE] --ar 16:9 --s 250
```

```
painted landscape study, layered snowy ridges and stylized pine forests, a ruined runestone in the foreground, burning sky in umber and orange, flat graphic shapes, [STYLE] --ar 16:9 --s 300
```

---

## 1. Title screen and key art

```
epic title screen key art, an oathbound company of six warriors and mystics on a cliff edge, seen from behind, looking at a vast valley where a giant spider-legged siege engine with a glowing teal crystal advances toward a burning capital, banners in the wind, [STYLE] --ar 16:9 --s 300 --sref STYLE_URL
```

```
caravan of refugees and soldiers crossing a frozen plain under a towering stormy sky, tiny figures, huge landscape, long shadows, a red banner at the front, [STYLE] --ar 21:9 --s 300 --sref STYLE_URL
```

---

## 2. Battle maps (empty, overhead three-quarter view)

All use the same camera so they read as one game.

```
top-down three-quarter isometric view of an empty battlefield, snowy riverbank with a narrow stone bridge across a frozen river, trampled mud roads, barrels and wooden stakes for cover, a burning walled city on the horizon at dusk, no people, game battle map background, [STYLE] --ar 16:9 --s 200 --sref STYLE_URL
```
Mission: The Last Patrol (Daeroth outer ward).

```
top-down three-quarter isometric view of an empty royal summer fort courtyard in the mountains, sealed bronze vault door covered in glowing amber runes, broken carts, snow drifts, torchlight, no people, game battle map background, [STYLE] --ar 16:9 --s 200 --sref STYLE_URL
```
Mission: The Summerhold.

```
top-down three-quarter isometric view of an empty grey coastline, ruined longships beached on black sand, alien bronze soul foundry with teal glowing pipes, tide pools, smoke, no people, game battle map background, [STYLE] --ar 16:9 --s 200 --sref STYLE_URL
```
Location: The Ashen Coast.

```
top-down three-quarter isometric view of an empty dwarven forge hall carved in stone, rivers of molten metal, giant anvils, rune-carved pillars glowing amber, no people, game battle map background, [STYLE] --ar 16:9 --s 200 --sref STYLE_URL
```
Location: Kharn Veyr.

```
top-down three-quarter isometric view of an empty ancient forest grown over a war cemetery, mossy grave cairns, enormous roots, cold mist, shafts of pale light, no people, game battle map background, [STYLE] --ar 16:9 --s 200 --sref STYLE_URL
```
Location: The Rootward.

---

## 3. Heroes

For each hero, first run the **full body** prompt, then the **portrait**.
Silhouette rules from the bible: role must read before costume detail, and not
every caster wears a robe.

**Rhen**: human Oathguard, a reluctant protector who distrusts prophecy.
```
full body character design, grizzled veteran shield guard, broad shoulders, round wooden shield painted with a red sun, long spear, mail shirt, oath-red wool cloak, nasal helm, weary eyes, standing guard pose, plain dark background, character turnaround front and back, [STYLE] --ar 3:2 --s 150 --sref STYLE_URL
```
```
bust portrait of a scarred veteran shield guard, nasal helm pushed back, grey stubble, tired stern eyes, red cloak, firelight from below, dark background, [STYLE] --ar 3:4 --s 200 --sref STYLE_URL
```

**Corin**: human Oathguard, an exhausted captain of the watch.
```
full body character design, exhausted middle-aged watch captain, faded blue-grey cloak, battered kite shield, sword, lantern on his belt, slumped but unbroken, plain dark background, character turnaround, [STYLE] --ar 3:2 --s 150 --sref STYLE_URL
```

**Aelyr**: the princess, later an Arcanist.
```
full body character design, young princess turned battle mage, travel-worn royal coat over light leather, staff topped with a violet faceted crystal, geometric violet sigils floating around her hands, determined, plain dark background, character turnaround, [STYLE] --ar 3:2 --s 150 --sref STYLE_URL
```

**Hakon Wolfbound**: Gor un Saga Reaver (a horned non-human people).
```
full body character design, towering horned warrior of a beastlike people, curling ram horns, braided hair, fur mantle, bare scarred arms with war paint, great axe over his shoulder, leaning forward ready to charge, plain dark background, character turnaround, [STYLE] --ar 3:2 --s 150 --sref STYLE_URL
```

**Yrsa Ashhand**: dwarven Rune Smith who traded an eye for forbidden knowledge.
```
full body character design, broad female dwarf rune smith, one eye covered by a carved bone patch, braided hair, leather apron, heavy rune hammer, gauntlet with glowing amber rune channels, pouch of runestones, plain dark background, character turnaround, [STYLE] --ar 3:2 --s 150 --sref STYLE_URL
```

**Svala Threadless**: elven Time Weaver.
```
full body character design, slender elven seer, pale gold threads suspended in the air around her, small glass hourglass charms, ritual spindle, layered grey and gold garments, calm sad expression, plain dark background, character turnaround, [STYLE] --ar 3:2 --s 150 --sref STYLE_URL
```

**Eydis Thornwake**: human Druid, guardian of a forest grown over a war cemetery.
```
full body character design, wild human druid woman, antler and bone headdress, cloak of moss and wolf fur, wooden spear wrapped in living vines, raven on her shoulder, plain dark background, character turnaround, [STYLE] --ar 3:2 --s 150 --sref STYLE_URL
```

**Torvald Emberwake**: Eludin Felbinder, a deserter and former engine technician.
```
full body character design, tall otherworldly deserter engineer, angular bronze armor stripped of insignia, burn scars, blackened teal embers drifting from his gauntlet, tool harness, haunted eyes, plain dark background, character turnaround, [STYLE] --ar 3:2 --s 150 --sref STYLE_URL
```

**Sigrun of the Last Breath**: human Judicar, the youngest guardian of the stone.
```
full body character design, young warrior priestess, ivory and steel armor, bell-shaped reliquary on a chain, mace, winged helm, ivory light, resolute, plain dark background, character turnaround, [STYLE] --ar 3:2 --s 150 --sref STYLE_URL
```

**Neris Manyhands**: Quin Chaos Seer, an alien diplomat.
```
full body character design, alien diplomat with four arms and practical travel gear, smooth grey-blue skin, prismatic broken light shards orbiting a strange instrument, non-human anatomy, plain dark background, character turnaround, [STYLE] --ar 3:2 --s 150 --sref STYLE_URL
```

**Veyra Redleaf**: human Blood Warden and healer.
```
full body character design, battlefield healer woman, dark red leather coat, ritual dagger and bone vessel, restrained crimson threads of light around her wrists, compassionate expression, plain dark background, character turnaround, [STYLE] --ar 3:2 --s 150 --sref STYLE_URL
```

**Astrid Stormglass**: Elementalist.
```
full body character design, tall storm mage woman, long copper braid, storm-grey cloak, staff with a frost crystal crackling with pale blue light, frost on her sleeves, plain dark background, character turnaround, [STYLE] --ar 3:2 --s 150 --sref STYLE_URL
```

**Maelin Seedkeeper**: Life Weaver.
```
full body character design, gentle gardener healer, satchel of glowing green seeds, living wood staff sprouting leaves, layered earth-toned wool, plain dark background, character turnaround, [STYLE] --ar 3:2 --s 150 --sref STYLE_URL
```

**Althon**: the bookkeeper and chronicler (camp only, never deployed).
```
bust portrait of an elderly bookkeeper and chronicler, ink-stained fingers, spectacles, fur-lined coat, stack of ledgers, warm candlelight, dark background, [STYLE] --ar 3:4 --s 200 --sref STYLE_URL
```

For portraits of the others, reuse Rhen's portrait prompt and swap in the
description.

---

## 4. Enemies

```
full body character design, otherworldly invader shield trooper, tall finned bronze helm with a glowing teal eye slit, tower shield set with a teal crystal, long spear, longship-culture armor fused with alien technology, plain dark background, front view, [STYLE] --ar 3:2 --s 150 --sref STYLE_URL
```
Eludin shield crew.

```
full body character design, lean invader raider throwing a barbed harpoon, coiled rope at the hip, fur mantle over bronze scale, glowing teal eyes, plain dark background, [STYLE] --ar 3:2 --s 150 --sref STYLE_URL
```
Harpoon raider.

```
full body character design, hooded invader mystic, ragged black robes, staff with a caged brazier venting blackened teal embers, face hidden in shadow except two teal points of light, plain dark background, [STYLE] --ar 3:2 --s 150 --sref STYLE_URL
```
Cinder adept.

```
giant articulated siege spider war machine, six armored bronze legs, central crystal housing glowing teal with trapped ghostly souls, visible feed lines and pipes, a lens cannon on the front, steam and smoke, three-quarter view, dark background, [STYLE] --ar 16:9 --s 250 --sref STYLE_URL
```
Spirit engine artillery.

```
colossal boss war machine with nine glowing feed lines and moving artillery legs, exposed soul core, looming over a burning battlefield, heroes tiny in the foreground, [STYLE] --ar 16:9 --s 300 --sref STYLE_URL
```
The Ninefold Engine.

```
full body character design, oathbroken knight, cracked armor overgrown with frost, torn tabard, hollow eyes glowing dim amber, plain dark background, [STYLE] --ar 3:2 --s 150 --sref STYLE_URL
```
Oathbroken knight.

```
full body character design, revenant warrior held together by damaged glowing rune carvings, bones and rusted mail, flickering amber light, plain dark background, [STYLE] --ar 3:2 --s 150 --sref STYLE_URL
```
Rune revenant.

```
a sulfur-eating dragon coiled on a volcanic vent, yellow sulfur crust, glowing gem in its throat, smoke, enormous scale, [STYLE] --ar 16:9 --s 300 --sref STYLE_URL
```
Dragon.

---

## 5. Camp and dialogue scenes

```
two weary warriors talking beside a campfire at night in a snowy forest camp, a veteran shield guard and an exhausted captain, rim lit by firelight, refugees sleeping in the background, [STYLE] --ar 16:9 --s 250 --sref STYLE_URL
```

```
war camp at dawn, tents and wagons, a dwarf smith working at a portable forge throwing sparks, a memorial cairn with carved names, banners, [STYLE] --ar 16:9 --s 250 --sref STYLE_URL
```

```
interior of a sealed ancient archive, a princess and an old chronicler reading a glowing treaty scroll, violet light, dust in the air, [STYLE] --ar 16:9 --s 250 --sref STYLE_URL
```

---

## 6. Travel and route map

```
hand-painted fantasy route map of a cold northern kingdom, coastlines, mountains, a besieged capital, a dwarven city, a sacred forest, an ash-covered coast, drawn on aged vellum, inked illustrations, warm firelight vignette, no text --ar 16:9 --s 250 --sref STYLE_URL
```

```
side view of a long marching column crossing a mountain pass in snow, flat layered parallax landscape, tiny figures, huge sky, [STYLE] --ar 21:9 --s 300 --sref STYLE_URL
```

---

## 7. Interface textures and ornaments

Midjourney is weak at real interface layout, so only ask it for materials.
I'll build the actual UI.

```
ornate dark carved wood and iron frame border, Norse knotwork, worn leather, empty center, flat front view, game UI panel texture, dark background --ar 3:2 --s 100 --no text
```

```
set of ten round magic school emblems on parchment: violet geometric facets, flame and frost, pale gold hourglass, blackened teal ember, crimson thread, ivory bell, amber rune, prismatic broken shards, green seed, antler and raven, flat icon style, black ink outlines --ar 16:9 --s 100 --no text
```
