# ARB Translation Updater

This project provides a Python script to automatically update and manage ARB (Application Resource Bundle) files for multi-language support in Flutter applications. It uses OpenAI's GPT-4o model to translate new strings and keep all language files in sync with the primary English ARB file.

## Features

- Synchronizes all ARB files with the primary English (`app_en.arb`) file
- Automatically translates new strings to all supported languages
- Removes obsolete keys from non-English ARB files
- Preserves context information for translations
- Handles JSON parsing errors gracefully

## Prerequisites

- Python 3.6+
- OpenAI API key

## Installation

1. Clone this repository:
   ```
   git clone https://github.com/yourusername/arb-translation-updater.git
   cd arb-translation-updater
   ```

2. Install the required Python packages:
   ```
   pip install openai
   ```

3. Set up your OpenAI API key:
   - Open the `update_translations.py` file
   - Replace `YOUR_KEY_HERE` with your actual OpenAI API key:
     ```python
     openai.api_key = "your_actual_api_key_here"
     ```

## Usage

1. Place your primary English ARB file named `app_en.arb` in the `lib/l10n/` directory.

2. Create empty ARB files for all other languages you want to support. For example:
   - `app_es.arb` for Spanish
   - `app_fr.arb` for French
   - `app_de.arb` for German
   
   These files should be empty or contain only the base structure of an ARB file (e.g., `{}`).

3. Run the script:
   ```
   python update_translations.py
   ```

4. The script will process all ARB files, translate new strings, remove obsolete keys, and update the files accordingly.

## English ARB File Structure

The English ARB file (`app_en.arb`) serves as the primary source for translations. Here's an example of what it might look like:

```json
{
  "helloWorld": "Hello World!",
  "@helloWorld": {
    "description": "The conventional newborn programmer greeting"
  },
  "welcomeMessage": "Welcome to our app, {username}!",
  "@welcomeMessage": {
    "description": "A welcome message displayed after login",
    "placeholders": {
      "username": {
        "type": "String",
        "example": "John Doe"
      }
    }
  }
}
```

In this structure:
- `"helloWorld"` and `"welcomeMessage"` are the keys for the translatable strings.
- The corresponding `"@helloWorld"` and `"@welcomeMessage"` objects contain metadata about these strings.
- The `"description"` field in the metadata provides context for the translators.

## String Descriptions

The `"description"` field in the ARB file plays a crucial role in the translation process:

1. **Context for Translators**: It provides additional context about the string's usage, helping to ensure more accurate translations.

2. **Used in the Script**: The script uses this description as context when calling the OpenAI API for translation. In the `translate_text` function, if a context is available, it's included in the API call:

   ```python
   if context:
       messages.append({"role": "user", "content": f"Context: {context}"})
   ```

3. **Improving Translation Quality**: By providing this context to the AI model, we can get more contextually appropriate and accurate translations, especially for strings that might be ambiguous without additional information.

4. **Preservation**: The script preserves these descriptions when updating the ARB files, ensuring that the context is maintained for future translations or updates.

## How It Works

1. The script loads the primary English ARB file (`app_en.arb`).
2. It then iterates through all other ARB files in the `lib/l10n/` directory.
3. For each non-English ARB file:
   - It removes keys that are not present in the English file.
   - It adds and translates any new keys found in the English file.
   - It preserves any existing translations and context information.
4. The updated ARB files are written back to disk.

## Customization

- You can modify the `translate_text` function to use a different translation service if desired.
- Adjust the `model` parameter in the OpenAI API call to use a different GPT model.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is open source and available under the [MIT License](LICENSE).

## Disclaimer

This script uses the OpenAI API, which may incur costs based on your usage. Please be aware of the OpenAI pricing structure and monitor your usage accordingly.