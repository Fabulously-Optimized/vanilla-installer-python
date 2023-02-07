# v0.2.0

## New features

- Add an option to use the [OpenDyslexic](https://opendyslexic.org) font ([#46])
- Include the fonts (Inter and OpenDyslexic) ([#46])
- **BREAKING**: Redo the config system ([#69])
  - This now uses TOML as opposed to plain text files in the `data` directory, so the end user will understand what it is for more easily.
  - As a result of this, **your settings from v0.1.0 will be reset**.

## Bug fixes

- Made the install button on the GUI unclickable while it is already installing ([#59], [`3a3a0c3`])
- Made the version selector a bit bigger, to fit longer version IDs ([#62], [`b169a5c`])

## Technical changes

- Updated various dependencies
- Updated issue templates
- Added dev builds for Windows back and updated Python builds to include new

[#46]: https://github.com/Fabulously-Optimized/vanilla-installer/pull/46
[#59]: https://github.com/Fabulously-Optimized/vanilla-installer/issues/59
[#62]: https://github.com/Fabulously-Optimized/vanilla-installer/issues/62
[#69]: https://github.com/Fabulously-Optimized/vanilla-installer/pull/69
[`3a3a0c3`]: https://github.com/Fabulously-Optimized/vanilla-installer/commit/3a3a0c36818f48d528c720baed299c18e9fa4842
[`b169a5c`]: https://github.com/Fabulously-Optimized/vanilla-installer/commit/b169a5cbfd42cbbc98e8b5cb12acf8cde7f72bf4
