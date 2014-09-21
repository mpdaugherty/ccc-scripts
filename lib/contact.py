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

  all_contacts = [] # Utility for searching, nothing more

  data_location = os.path.dirname(os.path.realpath(__file__)) + '/../data/final_contacts.csv'

  def __init__(self, account, **kwargs):
    self.account = account
    for property in ['first_name', 'last_name', 'title', 'honorific', 'member_level', 'member_last_date', 'member_join_date', 'primary_address', 'secondary_address']:
      self.__dict__[property] = kwargs.get(property)
    self.primary_address = self.primary_address or Address()
    self.secondary_address = self.secondary_address or Address()
    self.account.add_contact(self)
    Contact.all_contacts.append(self)

  def to_a(self):
    return [
        self.last_name or '',
        self.first_name or '',
        self.honorific or '',
        self.title or '',
        '', #Email,
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
  def fuzzy_match(new_name, new_address):
    # Don't return possible matches until the very end because a better, absolute match may be available
    possible_match = None
    for contact in Contact.all_contacts:
      address_match = False
      name_match = False
      name_almost_match = False

      for address in [contact.primary_address, contact.secondary_address]:
        if address_match or address is None:
          next

        old_address = address.street
        if len(new_address) > 0 and len(old_address) > 0:
          address_match = (old_address in new_address) or (new_address in old_address)

      name_match = len(new_name) > 0 and new_name == contact.full_name

      name_parts = contact.first_name.split() + contact.last_name.split()
      new_name_parts = new_name.split()
      common_parts = [part for part in name_parts if part in new_name_parts]
      name_almost_match = len(common_parts) >= 2

      if (name_match or name_almost_match):
        if address_match:
          return contact, True
        else:
          possible_match = contact

      if address_match:
        possible_match = contact

    return possible_match, False


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
    Contact.get_or_create(account,
                          last_name=row[0],
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
          writer.writerow(['Last Name', 'First Name', 'Salutation', 'Title', 'Email', 'Account Name', 'Primary Address Type', 'Mailing Street', 'Mailing City', 'Mailing State', 'Mailing Zip', 'Home Country', 'Other Address Type', 'Other Street', 'Other City', 'Other State', 'Other Zip', 'Other Country'])
          for acct in sorted(Account.all_accounts.values(), key=lambda acct: acct.name):
            for contact in sorted(acct.all_contacts(), key=lambda contact: contact.last_name):
              writer.writerow([unicode(s).encode('utf-8') for s in contact.to_a()])

