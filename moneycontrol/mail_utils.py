#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Mar 21 17:02:32 2020

@author: nishant.gupta
"""


# Python code to illustrate Sending mail from 
# your Gmail account 
import smtplib 

# import necessary packages
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

class smtp_client :
  @staticmethod
  def send_mail(receipient_address, message, subject) :
    # creates SMTP session 
    s = smtplib.SMTP('smtp.gmail.com', 587) 

    # start TLS for security 
    s.starttls() 

    # Authentication 
    s.login("nishant.gupta.trading", "qpzmQPZM2907") 
    
    msg = MIMEMultipart()       # create a message
    
    # setup the parameters of the message
    msg['From']= "nishant.gupta.trading@cohesity.com"
    msg['To']= receipient_address
    msg['Subject'] = subject
    
        # add in the message body
    msg.attach(MIMEText(message, 'plain'))

    # send the message via the server set up earlier.
    s.send_message(msg)
    
    del msg

    # sending the mail 
    #s.sendmail("nishant.gupta.trading", receipient_address, message) 

    # terminating the session 
    #s.quit()