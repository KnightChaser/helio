docker build -t fastapi .
docker-compose up -d

$exitCommand = Read-Host "Enter 'exit' to stop the containers and exit "
while ($exitCommand -ne "exit") {
    $exitCommand = Read-Host "Enter 'exit' to stop the containers and exit "
}

docker-compose down
