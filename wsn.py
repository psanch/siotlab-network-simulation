# -*- coding: utf-8 -*-
"""
Created on Mon Jun 19 19:34:43 2020

"""
import numpy as np
import math

class WSN:
    __instance = None
    B = 20000000 #MHz
    SIGMA = 3.92
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
        self.PR  = None #Matrix 
        self.SNR = None 
        self.RT = None 
    def calc_PL(self, aps, devices):
        """calculate the PL matrix"""
        
        self.PL = np.zeros(shape=(len(aps), len(devices)))
        for d in devices:
            for ap in aps: 
                self.PL[ap.ssid][d.ssid] = d.calc_power_loss(ap)
            
    def calc_SNR(self):
        self.SNR= np.zeros(shape = self.PL.shape)
        row_sum = np.sum(self.PL,axis=1)
        sigma_sqr = WSN.SIGMA**2 
        for j in range(self.SNR.shape[0]):
            for i in range(self.SNR.shape[1]):
                self.SNR[j][i] = self.PL[j][i]/(row_sum[j] - self.PL[j][i] + sigma_sqr)
            
    def calc_rate(self):
       self.RT= np.zeros(shape = self.PL.shape)
       for j in range(self.SNR.shape[0]):
            for i in range(self.SNR.shape[1]):
                self.RT[j][i] = WSN.B*math.log2(1 + self.SNR[j][i])    
        
    def get_rates(self):
        return self.RT

        
      
            
            
        