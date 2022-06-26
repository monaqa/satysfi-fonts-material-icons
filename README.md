# SATySFi Fonts Material Design Icons

[SATySFi](https://github.com/gfngfn/SATySFi) Font Library with [Satyrographos](https://github.com/na4zagin3/satyrographos): [Google Material Design Icons](https://github.com/google/material-design-icons)

To use this font, please install this package followed by `satyrographos install`.

## Installation
### Install SATySFi & Satyrographos
If you don't have them, please install them with this [instruction](https://github.com/na4zagin3/satyrographos).

### Install `satysfi-fonts-material-icons`
```sh
$ opam install satysfi-fonts-material-icons
$ satyrographos install
```

if you get error `bash: satyrographos: command not found`, please read this [instruction](https://github.com/na4zagin3/satyrographos).

## Installed Fonts
This package install the following fonts.

|SATySFi Font Name                                   |Font Filename                      |
|----------------------------------------------------|-----------------------------------|
|`fonts-material-icons:MaterialIconsOutlined-Regular`|`MaterialIconsOutlined-Regular.otf`|
|`fonts-material-icons:MaterialIconsRound-Regular`   |`MaterialIconsRound-Regular.otf`   |
|`fonts-material-icons:MaterialIconsSharp-Regular`   |`MaterialIconsSharp-Regular.otf`   |
|`fonts-material-icons:MaterialIconsTwoTone-Regular` |`MaterialIconsTwoTone-Regular.otf` |

## Usage

You can use icons via command-base APIs. Example:

```
@require: fonts-material-icons/fonts-material-icons

...

'<
  +p{\MDIconOutlined.add-a-photo;}
>
```
