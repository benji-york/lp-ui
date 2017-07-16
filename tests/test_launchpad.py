#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# __coconut_hash__ = 0xc797044f

# Compiled with Coconut version 1.2.3 [Colonel]

# Coconut Header: --------------------------------------------------------

from __future__ import generator_stop

import sys as _coconut_sys, os.path as _coconut_os_path
_coconut_file_path = _coconut_os_path.dirname(_coconut_os_path.abspath(__file__))
_coconut_sys.path.insert(0, _coconut_file_path)
from __coconut__ import _coconut, _coconut_MatchError, _coconut_tail_call, _coconut_tco, _coconut_igetitem, _coconut_compose, _coconut_pipe, _coconut_starpipe, _coconut_backpipe, _coconut_backstarpipe, _coconut_bool_and, _coconut_bool_or, _coconut_minus, _coconut_map, _coconut_partial
from __coconut__ import *
_coconut_sys.path.remove(_coconut_file_path)

# Compiled Coconut: ------------------------------------------------------

from .helpers import InitializationMixin  # line 1: from .helpers import InitializationMixin, WakeupsForeverMixin, FauxRef
from .helpers import WakeupsForeverMixin  # line 1: from .helpers import InitializationMixin, WakeupsForeverMixin, FauxRef
from .helpers import FauxRef  # line 1: from .helpers import InitializationMixin, WakeupsForeverMixin, FauxRef
from .helpers import faux_create  # line 2: from .helpers import faux_create, init_actor
from .helpers import init_actor  # line 2: from .helpers import faux_create, init_actor
import launchpad  # line 3: import launchpad
import thespian.actors  # line 4: import thespian.actors
import unittest  # line 5: import unittest



class FauxMidiPort(object):  # line 9: class FauxMidiPort(object):

    name = None  # line 11:     name = None
    polled = False  # line 12:     polled = False

    def __init__(self, name):  # line 14:     def __init__(self, name):
        self.name = name  # line 15:         self.name = name

    def poll(self):  # line 17:     def poll(self):
        self.polled = True  # line 18:         self.polled = True
        return None  # line 19:         return None



class TestMidiIn(unittest.TestCase, InitializationMixin, WakeupsForeverMixin):  # line 23: class TestMidiIn(unittest.TestCase, InitializationMixin, WakeupsForeverMixin):
    """Tests for the MidiIn actor."""  # line 24:     """Tests for the MidiIn actor."""

    def setUp(self):  # line 26:     def setUp(self):
        self.actor = faux_create(launchpad.MidiIn)  # line 27:         self.actor = faux_create(launchpad.MidiIn)
        self.actor.open_input_port = FauxMidiPort  # line 28:         self.actor.open_input_port = FauxMidiPort

    @init_actor  # line 29: 
    def test_midi_port_name(self):  # line 31:     def test_midi_port_name(self):
# The correct name is used when opening the MIDI port.
        self.assertEqual(self.actor.port.name, 'Launchpad MK2 MIDI 1')  # line 33:         self.assertEqual(self.actor.port.name, 'Launchpad MK2 MIDI 1')

    @init_actor  # line 34: 
    def test_wakeups_poll(self):  # line 36:     def test_wakeups_poll(self):
# Every time a wakeup message is received by the actor, the MIDI input
# port is polled.
        self.actor.open_input_port.polled = False  # line 39:         self.actor.open_input_port.polled = False
        self.actor.receiveMessage(thespian.actors.WakeupMessage(0), sender=None)  # line 40:         self.actor.receiveMessage(thespian.actors.WakeupMessage(0), sender=None)
        self.assertTrue(self.actor.port.polled)  # line 41:         self.assertTrue(self.actor.port.polled)
