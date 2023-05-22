from model.Vaccine import Vaccine
from model.Caregiver import Caregiver
from model.Patient import Patient
from util.Util import Util
from db.ConnectionManager import ConnectionManager
import pymssql
import datetime


'''
objects to keep track of the currently logged-in user
Note: it is always true that at most one of currentCaregiver and currentPatient is not null
        since only one user can be logged-in at a time
'''
current_patient = None

current_caregiver = None


def create_patient(tokens):
    """
    TODO: Part 1
    """
        # create_patient <username> <password>
    # check 1: the length for tokens need to be exactly 3 to include all information (with the operation name)
    if len(tokens) != 3:
        print("Failed to create user.")
        return

    username = tokens[1]
    password = tokens[2]
    # check 2: check if the username has been taken already
    if username_exists_patient(username):
        print("Username taken, try again!")
        return

    if len(password)<8:
       print("password must be minimum 8 characters")
       return
    
    if not(any(x.isupper() for x in password) and any(x.islower() for x in password)):
        print("password must be a mixture of both uppercase and lowercase characters")
        return

    if not(any(x.isdigit() for x in password)):
        print("password does not contain any digits as password must be mixture of letters and digits")
        return

    scs= ['!', '@', '#', '?']
    has_any = any([sc in password for sc in scs])
    if not has_any:
       print("password must contain at least one of these characters: ! @ # ?")
       return

    salt = Util.generate_salt()
    hash = Util.generate_hash(password, salt)

    # create the patient
    patient = Patient(username, salt=salt, hash=hash)

    # save to patient information to our database
    try:
        patient.save_to_db()
    except pymssql.Error as e:
        print("Failed to create user.")
        print("Db-Error:", e)
        quit()
    except Exception as e:
        print("Failed to create user.")
        print(e)
        return
    print("Created user ", username)

def username_exists_patient(username):
    cm = ConnectionManager()
    conn = cm.create_connection()

    select_username = "SELECT * FROM Patient WHERE Username_P = %s"
    try:
        cursor = conn.cursor(as_dict=True)
        cursor.execute(select_username, username)
        #  returns false if the cursor is not before the first record or if there are no rows in the ResultSet.
        for row in cursor:
            return row['Username_P'] is not None
    except pymssql.Error as e:
        print("Error occurred when checking username")
        print("Db-Error:", e)
        quit()
    except Exception as e:
        print("Error occurred when checking username")
        print("Error:", e)
    finally:
        cm.close_connection()
    return False


def create_caregiver(tokens):
    # create_caregiver <username> <password>
    # check 1: the length for tokens need to be exactly 3 to include all information (with the operation name)
    if len(tokens) != 3:
        print("Failed to create user.")
        return

    username = tokens[1]
    password = tokens[2]
    # check 2: check if the username has been taken already
    if username_exists_caregiver(username):
        print("Username taken, try again!")
        return

    if len(password)<8:
       print("password must be minimum 8 characters")
       return
    
    if not(any(x.isupper() for x in password) and any(x.islower() for x in password)):
        print("password must be a mixture of both uppercase and lowercase characters")
        return

    if not(any(x.isdigit() for x in password)):
        print("password does not contain any digits as password must be mixture of letters and digits")
        return

    scs= ['!', '@', '#', '?']
    has_any = any([sc in password for sc in scs])
    if not has_any:
       print("password must contain at least one of these characters: ! @ # ?")
       return
    
    salt = Util.generate_salt()
    hash = Util.generate_hash(password, salt)
    # create the caregiver
    caregiver = Caregiver(username, salt=salt, hash=hash)

    # save to caregiver information to our database
    try:
        caregiver.save_to_db()
    except pymssql.Error as e:
        print("Failed to create user.")
        print("Db-Error:", e)
        quit()
    except Exception as e:
        print("Failed to create user.")
        print(e)
        return
    print("Created user ", username)


