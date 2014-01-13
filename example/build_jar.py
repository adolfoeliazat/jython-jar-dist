#!/usr/bin/env jython
from __future__ import (absolute_import, print_function)

import glob
import importlib
import os
from os.path import abspath, dirname, exists, isabs, join, splitext
import shutil
import sys 
from zipfile import ZipFile

import logging
logging.basicConfig(level=logging.WARN)
log = logging.getLogger(__file__)


# MUST Configure
PACKAGE = 'blah'
RUN_FILE = '__run__.py'

# Optional Configuration
"These variables are required but probably do not need to be changed"
PWD = dirname(abspath(__file__))
BUILD_DIR = '_build'
DIST_DIR = 'dist'
EXTERNAL_JARS = ('lib/*.jar', ) 


def getJarName():
    try:
        pkg = importlib.import_module(PACKAGE)
        JAR_NAME = PACKAGE + '-' + pkg.__version__ + '.jar'
    except AttributeError:
        log.warn("No version found for package '%s'" % PACKAGE)
        JAR_NAME = PACKAGE + '.jar'
    log.debug("JAR_NAME will be: " + JAR_NAME)
    return(JAR_NAME)


def getJythonInstall():
    return sys.real_prefix

def getExternalJars():
    matches = []
    for path in EXTERNAL_JARS:
        if not isabs(path): path = join(PWD, path)
        matches.extend([abspath(f) for f in glob.glob(path)])
    return [p for p in matches if splitext(p)[1] == '.jar']

def explode(jar):
    with ZipFile(jar, 'r') as z:
        z.extractall('Lib')

def addToArchive(z, path):
    for root, dirs, files in os.walk(path):
        z.write(root)
        for f in files:
            z.write(join(root, f))

def clean():
    if exists(BUILD_DIR):
        shutil.rmtree(BUILD_DIR)
    #shutil.rmtree(DIST_DIR)


if __name__ == '__main__':
    if not hasattr(sys, 'real_prefix') or not hasattr(sys, 'JYTHON_JAR'):
        log.error("Jython Virtual Environment not activated")
        sys.exit(1)
        
    clean()
    JAR_NAME = getJarName()

    for d in [DIST_DIR, BUILD_DIR]:
        if not exists(d): os.makedirs(d)

    os.chdir(BUILD_DIR)

    JYTHON_INSTALL = getJythonInstall()
    log.debug(" JYTHON INSTALL Directory: " + JYTHON_INSTALL)

    shutil.copyfile(join(JYTHON_INSTALL, 'jython.jar'), JAR_NAME)

    shutil.copytree(join(JYTHON_INSTALL, 'Lib'), 'Lib',
            ignore=lambda p,f: ['test'] if p == join(JYTHON_INSTALL, 'Lib') else [])

    log.debug(" EXTERNAL_JARS: " + str(getExternalJars()))
    [explode(jar) for jar in getExternalJars()]

    shutil.copytree(join(PWD, PACKAGE), PACKAGE)
    shutil.copyfile(join(PWD, RUN_FILE), '__run__.py')

    with ZipFile(JAR_NAME, 'a') as z:
        addToArchive(z, 'Lib')
        addToArchive(z, PACKAGE)
        z.write('__run__.py')

    shutil.move(JAR_NAME, join(PWD, DIST_DIR, JAR_NAME))
    print(" BUILD Complete. see '%s'" % join(DIST_DIR, JAR_NAME))
