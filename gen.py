header = """
<html><head>
    <link rel="stylesheet" type="text/css"  
        href="blueprintcss/typography.css"/>
    <link rel="stylesheet" type="text/css"  
        href="blueprintcss/grid.css"/>
    <title>%s</title>
</head><body>
    <div class="container" id="main">
        <h1 id="title">%s</h1>
        <h3>Produced by members of the <a href="http://goto.case.edu/">CWRU Hacker Society</a></h3>
        <div class="span-8 colborder" id="sidebar">
"""

footer = """</div></div></body></html>"""

sidebar_divider = """</div><div class="span-15 last" id="content">"""

sanitize_major = lambda major: major.replace('/', '_')

def write_majors(f, mlists):
    f.write("""<h2>Majors</h2>""")
    titles = ('Academic Programs', 'College of Arts and Sciences', 
              'Case School of Engineering', 'Weatherhead School of Management', 
              'Professional Schools')
    for l, t in zip(mlists, titles):
        f.write("""<h3>%s</h3>""" % t)
        for m in sorted(l):
            f.write('<a href="%s.html">%s</a><br/>' % (sanitize_major(m), m))
    f.write(sidebar_divider)

def write_company(f, c):
    f.write('<h2>%s</h2>' % c.link())
    f.write('<strong>Degrees:</strong> %s<br/>' % ', '.join(c.degrees))
    f.write('<strong>Position types:</strong> %s<br/>' % ', '.join(c.position_types))
    f.write('<strong>Majors:</strong> %s<br/>' % ', '.join(c.majors))
    f.write('<br/>')
    
    f.write('<strong>Contact:</strong> <a href="mailto:%s">%s</a><br/>' % (c.contact_email, c.contact_name))
    f.write('<strong>Phone:</strong> %s <strong>Fax:</strong> %s<br/>' % (c.phone, c.fax))
    f.write('<strong>Locations:</strong> %s<br/>' % c.locations)
    f.write('<br/>')
    
    if c.oci:
        f.write('On-Campus Interviews<br/>')
    if c.ocif:
        f.write('On-Campus Interview Friday<br/>')
    if c.session:
        f.write('<strong>Session:</strong> %s<br/>' % c.session)
    if c.oci or c.ocif or c.session:
        f.write('<br/>')
    
    f.write('<br/>'.join(c.description.splitlines()))

def gen_index(majors, companies, path, title):
    with open('%s/index.html' % path, 'w') as f:
        f.write(header % (title, title))
        write_majors(f, majors)
        for c in companies:
            write_company(f, c)
        f.write(footer)

def gen(major, majors, companies, path):
    with open('%s/%s.html' % (path, sanitize_major(major)), 'w') as f:
        t = 'Companies looking for %s majors' % major
        f.write(header % (t, t))
        write_majors(f, majors)
        for c in [x for x in companies if major in x.majors]:
            write_company(f, c)
        f.write(footer)
