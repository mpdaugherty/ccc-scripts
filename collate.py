from __future__ import division
from __future__ import unicode_literals
from __future__ import absolute_import
from __future__ import print_function

import csv, re
from lib.person import Contact

# Import all the people from the master mailing list
people = []
not_people = []
titles = ['Assessor-Recorder', 'Supervisor', 'Governor', 'Senator', 'Mayor', 'Mr.', 'Mrs.', 'M.']
def parse_master_row(row):
  first_name = row[1].strip().decode('utf-8')
  last_name = row[2].strip().decode('utf-8')
  organization_name = row[3].strip()
  address_1 = row[4].strip()
  city = row[5].strip()
  state = row[6].strip()
  zip_code = row[7].strip()
  country = row[8].strip() or 'USA'
  title = ([t for t in titles if (t in first_name or t in last_name)] or [u''])[0]
  first_name = first_name.replace(title, '').strip()
  last_name = last_name.replace(title, '').strip()

  # Parse into individuals
  name_check(first_name, last_name)

  # Check for duplicates

def name_check(first_name, last_name):
  first_name = first_name.strip()
  last_name = last_name.strip()
  full_name = '{0} {1}'.format(first_name, last_name).strip()

  if not full_name:
    return

  full_name_regexes = [
    re.compile('^\S+ \S+$'),
    re.compile('^\S+ \S\.? \S+$')
    ]

  if [True for r in full_name_regexes if r.match(full_name)]:
    people.append(full_name)
    return

  split_keys = [' & ', ' and ', ' / ', ', ']
  for k in split_keys:
    split_names = first_name.split(k)
    if len(split_names) == 2:
      # TODO Perhaps add a first_name_regex set here to see if each name matches a first name
      return [name_check(n, last_name) for n in split_names]

  not_people.append(full_name)

with open('mailing_list_master.csv', 'rb') as csvfile:
  next(csvfile, None) # skip header
  reader = csv.reader(csvfile)
  reader.next()
  for row in reader:
    parse_master_row(row)

  print("Understandable People: {}".format(len(people)))
  print('')
  print('Maybe not people ({}):'.format(len(not_people)))
  print('')
  for item in not_people:
    print(item)
  print('')
  duplicate_set = set([n for n in people if people.count(n) > 1])
  print("Duplicates ({}):".format(len(duplicate_set)))
  print('')
  [print(name) for name in duplicate_set]



# Look for duplicates in the master mailing list
