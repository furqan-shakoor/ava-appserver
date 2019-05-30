from fabric import SerialGroup as Group, Connection

app_ws_servers = [
    "139.59.136.182",
    "165.22.89.205"

]

for app_ws_server_ip in app_ws_servers:
    app_ws = Connection(f"root@{app_ws_server_ip}")

    app_ws.run('ulimit -Sn 500000')

    app_ws.run('rm -rf avalanche')
    app_ws.run('rm -rf ava-appserver')

    app_ws.run('git clone git@github.com:furqan-shakoor/avalanche.git')
    app_ws.run('git clone git@github.com:furqan-shakoor/ava-appserver.git')

    app_ws.put('prod_settings.py', 'ava-appserver/settings.py')
    app_ws.put('prod_settings_avalanche.py', 'avalanche/settings.py')

    app_ws.run('cd ava-appserver && pip3 install -r requirements.txt')
    app_ws.run('cd avalanche && pip3 install -r requirements.txt')