def username_exists_caregiver(username):
    cm = ConnectionManager()
    conn = cm.create_connection()

    select_username = "SELECT * FROM Caregivers WHERE Username = %s"
    try:
        cursor = conn.cursor(as_dict=True)
        cursor.execute(select_username, username)
        #  returns false if the cursor is not before the first record or if there are no rows in the ResultSet.
        for row in cursor:
            return row['Username'] is not None
    except pymssql.Error as e:
        print("Error occurred when checking username")
        print("Db-Error:", e)
        quit()
    except Exception as e:
        print("Error occurred when checking username")
        print("Error:", e)
    finally:
        cm.close_connection()
    return False


def login_patient(tokens):
    """
    TODO: Part 1
    """
    global current_patient
    if current_caregiver is not None or current_patient is not None:
        print("User already logged in.")
        return

    # check 2: the length for tokens need to be exactly 3 to include all information (with the operation name)
    if len(tokens) != 3:
        print("Login failed.")
        return

    username = tokens[1]
    password = tokens[2]

    patient = None
    try:
        patient = Patient(username, password=password).get()
    except pymssql.Error as e:
        print("Login failed.")
        print("Db-Error:", e)
        quit()
    except Exception as e:
        print("Login failed.")
        print("Error:", e)
        return

    # check if the login was successful
    if patient is None:
        print("Login failed.")
    else:
        print("Logged in as: " + username)
        current_patient = patient


def login_caregiver(tokens):
    # login_caregiver <username> <password>
    # check 1: if someone's already logged-in, they need to log out first
    global current_caregiver
    if current_caregiver is not None or current_patient is not None:
        print("User already logged in.")
        return

    # check 2: the length for tokens need to be exactly 3 to include all information (with the operation name)
    if len(tokens) != 3:
        print("Login failed.")
        return

    username = tokens[1]
    password = tokens[2]

    caregiver = None
    try:
        caregiver = Caregiver(username, password=password).get()
    except pymssql.Error as e:
        print("Login failed.")
        print("Db-Error:", e)
        quit()
    except Exception as e:
        print("Login failed.")
        print("Error:", e)
        return

    # check if the login was successful
    if caregiver is None:
        print("Login failed.")
    else:
        print("Logged in as: " + username)
        current_caregiver = caregiver


def search_caregiver_schedule(tokens):
    """
    TODO: Part 2
    """
    global current_caregiver
    global current_patient
    if current_caregiver is None and current_patient is None:
        print("Please login first")
        return
    
    if len(tokens) != 2:
        print("Please try again!")
        return
    
    date = tokens[1]
    # assume input is hyphenated in the format mm-dd-yyyy
    date_tokens = date.split("-")
    month = int(date_tokens[0])
    day = int(date_tokens[1])
    year = int(date_tokens[2])
    d = datetime.datetime(year, month, day)
    cm = ConnectionManager()
    conn = cm.create_connection()
    caregiver_sch = "SELECT C.Username FROM Caregivers C, Availabilities A WHERE A.Username = C.Username AND A.Time = (%d) ORDER BY C.Username"
    vaccine_instock = "SELECT V.name, V.doses FROM Vaccines V"

    try:
        cursor = conn.cursor()
        cursor.execute(caregiver_sch, (d))
        print("caregiver_name")
        for row in cursor:
            print(str(row[0]))
            
    except pymssql.Error as e:
        print("caregiver schedule search failed. Please try again!")
        print("Db-Error:", e)
        return
    except Exception as e:
        print("error in caregiver schedule search. Please try again!")
        print("Error:", e)
        return
     
    try:
        cursor = conn.cursor()
        cursor.execute(vaccine_instock)
        print("Vaccine_name"," ","Number_of_doses")
        for row in cursor:
            print(str(row[0]),"           ", str(row[1]))
            
    except pymssql.Error as e:
        print("vaccine stock search failed. Please try again!")
        print("Db-Error:", e)
        quit()
    except Exception as e:
        print("error in vaccine stock check. Please try again!")
        print("Error:", e)
        return

    finally:
        cm.close_connection()


