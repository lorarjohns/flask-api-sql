# The Readership Ranking API
##

## Why rank articles?

Ranking articles by counting how many times each was "read" (or at least clicked on) by a unique visitor gives a straightforward overall picture of the _Times_ readership. Breaking that count down into topic sections begins to give us a more nuanced picture.

When we can add individual people's reading preferences into the analysis, though, the data can bring latent relationships to the fore. Besides knowing what any one person likes to read, we can discover sub-clusters of "reading clubs"---readership segments that don't map neatly to any preconceived categories. 

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

 Because of the limitations of `sqlite3`, the queries in this database are written using Python string interpolation. While it is not likely that these specific queries would be vulnerable to SQL injection, better practice would be to use an ORM framework like SQLAlchemy as an interface. I have mocked up database models but did not build out the entire Postgres/SQLAlchemy infrastructure, which would be a potential next step.

