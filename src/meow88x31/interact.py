import os
import questionary
from questionary import Style as QStyle

from .styles import get_style_names, get_style
from .animations import get_animation_names, get_animation
from .flags.palettes import get_flag_names, get_flag
from .core.badge import Badge


_qstyle = QStyle([
    ("qmark", "fg:cyan bold"),
    ("question", "fg:white bold"),
    ("answer", "fg:yellow bold"),
    ("pointer", "fg:cyan bold"),
    ("highlighted", "fg:cyan bold"),
    ("selected", "fg:green bold"),
    ("separator", "fg:gray"),
    ("instruction", "fg:gray italic"),
    ("text", "fg:white"),
    ("disabled", "fg:gray italic"),
])


def run_interactive():
    text = questionary.text(
        "Enter badge text:",
        default="meow :3",
        style=_qstyle,
    ).ask()
    if text is None:
        return

    bg_choice = questionary.select(
        "Background type:",
        choices=[
            "Solid color",
            "Gradient",
            "Pride flag",
        ],
        default="Solid color",
        style=_qstyle,
    ).ask()
    if bg_choice is None:
        return

    bg_color = "#336699"
    bg_gradient = None
    flag_name = None

    if bg_choice == "Solid color":
        bg_color = questionary.text(
            "Background color (e.g. 'navy', '#336699'):",
            default="#336699",
            style=_qstyle,
        ).ask()
        if bg_color is None:
            return
        bg_color = bg_color.strip()

    elif bg_choice == "Gradient":
        c1 = questionary.text("Gradient top/left color:", default="#ff6b6b", style=_qstyle).ask()
        if c1 is None:
            return
        c2 = questionary.text("Gradient bottom/right color:", default="#4ecdc4", style=_qstyle).ask()
        if c2 is None:
            return
        bg_gradient = [c1.strip(), c2.strip()]

    elif bg_choice == "Pride flag":
        flag_choices = get_flag_names()
        flag_name = questionary.select(
            "Select pride flag:",
            choices=flag_choices,
            style=_qstyle,
        ).ask()
        if flag_name is None:
            return

    style_choices = get_style_names()
    style_name = questionary.select(
        "Border style:",
        choices=style_choices,
        default="classic",
        style=_qstyle,
    ).ask()
    if style_name is None:
        return

    fg_color = questionary.text(
        "Text color (e.g. 'white', '#ffffff'):",
        default="white",
        style=_qstyle,
    ).ask()
    if fg_color is None:
        return
    fg_color = fg_color.strip()

    fg_gradient = None
    border_gradient = None
    gradient_direction = "horizontal"
    use_fg_grad = questionary.confirm("Apply gradient to the text itself?", default=False, style=_qstyle).ask()
    if use_fg_grad is None:
        use_fg_grad = False
    use_border_grad = questionary.confirm("Apply gradient to the border?", default=False, style=_qstyle).ask()
    if use_border_grad is None:
        use_border_grad = False
    if use_fg_grad or use_border_grad:
        gradient_direction = questionary.select(
            "Gradient direction:",
            choices=["horizontal", "vertical", "diagonal"],
            default="horizontal",
            style=_qstyle,
        ).ask()
        if gradient_direction is None:
            return
        if use_fg_grad:
            grad_str = questionary.text("Text gradient colors (comma-separated, e.g. #ff0000,#00ff00):", default="#ff0000,#00ff00", style=_qstyle).ask()
            if grad_str:
                fg_gradient = [c.strip() for c in grad_str.split(",")]
        if use_border_grad:
            grad_str = questionary.text("Border gradient colors (comma-separated, e.g. #ff0000,#00ff00):", default="#ff0000,#00ff00", style=_qstyle).ask()
            if grad_str:
                border_gradient = [c.strip() for c in grad_str.split(",")]

    border_color = questionary.text(
        "Border color (e.g. 'black', '#000000') — leave empty for default:",
        default="",
        style=_qstyle,
    ).ask()
    if border_color is None:
        return
    border_color = border_color.strip() or None

    text_border = questionary.text(
        "Text outline/stroke color (e.g. 'black') — leave empty for no outline:",
        default="",
        style=_qstyle,
    ).ask()
    if text_border is None:
        return
    text_border = text_border.strip() or None

    text_border_width = 1
    if text_border:
        text_border_width = questionary.text(
            "Text outline width (pixels):",
            default="1",
            style=_qstyle,
        ).ask()
        if text_border_width is None:
            return
        try:
            text_border_width = max(1, int(float(text_border_width.strip())))
        except (ValueError, OverflowError):
            text_border_width = 1

    font_choice = questionary.select(
        "Font:",
        choices=[
            "Default font (auto-sized)",
            "Custom font file (.ttf or .otf)",
        ],
        default="Default font (auto-sized)",
        style=_qstyle,
    ).ask()
    if font_choice is None:
        return

    font_weight = questionary.select(
        "Font weight:",
        choices=["Normal weight", "Bold weight"],
        default="Normal weight",
        style=_qstyle,
    ).ask()
    if font_weight is None:
        return
    font_weight = 700 if font_weight == "Bold weight" else 400

    font_path = None
    font_size = 0
    if font_choice == "Custom font file (.ttf or .otf)":
        font_path = questionary.text(
            "Full path to your .ttf or .otf font file:",
            style=_qstyle,
        ).ask()
        if font_path is None:
            return
        font_path = font_path.strip()
        if not os.path.exists(font_path):
            questionary.print(f"  ! Font not found, using default", style="red")

    anim_choices = ["None (static PNG)"] + get_animation_names()
    anim_name = questionary.select(
        "Animation:",
        choices=anim_choices,
        default="None (static PNG)",
        style=_qstyle,
    ).ask()
    if anim_name is None:
        return
    if anim_name == "None (static PNG)":
        anim_name = None

    default_ext = "gif" if anim_name else "png"
    default_name = f"badge.{default_ext}"
    output = questionary.text(
        "Output filename:",
        default=default_name,
        style=_qstyle,
    ).ask()
    if output is None:
        return
    output = output.strip()
    if not output:
        output = default_name

    questionary.print("", style="white")

    style_obj = get_style(style_name)

    badge = Badge(
        text=text,
        style=style_obj,
        fg_color=fg_color,
        bg_type="solid" if bg_choice == "Solid color" else ("gradient" if bg_choice == "Gradient" else "flag"),
        bg_color=bg_color if bg_choice == "Solid color" else "#336699",
        bg_gradient=bg_gradient,
        flag_name=flag_name,
        border_color=border_color,
        text_border_color=text_border,
        text_border_width=text_border_width,
        font_path=font_path if font_path and os.path.exists(font_path) else None,
        font_size=font_size,
        font_weight=font_weight,
        fg_gradient=fg_gradient,
        border_gradient=border_gradient,
        gradient_direction=gradient_direction,
    )

    questionary.print("Generating badge...", style="bold green")

    try:
        if anim_name:
            anim = get_animation(anim_name)
            frames = badge.render_animated(anim)
            badge.save(output, frames)
        else:
            badge.save(output)
        questionary.print(f"  Saved to {output}", style="bold green")
    except Exception as e:
        questionary.print(f"  Error: {e}", style="red")
