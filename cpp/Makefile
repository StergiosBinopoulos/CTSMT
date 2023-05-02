CC = g++
CFLAGS = -Wall -O3

# ****************************************************

core: action.o readwrite.o utils.o parameters.o passenger.o transmission.o socialforcemodel.o seat.o spot.o scenario.o main.o environment.o
	$(CC) $(CFLAGS) -o core action.o readwrite.o utils.o parameters.o passenger.o transmission.o socialforcemodel.o seat.o spot.o scenario.o main.o environment.o

main.o: main.cpp
	$(CC) $(CFLAGS) -c main.cpp

parameters.o: scenario/parameters.cpp scenario/parameters.h
	$(CC) $(CFLAGS) -c scenario/parameters.cpp

transmission.o: transmission/transmission.cpp transmission/transmission.h
	$(CC) $(CFLAGS) -c transmission/transmission.cpp

socialforcemodel.o: socialforcemodel/socialforcemodel.cpp socialforcemodel/socialforcemodel.h
	$(CC) $(CFLAGS) -c socialforcemodel/socialforcemodel.cpp

readwrite.o: io/readwrite.cpp io/readwrite.h
	$(CC) $(CFLAGS) -c io/readwrite.cpp

seat.o: scenario/seat.cpp scenario/seat.h
	$(CC) $(CFLAGS) -c scenario/seat.cpp

spot.o: scenario/spot.cpp scenario/spot.h
	$(CC) $(CFLAGS) -c scenario/spot.cpp

passenger.o: scenario/passenger.cpp scenario/passenger.h
	$(CC) $(CFLAGS) -c scenario/passenger.cpp

utils.o: utils/utils.cpp utils/utils.h
	$(CC) $(CFLAGS) -c utils/utils.cpp

scenario.o: scenario/scenario.cpp scenario/scenario.h
	$(CC) $(CFLAGS) -c scenario/scenario.cpp

environment.o: scenario/environment.cpp scenario/environment.h
	$(CC) $(CFLAGS) -c scenario/environment.cpp

action.o: scenario/action.cpp scenario/action.h
	$(CC) $(CFLAGS) -c scenario/action.cpp

clean:
	rm *.o