def reserve(tokens):
    """
    TODO: Part 2
    """
    global current_patient
    global current_caregiver
    if current_caregiver is None and current_patient is None:
        print("Please login first!")
        return

    if current_patient is None:
        print("Please login as a patient!")
        return

    if len(tokens) != 3:
        print("Please try again!")
        return

    date = tokens[1]
    vaccine_name = tokens[2]
    # assume input is hyphenated in the format mm-dd-yyyy
    date_tokens = date.split("-")
    month = int(date_tokens[0])
    day = int(date_tokens[1])
    year = int(date_tokens[2])
    d = datetime.datetime(year, month, day)
    cm = ConnectionManager()
    conn = cm.create_connection()

    caregiver_available = "SELECT Username FROM Availabilities WHERE Time = (%s) ORDER BY Username"
    vaccine_available = "SELECT Name, Doses FROM Vaccines WHERE Name = (%s)"
    appointment_id_select = "SELECT MAX(appointment_id) FROM Appointment"
    update_reserved_appointment = "INSERT INTO Appointment VALUES (%s, %s, %s, %s, %s)"
    availability_delete = "DELETE FROM Availabilities WHERE Time = (%d) AND Username = (%s)"
    caregiver_selected = ""

    try:
        cursor = conn.cursor()
        cursor.execute(caregiver_available, (d))
        caregiver_available = cursor.fetchone()
    except pymssql.Error:
        print("caregiver availability check failed. Please try again!")
        print("Db-Error:", e)
        return
    except Exception as e:
        print("Error occurred when checking for available caregivers. Please try again!")
        print("Error:", e)
        return
    if caregiver_available == None:
        print("No Caregiver is available!")
        return
    else:
        caregiver_selected =  caregiver_available[0]

    try:
        cursor = conn.cursor()
        cursor.execute(vaccine_available, (vaccine_name))
        vaccine_available = cursor.fetchone()  
    except pymssql.Error:
        print("vaccine availability check failed. Please try again!")
        print("Db-Error:", e)
        return
    except Exception as e:
        print("Error occurred when checking vaccine dose availability. Please try again!")
        print("Error:", e)
        return
    if vaccine_available == None:
        print("vaccine isn't available. Choose a different one!")
        return
    elif vaccine_available[1] == 0:
        print("Not enough available doses!")
        return

    try:
        cursor = conn.cursor()
        cursor.execute(appointment_id_select)
        largest = cursor.fetchone()
        if largest[0] == None:
            current_id= 1    
        else: 
            current_id= int(largest[0])+ 1
    except pymssql.Error:
        print("appointment id generation failed. Please try again!")
        print("Db-Error:", e)
        return
    except Exception as e:
        print("Error occurred for appointment id generation. Please try again!")
        print("Error:", e)
        return 
    appointment_id_select = current_id

    print("Appointment ID:", appointment_id_select, "Caregiver Username:", caregiver_selected)

    try:
        cursor = conn.cursor()
        cursor.execute(update_reserved_appointment, (appointment_id_select, d, current_patient.username, caregiver_selected, vaccine_name))
        conn.commit()
    except pymssql.Error:
        print("update operation failed. Please try again!")
        print("Db-Error:", e)
        return
    except Exception as e:
        print("Error occurred when update was made to the appointment table. Please try again!")
        print("Error:", e)
        return

    try:
        cursor = conn.cursor()
        cursor.execute(availability_delete, (date, caregiver_selected))
        conn.commit()
    except pymssql.Error as e:
        print("delete operation failed. Please try again!")
        print("Db-Error:", e)
        return
    except Exception as e:
        print("Error occurred when deleting caregiver availability. Please try again!")
        print("Error:", e)
        return
    
    try:
        vaccine_booked = Vaccine(vaccine_name,0)
        vaccine_booked.get()
        vaccine_booked.decrease_available_doses(1)
    except pymssql.Error as e:
        print("vaccine booking operation failed. Please try again!")
        print("Db-Error:", e)
        return
    except Exception as e:
        print("Error occurred when reducing doses. Please try again!")
        print("Error:", e)
        return
    finally:
        cm.close_connection()


