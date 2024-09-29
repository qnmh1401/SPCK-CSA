import requests 
import csv 
 
# Login credentials 
username = 'your_username' 
password = 'your_password' 
 
# URL of the webpage with the CSV file 
url = 'https://raw.githubusercontent.com/' 
csv_url = 'https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/cases_deaths/COVID-19%20Cases%20and%20deaths%20-%20WHO.csv' 
 
# Login process 
session = requests.Session() 
login_data = { 
    'username': username, 
    'password': password 
} 
response = session.post(url, data=login_data) 
 
# Check if login was successful 
if response.status_code == 200: 
    # Download the CSV file 
    csv_response = session.get(csv_url) 
 
    # Save the CSV file 
    with open('data.csv', 'w', newline='') as csvfile: 
        csvwriter = csv.writer(csvfile) 
        for row in csv.reader(csv_response.text.splitlines()): 
            csvwriter.writerow(row) 
 
    print('CSV file downloaded successfully.') 
else: 
    print('Login failed. Please check your credentials.') 
