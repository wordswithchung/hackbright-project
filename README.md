<kbd>![Destination: Anywhere](/static/da_homepage.png)</kbd>

## Description
[Destination: Anywhere](https://destination-anywhere.herokuapp.com/) has users input their airport, a month of travel, and trip duration and outputs a list of potential destinations with links to buy the flight on Kayak.

## Table of Contents
* [Technologies Used](#technologiesused)
* [Features](#features)
* [Data Modeling](#data)
* [Possible Improvements](#improvements)
* [Author](#author)

## <a name="technologiesused"></a>Technologies Used

* Python
* JavaScript/jQuery
* TypeAhead
* JSON
* Flask
* PostgreSQL
* Scrapy
* BeautifulSoup
* SQLAlchemy
* Jinja2
* HTML/CSS
* Bootstrap
* Google Maps API

## <a name="features"></a>Features

Users can input their airport, month of travel, and trip duration:

<kbd>![App at work](/static/da_search.gif)</kbd>

TypeAhead feature allows users to search by airport code, airport name, or city name:

<kbd>![TypeAhead](/static/da_typeahead.gif)</kbd>

Users can sort search results:

<kbd>![Sorting](/static/da_sort.gif)</kbd>

Database entries are viewable via Google Maps API:

<kbd>![Google Maps](/static/da_maps.gif)</kbd>

## <a name="data"></a>Data Modeling

Working with data -- acquisition, sanitization, storage, and manipulation -- was definitely one of my favorite parts of the project! Here's a colorful diagram to show the relationship between the tables (you can explore further in the [model.py file](https://github.com/wordswithchung/hackbright-project/blob/master/model.py)):

<kbd>![Data Model Diagram](/static/very_colorful_handwritten_data_model_diagram.jpg)</kbd>

Basics of the data model:

* I acquired data by scraping the [Fare Detective](http://www.faredetective.com/) details page by navigating from the listing pages for the top populous airports. See screenshots below of the Fare Detective pages.

<kbd>![Listings Page](/static/fare-detective-listings.png)</kbd>

<kbd>![Details Page](/static/fare-detective-details.png)</kbd>

* With the info thrown into a CSV (airports) and JSON (airfares) file, I parsed through the data with my [seed file](https://github.com/wordswithchung/hackbright-project/blob/master/seed.py). This was both nerve-wracking and fun. The first I had to discard the entire database because I forgot a field? So scary. The fifth time? Not too bad. And after iterating through and testing to ensure that I had the data I wanted and that they tied to each other nicely, I could proceed forward with the rest of my project!

## <a name="improvements"></a>Possible Improvements

This project was completed in under a month, so there are definitely areas for improvement. Specifically:

* Tests are needed!
* The "maps" feature was purely for practicing API integration. If this were a real site, I would like to either (a) expand the feature or (b) remove it altogether as it disrupts the user interaction with the site.
* The routes available are limited by the information scraped and there are only 6,900 data points. I would like to either scrape more pages for more data points or utilize another method for users to get airfare to interesting places (e.g., UNESCO heritage sites, best beaches in the world, or locations to view northern lights).

## <a name="author"></a>Author
Hi! My name is [Chung Nguyen](https://www.linkedin.com/in/chungtnguyen) and I am a software engineer. I received training from Hackbright Academy, an engineering bootcamp for women in San Francisco  (graduation: December 2016). I'm from the Bay Area and have a lot of experience in client-facing roles and training UX researchers, software developers, and product managers in remote usability testing. I'm currently seeking a full-time software developer role in the San Francisco Bay Area. If you have a role that I should hear about, feel free to email chung.nguyen at gmail. Thanks for reading!
