# Purpose

This script would allow the user to load covid data and census data and output to CSV file.
This loads static data from directory, and it can also download new data files.

## Dependent Packages

The script uses python 3.8.5 and uses the following packages stored in requirements.txt.

```text

click==7.1.2
pandas==1.0.5
requests==2.21.0

```

## Quick Setup on MAC

If you are running on MAC, then you can use these instructions, but it may the exact packages.

```sh

## clone repo
$ git clone https://github.com/oah22/covid_county_data.git
Cloning into 'covid_county_data'...
remote: Enumerating objects: 15, done.
remote: Counting objects: 100% (15/15), done.
remote: Compressing objects: 100% (13/13), done.
remote: Total 15 (delta 0), reused 15 (delta 0), pack-reused 0
Unpacking objects: 100% (15/15), 6.08 MiB | 1.62 MiB/s, done.

$ cd covid_county_data/

## install python and packages
$ brew install python
$ pip install -r requirements.txt

```

## Quick Run

This loads static data from directory. There is another option to download new data from web.

```sh

$ python3 covid_data.py --covid_data data/us-counties.csv --census_data data/co-est2019-alldata.csv --output results_daily.csv
INFO:root:processing data
INFO:root:processing population data: 3193, 164
INFO:root:processing county data 473026, 3203
INFO:root:creating diff columns
INFO:root:sample data: count: 701238
    fips        date  daily_cases  daily_deaths  cumulative_cases  cumulative_deaths
0  01001  2020-01-21          0.0           0.0                 0                  0
1  01001  2020-01-22          0.0           0.0                 0                  0
2  01001  2020-01-23          0.0           0.0                 0                  0
3  01001  2020-01-24          0.0           0.0                 0                  0
4  01001  2020-01-25          0.0           0.0                 0                  0
5  01001  2020-01-26          0.0           0.0                 0                  0
6  01001  2020-01-27          0.0           0.0                 0                  0
7  01001  2020-01-28          0.0           0.0                 0                  0
8  01001  2020-01-29          0.0           0.0                 0                  0
9  01001  2020-01-30          0.0           0.0                 0                  0
INFO:root:writing output file results_daily.csv

```

## Download new data from github and census website

```sh
python covid_data.py --covid_data https://raw.githubusercontent.com/nytimes/covid-19-data/master/us-counties.csv --census_data https://www2.census.gov/programs-surveys/popest/datasets/2010-2019/counties/totals/co-est2019-alldata.csv --download

INFO:root:processing population data: 3193, 164
INFO:root:processing county data 485962, 3204
INFO:root:creating diff columns
INFO:root:sample data: count: 714269
    fips        date  daily_cases  daily_deaths  cumulative_cases  cumulative_deaths
0  01001  2020-01-21          0.0           0.0                 0                  0
1  01001  2020-01-22          0.0           0.0                 0                  0
2  01001  2020-01-23          0.0           0.0                 0                  0
3  01001  2020-01-24          0.0           0.0                 0                  0
4  01001  2020-01-25          0.0           0.0                 0                  0
5  01001  2020-01-26          0.0           0.0                 0                  0
6  01001  2020-01-27          0.0           0.0                 0                  0
7  01001  2020-01-28          0.0           0.0                 0                  0
8  01001  2020-01-29          0.0           0.0                 0                  0
9  01001  2020-01-30          0.0           0.0                 0                  0
INFO:root:writing output file dl_results.csv
```

## Docker Setup in case your python installation has problems

```sh
$ docker-compose up  -d --build
Building covid_data
Step 1/11 : FROM python:3.8.5
 ---> 79cc46abd78d
...

$ docker exec -it covid_data bash
/app# python covid_data.py --covid_data data/us-counties.csv --census_data data/co-est2019-alldata.csv --output res.csv

INFO:root:processing data
INFO:root:processing population data: 3193, 164
INFO:root:processing county data 473026, 3203
INFO:root:creating diff columns
INFO:root:sample data: count: 701238
    fips        date  daily_cases  daily_deaths  cumulative_cases  cumulative_deaths
0  01001  2020-01-21          0.0           0.0                 0                  0
1  01001  2020-01-22          0.0           0.0                 0                  0
2  01001  2020-01-23          0.0           0.0                 0                  0
3  01001  2020-01-24          0.0           0.0                 0                  0
4  01001  2020-01-25          0.0           0.0                 0                  0
5  01001  2020-01-26          0.0           0.0                 0                  0
6  01001  2020-01-27          0.0           0.0                 0                  0
7  01001  2020-01-28          0.0           0.0                 0                  0
8  01001  2020-01-29          0.0           0.0                 0                  0
9  01001  2020-01-30          0.0           0.0                 0                  0
INFO:root:writing output file results_daily.csv

```

## Cleaning and Transformation

- covid_data dataframe
    1. reorder to fips, date, cases, deaths and drop state and country
    2. create another dataframe with aggregation/diff for cases and deaths (groupby fips)
    3. add groupby columns as daily_cases and daily_deaths
    4. rename cases, deaths to cumulative_cases, cumulative_deaths
    5. results is dates_df dataframe

- census_data dataframe
    0. load census file as dataframe using latin-1 encoding
    1. create fips column by multiplying state fips 1000 plus county fips
    2. select fips and POPESTIMATE2019
    3. rename POPESTIMATE2019 column to population
    4. results is pop_df dataframe

- join
    1. do a right join of population dataframe with groupby dataframe

- write to file
    1. write to output csv

## Help

```sh
$ python3 covid_data.py --help
Usage: covid_data.py [OPTIONS]

  Takes covid county data and census data, process, and output csv file.
  Examples:     $ python3 covid_data.py --covid_data data/us-counties.csv
  --census_data data/co-est2019-alldata.csv --output res.csv

Options:
  --covid_data TEXT   Path to covid data
  --census_data TEXT  Path to census data
  --output TEXT       Path to output file
  --csv_out TEXT      Write to CSV or print sample
  --download TEXT     Download from url
  --verbose TEXT      More logging messages
  --help              Show this message and exit.
```

```sh
```

## Structure

- Source code
  - covid_population.py

- Packages
  - requirements.txt

- Data
  - data/us-counties.csv
  - data/co-est2019-alldata.csv

- Config
  - pylintrc - linter config

- Docker Build Files
  - docker-compose.yml
  - Dockerfile
  - entrypoint.sh

## Download files

```sh

curl -LO https://www2.census.gov/programs-surveys/popest/datasets/2010-2019/counties/totals/co-est2019-alldata.csv
# iconv -f ISO-8859-1 -t UTF-8 data/co-est2019-alldata.csv > c.csv

```

## References

```sh
https://github.com/nytimes/covid-19-data/blob/master/README.md

- County Data
https://raw.githubusercontent.com/nytimes/covid-19-data/master/us-counties.csv

- Census Population
https://www.census.gov/data/datasets/time-series/demo/popest/2010s-counties-total.html

- Census Columns
https://www2.census.gov/programs-surveys/popest/technical-documentation/file-layouts/2010-2019/co-est2019-alldata.pdf

- Census Data
https://www2.census.gov/programs-surveys/popest/datasets/2010-2019/counties/totals/co-est2019-alldata.csv

```