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
    self.contacts = []

    Account.all_accounts[self.name] = self

  def add_contact(self, contact):
      self.contacts.append(contact)

  def to_a(self):
      return [
          self.name,
          self.type,
          self.phone] + self.billing_address.to_a() +  self.shipping_address.to_a()


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
          writer.writerows([acct.to_a() for acct in Account.all_accounts.values()])

