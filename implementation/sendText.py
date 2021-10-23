"""
Sends a text message or email to a user.
Authors: Alex Hoerler, Netra Gandhi, Girish Hari, Rachel Mittal
"""

import boto3
client = boto3.client('sns')

def sendMessage():
    topicArn = "arn:aws:sns:us-east-1:301338784186:phone-numbers"
    subject = "SOMEONE COULD NEED HELP"
    message = "For whoever's reading this,\n\nOn the CULC roof, someone could need help! Please check it out!"
    response = client.publish(TopicArn = topicArn, Subject = subject, Message = message)

    return "Message sent successfully"


if __name__ == '__main__':

    sendMessage()