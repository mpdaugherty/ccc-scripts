from __future__ import division
from __future__ import unicode_literals
from __future__ import absolute_import
from __future__ import print_function

import csv, re, os

from ccc.lib.account import Account
from ccc.lib.address import Address
from ccc.lib.contact import Contact
from ccc.lib import util

filename = 'donations_all.csv'
data_folder = os.path.dirname(os.path.realpath(__file__)) + '/data/todo/'

unparseable_accounts_filename = 'unparseable_accounts.csv'

def main():
    unsure_rows = []

    # Pull in the data
    with open(data_folder + filename, 'rb') as csvfile:
        next(csvfile, None) # skip header
        reader = csv.reader(csvfile)
        reader.next()
        for row in reader:
            row = [field.strip().decode('utf-8') for field in row]
            parse_row(row, unsure_rows)

    # Write out all the data that can be imported
    Account.write_all()
    Contact.write_all()

    # Write out all unrecognized data into its own spreadsheet
    with open(data_folder + unparseable_accounts_filename, 'wb') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Date', 'Company Name', 'Name', 'Address', 'Memo', 'Amount', 'Reason not imported'])
        for row in unsure_rows:
            try:
                writer.writerow(row)
            except:
                print('#################### Could not encode this row ####################')
                print(row)


address_regex = re.compile('^(.*), (\w{2}) ?(\d{5}(?:-\d{4})?)')
def parse_row(row, unsure_rows):
    txn_type, date, txn_num, company_name, full_name, address, memo, method, amount, extra = row
    amount = float(str(amount).replace(',','')) # The amounts in the original sheet are comma-delimited

    if not (company_name or full_name or address):
        unsure_rows.append(row + ['No name specified'])
        return

    acct, confident_in_acct = None, False
    acct1, confident_in_acct1 = Account.fuzzy_match(full_name, address)
    acct2, confident_in_acct2 = Account.fuzzy_match(company_name, address)
    if confident_in_acct1 or confident_in_acct2:
        # This donation has a matched account already, so we can just return. When we parse the donations spreadsheet later, we'll catch it.
        return
    else:
        acct = acct1 or acct2

    if acct and (not confident_in_acct):
        unsure_rows.append(row + ['Unsure match with Account: {}'.format(acct.name)])
        return

    contact, confident_in_contact = Contact.fuzzy_match(full_name, address)
    if confident_in_contact:
        # This donation has a matched contact; just return
        return
    elif contact:
        unsure_rows.append(row + ['Unsure match with Contact: {} {}'.format(contact.first_name, contact.last_name)])
        return

    # So now we know there is no matching account or contact for the donation. Therefore, make some
    title, full_name = util.extract_honorific(full_name)
    first_name, last_name = ' '.join(full_name.split(' ')[0:-1]), full_name.split(' ')[-1]
    street, city, state, zip_code, country = ['', '', '', '', 'USA'] # Note, we can't parse the city out of the addresses; I may be able to do it manually before importing.
    match = address_regex.search(address)
    if match:
        street, state, zip_code = match.groups()

    if util.is_individual(first_name, last_name, company_name):
        util.create_individual(first_name, last_name, company_name, street, city, state, zip_code, country, title)

    elif util.is_organization(first_name, last_name, company_name):
        util.create_organization(first_name, last_name, company_name, street, city, state, zip_code, country, title)

    elif util.is_multiple(first_name, last_name, company_name):
        util.create_multiple(first_name, last_name, company_name, street, city, state, zip_code, country, title)

main()
