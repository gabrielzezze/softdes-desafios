docker build -t softdes-dev-aberto ./
sudo docker run -d -p8080:8080 --name softdes softdes-dev-aberto   