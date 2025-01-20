#!/bin/bash
yum update -y
yum install -y docker git
systemctl start docker
sudo usermod -aG docker ec2-user
systemctl enable docker
ls -l /var/run/docker.sock
sudo chmod 666 /var/run/docker.sock

cd /tmp
git clone https://github.com/JonaNeyra/weather-data-project.git
sudo mkdir /var/opt weather_api
sudo cp -R /tmp/weather-data-project/weather_api /var/opt/weather_api
sudo chown -R www-data:www-data /var/opt/weather_api

docker build -t weather-api-image /var/opt/weather_api
docker run -it --name weather-container weather-api-image