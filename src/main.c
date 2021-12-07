#include <stdlib.h>
#include <stdio.h>
#include <stdbool.h>

/* MODEL PARAMETERS */
#define SIZE_0 1000 // size of the outer array
#define SIZE_1 10000 // size of the inner array
#define PERCENT_VACCINATED 50 // percentage of people that are vaccinated 
#define INIT_NUM_INFECTIONS 10 // number of initially infected people

typedef enum State {
    UNINFECTED,
    INFECTED
} state;

typedef struct Cell {
    state st;
    bool isVaccinated;
} cell;

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

    long vaccinatedCount = 0;
    long infectedCount = 0;

    for (int i = 0; i < SIZE_0; i++) {
        for (int j = 0; j < SIZE_1; j++) {
            grid[i][j].st = UNINFECTED;
            grid[i][j].isVaccinated = false;

            if (rnd() <= prob_infected) {
                grid[i][j].st = INFECTED;
                vaccinatedCount++;
            }

            if (rnd() <= prob_vaccinated) {
                grid[i][j].isVaccinated = true;
                infectedCount++;
            }
        }
    }

    printf("Vaccinated: %ld\n", vaccinatedCount);
    printf("Infected: %ld\n", infectedCount);
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

int main (int argc, char **argv) {    
    cell **grid_old, **grid_new;

    grid_old = grid_create();
    grid_new = grid_create();

    grid_init(grid_old);

    grid_free(grid_old);
    grid_free(grid_new);

    return 0;
}