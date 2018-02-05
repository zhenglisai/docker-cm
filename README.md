# docker-cm使用说明
功能说明：  
1，swarm集群管理  
使用说明  

docker准备  
1，使用make_tls_key.sh生成tls所需key  
2，将server文件夹下的文件复制到需要远程的docker服务器/root/.docker文件夹下。  
3，修改需要远程的docker服务器启动文件，以centos7为例：  
vim  /lib/systemd/system/docker.service

　　修改execstart配置

　　ExecStart=/usr/bin/dockerd -H unix:///var/run/docker.sock -D -H tcp://0.0.0.0:2375 --tlsverify --tlscacert=/root/.docker/ca.pem -- tlscert=/root/.docker/server-cert.pem --tlskey=/root/.docker/server-key.pem  
4，重新加载配置文件，重启docker进程  
　　systemctl daemon-reload  
　　service docker restart  
5，在本地服务器上执行以下命令，若范围docker信息，即为docker服务器设置成功  
将cert.pem,key.pem这两个文件复制到测试机上, curl中-k的意思是Allow connections to SSL sites without certs，不验证证书  
　　curl -k https://docker服务器IP:2375/info --cert ./cert.pem --key ./key.pem
