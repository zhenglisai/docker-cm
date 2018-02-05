#!/bin/bash
echo "根据提示输入相应信息："
openssl genrsa -aes256 -out ca-key.pem 4096
openssl req -new -x509 -days 3650 -key ca-key.pem -sha256 -out ca.pem
openssl genrsa -out server-key.pem 4096
openssl req -sha256 -new -key server-key.pem -out server.csr
openssl x509 -req -days 3650 -sha256 -in server.csr -CA ca.pem -CAkey ca-key.pem -CAcreateserial -out server-cert.pem
openssl genrsa -out key.pem 4096
openssl req -new -key key.pem -out client.csr
openssl x509 -req -days 3650 -sha256 -in client.csr -CA ca.pem -CAkey ca-key.pem -CAcreateserial -out cert.pem
rm -v client.csr server.csr ca-key.pem ca.srl
chmod -v 0400 key.pem server-key.pem
chmod -v 0444 ca.pem server-cert.pem cert.pem
mkdir server
mkdir client
mv ca.pem server-cert.pem server-key.pem server/
mv ca.pem cert.pem key.pem client/
