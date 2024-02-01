import requests
import json
from bs4 import BeautifulSoup

with open("config.json", "r") as f:
    config = json.load(f)
    is_first_time = config["first-time"]

# Pretend to be a browser
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
}

count = 1  # Add a counter
movies = []  # List to store movie names

if is_first_time:# If it is the first time to run the program
    with open("top250_movies.txt","w")as f:
        # Traverse all pages
        for i in range(0, 226, 25):  # Each page has 25 movies, so add 25
            url = f"https://movie.douban.com/top250?start={i}&filter="  # URL of each page
            response = requests.get(url, headers=headers)  # Get the webpage
            html = response.text  # Get the source code of the webpage
            soup = BeautifulSoup(html, "html.parser")  # Parse the webpage
            titles = soup.findAll("span", attrs={"class": "title"})  # Get all title elements

            # Traverse all title elements
            for title in titles:
                if '/' not in title.text:  # Remove the English name of the movie
                    movies.append(title.text)  # Add the movie name to the list
                    f.write(f"{title.text},")  # Add a number before each title
                    count += 1  # Increment the counter

config["first-time"] = False                    
with open("config.json","w")as f:# Update the config file
    json.dump(config,f)

with open("top250_movies.txt","r")as f:# Read the movie list
    movies = f.read().split(",")
    
while True:
    name = input("Please enter the movie name or the ranking:(say 'q' to quit) ")
    if name.isdigit():# If the input is a number
        print(f"The movie of this ranking is {movies[int(name) - 1]}\n")# Print the movie name
    else:# If the input is a movie name
        if name in movies:
            print(f"The ranking of this movie is Top {movies.index(name) + 1}\n")# Print the ranking
        elif name == "q":
            break# Quit the program
        else:
            print("This movie is not in the list\n")# Print the error message
