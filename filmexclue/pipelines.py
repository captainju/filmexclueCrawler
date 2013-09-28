import config
import json
from scrapy.exceptions import DropItem
import smtplib
from subprocess import Popen, PIPE
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


class FilmexcluePipeline(object):

    def process_item(self, item, spider):
        return item

    def close_spider(self, spider):
        emailMessage = ''
        #get all new items
        for newLine in open('itemsNew.json'):
            if newLine != '':
                jsonNodes = json.loads(newLine)
                emailMessage += '<div>\n<a href="'+jsonNodes['url'][0]+'">\n<h2>'+jsonNodes['title'][0]+'</h2>\n'
                emailMessage += '<img style="max-width:300px" src="'+jsonNodes['imgurl'][0]+'"/>\n'
                emailMessage += '<br><i>'+jsonNodes['desc'][0]+'</i>'
                emailMessage += '</a>\n</div>\n<div>&nbsp;</div>\n<hr>\n'

        if emailMessage != '':
            self.sendEmail(emailMessage.encode("utf-8"))

        fileitems = open('items.json', 'a')
        for line in open('itemsNew.json'):
            fileitems.write(line)

        fileitems.close()
        open('itemsNew.json', 'w').close()


    def sendEmail(self, message):
        SUBJECT = 'Derniers films'
        COMMASPACE = ', '
        # Create the container (outer) email message.
        msg = MIMEMultipart('alternative')
        msg['Subject'] = SUBJECT
        # me == the sender's email address
        # family = the list of all recipients' email addresses
        msg['From'] = config.mailfrom
        msg['To'] = COMMASPACE.join(config.mailto)
        msg.preamble = SUBJECT

        text = message
        html = """\
        <html>
          <head></head>
          <body>
            """+message+"""
          </body>
        </html>
        """

        # Record the MIME types of both parts - text/plain and text/html.
        part1 = MIMEText(text, 'plain')
        part2 = MIMEText(html, 'html')

        # Attach parts into message container.
        # According to RFC 2046, the last part of a multipart message, in this case
        # the HTML message, is best and preferred.
        msg.attach(part1)
        msg.attach(part2)

        # Send the message via local SMTP server.
        #s = smtplib.SMTP(config.mailsmtp)
        # sendmail function takes 3 arguments: sender's address, recipient's address
        # and message to send - here it is sent as one string.
        #s.sendmail(config.mailfrom, config.mailto, msg.as_string())
        #s.quit()

        p = Popen(["/usr/sbin/sendmail", "-t"], stdin=PIPE)
        p.communicate(msg.as_string())

class JsonWriterPipeline(object):

    def __init__(self):
        open('itemsNew.json', 'w').close()
        open('items.json', 'a').close()

    def process_item(self, item, spider):
        if '[TS]' in item['title'][0]:
            raise DropItem("TS in '%s'" % item['title'][0])

        if '[CAM]' in item['title'][0]:
            raise DropItem("CAM in '%s'" % item['title'][0])
        
        fileNew = open('itemsNew.json', 'a')
        line = json.dumps(dict(item)) + "\n"
        if not line in open('items.json').read():
            fileNew.write(line)
        fileNew.close()
        
        return item
