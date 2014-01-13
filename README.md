Jython in a Jar
===============

[Jython][1] is Python on the JVM. It can be easily [downloaded][2] and run
anywhere there is Java. There are many reasons to use Jython. If someone using
Jython is less familiar with Java as a platform this information may be
helpful.

The intention of this repository is to outline some of the issues associated
with packaging a Jython application into a single distributable jar file and
provide a somewhat reusable solution.

### Single Jar Jython Example 

There are a few examples on the web of people having done this or having
issues with a similar situation. It took more research for me to get this to
work than I thought anyone else should have to go through.

The best example I could find for something like this was Ryan McGuire's
[Single-JAR-Jython-Example][4]. Although it does create a single jar as
promised, there is one big issue, it doesn't include the Python source required
to run any of the standard libraries. I think this could be fixed pretty easily
but I decided to roll my own script, in Jython, to bundle the jar and remove
the dependency on Simon Tuffs' [One-JAR][5].

## Using `build_jar.py`

Basically, a jar is an archive file like a zip. If you can pack it the right way,
Java can run the jar appropriately. The idea is to get all the class files you need
in the correct place and then zip them up.

This approach assumes you are using a virtualenv with a Jython interpreter. The
script will check for both these conditions and error if either is not met. 

### **MUST** Configure Parameters

<table>
  <tr>
    <td><code>PACKAGE = 'blah'</code></td>
    <td>Jython code should be organized in a single package, a directory with a <code>__init__.py</code> file. 
    Optionally, <code>__init__.py</code> can provide a <code>__version__</code> which will be in the <code>JAR_NAME.</code></td>
  </tr>
  <tr>
    <td><code>RUN_FILE = '__run__.py'</code></td>
    <td>The Jython jar will look for a run file when executed without a specific file as argument. 
    Think of this as the <code>main</code>. In the jar, it must be called <code>__run__.py</code>.</td>
  </tr>
</table>

### Optionallly Configure Parameters

These variables are required but probably do not need to be changed

<table>
  <tr>
    <td><code>PWD = dirname(abspath(__file__))</code></td>
    <td>This is the absolute path to the project directory. 
    By default, it is automatically set the directory the build script is in.</td>
  </tr>
  <tr>
    <td><code>BUILD_DIR = '_build'</code></td>
    <td>This directory is used to assemble the jar.</td>
  </tr>
  <tr>
    <td><code>DIST_DIR = 'dist'</code></td>
    <td>This directory is the final resting place for the jar.</td>
  </tr>
  <tr>
    <td><code>EXTERNAL_JARS = ('lib/*.jar', )</code></td>
    <td>This is a tuple of paths that will be globbed for jar files to include. 
    You can place any external java jar libraries in the lib directory or modify 
    this parameter with explicit paths, relative or absolute.</td>
  </tr>
</table>

### Use a `virtualenv`

You should absolutely use a virtual environment when developing Python code
and, in my opinion, Jython should not be any different. However, the current
version of Jython (2.7b1) does not support `ssl` and therefore does not work
with `pip`. This can be a little annoying if your used to having practically
any package you want with a simple `pip install blah`. 

From what I've read and experienced, Jython will work with many `python2.7`
packages as long as they do not require some native C library or `ssl`
(although there may be work arounds in certain cases). If you want to install
an external package, there are two options I've found to work:

1. copy the source code to `$VENV/Lib/site-packages` or
2. use `easy_install blah-1.2.3.tar.gz`

TODO: Add these packages in build script. Include/exclude packages needed/not
needed for distribution (e.g., requests vs py.test).

### There's no place like `JYTHON_HOME`

**DO NOT** set `JYTHON_HOME` in your shell environment. This *will* cause
[issues][3] with `virtualenv`. You might see something non-obvious like:

    ERROR: The executable test-jython/bin/jython is not functioning
    ERROR: It thinks sys.prefix is u'/home/bnjmn/jython2.7b1' (should be u'/home/bnjmn/.venvs/test-jython')
    ERROR: virtualenv is not compatible with this system or executable

`unset JYTHON_HOME` and try again.

## Outstanding Issues

- Add external python libraries from virtualenv
- Automatically compile and jar java source files in `java/` dir
- Add java jar to classpath to avoid import issues on Java classes when running
  `build`

#### References

- [Slides on Jython
  tools](http://www.slideshare.net/fwierzbicki/jython-update-2012) and where
  Jython is headed. This deck roughly outlines the process required for
  creating a jar.
- [Install external pkgs w
  jython](http://stackoverflow.com/questions/6787015/how-can-i-install-various-python-libraries-in-jython)
  is a helpful SO post.
- [Jython Essentials -- Online
  book](http://oreilly.com/catalog/jythoness/chapter/ch01.html) is worth
  referencing.
- [5 things you didn't know about
  jars](http://www.ibm.com/developerworks/java/library/j-5things6/index.html)
  by IBM has some interesting info on what makes jars different than an other
  archive.
- [Jar file format on wiki might be worth a
  look](http://en.wikipedia.org/wiki/JAR_%28file_format%29)

[1]: http://www.jython.org/
[2]: http://www.jython.org/downloads.html
[3]: https://github.com/pypa/virtualenv/issues/185
[4]: https://github.com/EnigmaCurry/Single-JAR-Jython-Example
[5]: http://one-jar.sourceforge.net/
