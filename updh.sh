#!/bin/bash
base='/usr/share/webiopi/'
git='https://raw.githubusercontent.com/isk727/hiroshima/main/'
today=`date "+%Y%m%d%H%M%S"`
wget ${git}config.ini
chmod 777 config.ini
wget ${git}game.py
chmod 777 game.py
wget ${git}script.py
chmod 777 script.py
wget ${git}api.js
chmod 777 api.js
wget ${git}webiopi.html
chmod 777 webiopi.html
sudo mv ${base}python/config.ini ${base}python/config.ini.${today}
sudo mv config.ini ${base}python/config.ini
sudo mv ${base}python/game.py ${base}python/game.py.${today}
sudo mv game.py ${base}python/game.py
sudo mv ${base}python/script.py ${base}python/script.py.${today}
sudo mv script.py ${base}python/script.py
sudo mv ${base}htdocs/api/api.js ${base}htdocs/api/api.js.${today}
sudo mv api.js ${base}htdocs/api/api.js
sudo mv ${base}htdocs/api/webiopi.html ${base}htdocs/api/webiopi.html.${today}
sudo mv webiopi.html ${base}htdocs/api/webiopi.html
sudo systemctl restart webiopi
echo 'Update is completed!'
