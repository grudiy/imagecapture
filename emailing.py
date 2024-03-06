# Now gmail smtp doesn't work in such way, you need to create an app in google console, with
# client id, client secret and implement oauth.
# But will leave the code here to remember implementation in the future
import imghdr
import smtplib
from email.message import EmailMessage

PASSWORD = "********"
SENDER = "somegmail@gmail.com"
RECEIVER = "myemailIwantToReceive@gmail.com"


def send_email(image_path):
    email_message = EmailMessage()
    email_message["Subject"] = "Alarm! New Object on the Camera"
    email_message.set_content("Hey! See Captured Object in attach!")

    with open(image_path, "rb") as file:
        content = file.read()
    email_message.add_attachment(content, maintype="image", subtype=imghdr.what(None, content))

    gmail = smtplib.SMTP("smtp.gmail.com", 587)
    gmail.ehlo()
    gmail.starttls()
    gmail.login(SENDER, PASSWORD)
    gmail.sendmail(SENDER, RECEIVER, email_message.as_string())
    gmail.quit()

if __name__ == "__main__":
    send_email(image_path="images/11.png")
