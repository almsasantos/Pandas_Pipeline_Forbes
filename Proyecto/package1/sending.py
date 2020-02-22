import os
import smtplib
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
import os.path
import email
import glob
import re
import stdiomask


def sending_email(want_results):
    if want_results == 'y':
        print("To send you an email with your we'll need some information:")
        os.environ['sender_email'] = input('Please enter your personal gmail account: ').strip()
        os.environ['sender_password'] = stdiomask.getpass('Please enter your matching password: ')
        #os.environ['sender_password'] = 'sender_password'
        #os.environ['sender_email'] = 'sender_email'

        # For this function to work you need to unable the settings here: https://myaccount.google.com/lesssecureapps
        if 'sender_password' not in os.environ:
            raise ValueError('You must enter a password')
        elif 'sender_email' not in os.environ:
            raise ValueError('You must enter an email')


        #For the next 2 lines of code to work you need to create those two variables in os.environ
        sender_email = os.environ['sender_email']
        sender_password = os.environ['sender_password']

        server_email = 'smtp.gmail.com'
        server_port = 587
        receiver = input('Write the email you want to send the results to: ').strip()
        try:
            server = smtplib.SMTP(server_email, server_port)
            server.ehlo()
            server.starttls()  # So the message will be encripted
            server.ehlo()
            server.login(sender_email, sender_password)

        except:
            print('Connection not working, try again later')

        while not re.match(r"[^@]+@[^@]+\.[^@]+", receiver):
            print("The email you just entered it's not correct")
            receiver = input('Please try again: ')
        print(f'Sending email to {receiver}')


        img_data = open('../data/results/results.pdf', 'rb').read()
        msg = MIMEMultipart()
        msg['Subject'] = 'Results from billionaires in 2018'
        msg['From'] = sender_email
        msg['To'] = receiver

        text = MIMEText('Below you have your desired results from the analysis of the most billionaires in 2018!')
        msg.attach(text)
        data_pdf = MIMEApplication(img_data, name=os.path.basename('results.pdf'))
        msg.attach(data_pdf)

        server.sendmail(msg['From'], msg['To'], msg.as_string())

        print('Go check your email inbox, there you have it!')

        server.close()

    elif want_results == 'n':
        print('Thanks for participating!')
