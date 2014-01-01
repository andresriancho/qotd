#    Copyright (C) 2010 Yuen Ho Wong
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.

from distutils.core import setup


setup(name='QuoteOfTheDay',
      version='0.7.2',

      author='Yuen Ho Wong',
      author_email='wyuenho@gmail.com',

      maintainer='Andres Riancho',
      maintainer_email='andres.riancho@gmail.com',

      url='https://github.com/andresriancho/qotd',
      description='A simple quote of the day script users can invoke from their'
                  ' home directories without modifying /etc/motd.',
      long_description=open('README.rst', 'r').read(),
      classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Intended Audience :: End Users/Desktop',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Operating System :: POSIX',
        'Operating System :: MacOS',
        'Operating System :: Unix',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.5',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Topic :: Other/Nonlisted Topic',
        ],
      py_modules=['qotd'],
      scripts=['scripts/qotd']
      )
