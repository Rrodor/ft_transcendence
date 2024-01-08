#!/bin/bash

show_help() {
    echo "Usage: ./script.sh [dev|prod] [start|stop|status|log|clean] [bg]"
    echo "Commands:"
    echo "  start: Start the application."
    echo "  stop: Stop the application."
    echo "  status: Show the status of the application."
    echo "  log: Display log files."
    echo "  clean: Clean all Docker images and containers."
    echo "  bg: Run the application in the background (use with 'start')."
}

if [[ $1 == "dev" ]]; then
    COMPOSE_FILE="./transcendence/docker-compose.yml"
elif [[ $1 == "prod" ]]; then
    COMPOSE_FILE="./transcendence/docker-compose.prod.yml"
else
    show_help
    exit 1
fi

case $2 in
    start)
        if [[ $3 == "bg" ]]; then
            sudo docker-compose -f $COMPOSE_FILE up -d --build
        else
            sudo docker-compose -f $COMPOSE_FILE up --build
        fi
        ;;
    stop)
        sudo docker-compose -f $COMPOSE_FILE down
        ;;
    status)
        sudo docker-compose -f $COMPOSE_FILE ps
        ;;
    log)
        if [[ $3 == "bg" ]]; then
            sudo docker-compose -f $COMPOSE_FILE logs -f
        else
            echo "Log command is only available in bg mode."
        fi
        ;;
    clean)
        sudo docker system prune -a
        ;;
    help)
        show_help
        ;;
    *)
        show_help
        ;;
esac
