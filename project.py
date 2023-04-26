import random
import numpy as np
import sys

class Packet:
    def __init__(self, id, arrival_time):
        self.ID = id
        self.ArrivalTime = arrival_time
        self.DepartureTime = None
        self.TravelTime = None
        self.IsActive = True
    def Depart(self, departure_time):
        self.DepartureTime = departure_time
        self.TravelTime = departure_time - self.ArrivalTime
        self.IsActive = False

class Node:
    def __init__(self, id, edgeWeights):
        self.ID = id
        self.Queue = []
        self.QueueSize = 0
        self.Edges = edgeWeights
    def GetReceiverOptions(self):
        options = []
        packetID = None
        if self.QueueSize == 0:
            return options, packetID
        for i in range(len(self.Edges)):
            if random.random() < self.Edges[i] and not i == self.ID:
                options.append(i)
                packetID = self.Queue[-1]
        return options, packetID
    def RemovePacket(self):
        self.Queue.pop()
        self.QueueSize = self.QueueSize - 1
    def InsertPacket(self, packetID):
        if packetID:
            self.Queue.append(packetID)
            self.QueueSize = self.QueueSize + 1

class Graph:
    def __init__(self, queueSelection: bool):
        self.Nodes = []
        '''
        self.Edges = [[1, 0.4, 0, 0.4, 0, 0, 0],
                      [0, 1, 0.4, 0.4, 0.1, 0, 0],
                      [0, 0, 1, 0, 0.4, 0, 0],
                      [0, 0, 0, 1, 0.4, 0.1, 0],
                      [0, 0, 0, 0, 1, 0.4, 0.1],
                      [0, 0, 0, 0, 0, 1, 0.4],
                      [0, 0, 0, 0, 0, 0, 1]]
        '''
        self.Edges = [[1,0.5,0.5,0.5,0,0,0,0,0,0,0],
                      [0,1,0,0,0.5,0.5,0.5,0,0,0,0],
                      [0,0,1,0,0.5,0.5,0.5,0,0,0,0],
                      [0,0,0,1,0.5,0.5,0.5,0,0,0,0],
                      [0,0,0,0,1,0,0,0.5,0.5,0.5,0],
                      [0,0,0,0,0,1,0,0.5,0.5,0.5,0],
                      [0,0,0,0,0,0,1,0.5,0.5,0.5,0],
                      [0,0,0,0,0,0,0,1,0,0,0.5],
                      [0,0,0,0,0,0,0,0,1,0,0.5],
                      [0,0,0,0,0,0,0,0,0,1,0.5],
                      [0,0,0,0,0,0,0,0,0,0,1]]
        self.QueueSizes = []
        self.NetworkOccupancy = 0
        self.Packets = []
        self.Time = 1
        self.QueueSelection = queueSelection
        for i in range(len(self.Edges)):
            self.Nodes.append(Node(i, self.Edges[i]))
    def Run(self, arrivalCount):
        if arrivalCount:
            for i in range(arrivalCount):
                newPacket = Packet(len(self.Packets)+1, self.Time)
                self.Packets.append(newPacket)
                self.Nodes[0].InsertPacket(newPacket.ID)
                self.NetworkOccupancy += 1
        transfers = []
        for i in range(len(self.Nodes)-1):
            recv = {}
            tmp,id = self.Nodes[i].GetReceiverOptions()
            if tmp:
                recv["src"] = i
                if self.QueueSelection:
                    recv["dst"] = self.GetMinQueueNode(tmp)
                else:
                    recv["dst"] = max(tmp)
                recv["id"] = id
                transfers.append(recv)
        for transfer in transfers:
            src = transfer["src"]
            dst = transfer["dst"]
            id = transfer["id"]
            self.Nodes[src].RemovePacket()
            self.Nodes[dst].InsertPacket(id)
            if dst == len(self.Nodes)-1:
                self.Packets[id-1].Depart(self.Time)
                self.NetworkOccupancy -= 1
        queueSizesTemp = []
        for node in self.Nodes:
            queueSizesTemp.append(node.QueueSize)
        self.QueueSizes.append(queueSizesTemp)
        self.Time += 1 
    def GetMinQueueNode(self, nodeIds):
        minQueueNode = nodeIds[0]
        minQueueSize = 100*100*100*100
        for nodeId in nodeIds:
            if self.Nodes[nodeId].QueueSize < minQueueSize:
                minQueueNode = nodeId
                minQueueSize = self.Nodes[nodeId].QueueSize
        return minQueueNode

lam = 0.9

time = 0
n = 0

for i in range(10):
    arrivals = np.random.poisson(lam,1000)

    graph = Graph(False)
    for arrival in arrivals:
        graph.Run(arrival)
    for packet in graph.Packets:
        if packet.IsActive:
            n = n+1

n = n/10

print(n)
    