#!/usr/bin/env python3

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

import pipreqs
import piptools
import os
import fileinput

security = ["urllib3>=1.24.2", "requests>=2.20", "pillow>=6.2"]

os.system("pipreqs . --savepath requirements.in --use-local")

for line in fileinput.input(files=["requirements.in"], inplace=True, backup='.bak'):
  print(line.replace("==", ">="))

f=open("requirements.in", "a+")
f.write("%s\r\n" % "\r\n".join(security))
f.close()

os.system('CUSTOM_COMPILE_COMMAND="util/genreqs.py" pip-compile requirements.in')
