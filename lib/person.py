from __future__ import division
from __future__ import unicode_literals
from __future__ import absolute_import
from __future__ import print_function

import csv, os

class Address:
  # Has properties:
  # type (Work, Home, Other)
  # street
  # city
  # state
  # zip
  # country
  def __init__(self, **kwargs):
    for property in ['type', 'street', 'city', 'state', 'zip', 'country']:
      self.__dict__[property] = kwargs.get(property)

  def to_a(self):
    return [
        self.type,
        self.street,
        self.city,
        self.state,
        self.zip,
        self.country]

  @staticmethod
  def load_from_array(arr):
      return Address(type=   arr[0],
                     street= arr[1],
                     city=   arr[2],
                     state=  arr[3],
                     zip=    arr[4],
                     country=arr[5])

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
  def __init__(self, account, **kwargs):
    self.account = account
    for property in ['first_name', 'last_name', 'title', 'honorific', 'member_level', 'member_last_date', 'member_join_date', 'primary_address', 'secondary_address']:
      self.__dict__[property] = kwargs.get(property)
    self.primary_address = self.primary_address or Address()
    self.secondary_address = self.secondary_address or Address()
    self.account.add_contact(self)

  def to_array(self):
    return [
        self.last_name,
        self.first_name,
        self.honorific,
        self.title,
        None, #Email,
        self.account.name] + self.primary_address.to_a() + self.secondary_address.to_a()

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

