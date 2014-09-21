from __future__ import division
from __future__ import unicode_literals
from __future__ import absolute_import
from __future__ import print_function

import re

from ccc.lib.account import Account
from ccc.lib.address import Address
from ccc.lib.contact import Contact

def can_split(name):
    if len(split_names(name)) > 1:
        return True
    False

split_name_regex = re.compile(' & | and ')
def split_names(name):
    return [s.strip() for s in split_name_regex.split(name)]

def is_individual(first_name, last_name, organization):
    if not(first_name and last_name):
        return False

    if can_split(first_name):
        return False

    return True

honorific_regex = re.compile('(Mr\.)|(Mrs\.)|(Ms\.)|(Dr\.)|(Prof\.)')
def extract_honorific(name):
    match = honorific_regex.search(name)
    if match:
        return match.group(), honorific_regex.sub('', name).strip()
    else:
        return None, name

def create_individual(first_name, last_name, organization, street, city, state, zip_code, country, title):
    honorific, first_name = extract_honorific(first_name)

    account_name = "{} {}".format(first_name, last_name)
    account_type = 'Individual'
    address = Address(type = 'Home',
                      street = street,
                      city = city,
                      state = state,
                      zip = zip_code,
                      country = country)

    account = Account.get_or_create(name=account_name,
                                    type='Individual',
                                    shipping_address = address)

    contact = Contact.get_or_create(account,
                                    last_name  = last_name,
                                    first_name = first_name,
                                    honorific  = honorific,
                                    title      = title,
                                    primary_address = address)

def is_organization(first_name, last_name, organization):
    return not(first_name or last_name) and bool(organization)

def create_organization(first_name, last_name, organization, street, city, state, zip_code, country, title):
    address = Address(type = 'Work',
                      street = street,
                      city = city,
                      state = state,
                      zip = zip_code,
                      country = country)

    account = Account.get_or_create(name=organization,
                                    type='Other',
                                    shipping_address = address,
                                    billing_address = address)

def is_multiple(first_name, last_name, organization):
    return can_split(first_name)

def create_multiple(first_name, last_name, organization, street, city, state, zip_code, country, title):
    account_name = organization or '{} Household ({})'.format(last_name, first_name)
    if not last_name:
        account_name = '{} Household'.format(first_name)

    address = Address(type = 'Work' if organization else 'Home',
                      street = street,
                      city = city,
                      state = state,
                      zip = zip_code,
                      country = country)

    account = Account.get_or_create(name=account_name,
                                    type='Other',
                                    shipping_address = address,
                                    billing_address = address if organization else None)

    first_names = split_names(first_name)
    if last_name:
        for name in first_names:
            honorific, name = extract_honorific(name)
            contact = Contact.get_or_create(account,
                                            last_name  = last_name,
                                            first_name = name,
                                            honorific  = honorific,
                                            title      = title,
                                            primary_address = address)
    else:
        for name in first_names:
            honorific, name = extract_honorific(name)
            lname = name.split(' ')[-1].strip()
            fname = ' '.join(name.split(' ')[0:-1]).strip()
            contact = Contact.get_or_create(account,
                                            last_name  = lname,
                                            first_name = fname,
                                            honorific  = honorific,
                                            title      = title,
                                            primary_address = address)
