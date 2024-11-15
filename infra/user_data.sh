#!/bin/bash
chmod +x /path/to/your/script.sh
sudo su
yum update -y
yum install -y docker
service docker start
usermod -a -G docker ec2-user
docker run -p 80:5000 ninjadexter/triagem_facil_web:latest