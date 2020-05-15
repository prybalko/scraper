# Scraper
This is an application that parses [Hacker News](https://news.ycombinator.com/) website and stores top 30 posts.
Data can be retrieved using GET `/posts` endpoint.



## Deployment

    docker-compose up -d app


## Tests

    pip install pipenv
    pipenv install --dev
    pipenv run pytest
