
import subprocess
import time
import sys
import os
import json
from utils import isUp




class Helpers:

    file = "log"
    corruptedLog = "corrupted"
    ipflag = False
    ip = None
    screeshotpath = None
    dbhost = 'localhost'
    dbusername = 'root'
    dbpassword = ''
    dbdatabase = 'magellano'
    serverip = None
    _debug = False
    _identityFile = "/root/.ssh/id_rsa_server_quasar"
    cursor = None


    def __init__(self):
        None


        

    def sendJsonRPCommand(self,action):
        line  = None
        command = ["curl",
            '--header', 'Content-Type: application/json',
            '--data-binary',
            '%s' % action,
            'http://localhost:8080/jsonrpc']


        proc = subprocess.Popen(command, stdout=subprocess.PIPE)


        while True:
            line = proc.stdout.readline()
            
            if line != '':
                print("%s %s" % (command, line.rstrip()))
                return line
        

    def volume(self,up_down):
        #get current volume and status
        result = self.sendJsonRPCommand("{\"jsonrpc\": \"2.0\",\"method\": \"Application.GetProperties\",\"params\": [[\"volume\",\"muted\",\"version\"]],\"id\": 1}")
        json_res = json.loads(result)
        muted = json_res['result']['muted']
        current_volume = json_res['result']['volume']
        if muted:
            result = self.sendJsonRPCommand("{\"jsonrpc\": \"2.0\",\"method\": \"Application.SetMute\",\"params\": [false],\"id\": 1}")

        if up_down == 'UP':
            new_volume = (int) (current_volume + current_volume*0.1)            
        elif up_down == 'DWN' :
            new_volume = (int) (current_volume - current_volume*0.1)
        if new_volume <=100 and new_volume > 0:
            result = self.sendJsonRPCommand("{\"jsonrpc\": \"2.0\",\"method\": \"Application.SetVolume\",\"params\": ["+ "{}".format(new_volume)  +"],\"id\": 1}")


    def next_previous(self,direction):
        """ Set skin with json rpc command
        """
        print(direction)
        if direction == 'NEXT':
            self.sendJsonRPCommand("{\"jsonrpc\":\"2.0\",\"method\":\"Player.GoTo\",\"params\":[0,\"next\"],\"id\":1}")
        else:
            self.sendJsonRPCommand("{\"jsonrpc\":\"2.0\",\"method\":\"Player.GoTo\",\"params\":[0,\"previous\"],\"id\":1}")
        
