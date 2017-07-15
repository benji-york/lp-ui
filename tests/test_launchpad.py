#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# __coconut_hash__ = 0xeb7cfd46

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

import launchpad  # line 1: import launchpad
import thespian.actors  # line 2: import thespian.actors
import unittest  # line 3: import unittest 


class InitializationMixin(object):  # line 6: class InitializationMixin(object):
    """Tests for the MidiIn actor."""  # line 7:     """Tests for the MidiIn actor."""

    def test_initialization_needed(self):  # line 9:     def test_initialization_needed(self):
# When the actor is created, it is unititialized
        self.assertFalse(self.actor.initialized)  # line 11:         self.assertFalse(self.actor.initialized)

    def test_initialization_on_first_message(self):  # line 13:     def test_initialization_on_first_message(self):
# After the first message is processed, the actor is initialized.
        assert self.actor.initialized == False, 'unexpected initialization'  # line 15:         assert self.actor.initialized == False, 'unexpected initialization'
        self.actor.receiveMessage('nop', sender=None)  # line 16:         self.actor.receiveMessage('nop', sender=None)
        self.assertTrue(self.actor.initialized)  # line 17:         self.assertTrue(self.actor.initialized)


class FauxMidiPort(object):  # line 20: class FauxMidiPort(object):

    name = None  # line 22:     name = None
    polled = False  # line 23:     polled = False

    def __init__(self, name):  # line 25:     def __init__(self, name):
        self.name = name  # line 26:         self.name = name

    def poll(self):  # line 28:     def poll(self):
        self.polled = True  # line 29:         self.polled = True
        return None  # line 30:         return None


class FauxRef(object):  # line 33: class FauxRef(object):

    def __init__(self):  # line 35:     def __init__(self):
        self.wakeups = []  # line 36:         self.wakeups = []

    def wakeupAfter(self, timePeriod=None):  # line 38:     def wakeupAfter(self, timePeriod=None):
        self.wakeups.append(timePeriod)  # line 39:         self.wakeups.append(timePeriod)


def faux_create(actor_class):  # line 42: def faux_create(actor_class):
    actor = actor_class()  # line 43:     actor = actor_class()
    actor._myRef = FauxRef()  # line 44:     actor._myRef = FauxRef()
    return actor  # line 45:     return actor


class WakeupsForeverMixin(object):  # line 48: class WakeupsForeverMixin(object):
    """Does the actor keep a pending wakeup message forever?"""  # line 49:     """Does the actor keep a pending wakeup message forever?"""


    def test_init_wakeup(self):  # line 52:     def test_init_wakeup(self):
# Once initialized, the actor fires a wakeupAfter() so as to keep events pumping.
        wakeups = self.actor._myRef.wakeups  # line 54:         wakeups = self.actor._myRef.wakeups
        assert wakeups == [], 'unexpected early wakeups'  # line 55:         assert wakeups == [], 'unexpected early wakeups'
        self.actor.receiveMessage('nop', sender=None)  # line 56:         self.actor.receiveMessage('nop', sender=None)
        self.assertEqual(len(wakeups), 1)  # line 57:         self.assertEqual(len(wakeups), 1)

    def test_next_wakeup(self):  # line 59:     def test_next_wakeup(self):
# When sent a WakeupMessage, another will be queued.
        wakeups = self.actor._myRef.wakeups  # line 61:         wakeups = self.actor._myRef.wakeups
        assert wakeups == [], 'unexpected early wakeups'  # line 62:         assert wakeups == [], 'unexpected early wakeups'
# Since the actor isn't yet initialized and initialization creates a
# wakeup, we have to intiialize it and then clear the list of wakeups.
        self.actor.receiveMessage('nop', sender=None)  # line 65:         self.actor.receiveMessage('nop', sender=None)
        assert len(wakeups) == 1, 'init did not create wakeup'  # line 66:         assert len(wakeups) == 1, 'init did not create wakeup'
        del wakeups[:]  # line 67:         del wakeups[:]

# Now we're ready for the real test: does the actor create a new wakeup
# if it recieves one.
        self.actor.receiveMessage(thespian.actors.WakeupMessage(0), sender=None)  # line 71:         self.actor.receiveMessage(thespian.actors.WakeupMessage(0), sender=None)
        self.assertEqual(len(wakeups), 1)  # line 72:         self.assertEqual(len(wakeups), 1)


def init_actor(func):  # line 75: def init_actor(func):
    """Decorator to trigger actor initialzation by sending it a NO-OP message.
    """  # line 77:     """

    @_coconut_tco  # line 78: 
    def wrapper(self):  # line 79:     def wrapper(self):
        self.actor.receiveMessage('nop', sender=None)  # line 80:         self.actor.receiveMessage('nop', sender=None)
        assert self.actor.initialized == True, 'failed to initialize actor'  # line 81:         assert self.actor.initialized == True, 'failed to initialize actor'
        raise _coconut_tail_call(func, self)  # line 82:         return func(self)

    return wrapper  # line 84:     return wrapper


class TestMidiIn(unittest.TestCase, InitializationMixin, WakeupsForeverMixin):  # line 87: class TestMidiIn(unittest.TestCase, InitializationMixin, WakeupsForeverMixin):
    """Tests for the MidiIn actor."""  # line 88:     """Tests for the MidiIn actor."""

    def setUp(self):  # line 90:     def setUp(self):
        self.actor = faux_create(launchpad.MidiIn)  # line 91:         self.actor = faux_create(launchpad.MidiIn)
        self.actor.open_input_port = FauxMidiPort  # line 92:         self.actor.open_input_port = FauxMidiPort

    @init_actor  # line 93: 
    def test_midi_port_name(self):  # line 95:     def test_midi_port_name(self):
# The correct name is used when opening the MIDI port.
        self.assertEqual(self.actor.port.name, 'Launchpad MK2 MIDI 1')  # line 97:         self.assertEqual(self.actor.port.name, 'Launchpad MK2 MIDI 1')

    @init_actor  # line 98: 
    def test_wakeups_poll(self):  # line 100:     def test_wakeups_poll(self):
# Every time a wakeup message is received by the actor, the MIDI input
# port is polled.
        self.actor.open_input_port.polled = False  # line 103:         self.actor.open_input_port.polled = False
        self.actor.receiveMessage(thespian.actors.WakeupMessage(0), sender=None)  # line 104:         self.actor.receiveMessage(thespian.actors.WakeupMessage(0), sender=None)
        self.assertTrue(self.actor.port.polled)  # line 105:         self.assertTrue(self.actor.port.polled)
