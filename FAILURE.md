
## Getting Started: Download Jython and create VirtualEnv

Download a full traditional installer of Jython (2.7b1)

Install `ALL` to `$HOME/jython2.7b1`

Tried to create virtualenv with jython exe. FAIL

    ERROR: The executable test-jython/bin/jython is not functioning
    ERROR: It thinks sys.prefix is u'/home/bnjmn/jython2.7b1' (should be u'/home/bnjmn/.venvs/test5-jython2.5')
    ERROR: virtualenv is not compatible with this system or executable

Tried upgrading `virtualenwrapper`. Same ISSUE. 

Tried it with other jython install (`/opt/jython2.5.3`). Same ISSUE.

Realized `$JYTHON_HOME` was causing an issue. `unset JYTHON_HOME`. SUCCESS.

    mkvirtualenv -p /path/to/jython/exe venv-name

Afterward, found [issue](https://github.com/pypa/virtualenv/issues/185) about
this on github.

## Installing Additional Python Packages

`pip` doesn't work with jython right now (see jython-ssl)

`easy_install` doesn't seem to either.

BUT you can try to install from source (this doesn't always work). 
I was able to do this with the current development version of Django:

    $ git clone https://github.com/django/django.git && cd django/
    (jython-venv)$ python setup.py install
    (jython-venv)$ python
    Jython 2.7b1 (....)
    >>> import django
    >>> django.VERSION
    (1, 7, 0, 'alpha', 0)

Watch out for any packages that use `ssl`.

Now, if you go to `$VIRTUAL_ENV/Lib/site-packages`, you should find `django` in
all it's glory.  However, I would never actually use this as only Django1.4 has
been approved for use with Jython.

## Building a jar file that will actually work

I've found some issues with the `virtualenv` way of doing things.
Specifically, `virtualenv` modifies `site.py` with a method
`virtual_install_main_packages` for add your `virtualenv` installed packages to
the path. This looks for a file, `orig-prefix.txt`, on the file system. No
bueno for creating a distributable jar. Even if it did work, it would probably
find the original sources which would only work on the original machine, but I
digress.

My workaround...

Create a copy of the `jython.jar`

    cp $JYTHON_INSTALL/jython.jar blah.jar # you can use the $VIRTUAL_ENV/jython.jar as well, just a symlink

Now we need to add the python libraries. These must be the original files NOT
the virtualenv `Lib`

    cd $JYTHON_INSTALL
    zip -r blah.jar Lib

`blah.jar` is now a functioning distributable jython.jar 

    mv blah.jar /path/anywhere/in/the/world/.
    java -jar /path/anywhere/in/the/world/blah.jar
    Jython 2.7b1 (...)
    >>> import math; math.pi
    3.141592653589793
    >>> import django
    Traceback (most recent call last):
    File "<stdin>", line 1, in <module>
    ImportError: No module named django

But we want to be able to use other python packages.
We need to add them to the archive under `Lib/site-packages`.


## In progress

Find out how jython is actually searching for modules

eg. Where is `Lib` getting loaded. `import sys; sys.path` doesn't show.

Look at `__classpath__` and `__pythonpath__/`
