# -*- coding: utf-8 -*-
"""
Created on Mon Jun 19 19:34:43 2020

"""
import numpy as np
import math

class WSN:
    __instance = None
    B = 2.4 * 10**9 #0000000 #MHz
    SIGMA = 3.92 #Sigma
    @staticmethod 
    def getInstance():
        """ Static access method. """
        if WSN.__instance == None:
            WSN()
        return WSN.__instance
    def __init__(self, **kwargs):
        """ Virtually private constructor. """
        if WSN.__instance != None:
            raise Exception("Error: this class is not instance")
        else:
            WSN.__instance = self
        self.Dist = None 
        self.PR  = None #Matrix 
        self.SNR = None 
        self.RT = None 
        self.Demands = None #the demands from all devices to one access point 
   
    def calc_Dist(self, aps, devices):
        """calculate the DIST matrix"""
        
        self.Dist = np.zeros(shape=(len(aps), len(devices)))
        for d in devices:
            for ap in aps: 
                self.Dist[ap.ssid][d.ssid] = d.get_dist(ap)
    def calc_RSSI(self):
        """calculate the RSSI matrix"""
        self.RSSI = 1/self.Dist 
        
    def calc_PR(self, aps, devices):
        """calculate the PL matrix"""
        
        self.PR = np.zeros(shape=(len(aps), len(devices)))
        self.Demands = np.zeros(len(devices)) #this is a vector 
        for d in devices:
            for ap in aps: 
                self.PR[ap.ssid][d.ssid] = d.calc_power_received(ap)
            self.Demands[d.ssid] = d.demand 
                
    def calc_SNR(self):
        self.SNR= np.zeros(shape = self.PR.shape)
        row_sum = np.sum(self.PR,axis=1)
        
        
        sigma_sqr = WSN.SIGMA**2 
        for j in range(self.SNR.shape[0]):
            for i in range(self.SNR.shape[1]):
                self.SNR[j][i] = self.PR[j][i]/(row_sum[j] - self.PR[j][i] + sigma_sqr)
            
    def calc_rate(self, aps, devices):
        self.calc_Dist(aps, devices)
        self.calc_RSSI()
        self.calc_PR(aps, devices)
        self.calc_SNR()
        self.RT= np.zeros(shape = self.PR.shape)
        for j in range(self.SNR.shape[0]):
            for i in range(self.SNR.shape[1]):
                self.RT[j][i] = WSN.B*math.log2(1 + self.SNR[j][i])    
        
    def get_rates(self):
        return self.RT
 
        
     
            
            
        