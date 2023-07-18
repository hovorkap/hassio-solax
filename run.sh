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
## Get the 'serial' key from the user config options.
solax_port=$(bashio::config 'serial')
server_port=$(bashio::config 'port')
device_link="/solax/ttySolaxX3"

## Print the message the user supplied, defaults to "Hello World..."

ln -s ${solax_port} $device_link
bashio::log.info "Link created: ${solax_port} -> ${device_link}"

python3 power_scraper.py

# python3 -m http.server ${server_port:="34800"}

