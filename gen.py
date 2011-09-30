# -*- coding: utf-8 -*-
import codecs

header = u"""
<html><head>
    <link rel="stylesheet" type="text/css"  
        href="blueprintcss/typography.css"/>
    <link rel="stylesheet" type="text/css"  
        href="blueprintcss/grid.css"/>
    <title>%s</title>
    <script type="text/javascript">

      var _gaq = _gaq || [];
      _gaq.push(['_setAccount', 'UA-4517625-4']);
      _gaq.push(['_trackPageview']);

      (function() {
        var ga = document.createElement('script'); ga.type = 'text/javascript'; ga.async = true;
        ga.src = ('https:' == document.location.protocol ? 'https://ssl' : 'http://www') + '.google-analytics.com/ga.js';
        var s = document.getElementsByTagName('script')[0]; s.parentNode.insertBefore(ga, s);
      })();

    </script>
</head><body>
    <div class="container" id="main">
        <a href="http://studentaffairs.case.edu/careers/"><img src="banner.jpg" style="float: right"/></a>
        <h1 id="title">%s</h1>
        <h3>Produced by members of the <a href="http://goto.case.edu/">CWRU Hacker Society</a></h3>
        <div class="span-8 colborder" id="sidebar">
"""

footer = u"""</div></div></body></html>"""

sidebar_divider = u"""</div><div class="span-15 last" id="content">"""

sanitize_major = lambda major: major.replace('/', '_')

def html_escape(text):
    text = text.replace(u'&', u'&amp;')
    text = text.replace(u'"', u'&quot;')
    text = text.replace(u"'", u'&#39;')
    text = text.replace(u">", u'&gt;')
    text = text.replace(u"<", u'&lt;')
    text = text.replace(u"’", u'&apos;')
    text = text.replace(u"–", u'&#150;')
    return text

def write_majors(f, mlists):
    f.write("""<h2>Majors</h2>""")
    titles = ('', 'College of Arts and Sciences', 
              'Case School of Engineering', 'Weatherhead School of Management', 
              'Professional Schools')
    for l, t in zip(mlists, titles):
        if t:
            f.write("""<h3>%s</h3>""" % t)
        for m in sorted(l):
            f.write('<a href="%s.html">%s</a><br/>' % (sanitize_major(m), m))
    f.write(sidebar_divider)

def write_company(f, c):
    f.write(u'<h2>%s</h2>' % c.link())
    f.write(u'<strong>Degrees:</strong> %s<br/>' % ', '.join(c.degrees))
    f.write(u'<strong>Position types:</strong> %s<br/>' % ', '.join(c.position_types))
    f.write(u'<strong>Majors:</strong> %s<br/>' % ', '.join(c.majors))
    f.write(u'<strong>Locations:</strong> %s<br/>' % c.locations)
    f.write(u'<strong>F1:</strong> %s<br/>' % (u'Yes' if c.f1 else u'No'))
    f.write(u'<br/>')
    
    f.write(u'<strong>Contact:</strong> <a href="mailto:%s">%s</a>, %s<br/>' % (c.contact_email, c.contact_name, c.contact_title))
    f.write(u'<strong>Phone:</strong> %s <strong>Fax:</strong> %s<br/>' % (c.phone, c.fax))
    f.write(u'<strong>Address:</strong> <br/>%s<br/>' % c.address)
    f.write(u'<br/>')
    
    if c.oci:
        f.write(u'On-Campus Interviews<br/>')
    if c.ocif:
        f.write(u'On-Campus Interview Friday<br/>')
    if c.session:
        f.write('u<strong>Session:</strong> %s<br/>' % c.session)
    if c.oci or c.ocif or c.session:
        f.write('u<br/>')
    
    f.write(html_escape(u'<br/>'.join(c.description.splitlines())))

def gen_index(majors, companies, path, title):
    with codecs.open('%s/index.html' % path, mode='w', encoding='utf-8') as f:
        f.write(header % (title, title))
        write_majors(f, majors)
        for c in companies:
            write_company(f, c)
        f.write(footer)

def gen(major, majors, companies, path):
    with codecs.open('%s/%s.html' % (path, sanitize_major(major)), mode='w', encoding='utf-8') as f:
        t = u'Companies looking for %s majors' % major
        f.write(header % (t, t))
        write_majors(f, majors)
        for c in [x for x in companies if major in x.majors]:
            write_company(f, c)
        f.write(footer)