def upload_availability(tokens):
    #  upload_availability <date>
    #  check 1: check if the current logged-in user is a caregiver
    global current_caregiver
    if current_caregiver is None:
        print("Please login as a caregiver first!")
        return

    # check 2: the length for tokens need to be exactly 2 to include all information (with the operation name)
    if len(tokens) != 2:
        print("Please try again!")
        return

    date = tokens[1]
    # assume input is hyphenated in the format mm-dd-yyyy
    date_tokens = date.split("-")
    month = int(date_tokens[0])
    day = int(date_tokens[1])
    year = int(date_tokens[2])
    try:
        d = datetime.datetime(year, month, day)
        current_caregiver.upload_availability(d)
    except pymssql.Error as e:
        print("Upload Availability Failed")
        print("Db-Error:", e)
        quit()
    except ValueError:
        print("Please enter a valid date!")
        return
    except Exception as e:
        print("Error occurred when uploading availability")
        print("Error:", e)
        return
    print("Availability uploaded!")


def cancel(tokens):
    """
    TODO: Extra Credit
    """
    pass


def add_doses(tokens):
    #  add_doses <vaccine> <number>
    #  check 1: check if the current logged-in user is a caregiver
    global current_caregiver
    if current_caregiver is None:
        print("Please login as a caregiver first!")
        return

    #  check 2: the length for tokens need to be exactly 3 to include all information (with the operation name)
    if len(tokens) != 3:
        print("Please try again!")
        return

    vaccine_name = tokens[1]
    doses = int(tokens[2])
    vaccine = None
    try:
        vaccine = Vaccine(vaccine_name, doses).get()
    except pymssql.Error as e:
        print("Error occurred when adding doses")
        print("Db-Error:", e)
        quit()
    except Exception as e:
        print("Error occurred when adding doses")
        print("Error:", e)
        return

    # if the vaccine is not found in the database, add a new (vaccine, doses) entry.
    # else, update the existing entry by adding the new doses
    if vaccine is None:
        vaccine = Vaccine(vaccine_name, doses)
        try:
            vaccine.save_to_db()
        except pymssql.Error as e:
            print("Error occurred when adding doses")
            print("Db-Error:", e)
            quit()
        except Exception as e:
            print("Error occurred when adding doses")
            print("Error:", e)
            return
    else:
        # if the vaccine is not null, meaning that the vaccine already exists in our table
        try:
            vaccine.increase_available_doses(doses)
        except pymssql.Error as e:
            print("Error occurred when adding doses")
            print("Db-Error:", e)
            quit()
        except Exception as e:
            print("Error occurred when adding doses")
            print("Error:", e)
            return
    print("Doses updated!")


def show_appointments(tokens):
    '''
    TODO: Part 2
    '''
    global current_caregiver
    global current_patient
    if current_caregiver is None and current_patient is None:
        print("Please login first!")
        return
    
    if len(tokens) != 1:
        print("Please try again!")
        return

    cm = ConnectionManager()
    conn = cm.create_connection()
    caregiver_schedule = "SELECT appointment_id, Name, Time, Username_P FROM Appointment WHERE Username = (%s) ORDER BY appointment_id"
    patient_schedule = "SELECT appointment_id, Name, Time, Username FROM Appointment WHERE Username_P = (%s) ORDER BY appointment_id"
    try:
        if current_caregiver: 
           cursor = conn.cursor()
           try:
               cursor.execute(caregiver_schedule, (current_caregiver.username))
               print("Appointment_id", " Vaccine_Name", "  Date", "         Patient_name")
               for row in cursor:
                    print(str(row[0]) + "               " + str(row[1]) + "             " + str(row[2]) + "    " + str(row[3]))
           except pymssql.Error:
                print("error occurred when trying to show appointments of caregiver. Please try again!")
                print("Db-Error:", e)
                return
           except Exception as e:
                print("Error occurred for caregiver show appointments. Please try again!")
                print("Error:", e)
                return
        else:
            if current_patient: 
                try:
                    cursor = conn.cursor()
                    cursor.execute(patient_schedule, (current_patient.username))
                    print("Appointment_id", " Vaccine_Name", "  Date", "         Caregiver_name")
                    for row in cursor:
                        print(str(row[0]) + "               " + str(row[1]) + "             " + str(row[2]) + "    " + str(row[3]))
                except pymssql.Error:
                      print("error occurred when trying to show appointments of patient. Please try again!")
                      print("Db-Error:", e)
                      return
                except Exception as e:
                      print("Error occurred for patient show appointments. Please try again!")
                      print("Error:", e)
                      return
    except pymssql.Error:
        print("failed to show appointments. Please try again!")
        print("Db-Error:", e)
        return
    except Exception as e:
        print("error occurred when trying to show appointments. Please try again!")
        print("Error:", e)
        return
    finally:
        cm.close_connection()

