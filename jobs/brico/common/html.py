####
## Copyright © 2018 Beads Land-Trujillo.
##
## This program is free software: you can redistribute it and/or modify
## it under the terms of the GNU Affero General Public License as published
## by the Free Software Foundation, either version 3 of the License, or
## (at your option) any later version.
##
## This program is distributed in the hope that it will be useful,
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
## GNU Affero General Public License for more details.
##
## You should have received a copy of the GNU Affero General Public License
## along with this program.  If not, see <https://www.gnu.org/licenses/>.
####

class elem:
  def __init__(self, tag):
    self.tag = tag
    self.attributes = {}
    self.content = ""

  def __str__(self):
    front = [ "%s=\"%s\"" % (k, v) for (k, v) in self.attributes.items() ]
    front.insert(0, "<" + self.tag)
    front.append(">")
    return "".join([ " ".join(front), self.content, "</%s>" % self.tag ])

  def attr(self, attr, val):    self.attributes[attr] = val; return self;
  def inner(self, inner):       self.content = inner; return self;
  def str(self):                return self.__str__()

  def clss(self, clss):         return self.attr('class', clss);
  def id(self, id):             return self.attr('id', id);
  def style(self, style):       return self.attr('style', style);
  def src(self, src):           return self.attr('src', src);
  def href(self, src):          return self.attr('href', src);
  def target(self, src):        return self.attr('target', src);

class span(elem):
  def __init__(self):   elem.__init__(self, 'span')
class div(elem):
  def __init__(self):   elem.__init__(self, 'div')
class img(elem):
  def __init__(self):   elem.__init__(self, 'img')
class a(elem):
  def __init__(self):   elem.__init__(self, 'a')
