#!/usr/bin/env python3
import json
from datetime import datetime
from pathlib import Path

DATA_FILE = Path(__file__).with_name('amd_data.json')


def parse_date(s):
    if not s:
        return None
    for fmt in ("%Y-%m-%d", "%Y-%m-%dT%H:%M:%S"):
        try:
            return datetime.strptime(s, fmt).date()
        except Exception:
            continue
    return None


def main():
    data = json.loads(DATA_FILE.read_text())
    facts = data.get('facts', {})
    usgaap = facts.get('us-gaap', {})
    net = usgaap.get('NetIncomeLoss') or usgaap.get('NetIncomeLossAvailableToCommonStockholdersBasic') or usgaap.get('NetIncomeLossAvailableToCommonStockholdersDiluted')
    if not net:
        print('Net income field not found in data')
        return

    units = net.get('units', {})
    # pick USD if available, else the first currency
    currency = 'USD' if 'USD' in units else next(iter(units.keys()), None)
    if not currency:
        print('No units found for Net Income')
        return

    entries = units[currency]

    # choose best entry per fiscal year (prefer latest filed date)
    best = {}
    for e in entries:
        fy = e.get('fy')
        if fy is None:
            continue
        fp = e.get('fp')
        # prefer full-year entries; still accept others if FY not present
        if fp != 'FY':
            # we'll still consider non-FY only if no FY exists for year
            pass

        filed = parse_date(e.get('filed') or e.get('end'))
        prev = best.get(fy)
        if prev is None:
            best[fy] = (filed, e.get('val'))
        else:
            prev_filed = prev[0]
            # if current has a later filed date, replace
            if filed and (not prev_filed or filed > prev_filed):
                best[fy] = (filed, e.get('val'))

    # print yearly values sorted by year
    for year in sorted(best.keys()):
        val = best[year][1]
        print(f"{year}: {val}")


if __name__ == '__main__':
    main()


"""
Output:
2012: 471000000
2013: 491000000
2014: -1183000000
2015: -83000000
2016: -403000000
2017: -660000000
2018: -498000000
2019: -33000000
2020: 337000000
2021: 341000000
2022: 2490000000
2023: 3162000000
2024: 1320000000
2025: 1159000000

Not bad!  But dates shifted around a bit.
"""
