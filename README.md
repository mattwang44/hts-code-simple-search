# HTS Code Simple Search

A simple static website for looking up Harmonized Tariff Schedule (HTS) codes. The site generates static JSON files that can be accessed directly via URLs.

## Usage

Access the data through these URL patterns:

- List all available codes: `https://mattwang44.github.io/hts-code-simple-search/index`
- Get specific code data: `https://mattwang44.github.io/hts-code-simple-search/<code>`
- Search partial codes: `https://mattwang44.github.io/hts-code-simple-search/<partial_code>`

Example searches:
- Category level: `https://mattwang44.github.io/hts-code-simple-search/0101`
- Subcategory level: `https://mattwang44.github.io/hts-code-simple-search/0101.21`
- Full code: `https://mattwang44.github.io/hts-code-simple-search/0101.21.00`
- Most detailed level: `https://mattwang44.github.io/hts-code-simple-search/0101.21.00.10`

## Development

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Place your `htscode.csv` file in the root directory.

3. Run the build script:
   ```bash
   python build.py
   ```

This will generate static JSON files in the `dist` directory. The files are automatically deployed to GitHub Pages when pushed to the main branch.

## Data Format

Each HTS code entry contains:
- HTS Number
- Description
- Unit of Quantity
- Other relevant fields from the CSV

## Deployment

The site is automatically deployed to GitHub Pages using GitHub Actions when changes are pushed to the main branch. The workflow:

1. Sets up Python
2. Installs dependencies
3. Runs the build script
4. Deploys generated files to GitHub Pages

## License

MIT
