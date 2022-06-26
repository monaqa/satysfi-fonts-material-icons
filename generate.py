from pathlib import Path
import urllib.request

COMMIT_HASH = "9a68a7b2aa5131c31afd822fa796322754802bfb"


def convert_icon_names(icon_name: str) -> str:
    icon_name = icon_name.replace("_", "-")
    if icon_name[0] in "0123456789":
        icon_name = "icon-" + icon_name
    return icon_name


def parse_codepoint_line(line: str) -> tuple[str, int]:
    texts = line.strip().split(" ")
    return texts[0], int(texts[1], 16)


def get_codepoints(font_name: str) -> list[tuple[str, int]]:
    url = f"https://raw.githubusercontent.com/google/material-design-icons/{COMMIT_HASH}/font/{font_name}.codepoints"
    codepoints = urllib.request.urlopen(url)
    return [parse_codepoint_line(str(line, "utf-8")) for line in codepoints.readlines()]


def get_renamed_codepoints(font_name: str) -> list[tuple[str, int]]:
    return [
        (convert_icon_names(name), codepoint)
        for (name, codepoint) in get_codepoints(font_name)
    ]


def construct_satysfi_module(
    modname: str, font_name: str, codepoint_pairs: list[tuple[str, int]]
) -> str:
    lines: list[str] = []
    lines.append(f"module {modname} : sig")

    signitures = [f"  val \\{name} : [] inline-cmd" for (name, _) in codepoint_pairs]
    lines.extend(signitures)

    lines.append("end = struct")
    lines.append("")

    lines.extend(
        [
            "  let embed-icon ctx codepoint =",
            f"    let ctx = ctx |> set-font OtherScript (`fonts-material-icons:{font_name}`, 0.95, -0.125) in",
            "    string-unexplode [codepoint] |> embed-string |> read-inline ctx",
        ]
    )

    lines.append("")

    definitions = [
        f"  let-inline ctx \\{name} = embed-icon ctx 0x{codepoint:04X}"
        for (name, codepoint) in codepoint_pairs
    ]
    lines.extend(definitions)

    lines.append("end")

    return "".join(line + "\n" for line in lines)


def construct_doc(
    modname: str, varname: str, codepoint_pairs: list[tuple[str, int]]
) -> str:
    lines: list[str] = []
    lines.append(f"@import: ../../src/fonts-material-icons")
    lines.append(f"let {varname} = {{")

    lines.extend(
        [f"| \\{modname}.{name}; | `{name}`" for (name, _) in codepoint_pairs]
    )

    lines.append("|}")
    return "".join(line + "\n" for line in lines)


def main():
    """Main function."""

    Path("src/icon").mkdir(exist_ok=True)
    Path("doc/data").mkdir(exist_ok=True)

    outlined_data = get_renamed_codepoints("MaterialIconsOutlined-Regular")
    Path("src/icon/outlined.satyh").write_text(
        construct_satysfi_module(
            "MDIconOutlined", "MaterialIconsOutlined-Regular", outlined_data
        )
    )
    Path("doc/data/outlined.satyh").write_text(
        construct_doc(
            "MDIconOutlined", "outlined", outlined_data
        )
    )

    round_data = get_renamed_codepoints("MaterialIconsRound-Regular")
    Path("src/icon/round.satyh").write_text(
        construct_satysfi_module(
            "MDIconRound", "MaterialIconsRound-Regular", round_data
        )
    )
    Path("doc/data/round.satyh").write_text(
        construct_doc(
            "MDIconRound", "round", round_data
        )
    )

    sharp_data = get_renamed_codepoints("MaterialIconsSharp-Regular")
    Path("src/icon/sharp.satyh").write_text(
        construct_satysfi_module(
            "MDIconSharp", "MaterialIconsSharp-Regular", sharp_data
        )
    )
    Path("doc/data/sharp.satyh").write_text(
        construct_doc(
            "MDIconSharp", "sharp", sharp_data
        )
    )

    twotone_data = get_renamed_codepoints("MaterialIconsTwoTone-Regular")
    Path("src/icon/twotone.satyh").write_text(
        construct_satysfi_module(
            "MDIconTwoTone", "MaterialIconsTwoTone-Regular", twotone_data
        )
    )
    Path("doc/data/twotone.satyh").write_text(
        construct_doc(
            "MDIconTwoTone", "twotone", twotone_data
        )
    )


if __name__ == "__main__":
    main()
