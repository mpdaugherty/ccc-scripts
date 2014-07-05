from __future__ import division
from __future__ import unicode_literals
from __future__ import absolute_import
from __future__ import print_function

class Address:
  # Has properties:
  # type (Work, Home, Other)
  # street
  # city
  # state
  # zip
  # country
  def __init__(self, account, **kwargs):
    for property in ['type', 'street', 'city', 'state', 'zip', 'country']:
      self.__dict__[property] = kwargs.get(property)

  def to_a():
    return [
        self.type,
        self.street,
        self.city,
        self.state,
        self.zip,
        self.country]

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
        self.account.name] + self.primary_address.to_a + self.secondary_address.to_a

class Account:
  # Has properties:
  # name (Should be unique)
  # type (Individual, Other)
  # phone
  # billing_address
  # shipping_address
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
          self.phone] + self.billing_address.to_a +  self.shipping_address.to_a

  all_accounts = {}
  @classmethod
  def get(cls, name):
    cls.all_accounts.get(name)

  @classmethod
  def get_or_create(cls, **kwargs):
    if None == kwargs.get('name'):
      return None

    account = Account.get(kwargs.get('name'))
    return account or Account(**kwargs)

