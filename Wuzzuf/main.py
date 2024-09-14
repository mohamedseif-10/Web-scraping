import time
import pandas as pd
import re
from CleanTheData import parse_time_string
from selenium import webdriver
from selenium.webdriver.common.by import By
from sqlalchemy import create_engine, text

#########################################################################################################
# This project is about scraping the jobs from WUZZUUF website
# The user can choose the job title he wants to search for and the number of pages he wants to scrape 
# All the jobs will be stored in a csv file and then the user can read the data from the csv file
# The data will be stored in a mysql database or any other database and the user can query the database
# This is an example of data scraping and data Extraction and data loading which is the first (ETL) process
# The user can use the data for data analysis and data visualization
# The user can use the data for machine learning and deep learning models
#########################################################################################################


driver = webdriver.Chrome()
driver.maximize_window()
print("-" * 25)
print("Hello, This application will help you to get the jobs from WUZZUUF website")
while True:
    userChoice = int(
        input(
            "Please choose the job title you want to search for:\n1. Data Science\n2. Engineering\n3. Software Development\n4. Back-End Development\n5. Front-End Development\n6. Full-Stack Development\n7. Mobile Development\n8. Web Development\n9. DevOps\n10. Cloud Computing\n11. Cyber Security\n12. Artificial Intelligence\n"
        )
    )
    if userChoice in range(1, 13):
        break
    else:
        print("Invalid choice, Please try again")

JobsDict = {
    1: "data%20science",
    2: "engineering",
    3: "software%20development",
    4: "back-end%20development",
    5: "front-end%20development",
    6: "full-stack%20development",
    7: "mobile%20development",
    8: "web%20development",
    9: "devops",
    10: "cloud%20computing",
    11: "cyber%20security",
    12: "artificial%20intelligence",
}
baseURL = f"https://wuzzuf.net/search/jobs/?a=spbl&q={JobsDict[userChoice]}"


numPages = int(input(f"Enter the number of pages you want to scrape :"))

jobs = []
tmp = 0
for page in range(numPages):
    if tmp == numPages:
        break
    url = f"{baseURL}&start={page}" if page > 0 else baseURL
    print(f"Scraping page: {page + 1} of {numPages}")
    print("-" * 25)
    driver.get(url)
    time.sleep(10)
    try:
        maxNumberOfPages = driver.find_element(By.CLASS_NAME, "css-8neukt").text
        match = re.search(r"of\s+(\d+)", maxNumberOfPages)
        if match:
            total_jobs = int(match.group(1))
            jobs_per_page = 15
            total_pages = (total_jobs + jobs_per_page - 1) // jobs_per_page

            if numPages > total_pages:
                print(
                    f"Number of pages exceeds the total number of pages.\nScraping will be only {total_pages} pages."
                )
                numPages = total_pages
        else:
            print("Couldn't extract the total number of jobs.")

    except Exception as e:
        print(f"Error finding or processing total number of jobs: {e}")
    k = 0
    jobsList = driver.find_elements(By.CLASS_NAME, "css-pkv5jc")
    for job in jobsList:
        k += 1
        try:
            jobTime = job.find_element(By.CLASS_NAME, "css-do6t5g").text
        except Exception as e:
            continue

        try:
            jobTitle = job.find_element(By.CLASS_NAME, "css-o171kl").text
            CompanyName = job.find_element(By.CLASS_NAME, "css-17s97q8").text
            CompanyLocation = job.find_element(By.CLASS_NAME, "css-5wys0k").text
            jobType = job.find_element(By.CLASS_NAME, "css-1ve4b75").text

            try:
                element = job.find_element(
                    By.XPATH,
                    f"/html/body/div[1]/div/div[3]/div/div/div[2]/div[{k}]/div/div[2]/div[2]",
                )
                links = element.find_elements(By.TAG_NAME, "a")
                texts = [link.text for link in links]
                Requirements = " ".join(texts)
                # Requirements = re.sub(r"[^\x00-\x7F]+", ", ", Requirements)
                # Requirements = re.sub(r"\s*-\s*", " ", Requirements).strip()
                # Requirements = re.sub(r"\s*,\s*", ", ", Requirements).strip()
            except Exception as e:
                print(f"Error finding or processing Requirements: {e}")
                Requirements = ""
            CompanyName = CompanyName.replace(" -", "")

            jobs.append(
                (jobTitle, CompanyName, CompanyLocation, jobType, Requirements, jobTime)
            )
        except Exception as e:
            print(f"Error :{e}")
            continue
    tmp += 1

##################################################################################################
# The following code is for storing the data in a csv file and reading the data from the csv file
# I can save the data in EXCEl file or JSON file or any other file as well
##################################################################################################

df = pd.DataFrame(
    jobs,
    columns=[
        "Job Title",
        "Company Name",
        "Company Location",
        "Job Type",
        "Job Time",
        "Requirements",
    ],
)

df["Posted time"] = df["Job Time"].apply(lambda x: parse_time_string(x))

data = df.to_csv(f"{JobsDict[userChoice].replace('%20', ' ')}.csv", index=False)

driver.quit()

data = pd.read_csv(f"{JobsDict[userChoice].replace('%20', ' ')}.csv")

for j in range(min(10, len(data))):
    print(
        f"Job title: {data['Job Title'][j]} \nCompany Name: {data['Company Name'][j]} \nCompany Location: {data['Company Location'][j]} \nJob Type: {data['Job Type'][j]} \nRequirements: {data['Requirements'][j]} \nPosted time: {data['Posted time'][j]}"
    )
    print("-" * 25)
###########################################################################################
# The following code is for storing the data in a mysql database and querying the database
###########################################################################################
try:
    username = "root"
    password = "1234"
    host = "localhost"
    port = "3306"
    database = "data_science"

    engine = create_engine(
        f"mysql+mysqlconnector://{username}:{password}@{host}:{port}/{database}"
    )
    # if engine is not None:
    #     print("Connection is successful")
    
    # data = pd.read_csv("Data Science.csv")
    con = engine.connect()
    data.to_sql("jobs", con=engine, if_exists="replace", index=False)

    Query = "SELECT `Company Name`, `Job Title` FROM jobs ORDER BY `Company Name`, `Job Title`;"
    result = con.execute(text(Query))
    rows = result.fetchall()

    for row in rows:
        print(f"Company_name = {row[0]}\nJob Title = {row[1]}")
        print("------------------------")
    con.close()

except Exception as e:
    print("The error is:", e)
