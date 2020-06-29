# Flask Application

The backend is implemented using Flask python framework. 

- Setup the environment. Create a virtual environment and install all the requirements.
```
$ python3.6 -m venv venv
$ source venv/bin/activate
$ pip install -r requirements.txt
```

## Query Pre-processing

The system is supporting for queries like “අමරදේව හොදම ගීත”, “යමුනා මලනි රචිත ගීත”. To perform this, the context of the query(artist, writer, composer, rating) 
should identify. A simple rule-based approach is used to identify the context of the query. The query is tokenized and checks the tokens with predefined rules.
Sinhala query tokenizing is done by the "Sinling" python library. Also, tokens are converted into their bases and affixes(Sinling word splitter). The faceting
(aggregating) is used in elastic search.  When a query is about "හොදම ගීත", "ජනප්‍රිය ගීත", "ප්‍රධාන ගීත", the query processing part identify it and sort the results 
by "rating" of the song. The system is boosting queries by Elasticsearch boost. The individual fields set with higher weights after identifying the contexts such 
as artists, music composers, writers.

> The Sinling python library is used for Sinhala query tokenizing and spliting. For Sinling installion guid refer the [Sinling project Repository](https://github.com/ysenarath/sinling).

## Frontend

- The frontend is a simple single page web application. 
- It used [Materialize CSS](https://materializecss.com/), [JQuery](https://jquery.com/) libraries and frameworks.
