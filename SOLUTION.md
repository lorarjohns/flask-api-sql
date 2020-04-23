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

1. Simplicity

For purposes of this assignment, I wanted to build a prototype that did not have too many exotic dependencies and could be scaled or adapted. To that end, I used Flask-RESTful as a framework for API design. Since the design follows RESTful principles, I could easily convert this API to a YAML Swagger specification and reconfigure it to work in a different programming language or framework.



demonstrated how I think more than what code I can copy from Stack Exchange.