#!/usr/bin/with-contenv bashio
# ==============================================================================
# Start the example service
# s6-overlay docs: https://github.com/just-containers/s6-overlay
# ==============================================================================

bashio::log.info "Starting solax service..."

# Declare variables
declare solax_port
declare server_port
declare device_link
declare DEBUG
declare MQTT_HOST
declare MQTT_USER
declare MQTT_PASSWORD

## Get the 'serial' key from the user config options.
solax_port=$(bashio::config 'serial')
server_port=$(bashio::config 'port')
device_link="/solax/ttySolaxX3"
DEBUG=$(bashio::config 'debug')

MQTT_HOST=$(bashio::services mqtt "host")
MQTT_USER=$(bashio::services mqtt "username")
MQTT_PASSWORD=$(bashio::services mqtt "password")

## Print the message the user supplied, defaults to "Hello World..."

# bashio::log.info "Parameters set: MQTT_HOST=${MQTT_HOST} MQTT_USER=${MQTT_USER} MQTT_PASSWORD=${MQTT_PASSWORD}"

ln -sf ${solax_port} $device_link
bashio::log.info "Link created: ${solax_port} -> ${device_link}"

# ls /solax

python3 power_scraper.py ${MQTT_HOST} ${MQTT_USER} ${MQTT_PASSWORD}