from __future__ import division
from __future__ import unicode_literals
from __future__ import absolute_import
from __future__ import print_function

import csv, re, os

filename = 'donations_2010.csv'
data_folder = os.path.dirname(os.path.realpath(__file__)) + '/data/todo/'

can_import_filename = '2010_importable_donations.csv'
unknown_accounts_filename = '2010_unknown_donations.csv'

def main():
    unsure_rows = []
    sure_rows = []

    # Load a hash of all our existing Salesforce data
    existing_accounts, existing_contacts = load_existing_data()
    print(existing_accounts)
    raise('x')

    # Pull in the data
    with open(data_folder + filename, 'rb') as csvfile:
        next(csvfile, None) # skip header
        reader = csv.reader(csvfile)
        reader.next()
        for row in reader:
            row = [field.strip().decode('utf-8') for field in row]
            parse_row(existing_accounts, existing_contacts, row, sure_rows, unsure_rows)

    # Write out all the maybes into their own spreadsheet

    with open(data_folder + can_import_filename, 'wb') as csvfile:
          writer = csv.writer(csvfile)
          writer.writerow(['Date', 'Account ID', 'Memo', 'Amount'])
          for row in sure_rows:
            try:
              writer.writerow(row)
            except:
              print('#################### Could not encode this row ####################')
              print(row)

    with open(data_folder + unknown_accounts_filename, 'wb') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Date', 'Company Name', 'Name', 'Address', 'Memo', 'Amount', 'Reason not imported'])
        for row in unsure_rows:
            try:
                writer.writerow(row)
            except:
                print('#################### Could not encode this row ####################')
                print(row)


def load_existing_data():
    accounts_filename = 'accounts.csv'
    contacts_filename = 'contacts.csv'
    data_folder = os.path.dirname(os.path.realpath(__file__)) + '/data/exported/'

    existing_accounts = []
    existing_contacts = []

    # Load accounts
    with open(data_folder + accounts_filename, 'rb') as csvfile:
        next(csvfile, None) # skip header
        reader = csv.reader(csvfile)
        reader.next()
        for row in reader:
            row = [field.strip().decode('utf-8') for field in row]
            acct_id, name, billing_street, shipping_street = row
            existing_accounts.append({
                    'account_id': acct_id,
                    'account_name': name,
                    'billing_street': billing_street,
                    'shipping_street': shipping_street
                    })

    # Load contacts
    with open(data_folder + contacts_filename, 'rb') as csvfile:
        next(csvfile, None) # skip header
        reader = csv.reader(csvfile)
        reader.next()
        for row in reader:
            row = [field.strip().decode('utf-8') for field in row]
            account_id, accountt_name, contact_id, contact_name, mailing_street, other_street
            existing_contacts.append({
                    'id': contact_id,
                    'account_name': account_name,
                    'account_id': account_id,
                    'contact_name': contact_name,
                    'mailing_street': mailing_street,
                    'other_street': other_street
                    })

    return [existing_accounts, existing_contacts]

main()
