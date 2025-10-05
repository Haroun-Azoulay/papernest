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
elif [[ $1 == "all" ]]; then

    echo "[WAIT -------------------------- Launching your Docker compose...]"
    docker compose up --build
elif [[ $1 == "test" ]]; then

    echo "[WAIT -------------------------- Launching your Docker compose...]"
    docker compose up -d --build

    CONTAINER_ID=$(docker ps -q -f name=papernest-papernest-back_end)
    echo "$CONTAINER_ID"

    echo "[WAIT -------------------------- Launching Backend Test...]"
    docker exec -ti "$CONTAINER_ID" bash -c "cd /app && pytest -vv"

    echo "[WAIT -------------------------- Shut down Docker compose...]"
    docker compose down
    exit 1
elif [[ $1 == "coverage" ]]; then

    echo "[WAIT -------------------------- Launching your Docker compose...]"
    docker compose up -d --build

    CONTAINER_ID=$(docker ps -q -f name=papernest-papernest-back_end)
    echo "$CONTAINER_ID"

    echo "[WAIT -------------------------- Launching coverage Backend Test...]"
    docker exec -ti "$CONTAINER_ID" bash -c "cd /app && pytest --cov=app --cov-report=term-missing app/tests/"

    echo "[WAIT -------------------------- Shut down Docker compose...]"
    docker compose down
    exit 1
fi
launchApp() {
    echo -e "What do you want to do? Type 'run all' to launch all, 'run back' to launch the backend, 'run front' to launch the frontend, 'run test' to launch all tests, 'run coverage' to launch and display coverage raport, 'run delete' to shutdown docker compose and delete all volumes or 'help' to see instructions or 'exit' to leave the script: \n"

    read -r response
    response=$(echo "$response")

    if [[ "$response" == "run back" ]]; then
        echo "[WAIT -------------------------- Building your Docker backend image from Dockerfile...]"

        docker build -t paper-back .

        echo "[INFO -------------------------- Launching your container on port 8000]"
        cd ./front
        docker run -p 8000:8000 -it paper-back

    elif [[ "$response" == "run front" ]]; then
        echo "[WAIT -------------------------- Building your Docker frontend image from Dockerfile...]"
        cd ./front
        docker build -t build paper-front .

        echo "[INFO -------------------------- Launching your container on port 80]"
        docker run -ti -p 8080:80 paper-front
    elif [[ "$response" == "run all" ]]; then
        echo "[WAIT -------------------------- Launching your Docker compose...]"
        docker compose up --build

    elif [[ "$response" == "run test" ]]; then
        echo "[WAIT -------------------------- Launching your Docker compose...]"
        docker compose up -d --build

        CONTAINER_ID=$(docker ps -q -f name=papernest-papernest-back_end)
        echo "$CONTAINER_ID"

        echo "[WAIT -------------------------- Launching Backend Test...]"
        docker exec -ti "$CONTAINER_ID" bash -c "cd /app && pytest"

        echo "[WAIT -------------------------- Shut down Docker compose...]"
        docker compose down

    elif [[ $response == "run coverage" ]]; then

        echo "[WAIT -------------------------- Launching your Docker compose...]"
        docker compose up -d --build

        CONTAINER_ID=$(docker ps -q -f name=papernest-papernest-back_end)
        echo "$CONTAINER_ID"

        echo "[WAIT -------------------------- Launching coverage Backend Test...]"
        docker exec -ti "$CONTAINER_ID" bash -c "cd /app && pytest --cov=app --cov-report=term-missing app/tests/"

        echo "[WAIT -------------------------- Shut down Docker compose...]"
        docker compose down
        exit 1
    elif [[ $response == "run delete" ]]; then

        echo "[WAIT -------------------------- Shut down Docker compose and delete all volumes...]"
        docker compose down -v
        exit 1

    elif [[ "$response" == "help" ]]; then
        echo
        echo "=================== HELP ==================="
        echo "Available commands:"
        echo "  run all   -> Build the Docker compose, run the backend container on port 8080 and run the frontend container on port 8080"
        echo "  run back   -> Build the Docker backend image and run the backend container on port 8000"
        echo "  run frontend   -> Build the Docker frontend image and run the frontend container on port 8080"
        echo "  run test   -> Build the Docker compose, run the backend container on port 8080, run the frontend container on port 8080, test backend and shutdown the Docker compose"
        echo "  run coverage -> Build the Docker compose, run the backend container on port 8080, run the frontend container on port 8080, display coverage backend and shutdown the Docker compose"
        echo "  run delete -> Delete all volumes on Docker compose"
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
