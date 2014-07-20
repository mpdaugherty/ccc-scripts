from __future__ import division
from __future__ import unicode_literals
from __future__ import absolute_import
from __future__ import print_function

import csv, os
from ccc.lib.account import Account

class Donation:
  # Has properties
  # amount
  # name
  # close date
  # description

  data_location = os.path.dirname(os.path.realpath(__file__)) + '/../final_data/final_donations.csv'

  def __init__(self, account, **kwargs):
    self.account = account
    for property in ['amount', 'name', 'close_date', 'description']
      self.__dict__[property] = kwargs.get(property)
    self.account.add_donation(self)

  def to_a(self):
    return [
        self.amount or '',
        self.account.name or '',
        self.name or '',
        self.close_date or '',
        'Posted', # All the donations that I'm importing have been completed, so they are all Posted
        100, # And they are all at 100% probability
        self.description or '']

  @staticmethod
  def write_all():
      with open(Contact.data_location, 'wb') as csvfile:
          writer = csv.writer(csvfile)
          writer.writerow(['Amount', 'Account Name', 'Name', 'Close Date', 'Stage', 'Probability', 'Description'])
          for acct in sorted(Account.all_accounts.values(), key=lambda acct: acct.name):
            for donation in acct.donations:
              writer.writerow([unicode(s).encode('utf-8') for s in donation.to_a()])

