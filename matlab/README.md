# canparser.m

Designed for WUFR-22 data logging format:
```
time,id,data
00001311,00000001,37805d8063803780
```

Requirements:
- The most up to date [VEHICLE.dbc](https://github.com/WURacing/firmware/blob/master/2022/VEHICLE.dbc)
- The most up to date [PE3.dbc](https://github.com/WURacing/firmware/blob/master/2022/PE3.dbc)

Usage:
```
[messages, signals] = daqCanParse('LOG00121.CSV');
```

Double click on signals in workspace to see all data in timetables, per message.