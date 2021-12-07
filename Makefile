CC=gcc
CFLAGS=-g -Wall -pedantic -std=gnu99 -Wextra

MAIN=src/main
PROJ=sim

SOURCEDIR=src
INCLUDEDIR=include

all:
	$(CC) $(FLAGS) -o $(PROJ) $(MAIN).c

clean:
	rm *.o 