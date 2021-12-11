# %%
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

date_start = "2020-08-01"

def plot_model_output(csv_file, fig_location):
    df = pd.read_csv(csv_file)

    # convert floats to intengers
    df.time = df.time.astype(int)

    # add dates
    df["date"] = pd.to_datetime(date_start)
    df.date = df.date + pd.to_timedelta(df.time, "D")

    dfm = df.melt(id_vars=["date"],
                  value_vars=["susceptible", "exposed", "infectious",
                              "quarantined", "recovered", "dead", "vaccinated"],
                  var_name="compartment")

    g = sns.lineplot(
        data=dfm,
        x="date",
        y="value",
        hue="compartment"
    )

    g.get_figure().savefig(fig_location)
    g.get_figure().clf()

def plot_cummulative(csv_file, fig_location):
    df = pd.read_csv(csv_file)

    # convert floats to intengers
    df.time = df.time.astype(int)

    # add dates
    df["date"] = pd.to_datetime(date_start)
    df.date = df.date + pd.to_timedelta(df.time, "D")

    dfc = df[["date", "quarantined", "dead"]].copy()
    dfc["new_cases"] = dfc.quarantined.diff()
    dfc["new_cases"] = dfc["new_cases"].mask(dfc["new_cases"] < 0, 0)
    dfc["cases"] = dfc["new_cases"].cumsum()
    
    dfc["new_deaths"] = dfc.dead.diff()
    dfc["new_deaths"] = dfc["new_deaths"].mask(dfc["new_deaths"] < 0, 0)
    dfc["deaths"] = dfc["new_deaths"].cumsum()

    dfm = dfc.melt(id_vars=["date"],
                  value_vars=["cases", "deaths"],
                  var_name="type")

    g = sns.lineplot(
        data=dfm,
        x="date",
        y="value",
        hue="type"
    )

    g.get_figure().savefig(fig_location)
    g.get_figure().clf()

if __name__ == "__main__":
    plot_model_output("out/cr_validation.csv", "out/cr_validation_out.png")
    plot_cummulative("out/cr_validation.csv", "out/cr_validation_cummulative.png")
# %%
