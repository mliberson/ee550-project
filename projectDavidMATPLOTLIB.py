import random
import numpy as np
import sys

import matplotlib.pyplot as plt

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
                packetID = self.Queue[0]
        return options, packetID
    def RemovePacket(self):
        self.QueueSize = self.QueueSize - 1
    def InsertPacket(self, packetID):
        if packetID:
            self.Queue.append(packetID)
            self.QueueSize = self.QueueSize + 1

class Graph:
    def __init__(self, edges, queueSelection: bool):
        self.Nodes = []
        self.Edges = edges

        self.Edges = [[1,0.4,0.4,0.4,0,0,0,0,0],
                      [0,1,0,0,0.4,0.4,0,0,0],
                      [0,0,1,0.4,0.4,0.4,0,0,0],
                      [0,0,0,1,0,0,0,0.4,0],
                      [0,0,0,0,1,0,0.4,0.4,0],
                      [0,0,0,0,0,1,0.4,0.4,0.4],
                      [0,0,0,0,0,0,1,0,0.4],
                      [0,0,0,0,0,0,0,1,0.4],
                      [0,0,0,0,0,0,0,0,1]]
        '''
        self.Edges = [[1, 0.4, 0, 0.4, 0, 0, 0],
                      [0, 1, 0.4, 0.4, 0.1, 0, 0],
                      [0, 0, 1, 0, 0.4, 0, 0],
                      [0, 0, 0, 1, 0.4, 0.1, 0],
                      [0, 0, 0, 0, 1, 0.4, 0.1],
                      [0, 0, 0, 0, 0, 1, 0.4],
                      [0, 0, 0, 0, 0, 0, 1]]
        
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
        '''
        
        self.QueueSizes = []
        self.sumQueueSizes = []
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
        queueSizesTemp.pop()
        self.sumQueueSizes.append(sum(queueSizesTemp))
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

lam = 0.7

x_values = []
y_values_1t = []
y_values_1f = []
y_values_2t = []
y_values_2f = []
y_values_3t = []
y_values_3f = []

edges1 = [[1,0.4,0.4,0.4,0,0,0,0,0],
          [0,1,0,0,0.4,0.4,0,0,0],
          [0,0,1,0.4,0.4,0.4,0,0,0],
          [0,0,0,1,0,0,0,0.4,0],
          [0,0,0,0,1,0,0.4,0.4,0],
          [0,0,0,0,0,1,0.4,0.4,0.4],
          [0,0,0,0,0,0,1,0,0.4],
          [0,0,0,0,0,0,0,1,0.4],
          [0,0,0,0,0,0,0,0,1]]

edges2 = [[1, 0.4, 0, 0.4, 0, 0, 0],
          [0, 1, 0.4, 0.4, 0.1, 0, 0],
          [0, 0, 1, 0, 0.4, 0, 0],
          [0, 0, 0, 1, 0.4, 0.1, 0],
          [0, 0, 0, 0, 1, 0.4, 0.1],
          [0, 0, 0, 0, 0, 1, 0.4],
          [0, 0, 0, 0, 0, 0, 1]]

edges3 = [[1,0.5,0.5,0.5,0,0,0,0,0,0,0],
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

j = 0.01
while j <= lam:
    time = 0
    n = 0
    arrivals = np.random.poisson(j,1000)

    graph1t = Graph(edges1,True)
    graph1f = Graph(edges1,False)

    graph2t = Graph(edges2,True)
    graph2f = Graph(edges2,False)

    graph3t = Graph(edges3,True)
    graph3f = Graph(edges3,False)

    for arrival in arrivals:
        graph1t.Run(arrival)
        graph1f.Run(arrival)
        graph2t.Run(arrival)
        graph2f.Run(arrival)
        graph3t.Run(arrival)
        graph3f.Run(arrival)

    y_values_temp_1t = 0
    y_values_temp_1f = 0
    y_values_temp_2t = 0
    y_values_temp_2f = 0
    y_values_temp_3t = 0
    y_values_temp_3f = 0
    for i in range(len(graph1t.sumQueueSizes)):
        y_values_temp_1t = y_values_temp_1t + graph1t.sumQueueSizes[i]
        y_values_temp_1f = y_values_temp_1f + graph1f.sumQueueSizes[i]

        y_values_temp_2t = y_values_temp_2t + graph2t.sumQueueSizes[i]
        y_values_temp_2f = y_values_temp_2f + graph2f.sumQueueSizes[i]

        y_values_temp_3t = y_values_temp_3t + graph3t.sumQueueSizes[i]
        y_values_temp_3f = y_values_temp_3f + graph3f.sumQueueSizes[i]

    x_values.append(j)
    y_values_1t.append(y_values_temp_1t/1000)
    y_values_1f.append(y_values_temp_1f/1000)
    y_values_2t.append(y_values_temp_2t/1000)
    y_values_2f.append(y_values_temp_2f/1000)
    y_values_3t.append(y_values_temp_3t/1000)
    y_values_3f.append(y_values_temp_3f/1000)
    j = j+0.01

# Create a scatter plot

plt.scatter(x_values,y_values_1t,color='red',label="Queue Selection")
plt.scatter(x_values,y_values_1f,color='blue',label="Index Selection")

plt.xlabel('Lambda')
plt.ylabel('N')
plt.title('N vs Lambda from 0.01 to 0.6 for Graph 1')

plt.legend()
plt.grid(True)
plt.show()

plt.scatter(x_values,y_values_2t,color='red',label="Queue Selection")
plt.scatter(x_values,y_values_2f,color='blue',label="Index Selection")

plt.xlabel('Lambda')
plt.ylabel('N')
plt.title('N vs Lambda from 0.01 to 0.6 for Graph 2')

plt.legend()
plt.grid(True)
plt.show()

plt.scatter(x_values,y_values_3t,color='red',label="Queue Selection")
plt.scatter(x_values,y_values_3f,color='blue',label="Index Selection")

plt.xlabel('Lambda')
plt.ylabel('N')
plt.title('N vs Lambda from 0.01 to 0.6 for Graph 3')

plt.legend()
plt.grid(True)
plt.show()


    