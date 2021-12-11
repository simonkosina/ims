#ifndef CR_2020_NO_VACCINE_H

#define CR_2020_NO_VACCINE_H

// Initial values
#define V_RATE0 0.0
#define S0 ((1-V_RATE0)*10694364)    // susceptible
#define E0 20000    // exposed (infected, but not yet infectious)
#define I0 20000    // infectious
#define Q0 5000    // quarantined
#define R0 0    // recovered
#define D0 0    // dead
#define V0 (V_RATE0*S0)   // vaccinated

// Model paramters
#define LAMBDA 453 // new births and residents per unit of time
#define BETA 0.0000000342 // transmisson rate
#define ALPHA 0.000  // vaccination rate
#define MU 0.0000356    // natural death rate
#define GAMMA (1.0/5.5)   // incubation period
#define SIGMA 1  // vaccine inefficacy
#define DELTA (1.0/3.8)   // infection time
#define KAPPA 0.004 // mortality rate
#define THETA (0.10)    // average days until recovery
#define RHO (1.0/15)      // average days until death

#endif