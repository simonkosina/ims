#ifndef CR_2020_NO_VACCINE_H

#define CR_2020_NO_VACCINE_H

#define OUT_FILE "out/cr_2020_no_vaccine.csv"

// Initial values
#define E0 15000    // exposed (infected, but not yet infectious)
#define I0 15000    // infectious
#define Q0 15000    // quarantined
#define R0 0    // recovered
#define D0 500    // dead
#define V0 0   // vaccinated
#define S0 (10694364 - E0 - I0 - Q0 - V0)   // susceptible

// Model paramters
#define LAMBDA 453 // new births and residents per unit of time
#define BETA 0.0000000348 // transmisson rate
#define ALPHA 0.000  // vaccination rate
#define MU 0.0000356    // natural death rate
#define GAMMA (1.0/5.5)   // incubation period
#define SIGMA 1  // vaccine inefficacy
#define DELTA (1.0/3.8)   // infection time
#define KAPPA 0.004 // mortality rate
#define THETA (0.10)    // average days until recovery
#define RHO (1.0/15)      // average days until death

#endif