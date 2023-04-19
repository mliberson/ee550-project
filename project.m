% Define the network matrix
network = [1 0.8 0 0.8 0 0 0;
           0 1 0.8 0.8 0.5 0 0;
           0 0 1 0 0.8 0 0;
           0 0.8 0 1 0.8 0.5 0;
           0 0 0 0 1 0.8 0.5;
           0 0 0 0 0 1 0.8;
           0 0 0 0 0 0 1];

% Set the source and destination node indices
source = 1;
destination = 7;

time_elapsed_sum = 0;

% Initialize the packets
num_packets = 100000;
packets = repmat(struct('time_elapsed', 0, 'current_node', source, 'past_node', 0), 1, num_packets);

% Simulate the movement of the packets
while any([packets.current_node] ~= destination)
    % Transmit packets from nodes 1-6 (excluding the last one: 7)
    for node = 1:(size(network, 1)-1)
        % Find the neighbors of the current node
        neighbors = find(network(node, :) > 0);
        % Find the packets that are located at the node
        eligible_packets = find([packets.current_node] == node);
        for j = 1:length(eligible_packets)
                % Select an individual packet
                packet = packets(eligible_packets(j));
                % Transmit packet to the highest-numbered neighbor
                for i = 1:length(neighbors)
                    % Start at the highest numbered number
                    neighbor = neighbors(end-i+1);
                    if rand() < network(node, neighbor)
                        packet.time_elapsed = packet.time_elapsed + 1;
                        packet.past_node = packet.current_node;
                        packet.current_node = neighbor;
                        packets(eligible_packets(j)) = packet;
                        break;
                    end
                end
        end 
    end
    %global time across all packets
end

% Print the time elapsed for each packet to reach the destination
for i = 1:length(packets)
    %fprintf('Packet %d: %d time units\n', i, packets(i).time_elapsed);
    time_elapsed_sum = time_elapsed_sum + packets(i).time_elapsed;
end

fprintf('Average time %f\n', time_elapsed_sum/num_packets);