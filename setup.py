#! /usr/bin/env python

# setup.py - Distutils instructions for the pynids package

# This file is part of the pynids package, a python interface to libnids.
# See the file COPYING for license information.

from distutils.core import setup, Extension
from distutils.command.build import build    # nidsMaker
from distutils.spawn import spawn            # nidsMaker.run()
import os, os.path

pathjoin = os.path.join

BUILDDIR = 'libnids'

INCLUDE_DIRS  = ['/usr/local/include', '/opt/local/include']
LIBRARY_DIRS  = ['/usr/local/lib', '/opt/local/lib']
EXTRA_OBJECTS = []

class nidsMaker(build):
    NIDSDIR = BUILDDIR
    include_dirs = [ pathjoin(NIDSDIR, 'src') ]
    library_dirs = []
    extra_objects  = [ pathjoin(NIDSDIR, 'src', 'libnids.a') ]

    def buildNids(self):
        # extremely crude package builder
        if os.path.exists(self.extra_objects[0]):
            return None           # already built

        os.chdir(self.NIDSDIR)
        spawn([pathjoin('.','configure'), 'CFLAGS=-fPIC', '--disable-libglib', '--disable-libnet'])
        spawn(['make'], search_path = 1)
        os.chdir('..')

    def run(self):
        self.buildNids()
        build.run(self)

INCLUDE_DIRS = nidsMaker.include_dirs + INCLUDE_DIRS
EXTRA_OBJECTS = nidsMaker.extra_objects + EXTRA_OBJECTS

setup (# Distribution meta-data
        name = "pynids",
        version = "0.6.2",
        description = "libnids wrapper",
        author = "Wesley Shields",
        author_email = "wxs@atarininja.org",
        license = "GPL",
        long_description = \
'''pynids is a python wrapper for libnids, a Network Intrusion Detection System
library offering sniffing, IP defragmentation, TCP stream reassembly and TCP
port scan detection.
-------
''',
        cmdclass = {'build': nidsMaker},
        ext_modules = [ Extension(
                            "nidsmodule",
                            #define_macros = [ ("DEBUG", None), ],
                            sources=["nidsmodule.c"],
                            include_dirs = INCLUDE_DIRS,
                            libraries = ["pcap"],
                            library_dirs = LIBRARY_DIRS,
                            extra_objects = EXTRA_OBJECTS
                        ) 
                      ],
        url = "http://jon.oberheide.org/pynids/",
      )
