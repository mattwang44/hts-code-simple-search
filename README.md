# HTS Code Simple Search

A simple static website for looking up Harmonized Tariff Schedule (HTS) codes. The site generates static JSON files that can be accessed directly via URLs.

## Usage

```sh
> curl "https://mattwang44.github.io/hts-code-simple-search/" -sS | jq
{
   "available_codes": [
      "0101.21.00.10",
      "0101.21.00.20",
      ...
      "9922.52.11",
      "9922.52.12"
   ],
   "total_codes": 23655
}
```

```sh
> curl "https://mattwang44.github.io/hts-code-simple-search/codes/0202.20.10.00" -sS | jq
{
  "HTS Number": "0202.20.10.00",
  "Indent": 4,
  "Description": "High-quality beef cuts",
  "Unit of Quantity": [
    "kg"
  ],
  "General Rate of Duty": "4%",
  "Special Rate of Duty": "Free (A+,AU,BH,CL,CO,D,E*,IL,JO,KR,MA,OM,P,PA,PE,S,SG)",
  "Column 2 Rate of Duty": "20%"
}
```

## Development

1. Place your `htscode.csv` file in the root directory. You can download it from the USITC website:
   ```bash
   curl 'https://hts.usitc.gov/reststop/exportList?from=0000&to=9999.99.9999&format=CSV&styles=false' > htscode.csv
   ```

2. Run the build script:
   ```bash
   uv run build.py
   ```

This will generate static JSON files in the `dist` directory.

## Deployment

The site is automatically deployed to GitHub Pages using GitHub Actions when changes are pushed to the main branch. The workflow:

1. Sets up Python
2. Runs the build script
3. Deploys generated files to GitHub Pages

## License

MIT
