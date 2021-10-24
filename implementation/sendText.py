"""
Sends a text message or email to a user. This file should be triggered when the computer vision 
detects a person about to jump
Authors: Alex Hoerler, Netra Gandhi, Girish Hari, Rachel Mittal
"""

import boto3
import os
from cred import aws_access_key_id, aws_secret_access_key

def sendMessage():
    """
    Sends a message 
    return: a string acknowledging that the message has successfully been sent
    """
    client = boto3.client('sns', region_name='us-east-1', aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key)
    
    topicArn = "arn:aws:sns:us-east-1:301338784186:phone-numbers"
    subject = "SOMEONE COULD NEED HELP"
    message = "For whoever's reading this,\n\nOn the CULC roof, someone could need help! Please check it out!"
    response = client.publish(TopicArn = topicArn, Subject = subject, Message = message)

    return "Message sent successfully"

