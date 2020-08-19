from flask import Flask, render_template,redirect,url_for,request
from sendemail.sendemail import send_out_mail
import os
from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv('.env')) #look for the .env file
application = Flask(__name__) #init the flask application
application.config['SECRET_KEY']  = os.getenv('SEC_KEY') #get secret key from environment

#main page
@application.route('/')
def main():
    color = ''
    try: #check if it is a success or fail message and give color a value
        if 'Success' in request.args.get('message'):
            color = 'green'
        if 'Fail' in request.args.get('message'):
            color = 'red'
    except Exception:
        pass
    return render_template('index.html',message=request.args.get('message'),color=color)

#handles form submissions
@application.route('/submit',methods=['POST'])
def submit():
    if request.method == 'POST':
        email = request.form.get('email') #gets input value from the email field
        try:
            send_out_mail(email)
            message = 'Successfully sent to {}'.format(email)
        except Exception as error:
            print(error)
            message = 'Fail to send please try again later!'
        return redirect(url_for('main',message=message)) #redirect to the main page and pass in a GET message

if __name__ == '__main__':
    application.run(debug=False)
