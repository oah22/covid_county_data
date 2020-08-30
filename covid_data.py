"""Takes covid county data and census data and output csv file.

Examples:

"""
import logging

import click
import pandas as pd
import requests


def dl_file(input_url: str, output_file: str):
    """Download file and save to output
    Args:
        input_url: file url
        output_file: save file to path
    """
    try:
        resp = requests.get(input_url, allow_redirects=True)
        with open(output_file, 'wb') as fd:
            fd.write(resp.content)
    except Exception as exc:
        logging.exception("unable to download %s, %s", input_url, exc)
        return None
    return output_file


def combine_covid_data(county_data: str, census_data: str):
    """Create final table with this schema:
         population: population,
         case: daily cases,
         deaths: daily deaths,
         cumulative_cases: cumulative cases to date, and
         cumulative_deaths: cumulative death

    Args:
        county_data:
        census_data:

    Effects: Writes to CSV
    Return: None
    """
    # load dataframe
    #
    df1 = None
    df2 = None

    try:
        df1 = pd.read_csv(county_data, dtype={"fips": str})
        df2 = pd.read_csv("data/co-est2019-alldata.csv",
                          encoding="latin-1", dtype={"STATE": str, "COUNTY": str})
    except Exception as exc:
        logging.warning("unable to load df: %s", str(exc))
        return
    logging.info("processing population data: %s, %s", len(df2), len(df2.columns))
    # FIPS 6-4 used the 2 digits FIPS state code followed by 3 digits county
    df2["fips"] = df2["STATE"] + df2["COUNTY"]
    # use POPESTIMATE2019 as population
    pop_df = df2[["fips", "POPESTIMATE2019"]]
    pop_df = pop_df.rename(columns={"POPESTIMATE2019": "population"})

    logging.info("processing county data %s", len(df1))
    # groupby and aggregate cases, deaths
    # cols = ["fips", "date", "county", "state"]
    cols = ["fips", "date"]
    group_fin_df = df1.groupby(cols, as_index=False).agg(
        {"cases": "sum", "deaths": "sum"}
    )

    logging.info("creating cumulative sums")
    # get cumulative sum in separate df
    cumsum_df = group_fin_df.groupby(["fips"]).agg(
        {"cases": "cumsum", "deaths": "cumsum"})
    group_fin_df["cumulative_cases"] = cumsum_df["cases"]
    group_fin_df["cumulative_deaths"] = cumsum_df["deaths"]

    group_fin_df = group_fin_df.rename(columns={"deaths": "daily_deaths"})

    # do join on census data and population data on column fips
    # res_df = pd.merge(group_fin_df, pop_df, on="fips", how="left")
    res_df = pd.merge(pop_df, group_fin_df, on="fips", how="right")
    logging.info("sample data: count: %s \n%s", len(res_df), res_df.head(10))
    return res_df


@click.command()
@click.option("--covid_data", default="data/us-counties.csv", help="Path to covid data")
@click.option("--census_data", default="data/co-est2019-alldata.csv", help="Path to census data")
@click.option("--output", default="covid_population.csv", help="Path to output file")
@click.option("--csv_out", default=True, help="Write to CSV or print sample")
@click.option("--download", "-d", is_flag=True, help="Download from url")
@click.option("--verbose", is_flag=True, help="More logging messages")
# pylint: disable=R0913
def main(covid_data="", census_data="", output="", csv_out=True, download=False, verbose=False):
    """Takes covid county data and census data, process, and output csv file.
    Examples:

    $ python covid_data.py --covid_data data/us-counties.csv \\
        --census_data data/co-est2019-alldata.csv --output res.csv
    """
    # Above is used by click help
    """Main function that uses click for option handling
    Args:
        covid_data: covid input file or url
        census_data: census input file or url
        output: output csv
        csv_out: csv output or print sample
        download: download the files
        verbose: verbose usage
    Effects: Write out file or print
    Return: None
    """
    if verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    else:
        logging.getLogger().setLevel(logging.INFO)
    df = pd.DataFrame()
    if download:
        dl_covid = dl_file(covid_data, "dl-us-counties.csv")
        dl_census = dl_file(census_data, "dl-census-est2019.csv")
        if dl_covid and dl_census:
            df = combine_covid_data(dl_covid, dl_census)
        else:
            logging.error("ERROR: download url: %s, %s",
                          covid_data, census_data)
    else:
        logging.info("processing data")
        df = combine_covid_data(covid_data, census_data)
    if csv_out:
        logging.info("writing output file %s", output)
        df.to_csv(output, index=False)
    else:
        logging.warning("non csv output not supported")
        print("sample data table\n%s", str(df.head(100)))

    return 0


if __name__ == "__main__":
    main()
