CXX=g++
CXXFLAGS=-g -Wall -pedantic -std=c++11 

SIMLIB_DIR=./simlib/src
SIMLIB_DEPEND=$(SIMLIB_DIR)/simlib.so $(SIMLIB_DIR)/simlib.h

CXXFLAGS += -I$(SIMLIB_DIR)

MAIN=src/main
PROJ=sim

sim: all
	./sim
	python plot.py

all:
	$(CXX) $(CXXFLAGS) -o $(PROJ) $(MAIN).cpp $(SIMLIB_DEPEND) $(SIMLIB_DIR)/simlib.a -lm
	$(CXX) $(CXXFLAGS) -o $(PROJ) $(MAIN).cpp $(SIMLIB_DEPEND) $(SIMLIB_DIR)/simlib.so -lm

clean:
	rm *.o 