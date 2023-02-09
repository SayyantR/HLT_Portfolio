# NetID: sxr180064
# CS4395 - Mazidi
# HW1

import sys
import os
import re
import pickle

# Person class to contain employee information
class Person():
    def __init__(self, last, first, mi, empID, phone) -> None:
        self.last = last
        self.first = first
        self.mi = mi
        self.id = empID
        self.phone = phone
    
    # Method to print out employee details
    def display(self) -> None:
        print("Employee ID: {id}".format(id=self.id))
        print("Employee Name: {first} {middle}. {last}".format(first=self.first, middle=self.mi, last=self.last))
        print("Employee Phone {phone}\n".format(phone=self.phone))


# Read input file
def readFile(filepath):
    with open(os.path.join(os.getcwd(), filepath), 'r') as f:
        text_in = f.read()
    return text_in

# Method to check if employee ID matches format; returns true if not
def validateEmpID(empID):
    if len(empID) != 6: return False
    if not re.match(r'\A[a-zA-Z][a-zA-Z][0-9][0-9][0-9][0-9]\Z', empID): return False

# Method to process data from input file
def processData(data):
    #Split input data into employees
    employees = data.split("\n")[1:]
    employeeDict = {}

    # Iterate through employees
    for employee in employees:
        # Parse string from input file to get employee information
        first, last, middle, empID, phone = employee.split(",")

        # Capital case first and last name
        first = first[0].upper() + first[1:].lower()
        last = last[0].upper() + last[1:].lower()

        # Format middle name
        if middle: 
            middle = middle.upper()
        else:
            middle = 'X'
        
        # Prompt user to enter in valid employee ID until valid ID is provided
        while validateEmpID(empID) == False:
            empID = input("EmployeeID {empID} is invalid. Please enter a valid ID.\n".format(empID=empID))
        
        # Extract and format phone number
        numbers = re.findall(r'\d+', phone)
        rawPhoneNumber = ''.join(numbers)

        # Handle improper phone number
        while len(rawPhoneNumber) != 10:
            phone = input("Phone number {phone} is invalid. Please provide valid phone number.\n".format(phone=phone))
            numbers = re.findall(r'\d+', phone)
            rawPhoneNumber = ''.join(numbers)
        formattedPhoneNumber = rawPhoneNumber[0:3] + "-" + rawPhoneNumber[3:6] + "-" + rawPhoneNumber[6:]

        # Create Person object
        person = Person(last, first, middle, empID, formattedPhoneNumber)

        # Handle duplicate
        if person.id in employeeDict.keys():
            print("Duplicate ID found. Exiting program...")
            sys.exit()
        else:
            employeeDict[person.id] = person
    return employeeDict

if __name__ == '__main__':

    # Check for proper script invocation
    if len(sys.argv) < 2:
        print("Please provide directory to data file.")
        sys.exit()
    
    # Get input file contents
    fp = sys.argv[1]
    data = readFile(fp)

    # Process input file data contents
    employeeDict = processData(data)

    # Pickle file operations
    pickle.dump(employeeDict, open('employees.p', 'wb'))
    record = pickle.load(open('employees.p', 'rb'))

    # Print final data
    print("\n\nEmployee Directory\n")
    for key in record.keys():
        record[key].display()