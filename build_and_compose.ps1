# @file build_and_compose.ps1
# @brief Script to build a Docker image and start Docker containers using docker-compose.

# Check if running as administrator, if not, relaunch as administrator
if (-not ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole] "Administrator")) {
    Write-Warning "Please run this script as an administrator."
    Start-Sleep -Seconds 3
    Start-Process powershell.exe "-NoProfile -ExecutionPolicy Bypass -File `"$PSCommandPath`"" -Verb RunAs
    Exit
}

# Function to stop and start the winnat service
function Restart-WinNAT {
    Write-Output "Restarting WinNAT service..."
    net stop winnat
    net start winnat
}

# Build Docker image
docker build -t fastapi .

# Start Docker containers
docker-compose up -d

# Check for Docker port issue and restart winnat if necessary
if (-not (docker ps)) {
    Write-Warning "Docker failed to start. Checking for port issues..."
    $DockerPort = 8080
    if (Test-NetConnection -ComputerName localhost -Port $DockerPort -InformationLevel Quiet) {
        Write-Warning "Target port $DockerPort is in use. Restarting WinNAT service..."
        Restart-WinNAT
        Write-Warning "Trying to start Docker containers again..."
        docker-compose up -d
    }
}

# Loop until user enters 'exit'
$exitCommand = Read-Host "Enter 'exit' to stop the containers and exit "
while ($exitCommand -ne "exit") {
    $exitCommand = Read-Host "Enter 'exit' to stop the containers and exit "
}

# Stop Docker containers
docker-compose down
