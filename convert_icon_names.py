from pathlib import Path
import urllib.request


def convert_icon_names(icon_name: str) -> str:
    icon_name = icon_name.replace("_", "-")
    if icon_name[0] in "0123456789":
        icon_name = "icon-" + icon_name
    return icon_name


def parse_codepoint_line(line: str) -> tuple[str, int]:
    texts = line.strip().split(" ")
    return texts[0], int(texts[1], 16)


def get_codepoints(font_name: str) -> list[tuple[str, int]]:
    url = f"https://raw.githubusercontent.com/google/material-design-icons/master/font/{font_name}.codepoints"
    codepoints = urllib.request.urlopen(url)
    return [parse_codepoint_line(str(line, "utf-8")) for line in codepoints.readlines()]


def construct_satysfi_module(modname: str, font_name: str) -> str:
    codepoints_renamed = [
        (convert_icon_names(name), codepoint)
        for (name, codepoint) in get_codepoints(font_name)
    ]

    lines: list[str] = []
    lines.append(f"module {modname} : sig")

    signitures = [f"  val \\{name} : [] inline-cmd" for (name, _) in codepoints_renamed]
    lines.extend(signitures)

    lines.append("end = struct")
    lines.append("")

    lines.extend(
        [
            "  let embed-icon ctx codepoint =",
            f"    let ctx = ctx |> set-font OtherScript (`fonts-material-icons:{font_name}`, 1.0, 0.0) in",
            "    string-unexplode [codepoint] |> embed-string |> read-inline ctx",
        ]
    )

    lines.append("")

    definitions = [
        f"  let-inline ctx \\{name} = embed-icon ctx 0x{codepoint:04X}"
        for (name, codepoint) in codepoints_renamed
    ]
    lines.extend(definitions)

    lines.append("end")

    return "".join(line + "\n" for line in lines)


def main():
    """Main function."""
    Path("src/icon/outlined.satyh").write_text(
        construct_satysfi_module("MDIconOutlined", "MaterialIconsOutlined-Regular")
    )
    Path("src/icon/round.satyh").write_text(
        construct_satysfi_module("MDIconRound", "MaterialIconsRound-Regular")
    )
    Path("src/icon/sharp.satyh").write_text(
        construct_satysfi_module("MDIconSharp", "MaterialIconsSharp-Regular")
    )
    Path("src/icon/twotone.satyh").write_text(
        construct_satysfi_module("MDIconTwoTone", "MaterialIconsTwoTone-Regular")
    )


if __name__ == "__main__":
    main()
