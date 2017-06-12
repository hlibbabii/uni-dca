#!/usr/bin/python

import gtk
import pango

quotes = """<s>Excess of joy is harder to bear than any amount of sorrow.</s>
<span foreground="green">The more one judges, the less one loves. </span>
There is no such thing as a great talent without great will power.
"""


class PyApp(gtk.Window): 
    def __init__(self):
        super(PyApp, self).__init__()
        
        self.connect("destroy", gtk.main_quit)
        self.set_title("Pango Example")

        attributes, text, x = pango.parse_markup(quotes)
        label = gtk.Label(text)

        gtk.gdk.beep()

        fontdesc = pango.FontDescription("Serif bold 16")
        label.modify_font(fontdesc)

        gtk.Label.set_attributes(label, attributes)
        label.set_justify(gtk.JUSTIFY_CENTER)

        fix = gtk.Fixed()

        fix.put(label, 5, 5)
        
        self.add(fix)
        self.set_position(gtk.WIN_POS_CENTER)
        self.show_all()

PyApp()
gtk.main()
