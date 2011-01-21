to_emphasize = ('bachelors', 'masters', 'phd', 'doctoral')

import itertools

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

class Company(object):
    def __init__(self, values):
        self.name, self.url, self.description = values[:3]
        self.contact_name, self.contact_title = values[3:5]
        self.address, self.phone, self.fax, self.contact_email = values[5:9]
        self.position_types = liberate_semicolon_strings(values[9])
        self.degrees = liberate_semicolon_strings(values[10])
        
        self.majors = set(parse_nested_lists(values[11:16]))
        
        self.mlists = [liberate_semicolon_strings(values[11+i]) for i in xrange(5)]
        
        self.f1 = values[16].lower() == 'y'
        self.locations = values[17]
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
    
