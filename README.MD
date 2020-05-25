# Bloons TD 6 Pseudo-Rich Presence

**This rich presence will not work by itself.**

Unfortunately, BTD6 does not have an easy way to find what map you are playing. This "Pseudo-Rich Presence" will allow you to pass arguments for your current state and have that display on your profile.

## Installation

First, clone the repository.

```cmd
git clone https://www.github.com/yolodude25/btd6-rich-presence
```

Then, install the required modules

```cmd
cd btd6-rich-presence
```

```cmd
pip install -r requirements.txt
```

If `python-Levenshtein` causes an error, download [Microsoft C++ Build Tools](https://visualstudio.microsoft.com/visual-cpp-build-tools).

Alternatively, you can ignore it and just run the script, but it will just show a warning when running it.

## Usage

Make a copy of [`config.ini.example`](config.ini.example) and remove the `.example`, then [edit it](#config) if you want.

Run `presence.py` with your [arguments](#arguments).

To exit the program just close the python script.

## Arguments

### `-m, --map`

Map you are playing.

#### Available Values

List of all maps can be found in [`assets.json`](assets.json)

#### Notes

This argument uses fuzzy search, and you can type approximate map names and if they are close enough, it will recognize them.

### `-d, --difficulty`

Difficulty you are playing at.

#### Available Values

`easy`, `medium`, `hard`

#### Notes

Cannot be used without `--map` being set.

### `-v, --variation`

Difficulty variation.

#### Available Values

List of all variations can be found in [`assets.json`](/assets.json).

The variation must be available for the selected difficulty.

#### Notes

Cannot be used without `--difficulty` being set.

This argument uses fuzzy search, and you can type approximate variation names and if they are close enough, it will recognize them.

### `-c, --coop`

Number of players in your Co-Op game.

#### Available Values

`1`, `2`, `3`, `4`

#### Notes

Cannot be used without `--map` being set.

## Config

The [config](config.ini.example) allows you to change what is displayed on your rich presence.

### Available Values

- `{map_image}`: Image key of map. (e.g. "monkey_meadow")
- `{map_hf}`: Name of map. (e.g. "Monkey Meadow")
- `{difficulty_hf}`: Name of difficulty (e.g. "Easy")
- `{variation_image}`: Difficulty variation key of map. (e.g. "deflation")
- `{variation_hf}`: Name of difficulty variation (e.g. "Deflation")

### Rich Presence

#### `client-id`

The client id of the Discord Application. Don't modify this unless you are using custom assets and know what you are doing.

### Normal

Rich Presence when "map" and "difficulty" are set.

### No Difficulty

Rich Presence when only "map" is set.

### Co-Op

State when "coop" is set.

### No Map

State when nothing is set.

## Examples

### Monkey Meadow (Medium - Apopalypse)

#### Command-Line Arguments

```cmd
python presence.py -m "Monkey Meadow" -d Medium -v Apopalypse
```

#### Rich Presence

![Monkey Meadow - Apopalypse](assets/screenshots/monkey_meadow_apopalypse.png)

### Cubism (Hard - Standard) (Co-Op)

#### Command-Line Arguments

```cmd
python presence.py -m Cubism -d Hard -c 3
```

#### Rich Presence

![Cubism (Hard - Standard) (Co-Op)](assets/screenshots/cubism_hard_coop.png)

### #Ouch

#### Command-Line Arguments

```cmd
python presence.py -m #Ouch
```

#### Rich Presence

![#Ouch](assets/screenshots/ouch.png)

### In Menu

#### Command-Line Arguments

```cmd
python presence.py
```

#### Rich Presence

![In Menu](assets/screenshots/in_menu.png)