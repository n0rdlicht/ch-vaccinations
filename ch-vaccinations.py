from dataflows import Flow, load, dump_to_path, dump_to_zip, printer, add_metadata, duplicate, deduplicate, set_primary_key, select_fields, sort_rows, filter_rows


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
            sources=[{"title":"Markus Meier/Github","url":"https://github.com/maekke/vaccination_data"}],
            contributors=[{"role":"maintainer","title":"Thorben Westerhuys"}]
        ),
        duplicate(
            source='vaccination_data_total',
            target_name='vaccinations_latest',
        ),
        select_fields(
            fields=["canton","date","first_doses","second_doses","total_vaccinations","source"]
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