from fabric import SerialGroup as Group, Connection

app_ws_servers = [
    "139.59.136.182",
    "165.22.89.205",
    "165.227.167.134"
]

redis_server = "165.22.89.227"


def setup_systemd(conn):
    conn.run('cp ava-appserver/appserver.service /lib/systemd/system')
    conn.run('chmod 766 /lib/systemd/system/appserver.service')

    conn.run('cp ava-appserver/avalanche.service /lib/systemd/system')
    conn.run('chmod 766 /lib/systemd/system/appserver.service')

    conn.run('systemctl daemon-reload')


def install_avalanche(conn):
    conn.run('ulimit -n 500000')

    conn.run('rm -rf avalanche')
    conn.run('mkdir -p /var/log/avalanche')
    conn.run('touch /var/log/avalanche/avalanche.log')
    conn.run('chmod 766 /var/log/avalanche/avalanche.log')

    conn.run('git clone git@github.com:furqan-shakoor/avalanche.git')
    conn.put('prod_settings_avalanche.py', 'avalanche/settings.py')
    conn.run('cd avalanche && pip3 install -r requirements.txt')

    conn.run('systemctl restart avalanche.service')


def install_app_server(conn):
    conn.run('ulimit -n 500000')

    conn.run('rm -rf avalanche')
    conn.run('mkdir -p /var/log/avalanche')
    conn.run('touch /var/log/avalanche/appserver.log')
    conn.run('chmod 766 /var/log/avalanche/appserver.log')

    conn.run('rm -rf ava-appserver')
    conn.run('git clone git@github.com:furqan-shakoor/ava-appserver.git')
    conn.put('prod_settings.py', 'ava-appserver/settings.py')
    conn.run('cd ava-appserver && pip3 install -r requirements.txt')

    conn.run('systemctl restart appserver.service')


def install_perf_tests(conn):
    conn.run('ulimit -n 500000')

    conn.run('rm -rf ava-test')
    conn.run('git clone https://github.com/furqan-shakoor/ava-test.git')
    conn.run('cd ava-test && pip3 install -r requirements.txt')


def deploy():
    for app_ws_server_ip in app_ws_servers:
        app_ws = Connection(f"root@{app_ws_server_ip}")
        install_app_server(app_ws)
        install_avalanche(app_ws)

    redis_conn = Connection(f"root@{redis_server}")
    install_perf_tests(redis_conn)


if __name__ == "__main__":
    deploy()
