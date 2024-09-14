# WUZZUF Job Scraper

This project is a job scraper that extracts job postings from the WUZZUF website based on the user's chosen job title and the number of pages to scrape. The data is saved in a CSV file and optionally stored in a MySQL database. This project showcases data extraction, transformation, and loading (ETL) processes that are essential in data analysis, data visualization, and machine learning.

## Features

- **Interactive Job Selection:** Prompts the user to select a job category from a list of popular job titles.
- **Customizable Scraping:** Allows the user to specify the number of pages to scrape.
- **Data Extraction:** Extracts job details, including title, company name, location, job type, Experience, and requirements.
- **Data Cleaning:** Processes job posting times to a uniform date format (`YYYY-MM-DD`) this is only small example.
- **Data Storage:** Saves data in a CSV file and optionally stores it in a MySQL database for easy querying and analysis.
- **Extensible for Data Analysis:** The scraped data can be used for data analysis, visualization, and training machine learning models.
- **Error Handling:** Provides exception handling to deal with various potential scraping and data processing errors.

## Project Structure

- **`main.py`**: Main script that handles web scraping, data extraction, and storage.
- **`CleanTheData.py`**: Contains functions for data cleaning, including converting time strings to date format.
- **`requirements.txt`**: Lists Python dependencies required for the project.
- **`README.md`**: Documentation for the project.

## Setup

### Prerequisites

- Python 3.11
- MySQL database (optional, for database storage)
- Selenium WebDriver (e.g., ChromeDriver)
- Python packages listed in `requirements.txt`
- Create DB

### License


This documentation provides an overview of the project, instructions for setup and use, details on the script's functionality, and potential future enhancements. Feel free to adapt it as needed for your project!.



### Installing Dependencies

Install the necessary Python packages using `pip`:

```bash
pip install -r requirements.txt




