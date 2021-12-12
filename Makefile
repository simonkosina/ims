CXX=g++
CXXFLAGS=-g -Wall -pedantic -std=c++11 

SIMLIB_DIR=./simlib/src
SIMLIB_DEPEND=$(SIMLIB_DIR)/simlib.so $(SIMLIB_DIR)/simlib.h

CXXFLAGS += -I$(SIMLIB_DIR)

MAIN=src/main
PROJ=sim

all:
	$(CXX) $(CXXFLAGS) -o $(PROJ) $(MAIN).cpp $(SIMLIB_DEPEND) $(SIMLIB_DIR)/simlib.a -lm
	$(CXX) $(CXXFLAGS) -o $(PROJ) $(MAIN).cpp $(SIMLIB_DEPEND) $(SIMLIB_DIR)/simlib.so -lm

sim: all
	./sim

plot: sim
	python plot.py

clean:
	rm *.o 