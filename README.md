# meow88x31 :3c

a silly 88x31 maker :3

makes those lil 88x31 web buttons for ur site !! pride flags, animations,
gradients, custom fonts, border styles, the whole deal :3c

## installation

```bash
pip install meow88x31
```

## usage

### interactive mode (easiest !!)

```bash
meow88x31
```

it guides u through everything :3c

### command line mode

```bash
meow88x31 "meow :3" -o badge.png
meow88x31 "trans rights" --flag trans --style double -o badge.png
meow88x31 "sparkles !!" --animate rainbow --fg-gradient "#ff0000,#ffff00" -o badge.gif
```

### all the options or whatever

| Option | what it does |
|---|---|
| `TEXT` | what u want on the badge (leave blank for interactive) |
| `-o, --output` | where to save it (.png or .gif) |
| `--style` | border style: `classic`, `flat`, `raised`, `groove`, `double`, `none` |
| `--fg` | text color (name or `#hex`) |
| `--bg` | background color (name or `#hex`) |
| `--gradient` | background gradient as comma-separated colors |
| `--flag` | pride flag background ! |
| `--border-color` | border color (name or `#hex`) |
| `--text-border` | text outline/stroke color |
| `--text-border-width` | how thick the outline is (pixels) |
| `--font` | path to a .ttf or .otf font file |
| `--font-size` | font size (0 = auto fits the badge) |
| `--font-weight` | `normal` or `bold` |
| `--fg-gradient` | text gradient colors (comma-separated) |
| `--border-gradient` | border gradient colors (comma-separated) |
| `--gradient-direction` | `horizontal`, `vertical`, `diagonal` |
| `--animate` | make it a gif !! pick an animation |
| `-i, --interactive` | force interactive even if u gave text |
| `--list-styles` | show all border styles |
| `--list-animations` | show all animations |
| `--list-flags` | show all pride flags |
| `--version` | prints version nya |

### animations

`blink`, `blossom`, `rainbow`, `scanline`, `snow`, `typing`, `wave`

### pride flags >:3

`bi`, `femboy`, `genderfluid`, `lesbian`, `mlm`, `trans`, `transfem`, `transmasc`

## examples !!

```bash
# trans rights babyyy
meow88x31 "trans rights" --flag trans --style classic -o trans.png

# spinning rainbow chaos
meow88x31 "rainbowww" --animate rainbow --style flat -o chaos.gif

# cute gradient badge
meow88x31 "nyaa~" --gradient "#ff6b6b,#4ecdc4" --style raised -o cute.png

# bold text w a fat outline
meow88x31 "WOW" --fg "#ffffff" --text-border "#000000" --font-weight bold -o wow.png
```

## license

MIT !! do whatever ~
