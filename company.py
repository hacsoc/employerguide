from collections import namedtuple
from functools import reduce
import itertools
import re


Cols = namedtuple( 'Cols', [
    'company_name',
    'url',
    'description',
    'junk',
    'contact_name',
    'contact_title',
    'address',
    'phone',
    'fax',
    'contact_email',
    'position_types',
    'degrees',
    'majors_artsci',
    'majors_eng',
    'majors_mgmt',
    'majors_professional',
    'f1',
    'locations'])

def parse_nested_lists(mlists):
    """
    ['abc;def', 'ghi;jkl'] -> ['abc', 'def', 'ghi', 'jkl']
    """
    for mlist in mlists:
        for m in mlist.split(';'):
            if m.strip():
                yield m.strip()

def liberate_semicolon_strings(s):
    return [m.strip() for m in s.split(';') if m.strip()]

def html_escape(text):
    text = text.replace('&', '&amp;')
    text = text.replace('"', '&quot;')
    text = text.replace("'", '&#39;')
    text = text.replace(">", '&gt;')
    text = text.replace("<", '&lt;')
    text = text.replace("’", '&apos;')
    text = text.replace("–", '&#150;')
    return text

LOWER = 0
UPPER = 1
DIGIT = 2
WHITESPACE = None

def fix_address(a):
    # Fix the horribly broken nonexistent line breaks from the CSV
    words = [""]
    tok_type = WHITESPACE
    for c in a:
        new_space = False
        echo = False
        if c.islower():
            echo = True
            tok_type = LOWER
        elif c.isupper():
            echo = True
            if tok_type != UPPER and tok_type != WHITESPACE and words[0]:
                new_space = True
            tok_type = UPPER
        elif c.isdigit():
            echo = True
            if tok_type != DIGIT and tok_type != WHITESPACE and words[0]:
                new_space = True
            tok_type = DIGIT
        elif c.isspace():
            if tok_type != WHITESPACE:
                new_space = True
            tok_type = WHITESPACE
        elif c != ',':
            echo = True
        if new_space:
            words.append("")
        if echo:
            words[-1] = words[-1] + c
    words = [w.strip() for w in words]
    # OKAY, now let's try to do something with that mess
    state, zipcode = words[-2:]
    city = words[-3]

    if city in ('York',):
        city = 'New York'
        words[-4] = words[-4][:-3]

    if len(words) <= 4 or city == 'Ave.':
        return ' '.join(words) + '\n'

    index_of_first_number = 0
    while not words[index_of_first_number].isdigit() and not words[index_of_first_number] == 'P.O.':
        index_of_first_number += 1
    if index_of_first_number >= len(words)-3 or index_of_first_number <= 1:
        index_of_first_number = 0
    if index_of_first_number == 0:
        return "%s<br/>%s, %s %s" % (' '.join(words[:-3]), city, state, zipcode)
    else:
        firstline = ' '.join(words[:index_of_first_number])
        secondline = ' '.join(words[index_of_first_number:-3])
        return "%s<br/>%s<br/>%s, %s %s" % (firstline, secondline, city, state, zipcode)


class Company(object):
    def __init__(self, *values):
        cols = Cols(*values)
        self.name = cols.company_name
        self.url = cols.url
        self.description = html_escape(cols.description)
        self.contact_name = cols.contact_name
        self.contact_title = cols.contact_title
        self.contact_email = cols.contact_email
        # self.address = cols.address
        self.address = fix_address(cols.address)
        self.phone = cols.phone
        self.fax = cols.fax
        self.position_types = liberate_semicolon_strings(cols.position_types)
        self.degrees = liberate_semicolon_strings(cols.degrees)
        
        semi_mlists = (cols.majors_artsci, cols.majors_eng,
                       cols.majors_mgmt, cols.majors_professional)
        self.mlists = [liberate_semicolon_strings(x) for x in semi_mlists]
        self.majors = reduce(lambda a, b: set(a) | set(b), self.mlists, set())
        
        self.f1 = (cols.f1.lower()  == 'y')
        self.locations = cols.locations
        self.session = ''
        self.oci = False
        self.ocif = False
    
    def shortstring(self):
        return "%s - %s" % (self.name, self.url)
    
    def __str__(self):
        title = "%s - %s" % (self.name, self.url)
        titledashes = ''.join(['=' for c in title])
        contact = "%s (%s, %s)" % (self.contact_name, self.contact_email, self.phone)
        
        return '\n'.join([titledashes, 
                          title, 
                          titledashes, 
                          contact, 
                          self.locations, 
                          ', '.join(self.majors), 
                          '', 
                          self.description, 
                          '', 
                          self.session])
    
