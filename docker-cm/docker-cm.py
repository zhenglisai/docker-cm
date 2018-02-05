#!/usr/bin/env python
# -*- coding:utf-8 -*-
import sys
import flask
import docker
reload(sys)
sys.setdefaultencoding('utf-8')
#变量定义
tls_config = docker.tls.TLSConfig(client_cert=('D:\\onedrive\\docker-cm-tls\\cert.pem','D:\\onedrive\\docker-cm-tls\\key.pem'), verify=False)
base_url = "https://192.168.58.157:2375"
#主程序开始
app = flask.Flask(__name__, static_url_path='')
@app.route('/containers')
def containers():
    client = docker.DockerClient(base_url=base_url, tls=tls_config)
    node_list = client.nodes.list()
    return_list = []
    for node in node_list:
        node_name = node.attrs['Description']['Hostname']
        node_ip = node.attrs['Status']['Addr']
        client_tmp = docker.DockerClient(base_url='https://%s:2375' %node_ip, tls=tls_config)
        container_list = client_tmp.containers.list()
        for container in container_list:
            container_id = container.short_id
            container_name = container.name
            container_status = container.status
            container_createtime = container.attrs['Created'].split('.')[0]
            container_image = container.attrs['Config']['Image'].split('@')[0]
            data = {'node_name':node_name, 'node_ip':node_ip, 'container_id': container_id, 'container_name': container_name, 'container_status':container_status, 'container_createtime':container_createtime,'container_image':container_image}
            return_list.append(data)
    return str(return_list)
@app.route('/images')
def images():
    client = docker.DockerClient(base_url=base_url, tls=tls_config)
    node_list = client.nodes.list(filters={'role':'worker'})
    return_list = []
    for node in node_list:
        node_ip = node.attrs['Status']['Addr']
        client_image = docker.DockerClient(base_url='https://%s:2375' %node_ip, tls=tls_config)
        image_info = client_image.images.list()
        for image in image_info:
            image_id = image.short_id
            image_tag = image.tags
            image_name = image.attrs['RepoDigests'][0].split('@')[0]
            image_created = image.attrs['Created'].split('.')[0]
            image_size = str(int(image.attrs['Size'])//1000000) + "M"
            data = {'node_ip':node_ip, 'image_id':image_id, 'image_name':image_name, 'image_tag': image_tag,'image_created': image_created,'image_size':image_size}
            return_list.append(data)
    return str(return_list)
@app.route('/nodes')
def nodes():
    client = docker.DockerClient(base_url=base_url, tls=tls_config)
    node_list = client.nodes.list()
    return_list = []
    for node in node_list:
        node_ip = node.attrs['Status']['Addr']
        node_name = node.attrs['Description']['Hostname']
        node_mem = str(int(node.attrs['Description']['Resources']['MemoryBytes'])//1000000000) + "G"
        node_cpu = node.attrs['Description']['Resources']['NanoCPUs']
        node_role = node.attrs['Spec']['Role']
        node_stats = node.attrs['Spec']['Availability']
        node_created = node.attrs['CreatedAt'].split('.')[0]
        client_container = docker.DockerClient(base_url='https://%s:2375' %node_ip, tls=tls_config)
        container_running = len(client_container.containers.list(filters={'status':'running'}))
        container_stopped = len(client_container.containers.list(filters={'status':'exited'}))
        container_paused = len(client_container.containers.list(filters={'status':'paused'}))
        container_restart = len(client_container.containers.list(filters={'status':'restarting'}))
        data = {'node_ip':node_ip, 'node_name':node_name, 'node_mem':node_mem, 'node_cpu': node_cpu, 'node_role':node_role, 'node_stats': node_stats, 'node_created': node_created,'container_running': container_running, 'container_stopped': container_stopped, 'container_paused': container_paused, 'container_restart': container_restart}
        return_list.append(data)
    return str(return_list)
app.run(host='0.0.0.0', port=6011)