import argparse  # Import the argparse module to parse command line arguments
import urllib.request  # Import urllib.request module to download data from a URL
import logging  # Import the logging module for error logging
import datetime  # Import the datetime module to work with dates and times

# Function to download data from a given URL
def downloadData(url):
    try:
        with urllib.request.urlopen(url) as response:
            data = response.read().decode('utf-8')
        return data  # Return the downloaded data
    except Exception as e:
        print(f"Error downloading data: {str(e)}")
        exit(1)

# Function to process the CSV data and create a dictionary mapping IDs to (name, birthday) tuples
def processData(file_content):
    personData = {}  # Create an empty dictionary to store the processed data
    lines = file_content.split('\n')  # Split the file content into lines
    for line_num, line in enumerate(lines[1:], start=2):
        parts = line.split(',')
        if len(parts) == 3:
            user_id, name, birthday_str = parts
            try:
                birthday = datetime.datetime.strptime(birthday_str, '%d/%m/%Y').date()
                personData[int(user_id)] = (name, birthday)  # Store data in the dictionary
            except ValueError:
                # Log errors for malformed dates
                logger.error(f"Error processing line #{line_num} for ID #{user_id}")
    return personData  # Return the processed data

# Function to display a person's information based on their ID
def displayPerson(id, personData):
    if id in personData:
        name, birthday = personData[id]
        # Print the person's information in the specified format
        print(f"Person #{id} is {name} with a birthday of {birthday.strftime('%Y %m %d')}")
    else:
        print("No user found with that id")  # Print a message if the ID is not found

# Main function that orchestrates the program
def main(url):
    csvData = downloadData(url)  # Download CSV data from the specified URL
    
    # Configure logging to write errors to "errors.log" in the specified format
    logging.basicConfig(filename='errors.log', level=logging.ERROR, format='Error processing line #%(lineno)d for ID #%(id)s')
    logger = logging.getLogger('assignment2')
    
    personData = processData(csvData)  # Process CSV data into a dictionary
    
    while True:
        user_input = input("Enter an ID to lookup (enter a negative number or 0 to exit): ")
        try:
            id = int(user_input)
            if id <= 0:
                break  # Exit the program if the user enters a non-positive number
            displayPerson(id, personData)  # Display the person's information
        except ValueError:
            print("Invalid input. Please enter a valid ID.")  # Prompt for a valid ID if input is not an integer

# Entry point of the script
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", help="URL to the datafile", type=str, required=True)
    args = parser.parse_args()
    main(args.url)  # Call the main function with the provided URL as an argument
