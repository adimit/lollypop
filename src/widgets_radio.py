#!/usr/bin/python
# Copyright (c) 2014-2015 Cedric Bellegarde <cedric.bellegarde@adishatz.org>
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

from gi.repository import Gtk, Gdk

from lollypop.define import Objects, ArtSize, Navigation
from lollypop.widgets_album import AlbumWidget
from lollypop.pop_radio import PopRadio


# Radio widget is a pixbuf with one label: radio name
class RadioWidget(AlbumWidget):
    """
        Init radio widget
        @param name as string
        @param uri as string
        @param radios_manager as RadiosManager
    """
    def __init__(self, name, uri, radios_manager):
        AlbumWidget.__init__(self, None)
        builder = Gtk.Builder()
        builder.add_from_resource('/org/gnome/Lollypop/RadioWidget.ui')
        builder.connect_signals(self)
        self._cover = builder.get_object('cover')

        self._name = name
        self._uri = uri
        self._radios_manager = radios_manager
        self._popover = None

        self._title = builder.get_object('title')
        self._title.set_label(name)

        self.add(builder.get_object('widget'))
        self.set_cover()

    """
        Set name
        @param name as string
    """
    def set_name(self, name):
        self._name = name
        self._title.set_label(name)

    """
        Set uri
        @param uri as string
    """
    def set_uri(self, uri):
        self._uri = uri

    """
        Return radio name
        @return name as string
    """
    def get_name(self):
        return self._name

    """
        Set cover for album if state changed
        @param force as bool
    """
    def set_cover(self, force=False):
        selected = Objects.player.current.id == Navigation.RADIOS and\
                   self._name == Objects.player.current.title
        if self._cover is not None and (selected != self._selected or force):
            self._selected = selected
            pixbuf = Objects.art.get_radio(self._name,
                                           ArtSize.BIG,
                                           selected)
            self._cover.set_from_pixbuf(pixbuf)
            del pixbuf

    """
        Update cover for album id id needed
    """
    def update_cover(self):
        if self._cover is not None:
            self._selected = Objects.player.current.id == Navigation.RADIOS\
                             and self._name == Objects.player.current.title
            pixbuf = Objects.art.get_radio(self._name,
                                           ArtSize.BIG,
                                           self._selected)
            self._cover.set_from_pixbuf(pixbuf)
            del pixbuf

#######################
# PRIVATE             #
#######################
    """
        Edit radio
        @param widget as Gtk.Widget
        @param event as Gdk.Event
    """
    def _on_button_press(self, widget, event):
        self._popover = PopRadio(self._name, self._radios_manager)
        self._popover.set_relative_to(widget)
        self._popover.show()

    """
        Change cursor over cover eventbox
        @param eventbox as Gdk.Eventbox
    """
    def _on_eventbox_realize1(self, eventbox):
        eventbox.get_window().set_cursor(Gdk.Cursor(Gdk.CursorType.HAND1))

    """
        Change cursor over title eventbox
        @param eventbox as Gdk.Eventbox
    """
    def _on_eventbox_realize2(self, eventbox):
        eventbox.get_window().set_cursor(Gdk.Cursor(Gdk.CursorType.PENCIL))
