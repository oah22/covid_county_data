# Purpose

This script would allow the user to load covid data and census data and output to CSV file.

## Dependent Packages

The script uses python 3.8.5 and uses the following packages stored in requirements.txt.

```text

click==7.1.2
pandas==1.0.5
requests==2.21.0

```

## Quick Setup on MAC

If you are running on MAC, then you can use these instructions, but it will add the exact packages.

```sh

brew install python
pip install -r requirements.txt

```

## Quick Run

```sh

$ python covid_data.py --covid_data data/us-counties.csv --census_data data/co-est2019-alldata.csv --output res.csv
INFO:root:processing data
INFO:root:processing population data
INFO:root:processing county data
INFO:root:creating cumulative sums
INFO:root:sample data: count: 468468
   fips  population        date  cases  daily_deaths  cumulative_cases  cumulative_deaths
0  1001     55869.0  2020-03-24      1             0                 1                  0
1  1001     55869.0  2020-03-25      4             0                 5                  0
2  1001     55869.0  2020-03-26      6             0                11                  0
3  1001     55869.0  2020-03-27      6             0                17                  0
4  1001     55869.0  2020-03-28      6             0                23                  0
5  1001     55869.0  2020-03-29      6             0                29                  0
6  1001     55869.0  2020-03-30      7             0                36                  0
7  1001     55869.0  2020-03-31      7             0                43                  0
8  1001     55869.0  2020-04-01     10             0                53                  0
9  1001     55869.0  2020-04-02     10             0                63                  0
INFO:root:writing output file res.csv

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
INFO:root:processing population data
INFO:root:processing county data
INFO:root:creating cumulative sums
INFO:root:sample data: count: 468468
   fips  population        date  cases  daily_deaths  cumulative_cases  cumulative_deaths
0  1001     55869.0  2020-03-24      1             0                 1                  0
1  1001     55869.0  2020-03-25      4             0                 5                  0
2  1001     55869.0  2020-03-26      6             0                11                  0
3  1001     55869.0  2020-03-27      6             0                17                  0
4  1001     55869.0  2020-03-28      6             0                23                  0
5  1001     55869.0  2020-03-29      6             0                29                  0
6  1001     55869.0  2020-03-30      7             0                36                  0
7  1001     55869.0  2020-03-31      7             0                43                  0
8  1001     55869.0  2020-04-01     10             0                53                  0
9  1001     55869.0  2020-04-02     10             0                63                  0
INFO:root:writing output file res.csv
```

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