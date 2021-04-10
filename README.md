# xiblint

The `xiblint` script will test .xib and .storyboard files for compliance with best practices and team policies.

The linter messages contain the position within the XML files, and if applicable, an Object ID
which can be used in conjunction with Xcode's Find in Workspace to jump to the problematic object
in the .xib or .storyboard file.

## Rules

- `accessibility_format`

  Checks for incorrect use of Lyft extensions `accessibilityFormat` and `accessibilitySources`.

- `accessibility_labels_for_images`

  Checks for images with accessibility enabled and no accessibility label.
  In this case, VoiceOver will announce the image asset's name, which might be unwanted.

- `accessibility_labels_for_image_buttons`

  Checks for image buttons with no accessibility label.
  In this case, VoiceOver will announce the image asset's name, which might be unwanted.

- `accessibility_labels_for_text_with_placeholder`

  Checks for text fields and views with a placeholder and no accessibility label.
  This addresses common confusion about `placeholderText` coming instead of `accessibilityLabel`.

- `autolayout_frames`

  Checks for ambiguous and misplaced views.

- `automation_identifiers`

  Makes sure that interactive views have accessibility identifiers, to support testing through UI Automation.

- `automation_identifiers_for_outlet_labels`

  Checks for labels with outlets into a view controller that have no accessibility identifiers.
  Labels with outlets might get dynamic text, and therefore should be accessible to UI testing.

- `enforce_runtime_attributes`

  Ensures a runtime attribute is set to one of the allowed values. Configure `runtime_attributes` in a custom rule configuration using `rules_config` (see below). Use `null` as an option to allow no value.

- `enforce_system_properties`

  Ensures a property in a system type is set to one of the allowed values. Configure `system_properties` in a custom rule configuration using `rules_config` (see below). Use `null` as an option to allow default value.

- `named_colors`

  Ensures all colors are using named colors from an asset catalog. Configure `allowed_colors` to limit the colors to a subset (default is all named colors are allowed), `allow_system_colors` (default is `false`), `allow_clear_color` (default is `false`) and `ignore_alpha` (default is `false`) in a custom rule configuration using `rules_config` (see below).

- `no_trait_variations`

  Ensures Trait Variations are disabled.

- `simulated_metrics_retina4_0`

  Ensures simulated metrics are for the iPhone SE, which is currently the smallest display profile.

- `no_view_controller_links_to_other_bundles`

  Ensures there are no links to other storyboards in different bundles.

- `strict_fonts`

  Ensures all font names and sizes are in an allowed set. Configure `allowed_fonts` with an array of dictionaries containing a `name` and `size` in a custom rule configuration using `rules_config` (see below).

- `strict_font_names`

  Ensures all font namess are in an allowed set. Configure `allowed_fonts` and `allow_system_fonts` (default is `true`) in a custom rule configuration using `rules_config` (see below). This is a good option if `strict_fonts` is too strict.

- `strict_font_sizes`

  Ensures all font sizes are above a minimum font size. Configure `minimum_size` (default is `0`) and/or `maximum_size` (default is `1000`) in a custom rule configuration using `rules_config` (see below). This is a good option if `strict_fonts` is too strict.

- `unavailable_custom_classes`

  Prevent a list of classes from appearing as custom classes. Configure `custom_classes` in a custom rule configuration using `rules_config` (see below). This is a mapping of the full name of the class (`ModuleName.ClassName`) to the suggested replacement.

- `unavailable_system_classes`

  Ensures a system type uses a set of custom clases. Configure `system_classes` in a custom rule configuration using `rules_config` (see below).

## Usage

For a list of available rules, run `xiblint -h`.

Place a configuration file named `.xiblint.json` into the root of your source repository. A sample configuration file would be:

```json
{
  "rules": [
    "accessibility_format",
    "autolayout_frames"
  ],
  "paths": {
    "Pods": {
      "rules": []
    },
    "InaccessibleFeature": {
      "excluded_rules": [
        "accessibility_*"
      ]
    },
    "Modules": {
      "rules": ["some_rule"],
      "rules_config": {
        "some_rule": {
          "some_rule_specific_option": true
        }
      }
    }
  }
}
```

Then simply invoke `xiblint` in the source repository.

### --reporter

If you find yourself in need of a different structure of the output, there is the `--reporter` option.
You are able to choose from the default one, `raw`, or a `json` one. To switch between them, use the following:
```
xiblint --reporter json
xiblint --reporter raw
```

### Specyfing paths

Sometimes you want to lint only a few files and forget about the rest - for instance, when you want to lint only delta changes. For this case you can specify your files after the `xiblint` command:
```
xiblint "Project/Base.lproj/LaunchScreen.storyboard" "Project/Base.lproj/Main.storyboard"
```

If you want to combine paths with the reporter option, don't forget to _put the option before listing the paths_:
```
xiblint --reporter json "Project/Base.lproj/LaunchScreen.storyboard" "Project/Base.lproj/Main.storyboard"
```

## Installation

Using `pip`:
```
pip install xiblint
```

Manual:
```
git clone https://github.com/lyft/xiblint.git
cd xiblint && python setup.py install
```

## Contributing

### Code of conduct

This project is governed by [Lyft's code of conduct](https://github.com/lyft/code-of-conduct). All contributors and participants agree to abide by its terms.

### Sign the Contributor License Agreement (CLA)

We require a CLA for code contributions, so before we can accept a pull request we need to have a signed CLA. Please [visit our CLA service](https://oss.lyft.com/cla) and follow the instructions to sign the CLA.

### File issues in GitHub

Use GitHub issue to file bugs or enhancement requests. You may also use GitHub issues to discuss before implementing a change.

### Submit pull requests

Our only method of accepting code changes is through GitHub pull requests.
