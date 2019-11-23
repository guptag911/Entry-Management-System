# Entry-Management-System
We need an application, which can capture the Name, email address, phone no of the visitor and same information also needs to be captured for the host on the front end. At the back end, once the user enters the information in the form, the backend should store all of the information with time stamp of the entry. This should trigger an email and an SMS to the host informing him of the details of the visitor. There should also be a provision of the checkout time which the guest can provide once he leaves. This should trigger an email to the guest with the complete form which should include:

1. Name
2. Phone
3. Check-in time,
4. Check-out time,
5. Host name
6. Address visited.

### Language and API used
1. Python
2. Tkinter for GUI
3. Twilio for SMS services
4. SMTP for email services

### API Requirements
1. MySql
2. Python 3.6

### Extra Requirements
1. Gmail Account
2. Twilio Account

### Install required packages and libraries
1. Download the repository
2. open cmd and navigate to the download folder where repository is downloaded
3. Execute "python -m pip install -r requirements.txt"

Caution::Install python3.6 and check to add path to path variables.Ensure pip is installed on your system.

### Software in Action

Start Screen of the Application where Visitor can check in
![Start Screen of the Software](https://github.com/theannoying/Entry-Management-System/blob/master/images/startScreen.PNG)


Check-Out screen where visitor can Check-out
![Check-Out Screen of the Software](https://github.com/theannoying/Entry-Management-System/blob/master/images/Check-out.PNG)


When user details are valid and saved sucessfully!
![Saved Details](https://github.com/theannoying/Entry-Management-System/blob/master/images/saved%20details.PNG)


### How the application works?

This application is coded in Python 3.6 and GUI is implemented using tkinter.For SMS system twilio API is used and for email SMTP service is used.When visitor arrives ,he/she enters the details of the host as well of themselves.If the details are correct , the host receives a sms and email stating visitor's name and his contact number.MySQl is used to store the data with chech-in time as the current timestamp.If same visitor details are given again before check-out a popup is displayed.Even if the user enters wrong details a popup is displayed stating the same.During checkout the visitor check-out time is updated with current timestamp and the visitor gets an email stating all the details along with check-in and check-out time.Exception handling is used to handle the exception and errors.
The tester should have a twilio account for using this application along with a gmail ID.
