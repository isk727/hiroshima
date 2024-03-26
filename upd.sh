#!/bin/bash
base='/usr/share/webiopi/'
git='https://raw.githubusercontent.com/isk727/hiroshima/main/'
today=`date "+%Y%m%d%H%M%S"`
wget ${git}p2pv64.html
chmod 777 p2pv64.html
wget ${git}scriptv.js
chmod 777 scriptv.js
wget ${git}stylev.css
chmod 777 stylev.css
wget ${git}stylev_sp.css
chmod 777 stylev_sp.css
sudo mv ${base}p2pv.html ${base}p2pv.html.${today}
sudo mv p2pv64.html ${base}p2pv.html
sudo mv ${base}js/scriptv.js ${base}js/scriptv.js.${today}
sudo mv scriptv.js ${base}js/scriptv.js
sudo mv ${base}css/stylev.css ${base}css/stylev.css.${today}
sudo mv stylev.css ${base}css/stylev.css
sudo mv ${base}css/stylev_sp.css ${base}css/stylev_sp.css.${today}
sudo mv stylev_sp.css ${base}css/stylev_sp.css
echo 'Update is completed!'
