import yaml

commands = '''
git mv ./template/template.py ./template/{shortname}.py
git mv ./template/static/html/template.html ./template/static/html/{shortname}.html
git mv ./template/static/css/template.css ./template/static/css/{shortname}.css
git mv ./template/static/js/src/template.js ./template/static/js/src/{shortname}.js
git mv template {shortname}

find . -type f | grep -v git | xargs sed -i 's/template/{shortname}/g'
find . -type f | grep -v git | xargs sed -i 's/Template/{Shortname}/g'

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
readme.writelines(["{Shortname}XBlock".format(Shortname = settings["short-name"].capitalize()),
                   "==============", 
                   "",
                   settings["description"],
                   ""
                   settings["overview"]])
                   

for command in commands: 
    if len(command > 0):
        print command
        os.system(command)

