#!/bin/bash

echo -e "Welcome to the Papernest test! \n"
if [[ $1 == "back" ]]; then

    echo "[WAIT -------------------------- Building your Docker backend image from Dockerfile...]"
    docker build -t paper .

    echo "[INFO -------------------------- Launching your container on port 8000]"
    docker run -p 8000:8000 -it paper
elif [[ $1 == "front" ]]; then

    echo "[WAIT -------------------------- Building your Docker frontend image from Dockerfile...]"
    cd ./front
    docker build -t paper-front .

    echo "[INFO -------------------------- Launching your container on port 80]"
    docker run -p 8080:80 -it paper-front
fi
launchApp() {
    echo -e "What do you want to do? Type 'run back' to launch the backend, 'run front' to launch the frontend or 'help' to see instructions or 'exit' to leave the script: \n"

    read -r response
    response=$(echo "$response")

    if [[ "$response" == "run back" ]]; then
        echo "[WAIT -------------------------- Building your Docker backend image from Dockerfile...]"
        cd ./front
        docker build -t paper-back .

        echo "[INFO -------------------------- Launching your container on port 8000]"
        cd ./front
        docker run -p 8000:8000 -it paper-back

    elif [[ "$response" == "run front" ]]; then
        echo "[WAIT -------------------------- Building your Docker frontend image from Dockerfile...]"

        docker build -t build paper-front .

        echo "[INFO -------------------------- Launching your container on port 80]"

        docker run -ti -p 8080:80 paper-front

    elif [[ "$response" == "help" ]]; then
        echo
        echo "=================== HELP ==================="
        echo "Available commands:"
        echo "  run back   -> Build the Docker backend image and run the backend container on port 8000"
        echo "  run frontend   -> Build the Docker frontend image and run the backend container on port 8080"
        echo "  help  -> Display this help message"
        echo "  exit  -> Quit the script"
        echo
        launchApp
    elif [[ "$response" == "exit" || "$response" == "q" ]]; then
        echo "[INFO -------------------------- Your leave the script. Bye see you soon.]"
        exit 0
    else
        echo "[ERROR -------------------------- Unknown command. Please try again.]"
        launchApp
    fi
}
launchApp
