function [messages, signals] = daqCanParse(filename)
%DAQCANPARSE Load a LOG file from the WUFR22 data logger.
%   Detailed explanation goes here

% Load the CAN network descriptor files (these tell us how to decode the
% messages)
dbpe3 = canDatabase('PE3.dbc');
dbvehicle = canDatabase('VEHICLE.dbc');
db(1) = dbvehicle; db(2) = dbpe3;

% Load the log file (types: id=uint32, time=double, data=string)
opts = detectImportOptions(filename);
opts = setvartype(opts,{'id'},'uint32');
opts = setvartype(opts,{'data'},'string');
csv = readtable(filename, opts);

% Convert time to real seconds
csv.time = csv.time/1000.0;
% Convert hex data to cell arrays of 8 bytes
hex = reshape(char(csv.data).',2,[]).';
dec = uint8(hex2dec(hex));
csv.data = num2cell(reshape(dec, 8,size(csv,1)).', 2);

% Rename columns to what canMessageTimetable will expect
csv.Properties.VariableNames = {'Timestamp' 'ID' 'Data'};
% Other required properties
csv.Extended = csv.ID > 2047;  % not strictly true
csv.Remote = false(size(csv,1),1);
csv.Error = false(size(csv,1),1);

S = table2struct(csv);
% Convert and decode messages!
messages = canMessageTimetable(S, db);
signals = canSignalTimetable(messages);

end

