#!/usr/bin/python3

# Scrapes Inverter information from solax inverters and presents it to OpenEnergyMonitor
#
# Setup:
#   pip3 install toml twisted pymodbus influxdb_client
#   cp config-example.toml config.toml
#   vi config.toml
#
# Copyright (c)2018 Inferno Embedded   http://infernoembedded.com
#
# This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>.

import toml
from twisted.internet import task, reactor
#from twisted.internet.protocol import Protocol
from twisted.logger import globalLogPublisher

import logging
logging.basicConfig()
log = logging.getLogger()
log.setLevel(logging.INFO)

import traceback

from Inputs.SolaxX3RS485 import SolaxX3RS485
from Outputs.Mqtt import Mqtt

from twisted.internet.defer import setDebugging
setDebugging(True)

from twisted.logger._levels import LogLevel

import sys

def analyze(event):
    if event.get("log_level") == LogLevel.critical:
        log.error("Critical: ", event)

def outputActions(vals):
    global outputs
    if outputs is None:
        return

    for output in outputs:
        try:
            output.send(vals)
        except:
            log.error("Output call failed")

def inputActions(inputs):
    for input in inputs:
        try:
            input.fetch(outputActions)
        except:
            log.error("input call failed")

def shutdown():
    log.info("Shutdown")
    global SolaxModbusInverters
    for inverter in SolaxModbusInverters:
        inverter.shutdown()


globalLogPublisher.addObserver(analyze)

with open("config.toml") as conffile:
    global config
    config = toml.loads(conffile.read())


global outputs
outputs = []

global SolaxModbusInverters
SolaxModbusInverters = []

mqtt_config = {}
mqtt_config['mqtt_host'] = sys.argv[1]
mqtt_config['mqtt_port'] = 1883
mqtt_config['mqtt_keepalive'] = 60
mqtt_config['mqtt_user'] = sys.argv[2]
mqtt_config['mqtt_pass'] = sys.argv[3]
mqtt_config['mqtt_topic'] = "solax"

log.debug(f"{mqtt_config}")

log.info("Setting up Mqtt")
outputs.append(Mqtt(mqtt_config))

if 'SolaxX3RS485' in config:
    log.info("Setting up SolaxX3RS485")
    SolaxRS485Meters = []
    for meter in config['SolaxX3RS485']['ports']:
        modbusMeter = SolaxX3RS485(meter, config['SolaxX3RS485']['baud'], config['SolaxX3RS485']['parity'],
                                 config['SolaxX3RS485']['stopbits'], config['SolaxX3RS485']['timeout'])
        SolaxRS485Meters.append(modbusMeter)

    looperSolaxRS485 = task.LoopingCall(inputActions, SolaxRS485Meters)
    looperSolaxRS485.start(config['SolaxX3RS485']['poll_period'])

reactor.addSystemEventTrigger('before', 'shutdown', shutdown)

reactor.run()
