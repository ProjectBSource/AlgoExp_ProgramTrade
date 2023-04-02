"""
Copyright (C) 2019 Interactive Brokers LLC. All rights reserved. This code is subject to the terms
 and conditions of the IB API Non-Commercial License or the IB API Commercial License, as applicable.
"""

import collections
import inspect
import time

from ibapi import wrapper
from ibapi.client import EClient
from ibapi.utils import longMaxString
from ibapi.utils import iswrapper

# types
from ibapi.common import * # @UnusedWildImport
from ibapi.order_condition import * # @UnusedWildImport
from ibapi.contract import * # @UnusedWildImport
from ibapi.order import * # @UnusedWildImport
from ibapi.order_state import * # @UnusedWildImport
from ibapi.execution import Execution
from ibapi.execution import ExecutionFilter
from ibapi.commission_report import CommissionReport
from ibapi.ticktype import * # @UnusedWildImport
from ibapi.tag_value import TagValue

from ibapi.account_summary_tags import *

from ContractSamples import ContractSamples
from OrderSamples import OrderSamples
from AvailableAlgoParams import AvailableAlgoParams
from ScannerSubscriptionSamples import ScannerSubscriptionSamples
from FaAllocationSamples import FaAllocationSamples
from ibapi.scanner import ScanData

import threading

class Mytest(EClient, wrapper.EWrapper):
    
    def __init__(self):
        #init the Wrapper and EClient
        wrapper.EWrapper.__init__(self)
        self.wrapMeth2callCount = collections.defaultdict(int)
        self.wrapMeth2reqIdIdx = collections.defaultdict(lambda: -1)
        self.reqId2nAns = collections.defaultdict(int)
        self.setupDetectWrapperReqId()
        
        EClient.__init__(self, self)
        self.clntMeth2callCount = collections.defaultdict(int)
        self.clntMeth2reqIdIdx = collections.defaultdict(lambda: -1)
        self.reqId2nReq = collections.defaultdict(int)
        self.setupDetectReqId()
        
        self.nKeybInt = 0
        self.started = False
        self.nextValidOrderId = 1000
        self.permId2ord = {}
        self.reqId2nErr = collections.defaultdict(int)
        self.globalCancelOnly = False
        self.simplePlaceOid = None
        self.test_order_once = False
        
        # ! [connect]
        self.connect("127.0.0.1", 7496, clientId=0)
        # ! [connect]
        print("serverVersion:%s connectionTime:%s" % (self.serverVersion(), self.twsConnectionTime()))
        # run the thread
        thread = threading.Thread(target=self.run)
        thread.start()
        
    def setupDetectWrapperReqId(self):
        methods = inspect.getmembers(wrapper.EWrapper, inspect.isfunction)
        for (methName, meth) in methods:
            self.wrapMeth2callCount[methName] = 0
            # logging.debug("meth %s", name)
            sig = inspect.signature(meth)
            for (idx, pnameNparam) in enumerate(sig.parameters.items()):
                (paramName, param) = pnameNparam # @UnusedVariable
                # we want to count the errors as 'error' not 'answer'
                if 'error' not in methName and paramName == "reqId":
                    self.wrapMeth2reqIdIdx[methName] = idx
            setattr(wrapper.EWrapper, methName, self.countWrapReqId(methName, meth))
            
    def countWrapReqId(self, methName, fn):
        def countWrapReqId_(*args, **kwargs):
            self.wrapMeth2callCount[methName] += 1
            idx = self.wrapMeth2reqIdIdx[methName]
            if idx >= 0:
                self.reqId2nAns[args[idx]] += 1
            return fn(*args, **kwargs)
        return countWrapReqId_
    
    def setupDetectReqId(self):
        methods = inspect.getmembers(EClient, inspect.isfunction)
        for (methName, meth) in methods:
            if methName != "send_msg":
                # don't screw up the nice automated logging in the send_msg()
                self.clntMeth2callCount[methName] = 0
                # logging.debug("meth %s", name)
                sig = inspect.signature(meth)
                for (idx, pnameNparam) in enumerate(sig.parameters.items()):
                    (paramName, param) = pnameNparam # @UnusedVariable
                    if paramName == "reqId":
                        self.clntMeth2reqIdIdx[methName] = idx
                setattr(EClient, methName, self.countReqId(methName, meth))

    def countReqId(self, methName, fn):
        def countReqId_(*args, **kwargs):
            self.clntMeth2callCount[methName] += 1
            idx = self.clntMeth2reqIdIdx[methName]
            if idx >= 0:
                sign = -1 if 'cancel' in methName else 1
                self.reqId2nReq[sign * args[idx]] += 1
            return fn(*args, **kwargs)
        return countReqId_
            
    def nextOrderId(self):
        oid = self.nextValidOrderId
        self.nextValidOrderId += 1
        return oid
        
    _placeOrder = False    
    
    def run(self):
        while(self.isConnected() or not self.msg_queue.empty()):
            if(self._placeOrder==True):
                self.placeOrder("LMT", 1, 20358)
                self._placeOrder = False
            time.sleep(1)
            print("Thread running...")
                
    def placeLimitOrder(self, orderType, qty, price):
        self.reqIds(-1)
        self.reqAllOpenOrders()
        self.reqAutoOpenOrders(True)
        self.reqOpenOrders()
        
        contract = Contract()
        contract.symbol = "MHI"
        contract.secType = "FUT"
        contract.exchange = "HKFE"
        contract.currency = "HKD"
        contract.lastTradeDateOrContractMonth = "202304"
        
        order = Order()
        order.action = "BUY"
        order.orderType = orderType
        order.totalQuantity = qty
        order.lmtPrice = price
        
        self.placeOrder(self.nextOrderId(), contract, order)
    


dataStreaming = Mytest()