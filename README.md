# The Readership Ranking API

## Usage

This API is built using Python and Flask. It can be run in Docker from this directory using the following instructions.

To run the app:

0. Checkout git branch `johns-api`.
1. Run `sh run_app.sh` to build the Docker image and start the server. The app will be running locally on `http://0.0.0.0:5000`.
2. Then, run `python test_api.py` to view a demo of the API on the test data given in the assignment.

Other ways you may want to interact with the container:

3.  To attach to the container in a bash shell, run `docker exec -it flask-app /bin/sh`. From here, you can also run `python test_api.py` directly. To exit the interactive shell, press `CTRL+P CTRL+Q`.
4. To stop the container, run `docker stop flask-app`. To restart the container, run `docker start flask-app`.
5. To force remove the container, run `docker rm -f flask-app`.
6. To run the app in debug mode, run `docker run --name flask-app -p 5000:5000 -v $(pwd):/app/ -it flask-app`.
7. To stop the container, press `CTRL+C`.

## Structure of the API
As a prerequisite to building that graph of knowledge, we need the basics. This API provides an **article ranking endpoint** for two sets of data:
- NYTimes article data
- (fake) user reading history 

Specifically, the following three endpoints can be accessed. Please run `python test_api.py` for a demo of all three.

### `GET /healthcheck`

_parameters:_ _None_

This endpoint simply returns a status check for the server.

### `GET /stats/section`

_parameters:_ `user_id` (e.g. `u:012345`)

This request returns the number of unique articles a given user has read per section ('arts', 'world', 'science', etc.)

### `POST /rank/section`

_parameters_: `content_ids` (list of article ids)

Passing a list of article ids to this endpoint produces a ranking of those articles in order of a user's most frequently read sections.

If an article ID exists in the database but the given user has not read it, the endpoint uses aggregate section popularity as a fallback ranking.

## Tests

As noted, you can run the following tests by invoking `python test_api.py`.

### `/stats/section` test

@param input: /stats/section?user_id=u:0eccf48d721e
@returns: {"health": 15, "sports": 9, "style": 10, "upshot": 12, "world": 35}

@param input:  /stats/section?user_id=u:e6f4cc3ba334
@returns:  {"business": 32, "dining": 14, "education": 13, "health": 7, "science": 24, "technology": 9, "upshot": 6, "us": 21, "world": 41}

### `/rank/section test`

 @param input: `/rank/section?user_id=u:0eccf48d721e`
 @param input: `[
        'c2806f15-9b98-4bbc-b66a-13d131f63aac',
        '9728ca66-54a3-4229-adf2-70dbbfed5049',
        '675da7be-ac22-49f1-b4ba-b967abdd819e',
        'ed8d04f8-d103-4c02-ab35-55902fdf9f6d',
        'af56c5dd-fddc-4fe5-b0b7-2b74d951ec0b',
        '1bce63f2-f3c4-4f9e-9491-45d1c4aaec02',
        '9a1f8fb9-19ec-4451-aee8-d3a0e9dcfb30']`
@returns: `{"content_ids": ["1bce63f2-f3c4-4f9e-9491-45d1c4aaec02",
                 "675da7be-ac22-49f1-b4ba-b967abdd819e",
                 "9a1f8fb9-19ec-4451-aee8-d3a0e9dcfb30",
                 "9728ca66-54a3-4229-adf2-70dbbfed5049",
                 "af56c5dd-fddc-4fe5-b0b7-2b74d951ec0b",
                 "ed8d04f8-d103-4c02-ab35-55902fdf9f6d"]}`

## Data

Two data files (included in this repo) form the basis of the endpoints: `article_data.csv` and `user_history.csv`.

**`article_data.csv`** is a CSV file with the following columns: `content_id`, `section`, `title`, `url`. There are roughly 500-600 articles included in this file and represent NYTimes articles from late 2019 and early 2020.

**`user_history.csv`** is a CSV file with the following columns: `user_id`, `content_id`. This file represents some fake users and corresponding articles they have "read". The user_ids are synthetic and were randomly generated. Their corresponding articles attached to thm were also auto-generated, and so they don't represent real reading patterns of any actual people.

## Why rank articles?

Ranking articles by counting how many times each was "read" (or at least clicked on) by a unique visitor gives a straightforward overall picture of the _Times_ readership. Breaking that count down into topic sections begins to give us a more nuanced picture.

When we can add individual people's reading preferences into the analysis, though, the data can bring latent relationships to the fore. Besides knowing what any one person likes to read, we can discover sub-clusters of "reading clubs"---readership segments that don't map neatly to any preconceived categories. 

## Motivations

1. Versatility

For purposes of this assignment, I wanted to build a prototype that did not have too many exotic dependencies and could be scaled or adapted. To that end, I used Flask-RESTful as a framework for API design. Since the design follows RESTful principles, I could easily convert this API to a YAML Swagger specification and reconfigure it to work in a different programming language or framework.

2. Ubiquity

 I chose to use SQL for the core logic of the program for two main reasons. As SQL is the 'skinny waist' of data science, it isn't possible to turn raw data into refined information without knowing how to use it. While it's not a large-scale overall solution, `sqlite3` is part of the Python standard library; fast and lightweight; and easy to set up, all of which made it a good choice for fulfilling the explicit requirements of this assignment.

  Similarly, the entire application runs in Docker, to minimize setup effort and maximize portability.

 3. Extensibility

 I wanted to use concepts and tools that could be adapted to more data and would integrate well with machine learning components later on. To that end, I either tried to incorporate such design directly or, where that wasn't immediately feasible, to make a note of what future challenges we might encounter.

 ## Challenges and further development

 1. Known issues
 
 This is a prototype, so it doesn't have as much testing or as much robustness to real-life use as a production server should. Specifically, I would prioritize handling malformed user input and best-practice handling of cases in which no data is found. 

 Because of the limitations of `sqlite3`, the queries in this database are written using Python string interpolation. While it is not likely that these specific queries would be very vulnerable to SQL injection, better practice would be to use an ORM framework like SQLAlchemy as an interface. I have mocked up database models but did not build out the entire Postgres/SQLAlchemy infrastructure, which would be a good potential next step.

 The instructions weren't explicit about the ranking choice to make when there is no section tie, but a user has read _no_ articles in a section. In that case, I have ranked the article with more overall views higher (similarly to the logic for breaking category ties). While this is possible in SQL alone, not all versions of sqlite have window function capability (my native installation on Ubuntu LTS does not, for instance. To clarify my thought process and to make the program easier to read and debug, I rewrote the logic in Python.

2. Further development

I collected additional metadata from the New York Times Articles API using the URLs in the article_data csv. For building a collaborative filtering or graph algorithm to recommend content or segment user groups, we could leverage additional information from this data such as: 

- word count 
- byline
- human-engineered geographic and descriptive facets
- machine-learned latent facets
- dates and days of publication
- subsection
- abstract
- images and captions
- sentiment scores

Together with individualized user reading preference data, such features would allow for a marriage of collaborative filtering, which is based on data harvested from the individual use patterns of other users, and content-based recommendation, which focuses more on the aggregate characteristics of the articles. Either one alone might create a bias that drowns out interesting articles in the long tail of the distribution, but together enable recommending relevant but "surprising" and interesting content.