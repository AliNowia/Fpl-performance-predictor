# FPL-Predictor

FPL-Predictor is a python software based on selenium library to collect data from fantasy premier league website (link: https://fantasy.premierleague.com/statistics).

This data is players' performance in the last 3 seasons (24/25, 23/24, 22/23) with purpose to predict their behavior this season.

Machine learning model is not yet integrated but will be soon.

## prerequisites

- Python
- Chrome Webdriver
- Selenium
- Pandas

```bash
pip install selenium
pip install pandas
```

## Usage
- Only one input: number of pages to scrape.
- Maximum: 23
- Minimum: 1
```bash
How many pages to collect data ? [1 - 23]
input: <your-input>
```

## Checklist (todo list)
- ✅ Web-scraping (collect data from site)
- ⏸️ Preprocessing
- ⏸️ Feature Engineering
- ⏸️ Machine learning model
