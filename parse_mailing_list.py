#!/usr/bin/python
from __future__ import division
from __future__ import unicode_literals
from __future__ import absolute_import
from __future__ import print_function
import csv, re, os
from ccc.lib.account import Account
from ccc.lib.address import Address
from ccc.lib.contact import Contact

filename = 'clean_mailing_list_1.csv'
data_folder = os.path.dirname(os.path.realpath(__file__)) + '/data/todo/'

def main():
    # Reload all the existing data that we have already parsed
    Account.load_all()
    Contact.load_all()
    with open(data_folder + filename, 'rb') as csvfile:
        next(csvfile, None) # skip header
        reader = csv.reader(csvfile)
        reader.next()
        for row in reader:
            row = [field.strip().decode('utf-8') for field in row]
            parse_row(row)

def parse_row(row):
    first_name = row[0]
    last_name = row[1]
    organization = row[2]
    street = row[3]
    city = row[4]
    state = row[5]
    zip_code = row[6]
    country = row[7] or 'USA'
    title = row[8]

    if is_individual(first_name, last_name, organization):
        handle_individual(first_name, last_name, organization, street, city, state, zip_code, country, title)

    elif is_organization(first_name, last_name, organization):
        handle_organization(first_name, last_name, organization, street, city, state, zip_code, country, title)

    elif is_multiple(first_name, last_name, organization):
        handle_multiple(first_name, last_name, organization, street, city, state, zip_code, country, title)

    else:
        print('XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX')
        print('')
        print('Could not parse {}'.format(','.join(row)))

def can_split(name):
    split_keys = [' & ', ' and ']
    for k in split_keys:
        split_names = name.split(k)
        if len(split_names) == 2:
            return True
    False

def is_individual(first_name, last_name, organization):
    if not(first_name and last_name):
        return False

    if can_split(first_name):
        return False

    return True

def handle_individual(first_name, last_name, organization, street, city, state, zip_code, country, title):
    first_name = first_name.replace(title, '').strip()
    last_name = last_name.replace(title, '').strip()

    account_name = organization or "{} {}".format(first_name, last_name)
    is_individual = organization != account_name
    account_type = 'Individual' if is_individual else 'Other'
    account_address = Address(type = 'Home' if is_individual else 'Work',
                               street = street,
                               city = city,
                               state = state,
                               zip = zip_code,
                               country = country)

    account = Account.get_or_create(name=account_name,
                                    type='Individual',
                                    shipping_address = account_address)

def is_organization(first_name, last_name, organization):
    return not(first_name or last_name) and bool(organization)

def handle_organization(first_name, last_name, organization, street, city, state, zip_code, country, title):
    False

def is_multiple(first_name, last_name, organization):
    return can_split(first_name)

def handle_multiple(first_name, last_name, organization, street, city, state, zip_code, country, title):
    False

main()
#for account in Account.all_accounts.values():
    #print(account.to_a())
