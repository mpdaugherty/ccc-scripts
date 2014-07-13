from __future__ import division
from __future__ import unicode_literals
from __future__ import absolute_import
from __future__ import print_function

import csv, os
from ccc.lib.address import Address

class Account:
  # Has properties:
  # name (Should be unique)
  # type (Individual, Other)
  # phone
  # billing_address
  # shipping_address

  all_accounts = {}
  data_location = os.path.dirname(os.path.realpath(__file__)) + '/../final_data/final_accounts.csv'

  def __init__(self, **kwargs):
    for property in ['name', 'type', 'phone', 'billing_address', 'shipping_address']:
      self.__dict__[property] = kwargs.get(property)
    self.billing_address = self.billing_address or Address()
    self.shipping_address = self.shipping_address or Address()
    self.contacts = {}

    Account.all_accounts[self.name] = self

  def add_contact(self, new_contact):
      contact = self.contacts.get(new_contact.full_name)
      if not contact:
        self.contacts[new_contact.full_name] = new_contact

  def get_contact(self, first_name, last_name):
      full_name = '{} {}'.format(first_name, last_name)
      return self.contacts.get(full_name)

  def get_or_create_contact(self, **kwargs):
    full_name = '{} {}'.format(kwargs['first_name'], kwargs['last_name'])
    return self.contacts.get(full_name)

  def all_contacts(self):
    return self.contacts.values()

  def to_a(self):
      return [
          self.name or '',
          self.type or '',
          self.phone or ''] + self.billing_address.to_a() +  self.shipping_address.to_a()


  @classmethod
  def get(cls, name):
    return cls.all_accounts.get(name)

  @classmethod
  def get_or_create(cls, **kwargs):
    if None == kwargs.get('name'):
      return None

    account = cls.get(kwargs.get('name'))
    return account or Account(**kwargs)

  @staticmethod
  def load_all():
      with open(Account.data_location, 'rb') as csvfile:
          next(csvfile, None) # skip header
          reader = csv.reader(csvfile)
          for row in reader:
              Account.load_from_row(row)

  @staticmethod
  def load_from_row(row):
      return Account.get_or_create(name=row[0],
                                   type=row[1],
                                   phone=row[2],
                                   billing_address=Address.load_from_array(row[3:9]),
                                   shipping_address=Address.load_from_array(row[9:15]))

  @staticmethod
  def write_all():
      with open(Account.data_location, 'wb') as csvfile:
          writer = csv.writer(csvfile)
          writer.writerow(['Name', 'Type', 'Phone', 'Billing Address Type', 'Billing Street', 'Billing City', 'Billing State', 'Billing Zip', 'Billing Country', 'Shipping Address Type', 'Shipping Street', 'Shipping City', 'Shipping State', 'Shipping Zip', 'Shipping Country'])
          for acct in Account.all_accounts.values():
            try:
              writer.writerow([unicode(s).encode('utf-8') for s in acct.to_a()])
            except:
              print('#################### Could not encode this account ####################')
              print(acct.to_a())

