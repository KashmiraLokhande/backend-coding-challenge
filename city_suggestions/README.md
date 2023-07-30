# City Suggestions API Documentation
The City Suggestions API is a RESTful web service that provides auto-complete suggestions for large cities. It allows users to search for cities based on partial or complete search terms. The API returns a list of scored suggested matches, sorted by descending score, to help users find the most relevant cities.
#Requirements
To run the City Suggestions API, you need the following installations:

1. Python: The programming language used for building the API.
2. Django: The web framework used to create the API endpoints and handle HTTP requests.
3. PostgreSQL: The relational database used to store city data.
4. psycopg2: A Python library used to connect Django with PostgreSQL.
5. PostGIS: An extension for PostgreSQL that adds support for geographic objects and allows for spatial queries.

#Installation Steps
1. Install Python: You can download Python from the official website (https://www.python.org/) and follow the installation instructions for your operating system.

2. Install Django: Once Python is installed, open a terminal or command prompt and run the following command to install Django:

```
pip install django
```
3. Install PostgreSQL and PostGIS: Download and install PostgreSQL and PostGIS from their official websites (https://www.postgresql.org/ and https://postgis.net/). During the installation, set up a username and password for the PostgreSQL database.

4. Install psycopg2: After installing PostgreSQL, you can install psycopg2 using pip:

```
pip install psycopg2
```
#API Endpoint
The API endpoint for city suggestions is exposed at /suggestions. It accepts HTTP GET requests with query parameters to perform the search.

#Parameters
The API supports the following query parameters:

    - q: (Required) The search term for the city name. It can be a partial or complete city name.
    - latitude: (Optional) The latitude of the caller's location. Providing latitude and longitude will help improve the relevance of the suggestions.
    - longitude: (Optional) The longitude of the caller's location. Providing latitude and longitude will help improve the relevance of the suggestions.
#Response Format
The API response is a JSON object with an array of suggested cities:

```json
{
  "suggestions": [
    {
      "name": "City Name, Country Code",
      "latitude": "City Latitude",
      "longitude": "City Longitude",
      "score": "Suggestion Score"
    },
    ...
  ]
}
```

    * name: The name of the city along with its country code. For example, "London, CA" represents London in Canada.
    * latitude: The latitude of the city's location.
    * longitude: The longitude of the city's location.
    * score: A floating-point value between 0 and 1 (inclusive) indicating the confidence in the suggestion. Higher scores indicate more relevant matches.

#Scoring Algorithm
The scoring algorithm considers both the similarity of the city name with the search query and, if provided, the distance between the city and the caller's location.

1. If the search query exactly matches the city name, the suggestion receives the highest score of 1.0.

2. If the search query is a prefix of the city name, the suggestion receives a high score of 0.7.

3. If the search query is present anywhere in the city name, the suggestion receives a moderate score of 0.5.

4. If the search query is not present in the city name, the suggestion receives a lower score of 0.0.

5. If latitude and longitude are provided, an additional score of 0.1 is added to the suggestion if the city name contains the search query. The suggestion's score is further adjusted based on the distance between the city and the caller's location. The closer the city, the higher the score.

#Sample output
Near Match
<http://127.0.0.1:8000/suggestions?q=Londo&latitude=43.70011&longitude=-79.4163>

```json
{
  "suggestions": [
    {
      "name": "London, ON, Canada",
      "latitude": "42.98339",
      "longitude": "-81.23304",
      "score": 0.9
    },
    {
      "name": "London, OH, USA",
      "latitude": "39.88645",
      "longitude": "-83.44825",
      "score": 0.5
    },
    {
      "name": "London, KY, USA",
      "latitude": "37.12898",
      "longitude": "-84.08326",
      "score": 0.5
    },
    {
      "name": "Londontowne, MD, USA",
      "latitude": "38.93345",
      "longitude": "-76.54941",
      "score": 0.3
    }
  ]
}
``` 

No Match
<http://127.0.0.1:8000/suggestions?q=SomeRandomCityInTheMiddleOfNowhere>

```json
{
  "suggestions": []
}
```

#Implementation Details
The City Suggestions API is built using Python and Django, a web framework for rapid development and clean design. The database used is PostgreSQL. The API leverages the Haversine formula to calculate the distance between two sets of coordinates for scoring suggestions based on location.

#Unit Tests
The API includes a comprehensive set of unit tests to ensure the correctness of its functionality. The tests cover various scenarios, including exact matches, prefix matches, moderate matches, and suggestions with and without latitude and longitude.

#Workflow
1. Forked the given repository and cloned it to the local machine.
2. Created a Django project named "city_suggestions" and an app named "suggestions_app" to handle the API logic.
3. Configured the app's URLs to define the endpoint for the API.
4. Defined the City model in the app's models to represent the city data.
5. Migrated the database to create the required table for city data.
6. Created a folder management/command and inside that folder created  load_data file to load data from the given TSV file into the database.
7. Loaded data into the database using the load_data file.
8. Implemented the API logic in the views file to handle the suggestions search based on the query parameters.
9. Utilized a utils file to include functions for calculating scores and distances.
10. Created unit tests in the tests file to ensure the correctness of the API's behavior.
11. Run the Django development server to test the API.

Overall, the City Suggestions API is designed to be clean, maintainable, and extensible. It uses best practices in web development and employs proper unit testing for quality assurance. The API helps users find relevant city suggestions based on their search queries and, if available, their current location.




