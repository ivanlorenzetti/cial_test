# Cial Test

**Read text file with content a url sites and extract:**
* url
* phone
* logo


## Installation
1. git clone git@github.com:ivanlorenzetti/cial_test.git

## RUN - Python
1. pip install -r requirements.txt
2. cat website.txt | python3 -m bot

## RUN - Docker
1. docker build -t cial_test .
2. cat website.txt | docker run -i cial_test

