Basic python Markov chain program. 

Using the input text it creates a list of every unique word in the text (counting punctuation as a word) and then creates a dictionary for the probability that every other word will follow the word.
The result is a generated body that resembles normal text but does not make any sense, though how accurately it resembles actual text will vary based on the input.
Due to the massive size of the dictionaries created the process of scanning in a text can be very long.

The api's used in the project are for wikipedia: https://github.com/martin-majlis/Wikipedia-API
and for Archive of our Own: https://github.com/ArmindoFlores/ao3_api
