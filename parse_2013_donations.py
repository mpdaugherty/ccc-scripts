from __future__ import division
from __future__ import unicode_literals
from __future__ import absolute_import
from __future__ import print_function

import csv, re, os
from ccc.lib.account import Account
from ccc.lib.address import Address
from ccc.lib.contact import Contact

filename = '2013_individual_donations.csv'
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
          writer.writerow(['Type', 'Date', 'Num', 'Name', 'Memo', 'Pay Method', 'Amount'])
          for row in unsure_rows:
            try:
              writer.writerow(row)
            except:
              print('#################### Could not encode this row ####################')
              print(row)
    #Account.write_all()
    #Contact.write_all()

def parse_row(row, unsure_rows):
    log_type = row[0]
    date = row[1]
    log_number = row[2] # not used
    donator_name = row[3]
    address = row[4]
    description = row[5]
    method = row[6]
    amount = row[7]

    if 'Deposit' == log_type:
        print('--------------------------------------------------')
    else:
        # I don't know what to do with General Journals or Bills
        unsure_rows.append(row)

main()
