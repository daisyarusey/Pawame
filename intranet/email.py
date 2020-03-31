from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

def send_credentials(password,username,reciever):
    subject = 'Pawame Password Management.'
    sender = 'danielevans.karani@gmail.com'

    #passing in the context variables
    text_content = render_to_string('email/passwordemail.txt', {"password":password, "username":username})
    html_content =  render_to_string('email/passwordemail.html',{"password":password, "username":username})
    msg = EmailMultiAlternatives(subject,text_content,sender,[reciever])
    msg.attach_alternative(html_content, 'text/html')
    msg.send()
