#include <stdlib.h>
#include <stdio.h>
#include <simlib.h>

// Initial values
#define S_INIT 34217992    // susceptible
#define E_INIT 3    // exposed (infected, but not yet infectious)
#define I_INIT 3    // infectious
#define Q_INIT 1    // quarantined
#define R_INIT 0    // recovered
#define D_INIT 0    // dead
#define V_INIT 0    // vaccinated

// Model paramters
#define LAMBDA 2300 // new births and residents per unit of time
#define BETA 0.000000000858   // transmisson rate / N
#define ALPHA 0.000000000343  // vaccination rate
#define MU 30000    // natural death rate
#define GAMMA 5.5   // incubation period
#define SIGMA 0.05  // vaccine inefficacy
#define DELTA 3.8   // infection time
#define KAPPA 0.014 // mortality rate
#define THETA 10    // average days until recovery
#define RHO 15      // average days until death

#define MAX_TIME 1.80 // in days

// Model
struct SEIR {
    // N = S + E + I + Q + R + D + V
    Integrator S, E, I, Q, R, D, V;

    SEIR(
        double lambda,
        double beta,
        double alpha,
        double mu,
        double gamma,
        double sigma,
        double delta,
        double kappa,
        double theta,
        double rho
    ) :
        S(lambda - beta*S*I - alpha*S - mu*S, S_INIT),
        E(beta*S*I - gamma*E + sigma*beta*V*I - mu*E, E_INIT),
        I(gamma*E - sigma*I - mu*I, I_INIT),
        Q(sigma*I - (1 - kappa)*theta*Q - kappa*rho*Q - mu*Q, Q_INIT),
        R((1 - kappa)*theta*Q - mu*R, R_INIT),
        D(kappa*rho*Q, D_INIT),
        V(alpha*S - sigma*beta*V*I - mu*V, V_INIT) {}
};

// Create model instance
SEIR seir(LAMBDA, BETA, ALPHA, MU, GAMMA, SIGMA, DELTA, KAPPA, THETA, RHO);

void Sample() {
    Print("%6.2f,%.5g,%.5g,%.5g,%.5g,%.5g,%.5g,%.5g\n", T.Value(), seir.S.Value(), seir.E.Value(), seir.I.Value(), seir.Q.Value(), seir.R.Value(), seir.D.Value(), seir.V.Value());
}

Sampler S(Sample, 0.01);        // Output step 

int main() {
    double maxtime = MAX_TIME;
    SetOutput("seir.csv");    // Redirect output to file
    Print("time,s,e,i,q,r,d,v\n");
    Init(0, maxtime);           // Initialize simulator
    
    SetAccuracy(1e-8);          // Required accuracy
    Run();                      // Simulate
    SIMLIB_statistics.Output(); // Print simulation run statistics
    return 0;
}