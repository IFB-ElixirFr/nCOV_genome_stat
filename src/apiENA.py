from datetime import date, timedelta, datetime
from pprint import pprint

import requests, re
import json



def get_nb_submits_days(country_names=None, days=30):
    ###################################################################################################################
    # Date part
    ###################################################################################################################

    end_date = date.today()
    start_date = end_date - timedelta(days=days)
    delta = end_date - start_date  # as timedelta

    # Dico creation
    dates = dict()
    for i in range(delta.days + 1):
        day = start_date + timedelta(days=i)
        dates[day.strftime("%Y-%m-%d")] = []

    ###################################################################################################################
    # Request
    ###################################################################################################################
    # if country_names:
        # r = requests.get(f'https://www.ebi.ac.uk/ena/portal/api/search?result=sample&query=tax_eq(2697049)%20AND%20country={country_names}%20AND%20first_public>={start_date}%20AND%20first_public<={end_date}&sortFields=first_public&fields=country,first_public&limit=0&format=json')
    # else:
    r = requests.get(f'https://www.ebi.ac.uk/ena/portal/api/search?result=sample&query=tax_eq(2697049)%20AND%20first_public>={start_date}%20AND%20first_public<={end_date}&sortFields=first_public&fields=country,first_public&limit=0&format=json')

    if not r and not r.json():
        return False, False

    ena_results = r.json()

    ###################################################################################################################
    # Data treatment
    ###################################################################################################################

    countriesList = dict()
    for item in ena_results:
        c = item['country'].split(":")[0]
        c = c.lower()
        if c not in countriesList:
            countriesList[c] = 1
        else:
            countriesList[c] = countriesList[c] + 1

        if item['first_public'] not in dates:
            if country_names:
                x = re.search(country_names, item['country'], re.IGNORECASE)
                if x:
                    dates[item['first_public']] = [item['country']]
            else:
                dates[item['first_public']] = [item['country']]
        else:
            if country_names:
                x = re.search(country_names, item['country'], re.IGNORECASE)
                if x:
                    dates[item['first_public']].append(item['country'])
            else:
                dates[item['first_public']].append(item['country'])

    with open('home/static/data/countries.geojson') as f:
        data = json.load(f)

    for index in range(len(data['features'])):
        data['features'][index]['properties']['submissions'] = 0

    for c in countriesList :
        if c != "":
            pos = next((index for index,item in enumerate(data['features']) if item['properties']['ADMIN'].lower() == c), None)
            if pos:
                data['features'][pos]['properties']['submissions'] = countriesList[c]

    return list(dates.keys()), [len(dates[x]) for x in dates if isinstance(dates[x], list)], countriesList, data

if __name__ == '__main__':
    days, submits, subByCountries, map = get_nb_submits_days(days=10)
    pprint(map['features'][0])

