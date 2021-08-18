from pathlib import Path
import platform


CONFIG_TEMPLATE = """
font:
  size: {font_size}
"""

MACHINE_SPECIFIC_CONFIG_LOCATION = Path('~/.config/alacritty/machine-specific.yml').expanduser()

FONT_SIZE_OVERRIDES = {
    'bl': 14
}
DEFAULT_FONT_SIZE = 11.5


def main():
    current_host = platform.node()
    config = CONFIG_TEMPLATE.format(
        font_size=FONT_SIZE_OVERRIDES.get(current_host, DEFAULT_FONT_SIZE)
    )

    current_config = ''
    if MACHINE_SPECIFIC_CONFIG_LOCATION.exists():
        current_config = MACHINE_SPECIFIC_CONFIG_LOCATION.read_text()

    if config == current_config:
        print(MACHINE_SPECIFIC_CONFIG_LOCATION, "doesn't need updating.")
    else:
        print('Updating', MACHINE_SPECIFIC_CONFIG_LOCATION)
        print('The config is now:\n', config)
        MACHINE_SPECIFIC_CONFIG_LOCATION.write_text(config)


if __name__ == '__main__':
    main()
