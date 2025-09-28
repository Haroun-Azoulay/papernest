#!/bin/bash

echo -e "Welcome to the Papernest test! \n"
if [[ $1 == "run" ]]; then

    echo "[WAIT -------------------------- Building your Docker image from Dockerfile...]"
    docker build -t paper .

    echo "[INFO -------------------------- Launching your container on port 8000]"
    docker run -p 8000:8000 -it paper
fi
launchApp() {
    echo -e "What do you want to do? Type 'run' to launch the backend or 'help' to see instructions or 'exit' to leave the script: \n"

    read -r response
    response=$(echo "$response")

    if [[ "$response" == "run" ]]; then
        echo "[WAIT -------------------------- Building your Docker image from Dockerfile...]"

        docker build -t paper .

        echo "[INFO -------------------------- Launching your container on port 8000]"

        docker run -p 8000:8000 -it paper

    elif [[ "$response" == "help" ]]; then
        echo
        echo "=================== HELP ==================="
        echo "Available commands:"
        echo "  run   -> Build the Docker image and run the backend container on port 8000"
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
