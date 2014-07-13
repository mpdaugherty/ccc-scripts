from __future__ import division
from __future__ import unicode_literals
from __future__ import absolute_import
from __future__ import print_function

import csv, os
from ccc.lib.account import Account
from ccc.lib.address import Address

class Contact:
  # Has properties
  # account (from which we get account_name)
  # first_name, last_name, title
  # honorific (Mr. Mrs. Ms. Dr. Prof.)
  # birthdate (not available in our data, so probably not)
  #### member type (Board, C-Cubed)
  # member_last_date
  # member_level
  # member_join_date
  # primary_address
  # secondary_address

  data_location = os.path.dirname(os.path.realpath(__file__)) + '/../final_data/final_accounts.csv'

  def __init__(self, account, **kwargs):
    self.account = account
    for property in ['first_name', 'last_name', 'title', 'honorific', 'member_level', 'member_last_date', 'member_join_date', 'primary_address', 'secondary_address']:
      self.__dict__[property] = kwargs.get(property)
    self.primary_address = self.primary_address or Address()
    self.secondary_address = self.secondary_address or Address()
    self.account.add_contact(self)

  def to_a(self):
    return [
        self.last_name,
        self.first_name,
        self.honorific,
        self.title,
        None, #Email,
        self.account.name] + self.primary_address.to_a() + self.secondary_address.to_a()

  def full_name(first_name, last_name):
    '{} {}'

  @staticmethod
  def get_or_create(account, **kwargs):
    contact = account.get_contact(kwargs['first_name'], kwargs['last_name'])
    if not contact:
      kwargs['account'] = account
      contact = Contact(**kwargs)
    return contact

  @staticmethod
  def load_all():
      '''Note: Account.load_all() must be called before this'''
      with open(Contact.data_location, 'rb') as csvfile:
          next(csvfile, None) # skip header
          reader = csv.reader(csvfile)
          for row in reader:
              Contact.load_from_row(row)

  @staticmethod
  def load_from_row(row):
    account = Account.get(row[5]) or Account(name = '{} {}'.format(row[1], row[0]))
    account.get_or_create_contact(last_name=row[0],
                                  first_name = row[1],
                                  honorific = row[2],
                                  title = row[3],
                                  email = row[4],
                                  primary_address = Address.load_from_array(row[6:12]),
                                  secondary_address = Address.load_from_array(row[12:18]))

  @staticmethod
  def write_all():
      with open(Contact.data_location, 'wb') as csvfile:
          writer = csv.writer(csvfile)
          writer.writerow(['Last Name', 'First Name', 'Honorific', 'Title', 'Email', 'Account Name', 'Home Address Type', 'Home Street', 'Home City', 'Home State', 'Home Country', 'Other Address Type', 'Other Street', 'Other City', 'Other State', 'Other Country'])
          for acct in Account.all_accounts.values():
              writer.writerows([contact.to_a() for contact in acct.all_contacts()])

