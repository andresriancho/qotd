What is this?
-------------

Have you ever wondered how you get the login messages when you log
into your school's or companies' servers?

Have you ever wondered why some people get quotes of the day as their
login messages and some get the same boring notices everyday?

Have you ever wondered how you can configure your system to deliver
you some reasonably smart quotes and only discovered that you don't
have write permission to ``/etc/motd``?

If you have answered yes to any of the above questions, then
QuoteOfTheDay is for you. This module simply goes to The Quotations
Page (www.quotationspage.com) to pull the quotes and motivational
quotes of the day for the past 10 days, pickles the cached quotes in
your home directory (so we are all good netizens), and randomly picks
one to display on your console everytime you invoke the ``qotd``
script. As a bonus feature, you can also invoke this script in your
``.login`` files to see a quote of the day (or the session anyway) :P.


Download:
---------

Just grab the source package from below or follow the URL to download
the latest revision from the repository.


Install:
--------

Unzip or untar the package, change directory into the extracted
distribution and type:

::

    $ python setup.py install

or if you want to do a user-specific installation:

::

    $ python setup.py install --install-lib $YOUR_PYTHON_SITE_PACKAGES_PATH --install-scripts $YOUR_PYTHON_SCRIPT_PATH

or

::

    $ python setup.py install --home ~/

or something to these effects, as long as the end-users have access to
the qotd script.

If you want to see a quote every time you login using a terminal, you
can put something similiar to the following in your .bash_profile or
.bashrc if you use BASH.

::

    if [ -f ~/bin/qotd ]; then ~/bin/qotd; fi

As usual, consult your shell's manual to find out how to invoke a
script at login time.


Feedback and Bug reports:
-------------------------
See `this <https://github.com/andresriancho/qotd>`_ GitHub repository.


Release Notes:
--------------
- 0.7.3
  Moved to GitHub and re-added to PyPi

- 0.7.1
  No more ugly stacktraces when internet connection cannot be established 

- 0.7 release
  Fixed a few Unicode handling bugs, most notably a crasher and replace the
  Unicode replacement character with a space.

- 0.7b4
  Simplified error handling code.

- 0.7b3
  Rewrote connection handling to deal with redirects
  Added extra robustness to deal with bad XML data.

- 0.7b2
  Fixed bug where weird unicode string bombs out str().

- 0.7b1
  Initial beta release.
