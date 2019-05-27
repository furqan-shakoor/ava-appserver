from fabric import SerialGroup as Group, Connection

app_ws = Connection("root@165.22.94.86")

app_ws.run('rm -rf avalanche')
app_ws.run('rm -rf ava-appserver')
app_ws.run('git clone git@github.com:furqan-shakoor/avalanche.git')
app_ws.run('git clone git@github.com:furqan-shakoor/ava-appserver.git')
app_ws.put('prod_settings.py', 'ava-appserver/settings.py')
app_ws.run('cd ava-appserver && pip3 install -r requirements.txt')
app_ws.run('cd avalanche && pip3 install -r requirements.txt')