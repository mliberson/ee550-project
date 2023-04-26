classdef Node
    properties
        %Node id in network
        ID {mustBeInteger,mustBeNonnegative}
        %queue of packet ids
        Queue (1,:) {mustBeInteger,mustBeNonnegative}
        %number of packets in queue
        QueueSize {mustBeInteger,mustBeNonnegative}
        %transmission success probabilities to adjacent nodes
        Edges (1,:) {mustBeNonnegative}
        %indicator of transmission success used to remove from queue
        Status {mustBeNumericOrLogical}
    end
    methods
        function node = Node(id,edgeWeights)
            node.ID = id;
            node.Edges = edgeWeights;
            node.Queue = [];
            node.QueueSize = 0;
            node.Status = false;
        end
        function [node, options] = GetReceiverOptions(node)
            options = [];
            if node.QueueSize == 0
                return;
            end
            for i = 1:length(node.Edges)
                if rand(1,1) < node.Edges(i)
                    options{end+1} = i;
                    node.Status = true;
                end
            end
        end
        function [node, packetID] = RemovePacket(node)
            packetID = 0;
            if node.Status
                node.Queue = node.Queue(2:end);
                node.Status = false;
                packetID = node.Queue(end);
            end
        end
        function node = InsertPacket(node,packetID)
            if packetID
                node.Queue{end+1} = packetID;
                node.QueueSize = node.QueueSize + 1;
            end
        end
    end
end