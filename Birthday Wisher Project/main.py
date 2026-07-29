from datetime import datetime
import pandas
import random
import smtplib
from credentials import MY_EMAIL, MY_PASSWORD

SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587

today = datetime.now()
today_tuple = (today.month, today.day)

data = pandas.read_csv("birthdays.csv")
birthdays_dict = {
    (data_row["month"], data_row["day"]): data_row
    for (index, data_row) in data.iterrows()
}

if today_tuple in birthdays_dict:
    birthday_person = birthdays_dict[today_tuple]

    file_path = f"letter_templates/letter_{random.randint(1, 3)}.txt"
    with open(file_path) as letter_file:
        contents = letter_file.read()
        contents = contents.replace("[NAME]", birthday_person["name"])

    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as connection:
        connection.starttls() 
        connection.login(MY_EMAIL, MY_PASSWORD)
        connection.sendmail(
            from_addr=MY_EMAIL,
            to_addrs=birthday_person["email"],
            msg=f"Subject:Happy Birthday!\n\n{contents}"
        )

    print(f"Birthday email sent to {birthday_person['name']} ({birthday_person['email']}).")
else:
    print("No birthdays today.")