To better assess a candidate's development skills, we would like to provide the following challenge. You have as much time as you'd like (though we ask that you not spend more than a few hours). 

## Submission Instructions

1. You'll receive this repo as a .tar.gz file, which contains a git repo (.git). Please branch from master for your project.
2. Complete the project as described below within your branch.
3. Finally, create a zip file of your project/repo, including the .git directory. Please email the zip file (or link to it) to your Recruiting contact at The New York Times to let them know you have submitted a solution. In the email, please indicate the name of your branch.

## Project Description

This problem consists of building an API that marries two sample data sets (NYTimes article data and some fake user reading history) to build an article ranking endpoint. We'd like for you to build an endpoint that takes in a list of articles, represented by ids, and returns those articles ranked in order of a user's preferences. In this case, "preference" means a users interest or preference for articles from a given "section" of The New York Times. You will need to look at the user's reading history (i.e. articles they have read) to get a sense of which sections they read (if any). We have a few more requirements around this ranking endpoint, so please read the instructions below. Before building the ranking endpoint, you'll also build an endpoint which returns the number of unique articles read per section for a given user.

The API endpoints and data files are described in detail below.

### Here's what your API must do:

1. be written in either Python or Go

2. have an endpoint `GET /healthcheck` that returns the following JSON payload:

    ```
    {
        "status": "OK"
    }
    ```

3. have an endpoint `GET /stats/section` that accepts a `user_id` as a URL parameter and returns the number of unique articles the given user has read per section. For example, if user_id `u:1234` has read 12 `sports` articles, 7 `science` articles and 3 `climate` articles, the endpoint would return the following JSON payload:

    ```
    {
        "sports": 12,
        "science": 7,
        "climate": 3
    }
    ```

    The URL for this request would look something like this:

    `/stats/section?user_id=u:1234`

    The format of the `user_id` parameter should be `u:id` as found in the user_history.csv file.

4. have an endpoint `POST /rank/section` that takes in a list of content_ids and returns the content_ids ranked based on a given user's section "preference". You'll return the ranked list of content_ids as a JSON payload and (**important**) you'll remove any content_ids from the list that the given user has already read. Here is explicitly what we are looking for with this endpoint:

    1. like the stats endpoint, this endpoint should accept a `user_id` as a URL parameter. For example:
    
        `/rank/section?user_id=u:1234`

    2. this endpoint should accept a list of `content_ids` as JSON in the request body (Content-Type: application/json). The format of the body should look like this:

        ```
        {
            "content_ids": [
                "d685d651-31ab-42ba-9150-158f5a175241",
                "37b6e72c-6ca3-46e3-92e5-c4a66c2aa834",
                "d4817adf-6050-46dc-b2ed-77cc668069aa"
            ]
        }
        ```

    3. rank the list of `content_ids` in order of the user's section "preference" (based on the number of artices they have read per section - as you did in the `/stats/section` endpoint). If there are multiple articles from the same section, please rank those articles by their overall popularity (based on the total number of unique article "reads").

    4. remove any `content_ids` that the user had already read.

    5. return the remaining, ranked list of `content_ids` as JSON, like the following:

        ```
        {
            "content_ids": [
                "d4817adf-6050-46dc-b2ed-77cc668069aa"
                "37b6e72c-6ca3-46e3-92e5-c4a66c2aa834",
                "d685d651-31ab-42ba-9150-158f5a175241",
            ]
        }
        ```

5. include a SOLUTION.md file with an explanation of your approach and instructions for how to run your solution.

Your application does **not** need to handle authentication or authorization.

Your application should be easy to set up and should run on either Linux or Mac OS X. Please make sure you use Python 3.7+ or Go 1.12+. Feel free to use any framework (e.g. Flask) but your application should not require any for-pay software.

### Data Files:

Two data files (included in this repo) are to be used in your two endpoints: `article_data.csv` and `user_history.csv`.

**`article_data.csv`** is a CSV file with the following columns: `content_id`, `section`, `title`, `url`. There are roughly 500-600 articles included in this file and represent NYTimes articles from late 2019 and early 2020.

**`user_history.csv`** is a CSV file with the following columns: `user_id`, `content_id`. This file represents some fake users and corresponding articles they have read. The user_ids were auto-generated and don't represent any real users. The reading patterns (i.e. which articles they read) were also auto-generated and don't represent the reading habits of actual users.

### Testing:

Here is some data you can use in testing your `/stats/section` and `/rank/section` endpoints.

`/stats/section` test data:

```
 /stats/section?user_id=u:0eccf48d721e should return:
 
 {"health": 15, "sports": 9, "style": 10, "upshot": 12, "world": 35}


 /stats/section?user_id=u:e6f4cc3ba334 should return:
 
 {"business": 32, "dining": 14, "education": 13, "health": 7, "science": 24, "technology": 9, "upshot": 6, "us": 21, "world": 41}

```

`/rank/section` test data:

```
 /rank/section?user_id=u:0eccf48d721e using the following content_ids:

        c2806f15-9b98-4bbc-b66a-13d131f63aac
        9728ca66-54a3-4229-adf2-70dbbfed5049
        675da7be-ac22-49f1-b4ba-b967abdd819e
        ed8d04f8-d103-4c02-ab35-55902fdf9f6d
        af56c5dd-fddc-4fe5-b0b7-2b74d951ec0b
        1bce63f2-f3c4-4f9e-9491-45d1c4aaec02
        9a1f8fb9-19ec-4451-aee8-d3a0e9dcfb30

should return the following payload:

{"content_ids": ["1bce63f2-f3c4-4f9e-9491-45d1c4aaec02",
                 "675da7be-ac22-49f1-b4ba-b967abdd819e",
                 "9a1f8fb9-19ec-4451-aee8-d3a0e9dcfb30",
                 "9728ca66-54a3-4229-adf2-70dbbfed5049",
                 "af56c5dd-fddc-4fe5-b0b7-2b74d951ec0b",
                 "ed8d04f8-d103-4c02-ab35-55902fdf9f6d"]}

* please note that content_id c2806f15-9b98-4bbc-b66a-13d131f63aac has been removed from the returned payload because the user has already read that article.

```


## Evaluation

Evaluation of your submission will be based on the following criteria. Additionally, reviewers will attempt to assess your familiarity with standard libraries and how you've structured your submission.

1. Did your application fulfill the basic requirements?
2. Did you document the method for setting up and running your application?
3. Did you follow the instructions for submission?

Thank you and best of luck!