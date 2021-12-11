# %%
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

if __name__ == "__main__":
    df = pd.read_csv("seir.csv")

    # convert floats to intengers
    df.time = df.time.astype(int)

    # add dates
    df["date"] = pd.to_datetime("2020-03-02")
    df.date = df.date + pd.to_timedelta(df.time, "D")

    dfm = df.melt(id_vars=["date"],
                  value_vars=["susceptible", "exposed", "infectious",
                              "quarantined", "recovered", "dead", "vaccinated"],
                  var_name="compartment")

    sns.lineplot(
        data=dfm,
        x="date",
        y="value",
        hue="compartment"
    )

    plt.savefig("seir.png")

# %%
