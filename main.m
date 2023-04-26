lambda = 0.5;

p = poisscdf(1,lambda);

graph = Graph(false);

for t = 1:1000
    if rand(1,1) < p
        graph.Run(true);
    else
        graph.Run(false);
    end
end

