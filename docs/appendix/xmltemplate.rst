.. _xml_template_intro:

Introduction to XML::Template
=============================

.. Note:: This is shamelessly ripped from http://bzr.sesse.net/xml-template/doc/intro.txt
          and converted to RST. The examples are in Perl, but the syntax is close to
          identical.

XML::Template is a templating system; there are already many others, so if
you do not like it, look into a different one (its design is inspired by
at least Template Toolkit and Kid, probably also including elements from
others). XML::Template is (like Kid or TAL) designed to guarantee that your
output is well-formed XML, which is a good step on the road to give you
valid XHTML.

You can get the latest version of XML::Template with bzr; get bzr from your
favourite distribution and do::

    $ bzr get http://bzr.sesse.net/xml-template/

to check out the code and this documentation.

There is a lot to be said about design philosophy, but let's first give a
simple example to give you the feel of how it works. (The example is in Perl,
but there are also functionally equivalent PHP, Python and Ruby versions;
ports to other languages would be welcome.)

Template (simple.xml)

.. code-block:: xml

    <?xml version="1.0" encoding="UTF-8" standalone="yes"?>
    <!DOCTYPE
      html PUBLIC "-//W3C//DTD XHTML 1.1//EN"
      "http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">
    <html xmlns="http://www.w3.org/1999/xhtml" xmlns:t="http://template.sesse.net/" xml:lang="en">
      <head>
        <title />
      </head>
      <body>
        <p t:id="hello">This will be replaced.</p>
      </body>
    </html>

Code (simple.pl)

.. code-block:: perl

    #! /usr/bin/perl
    use XML::Template;

    my $doc = XML::Template::process_file('../xml/simple.xml', {
        'title' => 'A very basic example',
        '#hello' => 'Hello world!'
    });
    print $doc->toString;

Result

.. code-block:: xml

    <?xml version="1.0" encoding="UTF-8" standalone="yes"?>
    <!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN" "http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">
    <html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en">
      <head>
        <title>A very basic example</title>
      </head>
      <body>
        <p>Hello world!</p>
      </body>
    </html>

