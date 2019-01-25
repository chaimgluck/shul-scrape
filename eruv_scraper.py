from botocore.vendored import requests
from bs4 import BeautifulSoup
import boto3
import datetime

ses = boto3.client('ses')

from_email = ''
recipient_list = []
today = datetime.datetime.today().strftime('%A, %m-%d-%Y')
emaiL_subject = 'Shul Info: ' + today
CHARSET = "UTF-8"

def eruv_scrape(event, context):
    url = 'https://www.yikendall.com/'
    page = requests.get(url).text
    soup = BeautifulSoup(page)
    page_text = [p.get_text().strip().encode('utf8') for p in soup('p') if len(p.get_text().strip()) > 0]
    relevant_text = page_text[5:]
    text = [i.split('\n') for i in relevant_text]
    text = [item for sublist in text for item in sublist]
    text.insert(0, text.pop(4))
    text = [x.replace("\xc2\xa0", "") for x in text]
    text = [i.strip('()').replace(' (', ' - ') for i in text]
    body_text = '\n'.join(text)
    text = ['<p style="text-decoration:underline">' + i + '</p>' if text.index(i) in [2, 5, 11] else i for i in text]
    text = [i + ':' if text.index(i) in [1, 10, 12, 14] else i for i in text]
    text = ['<b>' + i + '</b>' if text.index(i) in [0, 1, 10] else i for i in text]
    text = ['<p>' + i + '</p>' if text.index(i) not in [0, 2, 5, 11] else i for i in text]
    html_string = '<html><head></head><body>'
    for i in text:
        if text.index(i) == 0:
            if 'up' in i.lower():
                html_string += '<p style="color:green">' + i + '</p><hr>'
            else:
                html_string += '<p style="color:red">' + i + '</p><hr>'
        elif text.index(i) in [9]:
            html_string += i + '<hr>'
        else:
            html_string += i
    html_string += '</body></html>'

    response = ses.send_email(
        Source = from_email,
        Destination={
            'ToAddresses': recipient_list
        },
        Message={
            'Subject': {
                'Charset': CHARSET,
                'Data': emaiL_subject
            },
            'Body': {
                'Html': {
                    'Charset': CHARSET,
                    'Data': html_string
                },
                'Text': {
                    'Charset': CHARSET,
                    'Data': body_text
                }
            }
        }
    )
