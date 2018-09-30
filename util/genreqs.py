#!/usr/bin/env python3

import pipreqs
import piptools
import os
import fileinput

os.system("pipreqs . --savepath requirements.in")

for line in fileinput.input(files=["requirements.in"], inplace=True, backup='.bak'):
  print(line.replace("==", ">="))

os.system('CUSTOM_COMPILE_COMMAND="util/genreqs.py" pip-compile requirements.in')
