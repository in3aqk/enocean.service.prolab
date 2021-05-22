#!/usr/bin/python3
# -*- encoding: utf-8 -*-
import json
from enocean.consolelogger import init_logging
import enocean.utils
from enocean.communicators.serialcommunicator import SerialCommunicator
from enocean.protocol.packet import RadioPacket
from enocean.protocol.constants import PACKET, RORG
import sys
import traceback
import helpers

helpers = helpers.Helpers()


DEBUG = False


try:
    import queue
except ImportError:
    import Queue as queue


def print_debug(message):
    if DEBUG:
        print(message)


def assemble_radio_packet(transmitter_id):
    return RadioPacket.create(rorg=RORG.BS4, rorg_func=0x20, rorg_type=0x01,
                              sender=transmitter_id,
                              CV=50,
                              TMP=21.5,
                              ES='true')


init_logging()
communicator = SerialCommunicator()
communicator.start()
print_debug('The Base ID of your module is %s.' % enocean.utils.to_hex_string(communicator.base_id))

if communicator.base_id is not None:
    print_debug('Sending example package.')
    communicator.send(assemble_radio_packet(communicator.base_id))

# endless loop receiving radio packets
while communicator.is_alive():
    try:
        # Loop to empty the queue...
        packet = communicator.receive.get(block=True, timeout=1)
        if packet.packet_type == PACKET.RADIO_ERP1 and packet.rorg == RORG.VLD:
            
            packet.select_eep(0x05, 0x00)
            packet.parse_eep()
            for k in packet.parsed:                
                print_debug('%s: %s' % (k, packet.parsed[k]))
        if packet.packet_type == PACKET.RADIO_ERP1 and packet.rorg == RORG.BS4:
            
            # parse packet with given FUNC and TYPE
            for k in packet.parse_eep(0x02, 0x05):                
                print_debug('%s: %s' % (k, packet.parsed[k]))
        if packet.packet_type == PACKET.RADIO_ERP1 and packet.rorg == RORG.BS1:            
            # alternatively you can select FUNC and TYPE explicitely
            packet.select_eep(0x00, 0x01)
            # parse it
            packet.parse_eep()
            for k in packet.parsed:                
                print_debug('%s: %s' % (k, packet.parsed[k]))
        if packet.packet_type == PACKET.RADIO_ERP1 and packet.rorg == RORG.RPS:
           
            action = "Boo"         
            for k in packet.parse_eep(0x02, 0x02): 
                
                #print('%s: %s' % (k, packet.parsed[k]))
                #js_packet = json.loads(packet.parsed[k])
                parsed_packet = packet.parsed[k]
                print_debug(parsed_packet)                
                if k == 'R1' :
                    if parsed_packet['value'] == 'Button BO' and parsed_packet['raw_value'] == 3:
                        action = "PREV"
                    if parsed_packet['value'] == 'Button BI' and parsed_packet['raw_value'] == 2:
                        action = "NEXT"
                    if parsed_packet['value'] == 'Button AI' and parsed_packet['raw_value'] == 0:
                        action = "UP"
                    if parsed_packet['value'] == 'Button AO' and parsed_packet['raw_value'] == 1:
                        action = "DWN"
                    
                if k=='EB' and parsed_packet['value'] == 'pressed':
                    #print (action)
                    if action == "UP":
                        helpers.volume("UP")
                    if action == "DWN":
                        helpers.volume("DWN")
                    if action == "PREV":
                        helpers.next_previous("PREV")
                    if action == "NEXT":
                        helpers.next_previous("NEXT")    


                    #print(parsed_packet)
                    #print(parsed_packet['value'])
                    #print(parsed_packet['raw_value'])
                    
                


    except queue.Empty:
        continue
    except KeyboardInterrupt:
        break
    except Exception:
        traceback.print_exc(file=sys.stdout)
        break

if communicator.is_alive():
    communicator.stop()
