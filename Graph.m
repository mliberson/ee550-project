classdef Graph
    properties
        %array of nodes in the network (type Node)
        Nodes (1,:) Node
        %edge weights in the network
        Edges = [1 0.8 0 0.8 0 0 0;
                0 1 0.8 0.8 0.5 0 0;
                0 0 1 0 0.8 0 0;
                0 0.8 0 1 0.8 0.5 0;
                0 0 0 0 1 0.8 0.5;
                0 0 0 0 0 1 0.8;
                0 0 0 0 0 0 1];
        %size of each queue at times t
        QueueSizes (:,:) {mustBeInteger,mustBeNonnegative}
        %size of all queues at times t
        NetworkOccupancy (1,:) {mustBeInteger,mustBeNonnegative}
        %packets
        Packets (1,:) Packet
        %time
        Time {mustBeInteger,mustBeNonnegative}
        %indicates whether queue sizesare considered when choosing next node
        QueueSelection {mustBeNumericOrLogical}
    end
    methods
        function graph = Graph(queueSelection)
            graph.NetworkOccupancy = 0;
            graph.QueueSelection = queueSelection;
            for i = 1:length(edgeWeights(:,1))
                graph.Nodes{end+1} = Node(i,edgeWeights(i,:));
            end
            graph.QueueSizes = zeros(1,length(graph.Nodes));
        end
        function graph = Run(graph,arrival)
            if arrival
                newPacket = Packet(length(graph.Packets),graph.Time);
                graph.Packets{end+1} = newPacket;
                graph.Nodes(1).InsertPacket(newPacket.ID);
                graph.NetworkOccupancy = graph.NetworkOccupancy + 1;
            end
            receivers = graph.GetReceivers();
            packetsToRoute = graph.GetPacketsToRoute();
            for i = 1:length(receivers)
                if receivers(i) == length(graph.Nodes)
                    Packets(packetsToRoute(i)).Depart(time);
                    graph.NetworkOccupancy = graph.NetworkOccupancy - 1;
                end
                graph.Nodes(receiver(i)) = graph.Nodes(receiver(i)).InsertPacket(packetsToRoute(i));
            end
            networkOccupancyTemp = 0;
            for node = graph.Nodes
                queueSizesTemp = node.QueueSize;
                networkOccupancyTemp = networkOccupancyTemp + queueSizesTemp;
            end
            graph.QueueSizes = [graph.QueueSizes; queueSizesTemp];
            graph.networkOccupancy{end+1} = networkOccupancyTemp;
            graph.Time = graph.Time + 1;
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
        function receivers = GetReceivers(graph)
            receivers = [];
            for i = 1:length(graph.Nodes)
                [graph.Nodes(i),temp,packetID] = graph.Nodes(i).GetReceiverOptions();
                minQueue = inf;
                minQueueNode = 0;
                if(graph.QueueSelection)
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