def logout(tokens):
    """
    TODO: Part 2
    """
    if len(tokens) != 1:
        print("Please try again!")
        return
    
    global current_caregiver
    global current_patient
    if current_caregiver is None and current_patient is None:
        print("Please login first.")
        return
    elif current_caregiver is not None or current_patient is not None:
       current_patient = None
       current_caregiver = None
       print("Successfully logged out!")
       return
    else:
        print("Please try again!")
        return


def start():
    stop = False
    print()
    print(" *** Please enter one of the following commands *** ")
    print("> create_patient <username> <password>")  # //TODO: implement create_patient (Part 1)
    print("> create_caregiver <username> <password>")
    print("> login_patient <username> <password>")  # // TODO: implement login_patient (Part 1)
    print("> login_caregiver <username> <password>")
    print("> search_caregiver_schedule(mm-dd-yyyy) <date>")  # // TODO: implement search_caregiver_schedule (Part 2)
    print("> reserve(mm-dd-yyyy) <date> <vaccine>")  # // TODO: implement reserve (Part 2)
    print("> upload_availability(mm-dd-yyyy) <date>")
    print("> cancel <appointment_id>")  # // TODO: implement cancel (extra credit)
    print("> add_doses <vaccine> <number>")
    print("> show_appointments")  # // TODO: implement show_appointments (Part 2)
    print("> logout")  # // TODO: implement logout (Part 2)
    print("> Quit")
    print()
    while not stop:
        response = ""
        print("> ", end='')

        try:
            response = str(input())
        except ValueError:
            print("Please try again!")
            break

        #response = response.lower()
        tokens = response.split(" ")
        if len(tokens) == 0:
            ValueError("Please try again!")
            continue
        operation = tokens[0]
        if operation == "create_patient":
            create_patient(tokens)
        elif operation == "create_caregiver":
            create_caregiver(tokens)
        elif operation == "login_patient":
            login_patient(tokens)
        elif operation == "login_caregiver":
            login_caregiver(tokens)
        elif operation == "search_caregiver_schedule(mm-dd-yyyy)":
            search_caregiver_schedule(tokens)
        elif operation == "reserve(mm-dd-yyyy)":
            reserve(tokens)
        elif operation == "upload_availability(mm-dd-yyyy)":
            upload_availability(tokens)
        elif operation == cancel:
            cancel(tokens)
        elif operation == "add_doses":
            add_doses(tokens)
        elif operation == "show_appointments":
            show_appointments(tokens)
        elif operation == "logout":
            logout(tokens)
        elif operation == "quit":
            print("Bye!")
            stop = True
        else:
            print("Invalid operation name!")


if __name__ == "__main__":
    '''
    // pre-define the three types of authorized vaccines
    // note: it's a poor practice to hard-code these values, but we will do this ]
    // for the simplicity of this assignment
    // and then construct a map of vaccineName -> vaccineObject
    '''

    # start command line
    print()
    print("Welcome to the COVID-19 Vaccine Reservation Scheduling Application!")

    start()
