% Define the network matrix
% Starting edge weights are 0.5
network = [1 0.5 0 0.5 0 0 0;
           0 1 0.5 0.5 0.5 0 0;
           0 0 1 0 0.5 0 0;
           0 0.5 0 1 0.5 0.5 0;
           0 0 0 0 1 0.5 0.5;
           0 0 0 0 0 1 0.5;
           0 0 0 0 0 0 1];


% Set the source and destination node indices
source = 1;
destination = 7;

time_elapsed_sum = 0;

% Initialize the packets
num_packets = 1000;

queueSizes = zeros(6, num_packets);
%start with one packet now
packets = repmat(struct('time_elapsed', 0, 'current_node', source), 1, 1);


% Simulate the movement of the packets
for i=1:num_packets
    % Transmit packets from nodes 6-1 (excluding the last one: 7)
    for iter = 1:(size(network, 1)-1)
        node = (size(network, 1)-1)-iter+1;
        % Find the neighbors of the current node
        neighbors = find(network(node, :) > 0);
        % Build the queue that is located at the node
        queue = find([packets.current_node] == node);
        % Only proceed if queue is nonempty
        if ~isempty(queue)
            % Get the first element of the queue
            packet = packets(queue(1));
            % Transmit packet to the highest-numbered neighbor
            for j = 1:length(neighbors)
                % Start at the highest numbered number
                neighbor = neighbors(end-j+1);
                if rand() < calculateEdgeProbability(node, neighbor, network)
                    packet.time_elapsed = packet.time_elapsed + 1;
                    packet.current_node = neighbor;
                    packets(queue(1)) = packet;
                    break;
                end
            end
        end
    end
    % TODO: change this so it only appends a packet every 1/lambda
    % iterations
    %add new packet to the end
    packets = [packets struct('time_elapsed', 0, 'current_node', source)];


    % Print the queue sizes
    for node = 1:(size(network, 1)-1)
        fprintf('Node %d: Queue size %d \n', node, length(find([packets.current_node] == node)));
        queueSizes(node,i) = length(find([packets.current_node] == node));
    end
end

% Set the color map to a sequence of unique colors
colors = hsv(6);

% Create a vector representing the column indices (time)
time = 1:size(queueSizes, 2);

% Plot the scatter graph with each row colored differently
figure;
hold on;
for i = 1:size(queueSizes, 1)
    scatter(time, queueSizes(i,:), [], colors(i,:), 'filled');
end
hold off;

% Set the axis labels and legend
xlabel('Time');
ylabel('Size');
legend('Queue 1', 'Queue 2', 'Queue 3', 'Queue 4', 'Queue 5', 'Queue 6');

function prob = calculateEdgeProbability(node, neighbor, network)
    %placeholder, probability is the edge weight as defined by the network
    prob = network(node, neighbor); 
end
