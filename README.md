# python_sraper_NG2
Google Maps scraping starter for Northern Virginia death-care lead generation.

## Recommended Google search keywords
For the **death-care / funeral sector**, these are the most useful search terms:

- `funeral home in Fairfax County, Virginia`
- `cremation service in Fairfax County, Virginia`
- `mortuary in Fairfax County, Virginia`
- `cemetery in Fairfax County, Virginia`
- `memorial park in Fairfax County, Virginia`
- `direct cremation in Fairfax County, Virginia`
- `funeral director in Northern Virginia`

### Are these all the same industry?
They are in the broader **death-care industry**, but not identical segments:

- **Funeral homes / mortuaries** = service providers for arrangements, viewings, ceremonies.
- **Cremation services** = can be part of funeral homes or standalone operators.
- **Cemeteries / memorial parks** = burial property operators (sometimes separate ownership).
- **Dormitorium** is not a common U.S. business category label; in English-language local search it usually performs worse than "mortuary," "funeral home," or "cremation service."

## How many companies can you expect in Fairfax + broader Northern Virginia?
Practical expectation:

- **Fairfax County only**: ~30–80 relevant businesses depending on keyword mix.
- **Broader Northern Virginia** (Fairfax, Arlington, Alexandria, Loudoun, Prince William): often **100+** records when combining keywords and de-duplicating.

## Script
`funeral_google_scraper_Feb2026.py` runs Playwright against Google Maps and exports:

- company name
- category
- phone number
- address/location
- website
- query used

Output file: `funeral_results.csv`

## Install
```bash
pip install playwright
python -m playwright install chromium
```

## Run
```bash
python funeral_google_scraper_Feb2026.py
```

## Important note
Google Maps scraping can violate Google's Terms of Service depending on usage.
For production/commercial use, consider Google Places API or licensed business data providers.
