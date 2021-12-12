#ifndef CR_2021_VACCINE

#define CR_2021_VACCINE

#define OUT_FILE "out/ex2_vaccination_40.csv"

#define LR ((double) 0.4)

// Initial values
#define N0 10702942 // total population
#define VR 0.4 // vaccination rate

#define E0 4934    // exposed (infected, but not yet infectious)
#define I0 4934    // infectious
#define Q0 2467    // quarantined
#define R0 (int) (1647761*LR)    // recovered
#define D0 0    // dead
#define V0 ((int) (N0*(VR)))   // vaccinated
#define S0 (N0 - R0 - E0 - I0 - Q0 - V0)    // susceptible

// Model paramters
#define LAMBDA 899 // new births and residents per unit of time
#define BETA 0.000000066 // transmisson rate
#define ALPHA 0.001  // vaccination rate
#define MU 0.0000396    // natural death rate
#define GAMMA (1.0/5.5)   // incubation period
#define SIGMA 0.27  // vaccine inefficacy
#define DELTA (1.0/3.8)   // infection time
#define KAPPA 0.0035 // mortality rate
#define THETA (0.10)    // average days until recovery
#define RHO (1.0/15)      // average days until death

#define MAX_TIME 120

#endif