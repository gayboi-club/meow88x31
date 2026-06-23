FLAGS: dict[str, list] = {
    "mlm": [
        "#078D70",
        "#26CEAA",
        "#98E8C1",
        "#FFFFFF",
        "#7BADE2",
        "#5049CC",
        "#3D1A78",
    ],
    "lesbian": [
        "#D52D00",
        "#EF7627",
        "#FF9A56",
        "#FFFFFF",
        "#D162A4",
        "#B55690",
        "#A30262",
    ],
    "bi": [
        {"color": "#D60270", "ratio": 0.4},
        {"color": "#9B4F96", "ratio": 0.2},
        {"color": "#0038A8", "ratio": 0.4},
    ],
    "trans": [
        "#5BCEFA",
        "#F5A9B8",
        "#FFFFFF",
        "#F5A9B8",
        "#5BCEFA",
    ],
    "femboy": [
        "#E75480",
        "#F4AAC2",
        "#FFFFFF",
        "#58CEF8",
        "#FFFFFF",
        "#F4AAC2",
        "#E75480",
    ],
    "transfem": [
        "#5BCEFA",
        "#F5A9B8",
        "#FFFFFF",
        "#F5A9B8",
        "#5BCEFA",
    ],
    "genderfluid": [
        "#FF76A4",
        "#FFFFFF",
        "#C011D7",
        "#000000",
        "#2F3CBE",
    ],
    "transmasc": [
        "#74DFFF",
        "#9AEBFF",
        "#CDF5FE",
        "#FFFFFF",
        "#FF8ABD",
    ],
}


def get_flag_names() -> list[str]:
    return sorted(FLAGS.keys())


def get_flag(name: str) -> list:
    if name not in FLAGS:
        raise ValueError(f"Unknown flag: {name}. Available: {', '.join(FLAGS)}")
    return FLAGS[name]
