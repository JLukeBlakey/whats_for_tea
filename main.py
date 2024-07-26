#!/usr/bin/env python3

import yaml
import random
import smtplib
from email.message import EmailMessage
import requests
from html.parser import HTMLParser
from dotenv import dotenv_values
from dotenv import load_dotenv
import os

load_dotenv()
recipients = {
    **dotenv_values(".env.emails")
}
hc_url = os.getenv('HC_URL')
smtp_ip = os.getenv('SMTP_IP')
meals = []
shopping_list = {}
recipes = yaml.safe_load(open("recipes.yaml"))
regulars = open("regulars.txt")
kristoff_open = "Bonjour, Kristoff here. Here's your shopping plan for this week:\n"
oddbox_data = []


def create_meal_plan():
    while len(meals) != 5:
        random_meal = random.choice(list(recipes))
        if random_meal not in meals:
            meals.append(random_meal)
    schedule = "\nMonday: " +  meals[0] + "\nTuesday: " + meals[1] + "\nWednesday: " + meals[2] + "\nThursday: " + meals[3] + "\nFriday: " + meals[4] + "\n"

    return schedule


def create_shopping_list(meals):
    for meal in meals:
        for ingredient, quantity in recipes[meal].items():
            if ingredient in shopping_list and shopping_list[ingredient][1] == quantity[1]:
                shopping_list[ingredient][0] = shopping_list[ingredient][0] + quantity[0]
            else:
                shopping_list[ingredient] = []
                shopping_list[ingredient].append(quantity[0])
                shopping_list[ingredient].append(quantity[1])

    # convert to readable string
    shopping_list_string = ""
    for k, v in sorted(shopping_list.items()):
        shopping_list_string = shopping_list_string + k + " (" + str(v[0]) + " " + v[1] + ")\n"

    return shopping_list_string


def email(content):
    for address in recipients:
        msg = EmailMessage()
        msg.set_content(content)
        msg["Subject"] = "Weekly Shop"
        msg["From"] = "kristoff@cyclingpenguin.uk"
        msg["To"] = recipients[address]
        mail = smtplib.SMTP(smtp_ip)
        mail.send_message(msg)
        mail.quit


class oddbox_html_parser(HTMLParser):
    def handle_data(self, data):
        oddbox_data.append(str.lower(data))


def oddbox(food):
    oddbox_html = requests.get("https://www.oddbox.co.uk/box-contents2")
    parser = oddbox_html_parser()
    parser.feed(oddbox_html.text)

    if food == "veg":
        items = oddbox_data[oddbox_data.index("small") + 1]
    elif food == "fruit":
        items = oddbox_data[oddbox_data.index("small") + 2]

    items = items.strip(".*")
#    items = items.split(sep=", ")

    return items


def main():
    content = kristoff_open \
          + create_meal_plan() \
          + "\nIngredients:\n" \
          + create_shopping_list(meals) \
          + "\nDon't forget the regulars!\n" \
          + regulars.read() \
          + "\nThis is what oddbox is delivering this week:" + "\n" \
          + "Veg: {}\n".format(oddbox("veg")) \
          + "\nKristoff out."

    email(content)

    if hc_url:
        requests.get(hc_url)


main()
