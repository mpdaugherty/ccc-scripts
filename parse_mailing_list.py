#!/usr/bin/python
from __future__ import division
from __future__ import unicode_literals
from __future__ import absolute_import
from __future__ import print_function
import csv, re, os
from ccc.lib.account import Account
from ccc.lib.address import Address
from ccc.lib.contact import Contact

filename = 'mailing_list_master.csv'
data_folder = os.path.dirname(os.path.realpath(__file__)) + '/data/'

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

titles = ['Assessor-Recorder', 'Supervisor', 'Governor', 'Senator', 'Mayor', 'Mr.', 'Mrs.', 'M.']
def parse_row(row):
    first_name = row[1]
    last_name = row[2]
    organization_name = row[3]
    address_1 = row[4]
    city = row[5]
    state = row[6]
    zip_code = row[7]
    country = row[8] or 'USA'
    title = ([t for t in titles if (t in first_name or t in last_name)] or [u''])[0]
    first_name = first_name.replace(title, '').strip()
    last_name = last_name.replace(title, '').strip()

    account_name = organization_name or "{} {}".format(first_name, last_name)
    is_individual = organization_name != account_name
    account_type = 'Individual' if is_individual else 'Other'
    account_address = Address(type = 'Home' if is_individual else 'Work',
                               street = address_1,
                               city = city,
                               state = state,
                               zip = zip_code,
                               country = country)

    account = Account.get_or_create(name=account_name,
                                    type='Individual',
                                    shipping_address = account_address)


main()
for account in Account.all_accounts.values():
    print(account.to_a())
