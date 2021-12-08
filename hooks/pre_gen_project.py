import os
ret = input("Do you want to install required dependencies (pyyaml, fabric) using pip? [y/N] ")
if ret.lower() == 'y':
  os.system("pip install pyyaml fabric3")
