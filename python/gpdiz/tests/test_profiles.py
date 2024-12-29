# -*- coding: utf-8 -*-
import pytest

from gpdiz.inifile import Profiles


class Test_profiles(object):

    def test_cd(self):
        prof = Profiles()
        (samp, bdep) = prof.content("cd")
        assert samp == 44100
        assert bdep == 16

    def test_16b48k(self):
        prof = Profiles()
        (samp, bdep) = prof.content("16b48k")
        assert samp == 48000
        assert bdep == 16

    def test_24b96k(self):
        prof = Profiles()
        (samp, bdep) = prof.content("24b96k")
        assert samp == 96000
        assert bdep == 24

    def test_24b384k(self):
        prof = Profiles()
        (samp, bdep) = prof.content("24b384k")
        assert samp == 384000
        assert bdep == 24
