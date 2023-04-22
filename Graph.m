classdef Graph
    properties
        %array of nodes in the network (type Node)
        Nodes (1,:)
        %edge weights in the network
        Edges (:,:) {mustBePositive}
        %size of each queue at times t
        QueueSizes (:,:) {mustBeInteger}
        %size of all queues at times t
        NetworkOccupancy (1,:) {mustBeInteger}
    end
    methods
        function graph = Graph(edgeWeights)
            graph.Edges = edgeWeights;
            graph.QueueSizes = zeros(1,length(edgeWeights(1,:)));
            graph.QueueSizes = 0;
            for i = 1:length(edgeWeights(:,1))
                graph.Nodes{end+1} = Node(i,edgeWeights(i,:));
            end
        end
        function graph = Run(graph,packetID,queueSelection)
            if packetID
                graph.Nodes(1).UpdateQueue(packetID);
                graph.NetworkOccupancy = graph.NetworkOccupancy + 1;
            end
            receivers = graph.GetReceivers(queueSelection);
            packetsToRoute = graph.GetPacketsToRoute();
            for i = 1:length(receivers)
                graph.Nodes(receiver(i)) = graph.Nodes(receiver(i)).InsertPacket(packetsToRoute(i));
            end
            networkOccupancyTemp = 0;
            for node = graph.Nodes
                queueSizesTemp = node.QueueSize;
                networkOccupancyTemp = networkOccupancyTemp + queueSizesTemp;
            end
            graph.QueueSizes = [graph.QueueSizes; queueSizesTemp];
            graph.networkOccupancy{end+1} = networkOccupancyTemp;
        end
        function packetsToRoute = GetPacketsToRoute(graph)
            packetsToRoute = [];
            for i = 1:length(graph.Nodes)
                [graph.Nodes(i),temp] = graph.Nodes(i).RemovePacket();
                if temp
                    packetsToRoute{end+1} = temp;
                end
            end
        end
        function receivers = GetReceivers(graph,QueueSelection)
            receivers = [];
            for i = 1:length(graph.Nodes)
                [graph.Nodes(i),temp,packetID] = graph.Nodes(i).GetReceiverOptions();
                minQueue = inf;
                minQueueNode = 0;
                if(queueSelection)
                    for option = temp
                        if graph.Nodes(option).QueueSize < minQueue
                            minQueue = graph.Nodes(option).QueueSize;
                            minQueueNode = option;
                        end
                    end
                    receivers{end+1} = minQueueNode;
                else
                    receivers{end+1} = temp(end);
                end
            end
        end
    end
end