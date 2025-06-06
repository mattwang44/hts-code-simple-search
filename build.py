# /// script
# dependencies = [
#     "pandas",
# ]
# ///
import pandas as pd
import json
import numpy as np
from pathlib import Path
import shutil


class NumpyJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        if isinstance(obj, np.floating):
            return float(obj)
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return super().default(obj)


def format_row(row):
    """Format a row into clean JSON data."""
    result = {}
    for col, val in row.items():
        # Skip empty values
        if pd.isna(val) or val == '':
            continue
        # Handle list-like strings (e.g., '["No."]')
        if isinstance(val, str):
            if val.startswith('[') and val.endswith(']'):
                try:
                    val = json.loads(val)
                except ValueError:
                    pass
        result[col] = val
    return result


def create_search_index(df):
    """Create search index for partial text search."""
    search_data = {}
    partial_matches = {}

    for _, row in df.iterrows():
        code = row['HTS Number']
        if not code:
            continue

        # Add code itself
        search_data[code] = {'type': 'exact', 'data': format_row(row)}

        # Add parts of the code (e.g., for 0101.21.00, add 0101, 0101.21)
        parts = code.split('.')
        for i in range(1, len(parts)):
            partial = '.'.join(parts[:i])
            if partial:
                if partial not in partial_matches:
                    partial_matches[partial] = []
                if code not in partial_matches[partial]:
                    partial_matches[partial].append(code)

    # Add partial matches to search data
    for partial, matches in partial_matches.items():
        search_data[partial] = {'type': 'partial', 'matches': sorted(matches)}

    return search_data


def main():
    # Create output directory
    output_dir = Path('dist')
    output_dir.mkdir(exist_ok=True)
    codes_dir = output_dir / 'codes'
    codes_dir.mkdir(exist_ok=True)

    # Read CSV file
    print('Reading CSV file...')
    df = pd.read_csv('htscode.csv')
    df['HTS Number'] = df['HTS Number'].fillna('').astype(str)

    # Create search index
    print('Creating search index...')
    search_index = create_search_index(df)

    # Save search index
    print('Saving search index...')
    with open(output_dir / 'search.json', 'w', encoding='utf-8') as f:
        json.dump(search_index, ensure_ascii=False, indent=None, separators=(',', ':'), cls=NumpyJSONEncoder, fp=f)

    # Generate JSON files for each unique code
    print('Generating code files...')
    codes_processed = 0

    for code, entry in search_index.items():
        if entry['type'] == 'exact':
            with open(codes_dir / code, 'w', encoding='utf-8') as f:
                json.dump(
                    entry['data'], ensure_ascii=False, indent=None, separators=(',', ':'), cls=NumpyJSONEncoder, fp=f
                )
            codes_processed += 1
            if codes_processed % 1000 == 0:
                print(f"Processed {codes_processed} codes...")

    # Create index with .json extension
    codes = sorted([code for code, entry in search_index.items() if entry['type'] == 'exact'])
    with open(output_dir / 'index.json', 'w', encoding='utf-8') as f:
        json.dump(
            {
                'available_codes': codes,
                'total_codes': len(codes),
                'example_searches': [
                    '0101',  # Category level
                    '0101.21',  # Subcategory level
                    '0101.21.00',  # Full code
                    '0101.21.00.10',  # Most detailed level
                ],
            },
            ensure_ascii=False,
            indent=None,
            separators=(',', ':'),
            cls=NumpyJSONEncoder,
            fp=f,
        )

    # Create .nojekyll file
    (output_dir / '.nojekyll').touch()

    # Copy 404.html to output directory if it exists
    if Path('dist/404.html').exists():
        shutil.copy('dist/404.html', output_dir / '404.html')

    print('Build completed successfully!')
    print('File structure:')
    print('  dist/')
    print('    codes/          - Directory containing individual code files')
    print('    search          - Search index for partial and exact matches')
    print('    index           - List of all available codes')
    print('    404.html       - Handler for displaying JSON content')
    print('    .nojekyll      - File to prevent GitHub Pages from processing files')


if __name__ == '__main__':
    main()
