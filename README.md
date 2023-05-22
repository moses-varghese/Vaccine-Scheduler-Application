# Vaccine-Scheduler-Application

A common type of application that connects to a database is a reservation system, where users schedule time slots for some centralized resource. In this project we will program part of an appointment scheduler for vaccinations, where the users are patients and caregivers keeping track of vaccine stock and appointments. This application runs on the command line terminal that can be deployed by hospitals or clinics and supports interaction with users, and connects to a database server created with Microsoft Azure account. 

We store patient information, and lets them interactively schedule their vaccine appointments. Caregivers use to manage the appointment slots and inventory.

The following are the entity sets in our database schema design:
● Patients: these are customers that want to receive the vaccine.
● Caregivers: these are employees of the health organization administering the vaccines.
● Vaccines: these are vaccine doses in the health organization's inventory of medical
supplies that are on hand and ready to be given to the patients.

Features of the application: Creation of profile for patient and caregiver with encrypted passwords by salting and hashing, reserve appointments and vaccines, display and search for available appointments and vaccine inventory, add vaccines and appointments to the database, login and logout of the application as patient or caregiver, cancel existing appointments by patient or caregiver.

