import pandas
import smtplib
import datetime as dt
from random import choice

# EMAIL SETUP
MY_EMAIL = "your@mail.com"
SMTP_CONFIG = "your_smtp_server"
MY_PASSWORD = "your_password"
MY_PORT = 0

# LETTER TEMPLATES
LETTER_LIST = ["letter_1.txt", "letter_2.txt", "letter_3.txt"]

# RANDOM LETTER
letter_random = f"./letter_templates/{choice(LETTER_LIST)}"
with open(letter_random, "r") as f:
    letter_template = f.read()

# GET DATE
actual_date = dt.datetime.now()
today = f"{actual_date.day}.{actual_date.month}"

# GET DATA - BIRTHDAYS
data_read = pandas.read_csv("birthdays.csv")
data = data_read.to_dict(orient="records")

# CHECK IF ITS BIRTHDAY
for i in data:
    birthday = f"{i['day']}.{i['month']}"
    if birthday == today:
        # WRITE LETTER
        with open(f"./letters_send/{birthday}_letter_to_{i['name']}", "w") as letter:
            new_text = letter_template.replace("[NAME]", i["name"])
            letter.write(new_text)
        birthday_email = i['email']

        # SEND EMAIL
        with smtplib.SMTP(SMTP_CONFIG, port=MY_PORT) as connection:
            connection.starttls()
            connection.login(user=MY_EMAIL, password=MY_PASSWORD)
            connection.sendmail(from_addr=MY_EMAIL,
                                to_addrs=birthday_email,
                                msg=f"Subject:Happy Birthday {i['name']}\n\n"
                                    f"{new_text}")
