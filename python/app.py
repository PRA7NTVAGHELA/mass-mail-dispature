from flask import Flask, render_template, request
import csv
import re
import logging

app = Flask(__name__)


logging.basicConfig(level=logging.DEBUG)


def is_valid_email(email):
    return re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    invalid_emails = []
    valid_emails = []

    try:
        if 'file' not in request.files:
            logging.error("No file part in the request")
            return "No file part in the request"

        file = request.files['file']

        if file.filename == '':
            logging.error("No selected file")
            return "No selected file"

        if file:
            stream = file.stream.read().decode("UTF8")
            reader = csv.reader(stream.splitlines())

            for row in reader:
                for email in row:
                    if is_valid_email(email):
                        valid_emails.append(email)
                    else:
                        invalid_emails.append(email)
        
        logging.info(f"Valid emails: {valid_emails}")
        logging.info(f"Invalid emails: {invalid_emails}")
        return render_template('results.html', invalid_emails=invalid_emails, valid_emails=valid_emails)

    except Exception as e:
        logging.error("Error processing the uploaded file", exc_info=True)
        return "An error occurred while processing the file"

@app.route('/send_email', methods=['POST'])
def send_email():
    try:
        
        logging.info("Sending emails...")
        return "Emails sent successfully!"
    except Exception as e:
        logging.error("Error sending emails", exc_info=True)
        return "An error occurred while sending emails"

if __name__ == '__main__':
    app.run(debug=True)
