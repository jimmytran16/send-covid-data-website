import smtplib, ssl, csv
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import schedule
import time
from datetime import datetime, timedelta
from covid.scrapcovid import scrap_from_new_website #import the function that returns a dictionary of states and its data
from dotenv import load_dotenv,find_dotenv #get the functions to load the variables inside .env
import os

def send_out_mail(email_to_send_to):
    load_dotenv(find_dotenv('../.env')) #function to look for the .env file to find the variables
    #get the states and data dictionary
    state_dict = scrap_from_new_website()
    sender_email = os.environ.get('EMAIL')
    password = os.environ.get("PASSWORD")
    today_date = (datetime.today() - timedelta(days=1)).strftime('%m-%d-%y')
    subject_field = f"COVID-19 STATUS UPDATE for {today_date}"
    str = ''
    for state,data in state_dict.items(): #iterate through the dict, and populating the data in to the rows of the html string
        str = str + '<tr><th>{}</th><th>{}</th><th>{}</th><th>{}</th><th>{}</th></tr>'.format(state,data[0],data[1],data[2],data[3]) #concatenate the rows into the strings

    # Create the plain-text and HTML version of your message
    text = """\
    This is a test email!!
    """
    html = """\
    <html>
    <style type="text/css" media="screen">
    td, th {
    border: 1px solid #dddddd;
    </style>
      <body>
        <p>Good Afternoon. Here is an update on yesterday's COVID-19 status in the United States. </p>
        <table>
        <tr><th><b>State</b></th><th><b>Total Cases</b></th><th><b>New Cases</b></th><th><b>Total Deaths</b></th><th><b>New Deaths</b></th></tr>
        """+str+"""
        </table>
      </body>
    </html>
    """

    # Turn these into plain/html MIMEText objects
    part1 = MIMEText(text, "plain")
    part2 = MIMEText(html, "html")
    names = {}
    names['receiver'] = email_to_send_to
    # Create secure connection with server and send email
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(sender_email, password)
        for company_name, company_email in names.items():
            try:
                message = MIMEMultipart("alternative")
                message["Subject"] = subject_field
                message["From"] = sender_email
                message["To"] = company_email

                # Add HTML/plain-text parts to MIMEMultipart message
                # The email client will try to render the last part first
                message.attach(part1)
                message.attach(part2)
                server.sendmail( #send the email
                    sender_email, company_email, message.as_string()
                )
                print(f'Success send email to {company_email}')
            except Exception as error:
                print(f'Fail to send email to {company_email}')
