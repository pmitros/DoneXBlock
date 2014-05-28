#!/usr/bin/env python
import yaml
import os

commands = '''
git mv ./done/done.py ./done/{shortname}.py
git mv ./done/static/html/done.html ./done/static/html/{shortname}.html
git mv ./done/static/css/done.css ./done/static/css/{shortname}.css
git mv ./done/static/js/src/done.js ./done/static/js/src/{shortname}.js
git mv done {shortname}

find . -type f | grep -v git | xargs sed -i 's/done/{shortname}/g'
find . -type f | grep -v git | xargs sed -i 's/Done/{Shortname}/g'

git remote rm origin
git remote add origin {github}
git commit -a -m "Initializing repo"
git push --set-upstream origin master
'''

os.system("editor config.yaml")

settings = yaml.load(open("config.yaml", 'r'))
commands = commands.format(shortname = settings["short-name"],
                           Shortname = settings["short-name"].capitalize(),
                           github = settings["github"])

readme = open("README.md", "w")
readme.write("\n".join(["{Shortname}XBlock".format(Shortname = settings["short-name"].capitalize()),
                        "==============", 
                        "",
                        settings["description"],
                        "",
                        settings["overview"]]))
                   
readme.close()

for command in commands.split("\n"): 
    if len(command) > 0:
        print command
        os.system(command)

