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

$ python covid_data.py --covid_data data/us-counties.csv --census_data data/co-est2019-alldata.csv --output res.csv
INFO:root:processing data
INFO:root:processing population data: 3193, 164
INFO:root:processing county data 473026
INFO:root:creating cumulative sums
INFO:root:sample data: count: 468468
    fips  population        date  cases  daily_deaths  cumulative_cases  cumulative_deaths
0  01001     55869.0  2020-03-24      1             0                 1                  0
1  01001     55869.0  2020-03-25      4             0                 5                  0
2  01001     55869.0  2020-03-26      6             0                11                  0
3  01001     55869.0  2020-03-27      6             0                17                  0
4  01001     55869.0  2020-03-28      6             0                23                  0
5  01001     55869.0  2020-03-29      6             0                29                  0
6  01001     55869.0  2020-03-30      7             0                36                  0
7  01001     55869.0  2020-03-31      7             0                43                  0
8  01001     55869.0  2020-04-01     10             0                53                  0
9  01001     55869.0  2020-04-02     10             0                63                  0
INFO:root:writing output file res.csv

```

## Download new data from github and census website

```sh
python covid_data.py --covid_data https://raw.githubusercontent.com/nytimes/covid-19-data/master/us-counties.csv --census_data https://www2.census.gov/programs-surveys/popest/datasets/2010-2019/counties/totals/co-est2019-alldata.csv --download

INFO:root:processing population data: 3193, 164
INFO:root:processing county data 479494
INFO:root:creating cumulative sums
INFO:root:sample data: count: 474874
    fips  population        date  cases  daily_deaths  cumulative_cases  cumulative_deaths
0  01001     55869.0  2020-03-24      1             0                 1                  0
1  01001     55869.0  2020-03-25      4             0                 5                  0
2  01001     55869.0  2020-03-26      6             0                11                  0
3  01001     55869.0  2020-03-27      6             0                17                  0
4  01001     55869.0  2020-03-28      6             0                23                  0
5  01001     55869.0  2020-03-29      6             0                29                  0
6  01001     55869.0  2020-03-30      7             0                36                  0
7  01001     55869.0  2020-03-31      7             0                43                  0
8  01001     55869.0  2020-04-01     10             0                53                  0
9  01001     55869.0  2020-04-02     10             0                63                  0
INFO:root:writing output file covid_population.csv
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
INFO:root:processing county data 473026
INFO:root:creating cumulative sums
INFO:root:sample data: count: 468468
    fips  population        date  cases  daily_deaths  cumulative_cases  cumulative_deaths
0  01001     55869.0  2020-03-24      1             0                 1                  0
1  01001     55869.0  2020-03-25      4             0                 5                  0
2  01001     55869.0  2020-03-26      6             0                11                  0
3  01001     55869.0  2020-03-27      6             0                17                  0
4  01001     55869.0  2020-03-28      6             0                23                  0
5  01001     55869.0  2020-03-29      6             0                29                  0
6  01001     55869.0  2020-03-30      7             0                36                  0
7  01001     55869.0  2020-03-31      7             0                43                  0
8  01001     55869.0  2020-04-01     10             0                53                  0
9  01001     55869.0  2020-04-02     10             0                63                  0
INFO:root:writing output file res.csv
```

## Cleaning and Transformation

- covid_data dataframe
    1. aggregate cases, deaths with sum by fips and date (groupby)
    2. create another dataframe with aggregation/cumulative sum for cases and deaths (groupby fips)
    3. rename the columns to cumulative_cases and cumulative_deaths
    4. add the cumulative columns to first dataframe covid_data
    5. results is groupby dataframe

- census_data dataframe
    0. load census file as dataframe using latin-1 encoding
    1. create fips column by multiplying state fips 1000 plus county fips
    2. select fips and POPESTIMATE2019
    3. rename POPESTIMATE2019 column to population
    4. this is called population dataframe

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