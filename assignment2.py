import argparse
import urllib.request
import logging
import datetime

def downloadData(url):
    """Downloads the data"""
    try:
        with urllib.request.urlopen(url) as response:
            return response.read().decode('utf-8')
    except Exception as e:
        logging.error(f"Error downloading data: {e}")
        print("Error downloading data. Please check the URL or your internet connection.")
        exit()

def processData(file_content):
    """Processes the data"""
    personData = {}
    lines = file_content.split('\n')[1:]
    for line in lines:
        if line:
            parts = line.split(',')
            personData[int(parts[0])] = (parts[1], datetime.datetime.strptime(parts[2], '%d/%m/%Y').date())
    return personData

def displayPerson(id, personData):
    """Displays person data"""
    if id in personData:
        name, dob = personData[id]
        print(f"Person ID: {id}, Name: {name}, Date of Birth: {dob}")
    else:
        print(f"No person found with ID {id}")

def setupLogger():
    """Sets up the logger"""
    logging.basicConfig(filename='errors.log', level=logging.ERROR, format='%(asctime)s - %(levelname)s: %(message)s', filemode='w')

def main(url):
    print(f"Running main with URL = {url}...")
    setupLogger()
    csvData = downloadData(url)
    personData = processData(csvData)
    while True:
        user_input = input("Enter an ID to lookup (enter a negative number or 0 to exit): ")
        try:
            user_input = int(input("Enter an ID to lookup (Enter a negative number or 0 to exit): "))
            if user_input <= 0:
                break
            displayPerson(user_input, personData)
        except ValueError:
            print("Invalid input. Please enter a valid integer.")

if __name__ == "__main__":
    """Main entry point"""
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", help="URL to the datafile", type=str, required=True)
    args = parser.parse_args()
    main(args.url)
