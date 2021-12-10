#include <stdlib.h>
#include <stdio.h>
#include <simlib.h>

// Initial conditions
double S0 = 47431256;
double E0 = 100;
double I0 = 20;
double R0 = 2;
double D0 = 1;
double N = S0 + E0 + I0 + R0 + D0;

// Model paramters
double lambda = 0;
double v = 0;
double vr = 0.05;
double omega = 0.2;
double psi = 0.542;
double rho = 0.1924;
double kappa = 0.095;
double d = 0;
double l = 0.11;

#define MAX_TIME 180

// Model
struct SEIR {
    Integrator S, E, I, R, D;

    SEIR(
        double lambda_,
        double v_,
        double vr_,
        double omega_,
        double psi_,
        double rho_,
        double kappa_,
        double d_,
        double l_
    ) :
        S(lambda_*N - lambda_*v_*N + omega_*R - psi_*((S*I)/N) - vr_*S - d_*S, S0),
        E(psi_*((S*I)/N) - rho_*E - d_*E -l_*E, E0),
        I(rho_*E - kappa_*I - d_*I - l_*I, I0),
        R(lambda_*v_*N + kappa_*I - d_*R - omega_*R + vr_*S, R0),
        D(d_*S + d_*E + d_*I + d_*R + l_*E + l_*I, D0) {}
};

// Create model instance
SEIR seir(lambda, v, vr, omega, psi, rho, kappa, d, l);

void Sample() {
    Print("%6.2f,%.5g,%.5g,%.5g,%.5g,%.5g\n", T.Value(), seir.S.Value(), seir.E.Value(), seir.I.Value(), seir.R.Value(), seir.D.Value());
}

Sampler S(Sample, 1);        // Output step 

int main() {
    double maxtime = MAX_TIME;
    SetOutput("seir.csv");    // Redirect output to file
    Print("time,susceptible,exposed,infectious,recovered,death\n");
    Init(0, maxtime);           // Initialize simulator
    SetMethod("rke"); 
    SetAccuracy(1e-8);          // Required accuracy
    Run();                      // Simulate
    return 0;
}