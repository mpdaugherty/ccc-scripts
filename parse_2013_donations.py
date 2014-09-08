from __future__ import division
from __future__ import unicode_literals
from __future__ import absolute_import
from __future__ import print_function

import csv, re, os
from ccc.lib.account import Account
from ccc.lib.address import Address
from ccc.lib.contact import Contact
from ccc.lib.donation import Donation

filename = '08_10_donations_new_contacts.csv'
data_folder = os.path.dirname(os.path.realpath(__file__)) + '/data/todo/'

temporary_filename = '2013_partial_donations.csv'

def main():
    # Reload all the existing data that we have already parsed
    Account.load_all()
    Contact.load_all()

    unsure_rows = []
    with open(data_folder + filename, 'rb') as csvfile:
        next(csvfile, None) # skip header
        reader = csv.reader(csvfile)
        reader.next()
        for row in reader:
            row = [field.strip().decode('utf-8') for field in row]
            parse_row(row, unsure_rows)

    # Write out all the maybes into their own spreadsheet

    with open(data_folder + temporary_filename, 'wb') as csvfile:
          writer = csv.writer(csvfile)
          writer.writerow(['Type', 'Date', 'Num', 'Name', 'Memo', 'Pay Method', 'Amount', 'Reason not imported'])
          for row in unsure_rows:
            try:
              writer.writerow(row)
            except:
              print('#################### Could not encode this row ####################')
              print(row)
    #Account.write_all()
    #Contact.write_all()
    Donation.write_all()

def parse_row(row, unsure_rows):
    log_type = row[0]
    date = row[1]
    log_number = row[2] # not used
    donator_name = row[3].replace('(AR)', '').replace('(C)','').strip()
    address = row[4]
    description = row[5]
    method = row[6]
    amount = row[7]

    if 'Deposit' == log_type:
        contact, is_definite = None, False#Contact.fuzzy_match(donator_name, address)
        account = None

        if is_definite:
            # Add a donation that matches this contact
            account = contact.account
            pass
        elif False:#None == contact: # ie there was not even a fuzzy contact match
            account, is_definite = Account.fuzzy_match(donator_name, address)
            if is_definite:
                #print('found account match')
                print('------------------------------------------------------------')
            elif account:
                print('--------------------Fuzzy Account--------------------')

            if account:
                print('Account: {} {}'.format(account.name, account.shipping_address.to_a()))
                print('New Contact: {}, {}'.format(donator_name, address))
                # Add a donation that matches this account

        if None == contact and None == account:
            # TODO Make a new contact / account and import it
            print('making new contact and account')
            #if len(donator_name) == 0 or len(address) == 0:
            #    unsure_rows.append(row + ['Empty name or address'])
            #else:
            #    unsure_rows.append(row + ['Did not match anyone; unhandled so far'])
        elif not(is_definite):
            match = contact or account
            unsure_rows.append(row + ['Possible match: {}'.format(match.to_a())])
        elif is_definite:
            Donation(account,
                     amount=amount,
                     close_date=date,
                     description='{} - {}'.format(description, method),
                     name='{} Donation {}'.format(donator_name, date))

        else:
            print('We should never get here. What happened? {}'.format(row))
    else:
        # I don't know what to do with General Journals or Bills
        unsure_rows.append(row + ['Unknown log type'])

main()
