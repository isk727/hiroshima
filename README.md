1) /usr/share/webiopy直下に"python"ディレクトリを作成する
$ sudo mkdir /usr/share/webiopi/python
$ sudo chmod 777 /usr/share/webiopi/python -fR

2) /usr/share/webiopy/htdocs直下に"api"ディレクトリを作成する
$ sudo mkdir /usr/share/webiopi/htdocs/api
$ sudo chmod 777 /usr/share/webiopi/htdocs/api -fR

3) install用バッチファイルをダウンロードして実行
$ wget https://raw.githubusercontent.com/isk727/hiroshima/main/upd.sh
$ sudo chmod 777 upd.sh
$ ./upd.sh

4) webiopiを再起動する
$ sudo systemctl restart webiopi