This is about as simple as it gets, but we've already touched on most of the
functionality we want or need. A few points are worth commenting on:

 - We template by first _selecting_ certain elements (either by tag name, or
   by ID -- the syntax is borrowed from CSS since you probably already know
   it), then _replace_ their contents. (Soon, we'll also _clone_ elements.)
 - We get a DOM tree out, which we can either print out or do other things
   with (say, style further if XML::Template should not prove enough).
   (Actually, we start with a DOM tree as well, but process_file is a
   shortcut to read in an XML file and parse it into a DOM tree first, since
   that's usually what we want.)
 - All traces of our templating system have been removed -- there is a flag
   you can give to prohibit this "cleaning" in case you don't want that.

Note how little syntax we need to do simple things -- XML::Template is
designed to *keep simple things simple*, since you want to do simple things
most of the time. (I don't believe in "lines of code" as the primary metric
for API usability in general, though.)

We move on to another useful operation, cloning.

Template (clone.xml)

.. code-block:: xml

  <?xml version="1.0" encoding="UTF-8" standalone="yes"?>
  <!DOCTYPE
    html PUBLIC "-//W3C//DTD XHTML 1.1//EN"
    "http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">
  <html xmlns="http://www.w3.org/1999/xhtml" xmlns:t="http://template.sesse.net/" xml:lang="en">
    <head>
      <title>Cloning test</title>
    </head>
    <body>
       <p>My favourite color is <t:color />; I like that very much.
         All my favourite things:</p>
      <ul t:id="things">
        <li />
      </ul>
    </body>
  </html>

Code (clone.pl)

.. code-block:: perl

  #! /usr/bin/perl
  use XML::Template;

  my $doc = XML::Template::process_file('../xml/clone.xml', {
      'color' => 'blue',
      '#things' => [
          { 'li' => 'Raindrops on roses' },
          { 'li' => 'Whiskers on kittens' },
          { 'li' => 'Bright copper kettles' },
          { 'li' => 'Warm, woolen mittens'}
      ]
  });
  print $doc->toString;

Result

.. code-block:: xml

  <?xml version="1.0" encoding="UTF-8" standalone="yes"?>
  <!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN" "http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">
  <html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en">
    <head>
      <title>Cloning test</title>
    </head>
    <body>
       <p>My favourite color is blue; I like that very much.
         All my favourite things:</p>
      <ul>
        <li>Raindrops on roses</li>

        <li>Whiskers on kittens</li>

        <li>Bright copper kettles</li>

        <li>Warm, woolen mittens</li>
      </ul>
    </body>
  </html>

This isn't much harder than the example above; we've done a simple replacement
of the contents of <t:color> to "blue" (and after that just removed the tag;
any tag you use in the templating namespace will automatically get stripped
away), and then cloned the contents of our "things" bullet list. Note that
XML::Template automatically recurses after the cloning, since you probably
don't want four identical elements. You can recurse as many times as you'd like,
in case you'd need lists of lists or multiple tables and rows and columns --
you don't even have to understand what's happening to get it to work.

Note that we did all of this without any logic in the template at all. This
is completely intentional -- it's a bit of an experiment, really, but hopefully
it will all turn out well. There is no logic in the templating system at all;
if-s are handled with replacements (or DOM deletions), for-s are handled with
cloning and expressions are handled by the language you're using.

This means we have introduced all three operations we need (replacement,
substitution/selection and repeating/cloning), and only need two more features
before we're all done.

The first one is just a variation on replacement; instead of replacing with
a string, you can replace with a DOM tree or document. This facilitates simple
inclusion, since you probably want some header and footer to be the same
across all your pages. (No example here, you can probably work it out by
yourself; just send a DOM object instead of a string. There's an example in
the source code distribution if you need it.)

The second one is also a variation on replacement; sometimes, you want to
set attributes on elements instead of replacing their contents, and for that,
we have a small hack:

Template (clone.xml), repeated for your convenience

.. code-block:: xml

  <?xml version="1.0" encoding="UTF-8" standalone="yes"?>
  <!DOCTYPE
    html PUBLIC "-//W3C//DTD XHTML 1.1//EN"
    "http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">
  <html xmlns="http://www.w3.org/1999/xhtml" xmlns:t="http://template.sesse.net/" xml:lang="en">
    <head>
      <title>Cloning test</title>
    </head>
    <body>
      <p>My favourite color is <t:color />; I like that very much.
        All my favourite things:</p>
      <ul t:id="things">
        <li />
      </ul>
    </body>
  </html>


Code (attribute.pl)

.. code-block:: perl

  #! /usr/bin/perl
  use XML::Template;

  my $doc = XML::Template::process_file('../xml/clone.xml', {
      'color' => 'red',
      '#things' => [
          { 'li' => 'Raindrops on roses',    'li/class' => 'odd' },
          { 'li' => 'Whiskers on kittens',   'li/class' => 'even' },
          { 'li' => 'Bright copper kettles', 'li/class' => 'odd' },
          { 'li' => 'Warm, woolen mittens',  'li/class' => 'even' }
      ]
  });
  print $doc->toString;

Result

.. code-block:: xml

  <?xml version="1.0" encoding="UTF-8" standalone="yes"?>
  <!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN" "http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">
  <html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en">
    <head>
      <title>Cloning test</title>
    </head>
    <body>
       <p>My favourite color is red; I like that very much.
         All my favourite things:</p>
      <ul>
        <li class="odd">Raindrops on roses</li>

        <li class="even">Whiskers on kittens</li>

        <li class="odd">Bright copper kettles</li>

        <li class="even">Warm, woolen mittens</li>
      </ul>
    </body>
  </html>

Naturally, you can't put anything else than a simple string into an attribute,
but it's not like this is a big limitation. (There's also a shortcut for doing
stuff like odd/even automatically, but I'll leave that for yourself to find out;
see the attribute2 example.)

That's it for the examples; now let's turn to the boring design philosophy.

The main thoughts behind XML::Template have been, in no particular order:

 - Make the simple things simple. (A template should not be much more cumbersome
   to write than if you wrote the page statically.) More complex things can be
   harder if it makes the simple things simpler; that's OK.
 - Make it easy for the user to do the right thing. (Guarantee well-formed XML,
   and make a design that makes it easy to separate back-end logic, viewing logic
   and HTML templating. Incidentially, I've only seen one library ever that does
   the same properly for database logic and other back-end logic, and that is the
   excellent libpqxx library.)
 - Premature optimization is the root of all evil; most web systems are not
   performance limited by their output anyway.
 - Don't try to be everything for everyone. (XML::Template can not output to
   plain text or PostScript, even though that would clearly be useful for some
   people in some cases.)
 - Be language agnostic. (DOM is rather universal, and there's a useful
   implementation for most web-relevant languages out there.) Maintaining
   several implementations in several languages is suboptimal, but it's better
   than only supporting one language or having someting that needs to reimplement
   the entire DOM with wrappers for each language. (Thankfully, by relying on
   the DOM support in each language, the code so far is under 200 lines per
   implementation, so maintaining this hopefully shouldn't be much work.) As
   proof-of-concept, there are got Perl, PHP, Python and Ruby implementations
   that work and feel largely the same (and even a SAX-based Perl
   implementation, for larger trees that won't fit into memory) -- other
   implementations are welcome.  This is backed up by a test suite, which
   ensures that all the different implementations return structurally
   equivalent XML for a certain set of test cases. Porting to a new language
   is not difficult, and once you've got all the test cases to pass, your
   work is most likely done.

As a side note to the second point, I've spent some time wondering exactly
_why_ you want to separate the back-end logic from your HTML, and why people
don't seem to do it. After some thought, I've decided that what I really want
is to get the HTML away from my code -- not the other way round. (In other
words, HTML uglifies code more then code uglifies HTML -- someone using a
WYSIWYG editor to generate their HTML might disagree, though.)

However, this also means that you want the _entire_ viewing logic away from
your back-end logic if you can. When you process your data, you really don't
want to care if you're on an odd or even row to get those styled differently
in the HTML; that's for another part. XML::Template, incidentially, by
moving the entire output logic to the end of your script, makes this easy
for you; you *can* do the viewing logic "underway" if you really want to,
but there's no incentive to, and the natural modus operandi is to split
viewing and other logic into two distinct parts.

An open question is how to do internationalization on web pages; I haven't
yet seen a good system for handling this. To be honest, this might be something
handled in another layer (cf. "don't try to be everything to everyone" above),
but I'd be interesting to hear others' thoughts on this, especially how
you could achieve clean text/markup separation (stuff like gettext doesn't
really work well with markup in general).

More to come here at some point, probably. Now, go out and just _use_ the
thing -- I hope it will make your life on the web simpler. :-)

  - Steinar H. Gunderson <sgunderson@bigfoot.com>, http://www.sesse.net/

