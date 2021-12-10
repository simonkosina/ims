#include <stdlib.h>
#include <stdio.h>
#include <simlib.h>
#include <math.h>

// Inspired by https://github.com/InstituteforDiseaseModeling/covasim/tree/master/covasim
// article behaviour of modeling https://journals.plos.org/ploscompbiol/article?id=10.1371/journal.pcbi.1009149

#define POPULATION 1000000 // people in simulation

// age https://www.worldometers.info/coronavirus/coronavirus-age-sex-demographics/
//cr stats https://www.czso.cz/csu/czso/vekove-slozeni-obyvatelstva-2020

#define AGE1 0.186972// rate of people 0-17 years
#define AGE2 0.349007// rate of people 18-44 years
#define AGE3 0.246632// rate of people 45-64 years
#define AGE4 0.119872// rate of people 65-74 years
#define AGE5 0.079459// rate of people 75+ years

#define DEATH_RATE_AGE1 //probability of dying when got infected

int exposed_ppl = 0;

/* function headers */
void setUpInitialParam(int i);

class People : public Process {
    public:
    unsigned int uid;

    //stats of person
    short int age;
    double death_prob;
    int n_infections;  // can be exposed multiple time
    
    //states booleans
    short int susceptible;
    short int exposed;
    short int infectious;
    short int critical;
    short int quarantined;
    short int vaccinated;
    short int recovered;
    short int dead;

    //vakcinacia states -- important!
    short int doses;
    short int type_of_vaccine;

    //odbornik mysli ze aj variant kovidu by bol dobry dopracovat, to sa ked tak dorobi ale vacsinou 
    //je vo vzduchu majoritne jeden variant takze sa daju staty toho


    void Behavior(){
       //Wait(Normal(10,3)); // wait 
        this->exposed = 1;
        exposed_ppl++;
    }
    

};




/*
Default transmission probabilities are roughly 0.050 per contact per day for households, 0.010 for workplaces and schools, and 0.005 for the community. 
https://journals.plos.org/ploscompbiol/article?id=10.1371/journal.pcbi.1009149
*/
/*
Poisson distribution whose mean value can be specified by the user depending on the modeling context (with a default value of 20)
*/


//TODO Event ktory bude generovat novych ludi - narodeny + imigranti
class Generator : public Event{
    double dt;
    void Behavior(){
        new People;
        Activate(Time+Exponential(dt));
    }
    public:
        Generator(double d) : dt(d){Activate();}
};


People *all_people[POPULATION];

//this function will generate people with their custom atributes
void generatePeople(){
    for(int i=1; i<=POPULATION; i++){
        People *person = new People;
        all_people[i-1] = person;

        setUpInitialParam(i);
        person->Activate();
    }
}

void setUpInitialParam(int i){
    People *person = all_people[i-1];
    person->uid = i; // add uid
    person->exposed = 0;
    person->susceptible= 0;
    person->exposed= 0;
    person->infectious= 0;
    person->critical= 0;
    person->quarantined= 0;
    person->vaccinated=0;
    person->recovered= 0;
    person->dead=0;

    //setup by parameters will go through categories and will set uniform age for number of ppl in that category
    if(i+1 < POPULATION*AGE1){
        person->age=round(Uniform(0,17));
    }
    else if(i+1 < POPULATION*AGE1 + POPULATION*AGE2){
        person->age=round(Uniform(18,44));
    }
    else if(i+1 < POPULATION*AGE1 + POPULATION*AGE2 + POPULATION*AGE3){
        person->age=round(Uniform(45,64));
    }
    else if(i+1 < POPULATION*AGE1 + POPULATION*AGE2 + POPULATION*AGE3 + POPULATION*AGE4){
        person->age=round(Uniform(64,74));
    }
    else if(i+1 < POPULATION*AGE1 + POPULATION*AGE2 + POPULATION*AGE3 + POPULATION*AGE4 + POPULATION*AGE5){
        person->age=round(Uniform(75,100));
    }
    
}


void Sample() {
    //Print("%6.2f,%d\n", T.Value(),exposed_ppl);
}

Sampler S(Sample, 1);   

int main() {
    SetOutput("seir.csv");
    Init(0,30);
    generatePeople();
    Print("time,people\n");
    Run();
    
    int age[101];
    for(int i=0; i<101;i++){
        age[i]=0;
    }
    for(int i=0; i< POPULATION; i++){
        age[(all_people[i]->age)]++;
    }

    for(int i=0; i<=100;i++){
        Print("%d, %d\n",i,age[i]);
    }
    int total = 0;
    int average_sum=0;
    for(int i=0; i<101;i++){
        total += age[i];
        average_sum += age[i]*i;
    }
    Print("\n ---- %d  avg %f \n",total, (float) average_sum / POPULATION);
    return 0;
}