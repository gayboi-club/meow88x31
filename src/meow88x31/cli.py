import sys
import click

from . import __version__
from .styles import get_style_names, get_style
from .animations import get_animation_names, get_animation
from .flags.palettes import get_flag_names
from .core.badge import Badge

_MLM = [
    (7, 141, 112),
    (38, 206, 170),
    (152, 232, 193),
    (255, 255, 255),
    (123, 173, 226),
    (80, 73, 204),
    (61, 26, 120),
]


def _init_color():
    try:
        import colorama
        colorama.just_fix_windows_console()
    except Exception:
        pass


def _spread(length, colors):
    n = len(colors)
    repeat = length // n
    weights = [repeat] * n
    extra = length % n
    if extra % 2:
        extra -= 1
        weights[n // 2] += 1
    i = 0
    while extra:
        extra -= 2
        weights[i] += 1
        weights[-(i + 1)] += 1
        i += 1
    result = []
    for idx, w in enumerate(weights):
        result.extend([colors[idx]] * w)
    return result


_CONTOUR = set("╔═╗║╚╝")


def _cline(text):
    cols = _spread(len(text), _MLM)
    out = []
    for ch, (r, g, b) in zip(text, cols):
        if ch in _CONTOUR:
            out.append(f"\033[38;2;{r};{g};{b}m{ch}\033[0m")
        else:
            out.append(f"\033[38;2;255;255;255m{ch}\033[0m")
    return "".join(out)


def print_banner():
    _init_color()
    sys.stdout.write("\n")
    sys.stdout.write(_cline("  ╔══════════════════════╗") + "\n")
    sys.stdout.write(_cline("  ║   meow88x31 v{}   ║".format(__version__)) + "\n")
    sys.stdout.write(_cline("  ║a silly 88x31 maker :3║") + "\n")
    sys.stdout.write(_cline("  ╚══════════════════════╝") + "\n")
    sys.stdout.write("\n")


@click.command()
@click.argument("text", required=False, default=None)
@click.option("-o", "--output", help="Output file path (.png or .gif)")
@click.option("--style", type=click.Choice(get_style_names()), default=None, help="Border style")
@click.option("--fg", default=None, help="Text color (name, #hex)")
@click.option("--bg", default=None, help="Background color (name, #hex)")
@click.option("--gradient", default=None, help="Comma-separated gradient colors")
@click.option("--flag", default=None, help="Pride flag background")
@click.option("--border-color", default=None, help="Border color (name, #hex)")
@click.option("--text-border", default=None, help="Text outline color (name, #hex)")
@click.option("--text-border-width", type=int, default=1, help="Text outline width")
@click.option("--font", default=None, help="Path to TTF/OTF font")
@click.option("--font-size", type=int, default=None, help="Font size (0 = auto)")
@click.option("--font-weight", type=click.Choice(["normal", "bold"]), default=None, help="Font weight (normal or bold)")
@click.option("--fg-gradient", default=None, help="Comma-separated text gradient colors")
@click.option("--border-gradient", default=None, help="Comma-separated border gradient colors")
@click.option("--gradient-direction", type=click.Choice(["horizontal", "vertical", "diagonal"]), default=None, help="Gradient direction (horizontal, vertical, diagonal)")
@click.option("--animate", default=None, help="Animation name")
@click.option("-i", "--interactive", is_flag=True, default=False, help="Force interactive mode")
@click.option("--list-styles", is_flag=True, help="List available styles")
@click.option("--list-animations", is_flag=True, help="List available animations")
@click.option("--list-flags", is_flag=True, help="List available pride flags")
@click.option("--version", is_flag=True, help="Show version")
def main(
    text,
    output,
    style,
    fg,
    bg,
    gradient,
    flag,
    border_color,
    text_border,
    text_border_width,
    font,
    font_size,
    font_weight,
    fg_gradient,
    border_gradient,
    gradient_direction,
    animate,
    interactive,
    list_styles,
    list_animations,
    list_flags,
    version,
):
    if version:
        click.echo(f"meow88x31 v{__version__}")
        return

    if list_styles:
        click.echo("Styles:")
        for s in get_style_names():
            click.echo(f"  {s}")
        return

    if list_animations:
        click.echo("Animations:")
        for a in get_animation_names():
            click.echo(f"  {a}")
        return

    if list_flags:
        click.echo("Pride Flags:")
        for f in get_flag_names():
            click.echo(f"  {f}")
        return

    if interactive or text is None:
        from .interact import run_interactive
        print_banner()
        run_interactive()
        return

    style_obj = get_style(style or "classic")
    font_size = font_size or 0
    font_weight = 700 if font_weight == "bold" else 400
    fg_gradient_parsed = [c.strip() for c in fg_gradient.split(",")] if fg_gradient else None
    border_gradient_parsed = [c.strip() for c in border_gradient.split(",")] if border_gradient else None
    gradient_direction = gradient_direction or "horizontal"
    bg_type = "solid"
    bg_color = bg or "#336699"
    bg_gradient = None

    if flag:
        bg_type = "flag"
        bg_color = None

    if gradient:
        bg_type = "gradient"
        bg_gradient = [c.strip() for c in gradient.split(",")]

    badge = Badge(
        text=text,
        style=style_obj,
        fg_color=fg or "white",
        bg_type=bg_type,
        bg_color=bg_color,
        bg_gradient=bg_gradient,
        flag_name=flag,
        border_color=border_color,
        text_border_color=text_border,
        text_border_width=text_border_width or 1,
        font_path=font,
        font_size=font_size,
        font_weight=font_weight,
        fg_gradient=fg_gradient_parsed,
        border_gradient=border_gradient_parsed,
        gradient_direction=gradient_direction,
    )

    out_path = output or f"badge.{'gif' if animate else 'png'}"

    if animate:
        anim = get_animation(animate)
        frames = badge.render_animated(anim)
        badge.save(out_path, frames)
    else:
        badge.save(out_path)

    click.echo(f"Saved to {out_path}")


if __name__ == "__main__":
    main()
