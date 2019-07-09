# AdjustHomeTask

### Setup


All the requirements have been described in `requirements.txt`. Initial requirements include:

- Django
- Django Rest Framework
- Postgres

The application uses Postgres for the database by default. Which will need to be running on localhost. Set up the db with the following

    psql -U postgres -c "create user adjust with password 'adjust';"
    psql -U postgres -c "alter user adjust with superuser"
    psql -U postgres -c "alter user adjust with createdb"
    psql -U postgres -c "alter user adjust with login"
    psql -U postgres -c "create database adjust with owner adjust;"

Install application requirements

    pip install -r requirements.txt
    
    
Migrate the database before the first run

    python manage.py migrate

Create a superuser

    python manage.py createsuperuser

Loading initial data for project

    python manage.py load_sample_data

### Running the application

    python manage.py runserver
    
The application should be visible at `localhost:8000/` after that


### Running test

    python manage.py test


## API Documentation

Authenticate yourself by visiting `localhost:8000/admin/`, where you will be prompted for a username and password

The endpoint is located at `localhost:8000/metrics/`, after authentication.
For the sake of performance, the API is paginated.

### 1. Filtering

Filter the results by specifying any of the Metric columns as query params. i.e. To filter by 'os' your would perform a `GET` request such as:
    
    localhost:8000/metrics/?os=android
    
To filter by several fields, add more query params. For example:

    http://localhost:8000/metrics/?os=android&country=GB&date_from=2017-05-17
    

**Additionally you can specify `date_from` and `date_to` which are valid query parameters**
  
The result will be a JSON response in the shape of:

```
{
    "count": 126,
    "next": "http://localhost:8000/metrics/?country=GB&date_from=2017-05-17&limit=100&offset=100&os=android",
    "previous": null,
    "results": [
        {
            "id": 2216,
            "cpi": "2.000",
            "date": "2017-05-17",
            "channel": "chartboost",
            "country": "GB",
            "os": "android",
            "impressions": 3210,
            "clicks": 117,
            "installs": 18,
            "spend": "36.0",
            "revenue": "59.60"
        },
        {
            "id": 2224,
            "cpi": "4.220",
            "date": "2017-05-17",
            "channel": "facebook",
            "country": "GB",
            "os": "android",
            "impressions": 6358,
            "clicks": 196,
            "installs": 20,
            "spend": "84.4",
            "revenue": "20.00"
        },
        ...
    }

```


### 2. Ordering

You can order the results by sending a query param named 'ordering' and specifying any of the Metric columns as the value. i.e. To order by 'date' your would perform a `GET` request such as:
    
    localhost:8000/metrics/?ordering=android
    
To order by several fields, separate the field names by a comma (,). For example:

    localhost:8000/metrics/?ordering=date,country
    
You can order in descending order by putting a `-` before the column name, for example:

    localhost:8000/metrics/?ordering=-date,country

The result will be a JSON response in the shape of:

```
{
    "count": 1096,
    "next": "http://localhost:8000/metrics/?limit=100&offset=100&ordering=-date%2Ccountry",
    "previous": null,
    "results": [
        {
            "id": 3293,
            "cpi": "2.000",
            "date": "2017-06-15",
            "channel": "unityads",
            "country": "CA",
            "os": "ios",
            "impressions": 3410,
            "clicks": 101,
            "installs": 19,
            "spend": "38.0",
            "revenue": "10.00"
        },
        {
            "id": 3278,
            "cpi": "2.067",
            "date": "2017-06-15",
            "channel": "facebook",
            "country": "CA",
            "os": "android",
            "impressions": 3456,
            "clicks": 93,
            "installs": 18,
            "spend": "37.2",
            "revenue": "20.00"
        },
        ...
    }

```

### 3. Grouping

You can group the results by sending a query param named 'grouping' and specifying any of the Metric columns as the value. i.e. To group by 'os' your would perform a `GET` request such as:
    
    localhost:8000/metrics/?grouping=os
    
To group by several columns, separate the column names by a comma (,). For example:

    localhost:8000/metrics/?grouping=channel,country

The result will be a JSON response in the shape of:  
    
```
{
    "count": 25,
    "next": null,
    "previous": null,
    "results": [
        {
            "channel": "facebook",
            "country": "CA",
            "cpi": 2.0748663101604277,
            "impressions": 99126,
            "clicks": 2910,
            "installs": 561,
            "spend": 1164.0,
            "revenue": 1928.0
        },
        {
            "channel": "unityads",
            "country": "CA",
            "cpi": 2.0,
            "impressions": 198767,
            "clicks": 6822,
            "installs": 1321,
            "spend": 2642.0,
            "revenue": 3579.6
        },
        ...
    }

```

The `impressions`, `clicks`, `installs`, `spend`, `revenue` fields will be summed returned.


### 4. Applying all filters

Any combination of grouping, filtering and ordering can be applied.

An example request with all 3 would be 

    localhost:8000/metrics/?date_to=2017-06-01&grouping=channel,country&ordering=-clicks
    
This would return the number of impressions and clicks that occurred before the 1st of June 2017, broken down by channel and country, sorted by clicks in descending order

```
{
    "count": 25,
    "next": null,
    "previous": null,
    "results": [
        {
            "channel": "adcolony",
            "country": "US",
            "cpi": 1.624617294166322,
            "impressions": 532608,
            "clicks": 13089,
            "installs": 2417,
            "spend": 3926.7,
            "revenue": 6485.94
        },
        {
            "channel": "apple_search_ads",
            "country": "US",
            "cpi": 2.0,
            "impressions": 369993,
            "clicks": 11457,
            "installs": 2235,
            "spend": 4470.0,
            "revenue": 7432.99
        },
        ...
    }

```
