import argparse
import urllib.request
import logging
import datetime

def downloadData(url):
    try:
        # Try to open the URL and read its contents
        with urllib.request.urlopen(url) as response:
            data = response.read().decode('utf-8')
        return data
    except Exception as e:
        # If there's an error while downloading, print an error message and exit
        print(f"Error downloading data: {str(e)}")
        exit(1)

def processData(file_content):
    personData = {}  # Create an empty dictionary to store person data
    lines = file_content.split('\n')  # Split the file content into lines
    for line_num, line in enumerate(lines[1:], start=2):
        # Loop through each line in the file, skipping the header line (index 0)
        parts = line.split(',')
        if len(parts) == 3:
            # Check if there are three parts (ID, name, birthday) in the line
            user_id, name, birthday_str = parts
            try:
                # Convert the birthday string to a datetime object
                birthday = datetime.datetime.strptime(birthday_str, '%d/%m/%Y')
                # Store the person's data in the dictionary with ID as the key
                personData[int(user_id)] = (name, birthday)
            except ValueError:
                # If there's an error parsing the date, log it with the line number and ID
                logger.error(f"Error processing line #{line_num} for ID #{user_id}")
    return personData

def displayPerson(id, personData):
    if id in personData:
        # If the ID exists in the person data, print the person's information
        name, birthday = personData[id]
        print(f"Person #{id} is {name} with a birthday of {birthday.strftime('%Y %m %d')}")
    else:
        # If the ID does not exist, print a message
        print("No user found with that id")

def main(url):
    csvData = downloadData(url)
    
    # Configure logging to write errors to a file called 'errors.log'
    logging.basicConfig(filename='errors.log', level=logging.ERROR, format='Error processing line #%(lineno)d for ID #%(id)s')
    logger = logging.getLogger('assignment2')
    
    personData = processData(csvData)  # Process the CSV data into a dictionary
    
    while True:
        user_input = input("Enter an ID to lookup (enter a negative number or 0 to exit): ")
        try:
            id = int(user_input)
            if id <= 0:
                # If the user enters a negative number or 0, exit the program
                break
            displayPerson(id, personData)  # Display the person's information
        except ValueError:
            # If the user enters invalid input, prompt them to enter a valid ID
            print("Invalid input. Please enter a valid ID.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", help="URL to the datafile", type=str, required=True)
    args = parser.parse_args()
    main(args.url)
