from dataflows import Flow, load, dump_to_path, dump_to_zip, printer, add_metadata, duplicate, deduplicate, set_primary_key, select_fields, sort_rows, filter_rows, unpivot


def select_vaccination_rows(row):
    if row["total_vaccinations"] != None and row["date"] != None:
        return True
    return False

def vaccination_data_total_csv():
    flow = Flow(
        # Load inputs
        load('https://raw.githubusercontent.com/maekke/vaccination_data/master/vaccination_data_total.csv', format='csv', ),
        # Save the results
        add_metadata(
            name='ch-vaccinations', 
            title='Total vaccinations for Switzerland',
            description='A simple Data Package Wrapper for the cantonal vaccination data as published by the cantons and scraped by Markus Meier.',
            sources=[{"title":"Markus Meier Github Scraper/Kantone","path":"https://github.com/maekke/vaccination_data"}],
            contributors=[{"role":"maintainer","title":"Thorben Westerhuys"}],
            # views=[{"name":"total-vaccinations","title":"Total Vaccinations Switzerland","resources":["vaccinations_latest"],"specType":"simple","spec":{"type":"line","group":"date","series":["VS","BE","GE","GL","GR","SO","ZG","ZH","AG","AR","AI","LU","LU","BL","BS","UR","SZ","OW","NW","FR","SH","TG","TI","NE","SG","JU","VD"]}}]
        ),
        duplicate(
            source='vaccination_data_total',
            target_name='vaccinations_latest',
        ),
        select_fields(
            fields=["canton","date","first_doses","second_doses","total_vaccinations","source"],
            resources='vaccinations_latest',
        ),
        filter_rows(
            condition=select_vaccination_rows,
            resources='vaccinations_latest',
        ),
        sort_rows(
            "date", resources='vaccinations_latest', reverse=True
        ),
        # printer(tablefmt="github"),
        dump_to_path('data'),
    )
    flow.process()


if __name__ == '__main__':
    vaccination_data_total_csv()