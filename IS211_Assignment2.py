import urllib
import csv
import argparse
import datetime
import logging


def downloadData(url):
    """Function to download the data from given url
    using urllib.

    Parameters:
        url : str
            URL string

    Returns:
        The caller (object of urllib)
    """

    return urllib.urlopen(url)


def processData(infile):
    """Function to process the data of the given file
    and convert it into a dictionary and return it.

    Parameters:
        infile
            Object returned by downloadData()
            function.

    Returns:
        A dictionary having persons id as key and tuple
        of name and datetime object as its value.
    """
    # dictionary to store processed data
    processed_data = {}

    # get csv reader object
    csv_reader = csv.reader(infile)

    # skip header
    next(csv_reader)

    # iterate through the reader object
    for i, person in enumerate(csv_reader):
        # try-except block to get rid of invalid data
        try:
            # get person id
            p_id = int(person[0])
            # get person name
            p_name = person[1]
            # get object of datetime object (it will raise an error if birthday
            # is in invalid format)
            p_birth_date = datetime.datetime.strptime(person[2], "%d/%m/%Y")

            # if any error not raised, store the data into the dictionary
            processed_data[p_id] = (p_name, p_birth_date)

        # to log error if any exception raised while processing the data
        except:
            # prepare error message to log
            error_msg = "Error processing line #{} for ID #{}.".format(i, p_id)
            # open the error log file at ERROR level
            logging.basicConfig(filename="error.log", level=logging.ERROR)
            # get logger by name "assignment2"
            logger = logging.getLogger("assignment2")
            # write the error message
            logger.error(error_msg)

    # return the dictionary containing processed data
    return processed_data


def displayPerson(pid, dict_data):
    """Function to get name of birthday of the
    person having id equal to given pid parameter.

    Parameters:
        pid : int
            An integer that represents the id of the
            person for whom details should be returned.
        dict_data : dict
            Dictionary conataining data of all person
            returned by the processData() function.

    Prints:
        A string containing id along with person's name
        and birth date in the specified format:
        Person # is <name>  with a birthday of <date>.
    """

    # check if person id exits in the dict_data
    if pid in dict_data:  # if exists
        # get name
        name = dict_data[pid][0]
        # get date in format "YYY-MM-DD"
        bdate = datetime.datetime.strftime(dict_data[pid][1], "%Y-%m-%d")

        # then, print the details
        print("Person #{} is {}  with a birthday of {}.".format(pid, name, bdate))

    # if person id not found the dict_data
    else:
        print("No user found with that id.")


def main():
    """Driver function to use the defined
    functions to drive this program.
    """

    downloaded_data = None

    # create an objecct of ArgumentParser for parsing command line arguments
    parser = argparse.ArgumentParser()
    # add arguments to the object
    parser.add_argument("--url", required=True, help="Provide the csv file's URL.")
    # parse the command line arguments
    args = parser.parse_args()

    # try to download the file using the url passed as arguments
    try:
        downloaded_data = downloadData(args.url)

    # if failed to download the file
    except:
        print("Error occured while downloading the file !!!")

    # process the data returned by the downloadData() function
    process_dict = processData(downloaded_data)

    # run loop until enter enter 0 or negative to exit
    while True:
        # ask user to enter id to search
        pid = int(input("Enter ID to lookup: "))

        # check exit condition
        if pid <= 0:
            break

        # otherwise, display the person data
        else:
            displayPerson(pid, process_dict)


if __name__ == "__main__":
    main()
