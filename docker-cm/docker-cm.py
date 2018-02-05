#!/usr/bin/env python
# -*- coding:utf-8 -*-
import flask
import docker
tls_config = docker.tls.TLSConfig(client_cert=('D:\\onedrive\\docker-cm-tls\\cert.pem','D:\\onedrive\\docker-cm-tls\\key.pem'), verify=False)
app = flask.Flask(__name__, static_url_path='')
@app.route('/containers')
def index():
    client = docker.DockerClient(base_url='https://192.168.58.157:2375', tls=tls_config)
    docker_list = client.containers.list()
    return docker_list
app.run(host='0.0.0.0', port=6011)