classdef Packet 
    properties
        ID {mustBeInteger,mustBeNonnegative}
        ArrivalTime {mustBeNonnegative}
        DepartureTime {mustBeNonnegative}
        TravelTime {mustBeNonnegative}
        IsActive {mustBeNumericOrLogical}
    end
    methods
        function packet = Packet(id,arrivalTime) 
            packet.ID = id;
            packet.ArrivalTime = arrivalTime;
            packet.IsActive = true;
        end
        function packet = Depart(departureTime)
            packet.DepartureTime = departureTime;
            packet.TravelTime = departureTime - packet.ArrivalTime;
            packet.IsActive = false;
        end
    end
end