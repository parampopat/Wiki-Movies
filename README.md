# Wiki-Movies

A wikipedia based Web-Scrapper to fetch the plot of various movies and then train a movie script generator using the data.

The script generator is an LSTM that learns the vocabulary of the movies and patterns in the plot. Once the learning is done, the LSTM will generate scripts based on what it learnt. 