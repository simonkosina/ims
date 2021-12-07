#include <stdlib.h>
#include <stdio.h>
#include <stdbool.h>
#include <string.h>

/* MODEL PARAMETERS */
#define SIZE_0 1000 // size of the outer array
#define SIZE_1 10000 // size of the inner array
#define PERCENT_VACCINATED 50 // percentage of people that are vaccinated 
#define INIT_NUM_INFECTIONS 10 // number of initially infected people

/* CONSTANTS */
#define NUM_NEIGHBORS 12 // number of neighbors in the Von Neumann neighborhood


typedef enum State {
    UNINFECTED,
    INFECTED
} state;


typedef struct Cell {
    state st;
    bool isVaccinated;
} cell;


/* Grids */
cell **grid_new; // user for storing new values
cell **grid_old; // used for computing new values


/* Stats */
long numVaccinated = 0;
long numInfected = 0;


/**
* Generate a random number in the [0, 1] interval.
*/
double rnd() {
    return rand() / ((double) RAND_MAX);
}


/**
* Create a 2d grid of cell structures. Function grid_free should be 
* called when the program is done working with the grid.
*/
cell** grid_create() {
    cell **grid;

    grid = malloc(SIZE_0*sizeof(cell*));

    if (grid == NULL) {
        return NULL;
    }

    for (int i = 0; i < SIZE_0; i++) {
        grid[i] = malloc(SIZE_1*sizeof(cell));

        if (grid[i] == NULL) {
            return NULL;
        }
    }

    return grid;
}


/**
* Initialize the cells in the grid according
* to the defined model parameters.
*/
void grid_init(cell **grid) {
    double prob_vaccinated = PERCENT_VACCINATED / ((double) 100);
    double prob_infected = ((double) INIT_NUM_INFECTIONS) / ((double) (((long) SIZE_0) * ((long) SIZE_1)));

    for (int i = 0; i < SIZE_0; i++) {
        for (int j = 0; j < SIZE_1; j++) {
            grid[i][j].st = UNINFECTED;
            grid[i][j].isVaccinated = false;

            if (rnd() <= prob_infected) {
                grid[i][j].st = INFECTED;
                numInfected++;
            }

            if (rnd() <= prob_vaccinated) {
                grid[i][j].isVaccinated = true;
                numVaccinated++;
            }
        }
    }
}


/**
* Free the memory allocated for the grid.
*/
void grid_free(cell** grid) {
    for (int i = 0; i < SIZE_0; i++) {
        free(grid[i]);
    }

    free(grid);
}


/**
* Replace the old grid with the newly copmuted grid.
*/
void grid_save(cell **old, cell **new) {
    for (int i = 0; i < SIZE_0; i++) {
        old[i] = memcpy(old[i], new[i], SIZE_1*sizeof(cell));
    }
}


/**
* Reset the global statistics counters before the next iteration.
*/
void stats_reset() {
    numVaccinated = 0;
    numInfected = 0;
}


/**
* Print out the statistics in the .csv format using ',' as a separator.
* If called for the first time it also prints the header.
*/
void stats_print() {
    bool static headerPrinted = false;

    if (!headerPrinted) {
        printf("vaccinated,infected\n");
        headerPrinted = true;
    }

    printf("%ld,%ld\n", numVaccinated, numInfected);
}


/**
* Find the neigboring cells using the Von Neumann neighborhood
* with Manhattan distance of 2 and periodic boundary conditions.
* https://en.wikipedia.org/wiki/Von_Neumann_neighborhood
*/
void cell_neighbors(int i, int j, int **neighbors) {
    // set the indices
    neighbors[0][0] = i + 1;
    neighbors[0][1] = j;
    
    neighbors[1][0] = i - 1;
    neighbors[1][1] = j;
    
    neighbors[2][0] = i;
    neighbors[2][1] = j + 1;
    
    neighbors[3][0] = i;
    neighbors[3][1] = j - 1;
    
    neighbors[4][0] = i + 1;
    neighbors[4][1] = j + 1;
    
    neighbors[5][0] = i + 1;
    neighbors[5][1] = j - 1;
    
    neighbors[6][0] = i - 1;
    neighbors[6][1] = j + 1;
    
    neighbors[7][0] = i - 1;
    neighbors[7][1] = j - 1;
    
    neighbors[8][0] = i + 2;
    neighbors[8][1] = j;
    
    neighbors[9][0] = i - 2;
    neighbors[9][1] = j;
    
    neighbors[10][0] = i;
    neighbors[10][1] = j + 2;
    
    neighbors[11][0] = i;
    neighbors[11][1] = j - 2;

    // apply periodic boundary conditions
    for (int i = 0; i < NUM_NEIGHBORS; i++) {
        if (neighbors[i][0] < 0) {
            neighbors[i][0] = SIZE_0 + neighbors[i][0];
        } else {
            neighbors[i][0] = neighbors[i][0] % SIZE_0;
        }

        if (neighbors[i][1] < 0) {
            neighbors[i][1] = SIZE_1 + neighbors[i][1];
        } else {
            neighbors[i][1] = neighbors[i][1] % SIZE_1;
        }
    }
}


/**
* Simulate a step for the given cell and update
* cells in the neighborhood.
*/
void cell_step(int i, int j) {    
    int* neighbors[NUM_NEIGHBORS];

    for (int i = 0; i < NUM_NEIGHBORS; i++) {
        neighbors[i] = malloc(2*sizeof(int));

        if (neighbors[i] == NULL) {
            return; // FIXME: error what to do?
        }
    }

    cell_neighbors(i, j, (int **) neighbors);

    for (int i = 0; i < NUM_NEIGHBORS; i++) {
        printf("%d:\n", i);
        printf("\t%d:\n", neighbors[i][0]);
        printf("\t%d:\n", neighbors[i][1]);
    }

    // TODO: Free neighbors!
}


int main (int argc, char **argv) {
    grid_old = grid_create();
    grid_new = grid_create();

    grid_init(grid_new);
    grid_save(grid_old, grid_new);

    stats_print();
    stats_reset();

    cell_step(0,0);

    grid_free(grid_old);
    grid_free(grid_new);

    return 0;
}