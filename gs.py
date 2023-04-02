import time
from bs4 import BeautifulSoup
import requests
from unidecode import unidecode
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication

# Define your email and password for authentication
email_address = ""
email_password = ""

# Define the recipient email address
recipient_email = ""

# Define the search texts
search_texts = ["kara gümrük", "karagümrük", "fatih", "satış", "satışa çıktı", "çıktı", "satışta", "bilet", "biletleri"]

while True:
    # Define the message body
    message_body = ""

    # Get the search results from the Galatasaray website
    url = "https://www.galatasaray.org/anasayfa"
    req = requests.get(url)
    soup = BeautifulSoup(req.text, "html.parser")

    found_results = []
    for search_text in search_texts:
        variations = [search_text, search_text.lower(), search_text.upper(), search_text.capitalize(), search_text.title(),
                      unidecode(search_text), unidecode(search_text.lower()), unidecode(search_text.upper()),
                      unidecode(search_text.capitalize()), unidecode(search_text.title()), search_text.replace("i", "İ"),
                      search_text.lower().replace("i", "İ")]

        # Add variations with accents and special characters

        # Add variation with lowercase letter i replaced with uppercase İ

        # Manually replace uppercase "I" with uppercase "İ"
        for i in range(len(variations)):
            if "I" in variations[i]:
                variations[i] = variations[i].replace("I", "İ")

        # Add variation with all uppercase letters
        variations.append(search_text.upper())

        # Add variation with all capitalized words
        variations.append(search_text.title())

        # Add variation with all uppercase letters and capitalized words
        variations.append(search_text.upper().title())

        for text in variations:
            results = soup.find_all(string=lambda t: text in t)
            if results:
                for result in results:
                    if result not in found_results:
                        found_results.append(result)

    # Format the email message body
    if found_results:
        message_body = "The following results were found:\n\n"
        for result in found_results:
            message_body += result + "\n"
    else:
        message_body = "No results found."

    # Define the email message
    message = MIMEMultipart()
    message["Subject"] = "Galatasaray Website Search Results"
    message["From"] = email_address
    message["To"] = recipient_email
    message.attach(MIMEText(message_body))

    # Create an SMTP connection
    with smtplib.SMTP("smtp.gmail.com", 587) as smtp:
        smtp.starttls()
        smtp.login(email_address, email_password)

        # Send the email
        smtp.sendmail(email_address, recipient_email, message.as_string())

    # Wait for 30 minutes before searching again
    time.sleep(1800)
