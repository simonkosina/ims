#include <stdlib.h>
#include <stdio.h>
#include <simlib.h>

// Initial values
#define V_RATE 0.0

#define S0 ((1-V_RATE)*10694364)    // susceptible
#define E0 20000    // exposed (infected, but not yet infectious)
#define I0 20000    // infectious
#define Q0 10000    // quarantined
#define R0 0    // recovered
#define D0 0    // dead
#define V0 (V_RATE*S0)   // vaccinated

// Model paramters
#define LAMBDA 453 // new births and residents per unit of time
#define BETA 0.000000034 // transmisson rate
#define ALPHA 0.000  // vaccination rate
#define MU 0.0000356    // natural death rate
#define GAMMA (1.0/5.5)   // incubation period
#define SIGMA 1  // vaccine inefficacy
#define DELTA (1.0/3.8)   // infection time
#define KAPPA 0.005// mortality rate
#define THETA (0.10)    // average days until recovery
#define RHO (1.0/15)      // average days until death

#define MAX_TIME 120

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
        S(lambda - beta*S*I - alpha*S - mu*S, (double) S0),
        E(beta*S*I - gamma*E + sigma*beta*V*I - mu*E, (double) E0),
        I(gamma*E - delta*I - mu*I, (double) I0),
        Q(delta*I - (1 - kappa)*theta*Q - kappa*rho*Q - mu*Q, (double) Q0),
        R((1 - kappa)*theta*Q - mu*R, (double) R0),
        D(kappa*rho*Q, (double) D0),
        V(alpha*S - sigma*beta*V*I - mu*V, (double) V0) {}
};

// Create model instance
SEIR seir(LAMBDA, BETA, ALPHA, MU, GAMMA, SIGMA, DELTA, KAPPA, THETA, RHO);

void Sample() {
    Print("%6.2f,%.5g,%.5g,%.5g,%.5g,%.5g,%.5g,%.5g\n", T.Value(), seir.S.Value(), seir.E.Value(), seir.I.Value(), seir.Q.Value(), seir.R.Value(), seir.D.Value(), seir.V.Value());
}

Sampler S(Sample, 1);        // Output step 

int main() {
    double maxtime = MAX_TIME;
    printf("%lf,%lf,%lf,%lf,%lf,%lf,%lf,%lf,%lf,%lf\n", (double) LAMBDA, ((double) BETA),(double)  ALPHA,(double)  MU,(double)  GAMMA,(double)  SIGMA,(double)  DELTA,(double)  KAPPA,(double)  THETA,(double)  RHO);
    SetOutput("out/cr_validation.csv");    // Redirect output to file
    Print("time,susceptible,exposed,infectious,quarantined,recovered,dead,vaccinated\n");
    Init(0, maxtime);           // Initialize simulator
    SetAccuracy(1e-8);          // Required accuracy
    Run();                      // Simulate
    return 0;
}