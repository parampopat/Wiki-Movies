"""
__author__ = "Param Popat"
__version__ = "1"
__git__ = "https://github.com/parampopat/"
"""

import os
import pandas as pd
import wikipedia
from wikipedia.exceptions import DisambiguationError


def legalize(name, illegal):
    """
    Removes illegal filename characters
    :param name: File Name
    :param illegal: List of illegal Characters
    :return: Legalized File Name
    """
    for char in name:
        if char in illegal:
            name = name.replace(char, "")
    return name


if __name__ == '__main__':
    # Define the task. For Example "Plot"
    task = "Plot"
    author = "_James_Cameron"
    csvname = "jamescameron.csv"
    # Wikipedia header format
    header = "== " + task + " =="

    # List of illegal File Name Characters
    illegalCharacters = [':', '%', '/', '\\', '.', '>', '<', '?', '|', '*', '"', ]

    # Path to save task files.
    path = "F:\\PARAM\\Wiki-Movies\\" + task + author + "\\"

    # Check if folder exists otherwise create it.
    if not os.path.exists(path):
        os.mkdir(path)

    # Open the CSV containing names of movies
    listOfMovies = pd.read_csv(path.replace(task + author + "\\", "") + csvname).iloc[:, 0].values
    listOfFiles = []

    # For each movie, extract plot and save it in text file.
    for movieName in listOfMovies:
        try:
            text = wikipedia.page(movieName).content.replace("\n", "")
        except DisambiguationError:
            text = wikipedia.page(movieName + " (film)").content.replace("\n", "")
        # If page doesnt have the task header, try adding (film) to the movie name.
        if header not in text:
            try:
                text = wikipedia.page(movieName + " (film)").content.replace("\n", "")
            except wikipedia.exceptions.PageError:
                # If page doesn't exist
                print(movieName, 'NA')
                continue
        # Select text from after the task header till the start of next header.
        plot = text[
               text.find(header) + 10:(
                       text[(text.find(header) + 10):].find("==") + text.find(header) + 10)]

        # Check and solve for illegal characters in movie name.
        fileName = legalize(movieName, illegalCharacters)

        # Keep a track of filenames`
        listOfFiles.append([movieName, fileName])

        # Save the task content in text files.
        with open(path + fileName + ".txt", 'w', encoding="UTF-8") as f:
            f.write(plot)
        f.close()

    # Save the movie name to file name association for future reference.
    assoc = pd.DataFrame(listOfFiles, columns=['Movie Name', 'File Name'])
    assoc.to_csv(path.replace(task + author + "\\", "") + task + author + '_associations.csv', index=None)
