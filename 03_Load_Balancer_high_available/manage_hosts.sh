#!/bin/bash

# List of hostnames to manage
HOSTS=("loadbalancer.tevs")
IP="127.0.0.1"

add_hosts() {
    for host in "${HOSTS[@]}"; do
        if grep -q "$host" /etc/hosts; then
            echo "$host already exists in /etc/hosts"
        else
            echo "Adding $host to /etc/hosts..."
            echo "$IP $host" | sudo tee -a /etc/hosts > /dev/null
        fi
    done
}

remove_hosts() {
    for host in "${HOSTS[@]}"; do
        if grep -q "$host" /etc/hosts; then
            echo "Removing $host from /etc/hosts..."
            sudo sed -i "/$host/d" /etc/hosts
        else
            echo "$host not found in /etc/hosts"
        fi
    done
}

case "$1" in
    add)
        add_hosts
        ;;
    remove)
        remove_hosts
        ;;
    *)
        echo "Usage: $0 {add|remove}"
        exit 1
        ;;
esac
