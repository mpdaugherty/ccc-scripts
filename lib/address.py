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
  def __init__(self, **kwargs):
    for property in ['type', 'street', 'city', 'state', 'zip', 'country']:
      self.__dict__[property] = kwargs.get(property)

  def to_a(self):
    return [
        self.type or '',
        self.street or '',
        self.city or '',
        self.state or '',
        self.zip or '',
        self.country or '']

  @staticmethod
  def load_from_array(arr):
      return Address(type=   arr[0],
                     street= arr[1],
                     city=   arr[2],
                     state=  arr[3],
                     zip=    arr[4],
                     country=arr[5])
