####
# Original recipes from "1.18. Replacing Multiple Patterns in a Single Pass",
# Python Cookbook™, Second Edition copyright (c) 2005, 2002 Xavier Defrang
# and Alex MartelliAlex Martelli. Published by O’Reilly Media, Inc.
# ISBN: 0596007973.
# https://www.oreilly.com/library/view/python-cookbook-2nd/0596007973/ch01s19.html
#
# O'Reilly books are here to help you get your job done. In general,
# you may use the code in O'Reilly books in your programs and documentation.
# You do not need to contact us for permission unless you're reproducing a
# significant portion of the code. For example, writing a program that uses
# several chunks of code from our books does not require permission.
# Answering a question by citing our books and quoting example code does
# not require permission. On the other hand, selling or distributing a
# CD-ROM of examples from O'Reilly books does require permission.
# Incorporating a significant amount of example code from our books into
# your product's documentation does require permission.
#
# We appreciate, but do not require, attribution. An attribution usually
# includes the title, author, publisher, and ISBN.
#
# If you think your use of code examples falls outside fair use or the
# permission given here, feel free to contact us at permissions@oreilly.com.
#
# Please note that the examples are not production code and have not been
# carefully tested. They are provided "as-is" and come with no warranty
# of any kind.
####

import re
def make_xlat(*args, **kwds):
    adict = dict(*args, **kwds)
    rx = re.compile('|'.join(map(re.escape, adict)))
    def one_xlat(match):
        return adict[match.group(0)]
    def xlat(text):
        return rx.sub(one_xlat, text)
    return xlat

def multiple_replace(text, adict):
  translate = make_xlat(adict)
  return translate(text)
