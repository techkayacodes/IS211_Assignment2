import argparse
import urllib.request
import logging
import datetime

def downloadData(url):
    try:
        with urllib.request.urlopen(url) as response:
            data = response.read().decode('utf-8')
        return data
    except Exception as e:
        print(f"Error downloading data: {str(e)}")
        exit(1)

def processData(file_content, logger):  # Pass logger as an argument
    personData = {}
    lines = file_content.split('\n')
    for line_num, line in enumerate(lines[1:], start=2):
        parts = line.split(',')
        if len(parts) == 3:
            user_id, name, birthday_str = parts
            try:
                birthday = datetime.datetime.strptime(birthday_str, '%d/%m/%Y')
                personData[int(user_id)] = (name, birthday)
            except ValueError:
                logger.error(f"Error processing line #{line_num} for ID #{user_id}")
    return personData

def displayPerson(id, personData):
    if id in personData:
        name, birthday = personData[id]
        print(f"Person #{id} is {name} with a birthday of {birthday.strftime('%Y %m %d')}")
    else:
        print("No user found with that id")

def main(url):
    csvData = downloadData(url)
    
    # Configure logging to write errors to a file called 'errors.log'
    logging.basicConfig(filename='errors.log', level=logging.ERROR, format='Error processing line #%(lineno)d for ID #%(id)s')
    logger = logging.getLogger('assignment2')
    
    personData = processData(csvData, logger)  # Pass logger to processData
    
    while True:
        user_input = input("Enter an ID to lookup (enter a negative number or 0 to exit): ")
        try:
            id = int(user_input)
            if id <= 0:
                break
            displayPerson(id, personData)
        except ValueError:
            print("Invalid input. Please enter a valid ID.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", help="URL to the datafile", type=str, required=True)
    args = parser.parse_args()
    main(args.url)
