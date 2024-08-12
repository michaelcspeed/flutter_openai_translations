import openai
import json
import os
import subprocess


# Set up your OpenAI API key
openai.api_key = YOUR_KEY_HERE

# Function to translate text with context
def translate_text(text, target_language, context=None):
    messages = [
        {"role": "system", "content": f"Translate the following text to {target_language}:"}
    ]
    if context:
        messages.append({"role": "user", "content": f"Context: {context}"})
    messages.append({"role": "user", "content": text})

    response = openai.chat.completions.create(
        model="gpt-4o",
        messages=messages
    )
    return response.choices[0].message.content.strip()

# Load English ARB file
def load_json_file(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as file:
            return json.load(file)
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON in file {filepath}: {e}")
        print("Please check the syntax of the file around the indicated line and column.")
        exit(1)

# Function to determine language code from file name
def get_language_code(filename):
    return filename.split('_')[1].split('.')[0]

# Function to run Flutter gen-l10n command
def run_flutter_gen_l10n():
    try:
        result = subprocess.run(['flutter', 'gen-l10n'], check=True, capture_output=True, text=True)
        print("Flutter gen-l10n command executed successfully.")
        print(result.stdout)
    except subprocess.CalledProcessError as e:
        print("Error executing Flutter gen-l10n command:")
        print(e.stderr)

# Load English ARB file
en_arb = load_json_file('lib/l10n/app_en.arb')

# Get list of ARB files in the l10n directory
l10n_dir = 'lib/l10n'
arb_files = [f for f in os.listdir(l10n_dir) if f.endswith('.arb') and f != 'app_en.arb']

# Get the set of keys from the English ARB file
en_keys = set(en_arb.keys())

# Iterate over each ARB file and update the content
for arb_file in arb_files:
    filepath = os.path.join(l10n_dir, arb_file)
    lang = get_language_code(arb_file)

    arb_content = load_json_file(filepath)

    # Remove keys that are not in the English ARB file
    arb_keys = set(arb_content.keys())
    keys_to_remove = arb_keys - en_keys
    if keys_to_remove:
        print(f"\nIn {arb_file}:")
    for key in keys_to_remove:
        if not key.startswith('@'):
            print(f"  Removing key: {key}")
            del arb_content[key]
        else:
            # Also remove associated metadata
            associated_key = key[1:]
            if associated_key not in en_keys:
                print(f"  Removing metadata: {key}")
                del arb_content[key]

    # Check for new keys in the English ARB file and translate them
    for key, value in en_arb.items():
        if key not in arb_content and not key.startswith('@'):
            # Get context if available
            context_key = f"@{key}"
            context = en_arb.get(context_key, {}).get("description", None)

            # Translate and add the new key to the language ARB
            translated_text = translate_text(value, lang, context)
            arb_content[key] = translated_text
            if context:
                arb_content[context_key] = {"description": context}
            print(f"  Added key: {key} with translation: {translated_text}")

    # Write the updated ARB file back to disk
    with open(filepath, 'w', encoding='utf-8') as file:
        json.dump(arb_content, file, ensure_ascii=False, indent=2)

print("\nTranslation update complete.")

# Run Flutter gen-l10n command
print("\nGenerating localization files...")
run_flutter_gen_l10n()