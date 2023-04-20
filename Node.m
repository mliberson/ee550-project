classdef Node
    properties
        %Node id in network
        ID {mustBeNumeric}
        %queue of packet ids
        Queue (1,:) {mustBeNumeric}
        %number of packets in queue
        QueueSize {mustBeNumeric}
        %transmission success probabilities to adjacent nodes
        Edges (1,:) {mustBeNumeric}
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
        function options = Send(node)
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
        function node = UpdateQueue(node,packetID)
            if packet
                node.Queue{end+1} = packetID;
                node.QueueSize = node.QueueSize + 1;
            end
            if node.Status
                node.Queue = node.Queue(2:end);
                node.Status = false;
            end
        end
    end
end