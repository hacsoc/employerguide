# -*- coding: utf-8 -*-
import itertools
import re

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

    if len(words) <= 4 or city == u'Ave.':
        return u' '.join(words) + u'\n'

    index_of_first_number = 0
    while not words[index_of_first_number].isdigit() and not words[index_of_first_number] == 'P.O.':
        index_of_first_number += 1
    if index_of_first_number >= len(words)-3 or index_of_first_number <= 1:
        index_of_first_number = 0
    if index_of_first_number == 0:
        return u"%s<br/>%s, %s %s" % (u' '.join(words[:-3]), city, state, zipcode)
    else:
        firstline = u' '.join(words[:index_of_first_number])
        secondline = u' '.join(words[index_of_first_number:-3])
        return u"%s<br/>%s<br/>%s, %s %s" % (firstline, secondline, city, state, zipcode)

NAME_URL_DESC = (0, 3)
CONTACTNAME = (4, 6)
CONTACTINFO = (6, 10)
POSITIONTYPES = 11
DEGREES = 12
MAJORS = (13, 18)
F1 = 18
LOCATIONS = 19

def test(values):
    print values[NAME_URL_DESC[0]:NAME_URL_DESC[1]]
    print values[CONTACTNAME[0]:CONTACTNAME[1]]
    print values[CONTACTINFO[0]:CONTACTINFO[1]]
    print liberate_semicolon_strings(values[POSITIONTYPES])
    print liberate_semicolon_strings(values[DEGREES])
    print set(parse_nested_lists(values[MAJORS[0]:MAJORS[1]]))
    print [liberate_semicolon_strings(values[MAJORS[0]+i]) for i in xrange(5)]
    print values[F1].lower() == 'y'
    print values[LOCATIONS]

class Company(object):
    def __init__(self, values):
        self.name, self.url, self.description = values[NAME_URL_DESC[0]:NAME_URL_DESC[1]]
        self.contact_name, self.contact_title = values[CONTACTNAME[0]:CONTACTNAME[1]]
        self.address, self.phone, self.fax, self.contact_email = \
            values[CONTACTINFO[0]:CONTACTINFO[1]]
        self.address = fix_address(self.address)
        self.position_types = liberate_semicolon_strings(values[POSITIONTYPES])
        self.degrees = liberate_semicolon_strings(values[DEGREES])
        
        self.majors = set(parse_nested_lists(values[MAJORS[0]:MAJORS[1]]))
        
        self.mlists = [liberate_semicolon_strings(values[MAJORS[0]+i]) for i in xrange(5)]
        
        self.f1 = values[F1].lower() == 'y'
        self.locations = values[LOCATIONS]
        self.session = ''
        self.oci = False
        self.ocif = False
    
    def shortstring(self):
        return "%s - %s" % (self.name, self.url)
    
    def link(self):
        return '<a href="%s">%s</a>' % (self.url, self.name)
    
    def __str__(self):
        title = "%s - %s" % (self.name, self.url)
        titledashes = ''.join(['=' for c in title])
        contact = "%s (%s, %s)" % (self.contact_name, self.contact_email, self.phone)
        
        return '\n'.join([titledashes, 
                          title, 
                          titledashes, 
                          contact, 
                          self.locations, 
                          ', '.join(self.looking_for), 
                          ', '.join(self.majors), 
                          '', 
                          self.description, 
                          '', 
                          self.session])
    
