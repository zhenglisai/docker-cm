#!/usr/bin/env python
# -*- coding:utf-8 -*-
import docker
client = docker.DockerClient(base_url='http://192.168.58.157:6011')
a = client.containers.get('341a9c44fb06fb65f8c47ccbb8d9084ee4fa4c2e67334f04fa143790c8b6d6c2')
print a.logs()