from __future__ import division
from __future__ import unicode_literals
from __future__ import absolute_import
from __future__ import print_function

import csv, re, os

year = 'all'

filename = 'donations_{}.csv'.format(year)
data_folder = os.path.dirname(os.path.realpath(__file__)) + '/data/todo/'

can_import_filename = '{}_importable_donations.csv'.format(year)
unknown_accounts_filename = '{}_unknown_donations.csv'.format(year)

def main():
    unsure_rows = []
    sure_rows = []

    # Load a hash of all our existing Salesforce data
    existing_accounts, existing_contacts = load_existing_data()

    # Pull in the data
    with open(data_folder + filename, 'rb') as csvfile:
        next(csvfile, None) # skip header
        reader = csv.reader(csvfile)
        reader.next()
        for row in reader:
            row = [field.strip().decode('utf-8') for field in row]
            parse_row(existing_accounts, existing_contacts, row, sure_rows, unsure_rows)

    # Write out all the data that can be imported
    with open(data_folder + can_import_filename, 'wb') as csvfile:
          writer = csv.writer(csvfile)
          writer.writerow(['Close Date', 'Account ID', 'Description', 'Amount', 'Stage', 'Probability', 'Name'])
          for row in sure_rows:
            try:
              writer.writerow(row + ['Posted',100,'Donation'])
            except:
              print('#################### Could not encode this row ####################')
              print(row)

    # Write out all unrecognized data into its own spreadsheet
    with open(data_folder + unknown_accounts_filename, 'wb') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Date', 'Company Name', 'Name', 'Address', 'Memo', 'Amount', 'Reason not imported'])
        for row in unsure_rows:
            try:
                writer.writerow(row)
            except:
                print('#################### Could not encode this row ####################')
                print(row)

def parse_row(existing_accounts, existing_contacts, row, sure_rows, unsure_rows):
    txn_type, date, txn_num, company_name, full_name, address, memo, method, amount, extra = row
    amount = float(str(amount).replace(',','')) # The amounts in the original sheet are comma-delimited

    acct, confident_in_acct = find_account(existing_accounts, full_name, company_name, address)
    if confident_in_acct:
        sure_rows.append([date, acct['account_id'], memo, amount])
        return

    # At this point, I know we're not confident in the account, so look for a contact that we are confident in
    contact, confident_in_contact = find_contact(existing_contacts, full_name, company_name, address)
    if confident_in_contact:
        sure_rows.append([date, contact['account_id'], memo, amount])
        return

    # Now, we're not confident in the account or the contact
    reason = ''
    if None is not acct:
        reason = 'Possible account: {}'.format(acct['account_name'])
    elif None is not contact:
        reason = 'Possible contact: {} ({})'.format(contact['contact_name'], contact['account_name'])
    else:
        reason = 'No possible match'

    unsure_rows.append(row + [reason])

def find_account(existing_accounts, full_name, company_name, address):
    for acct in existing_accounts:
        if acct['account_name'] == full_name:
            return acct, True
        elif acct['account_name'] == company_name:
            return acct, True

    return None, False

def find_contact(existing_contacts, full_name, company_name, address):
    for contact in existing_contacts:
        if contact['contact_name'] == full_name:
            return contact, True
        elif contact['contact_name'] == company_name:
            return contact, True

    return None, False

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
            account_id, account_name, billing_street, shipping_street = row
            existing_accounts.append({
                    'account_id': account_id,
                    'account_name': account_name,
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
            account_id, account_name, contact_id, contact_name, mailing_street, other_street = row
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
