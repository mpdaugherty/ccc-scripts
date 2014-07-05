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

class Contact:
  # Has properties
  # account (from which we get account_name)
  # first_name, last_name, title
  # honorific (Mr. Mrs. Ms. Dr. Prof.)
  # birthdate (not available in our data, so probably not)
  # member type (Board, C-Cubed)
  # primary address
  # secondary address
  # membership end date
  # membership level
  # membership join date
  def __init__(first_name):
    self.first_name = first_name

  def __init__eq__(self, other):
      isinstance(other, self.__class__) and \
          self.first_name == other.first_name and \
          self.last_name == other.last_name and \
          (self.address == other.address or self.address is None or other.address is None)

  def __ne__(self, other):
      return not self.__eq__(other)

class Account:
  # Has properties:
  # name (Should be unique)
  # type (Individual, Other)
  # phone
  # billing_address
  # shipping_address

