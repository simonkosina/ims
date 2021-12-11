# %%
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

from matplotlib import dates

def plot_model_output(csv_file, fig_location, date_start, title, ylabel):
    df = pd.read_csv(csv_file)

    # convert floats to intengers
    df.time = df.time.astype(int)

    # add dates
    df["date"] = pd.to_datetime(date_start)
    df.date = df.date + pd.to_timedelta(df.time, "D")

    dfm = df.melt(id_vars=["date"],
                  value_vars=["susceptible", "exposed", "infectious",
                              "quarantined", "recovered", "dead", "vaccinated"],
                  var_name="Trieda")
    
    dfm["Trieda"] = dfm["Trieda"].map(lambda x: x.upper()[0])

    ax = sns.lineplot(
        data=dfm,
        x="date",
        y="value",
        hue="Trieda"
    )

    ax.set_title(title)

    ax.set_ylabel(ylabel)
    ax.set_xlabel("Dátum")

    ax.xaxis.set_major_formatter(dates.DateFormatter("%d-%b"))
    
    ax.get_figure().tight_layout()
    ax.get_figure().savefig(fig_location)
    ax.get_figure().clf()


def plot_comparison(csv_file, fig_location, ref_column, pred_column, date_start, title, ylabel, ref_offset=0):
    df_pred = pd.read_csv(csv_file)

    df_ref = get_real_dataframe()[["date", ref_column]].copy()
    df_ref.columns = ["date", "Dáta"]

    # offset the value
    df_ref["Dáta"] = df_ref["Dáta"] - ref_offset

    # convert floats to intengers
    df_pred.time = df_pred.time.astype(int)

    # add dates
    df_pred["date"] = pd.to_datetime(date_start)
    df_pred.date = df_pred.date + pd.to_timedelta(df_pred.time, "D")

    df_pred = df_pred[["date", pred_column]].copy()
    df_pred["diff"] = df_pred[pred_column].diff()
    df_pred["diff"] = df_pred["diff"].mask(df_pred["diff"] < 0, 0)
    df_pred["Model"] = df_pred["diff"].cumsum()

    df_cmp = df_pred.merge(df_ref, on="date", how="left")
    df_cmp = df_cmp.melt(id_vars=["date"],
                         value_vars=["Model", "Dáta"],
                         var_name="type")

    ax = sns.lineplot(
        data=df_cmp,
        x="date",
        y="value",
        style="type",
        hue="type"
    )


    ax.get_legend().set_title(None)

    ax.set_title(title)

    ax.set_ylabel(ylabel)
    ax.set_xlabel("Dátum")

    ax.xaxis.set_major_formatter(dates.DateFormatter("%d-%b"))

    ax.get_figure().tight_layout()
    ax.get_figure().savefig(fig_location)
    ax.get_figure().clf()


def get_real_dataframe(csv_file="data/owid-covid-data.csv"):
    df = pd.read_csv(csv_file,
                     usecols=["iso_code", "date", "total_cases", "total_deaths"])

    df = df[df["iso_code"] == "CZE"][[
        "date", "total_cases", "total_deaths"]].copy()
    df.date = pd.to_datetime(df.date)
    df["date"] = df["date"].dt.strftime('%Y-%m-%d')
    df["date"] = pd.to_datetime(df.date)

    return df


def plot_2021_vaccine():
    template = "out/cr_2021_{}"
    date_start = "2021-08-01"

    plot_model_output(csv_file=template.format("vaccine.csv"),
                      fig_location=template.format("vaccine.png"),
                      ylabel="Počet prípadov",
                      title="Model - jeseň 2021",
                      date_start=date_start)

    plot_comparison(csv_file=template.format("vaccine.csv"),
                    fig_location=template.format("vaccine_cases.png"),
                    ref_column="total_cases",
                    ref_offset=1_680_000,
                    pred_column="quarantined",
                    date_start=date_start,
                    title="Prípady - jeseň 2021",
                    ylabel="Celkový počet prípadov"
                    )

    plot_comparison(csv_file=template.format("vaccine.csv"),
                    fig_location=template.format("vaccine_deaths.png"),
                    ref_column="total_deaths",
                    ref_offset=30_369,
                    pred_column="dead",
                    date_start=date_start,
                    title="Úmrtia - jeseň 2021",
                    ylabel="Celkový počet úmrtí"
                    )


def plot_2020_no_vaccine():

    template = "out/cr_2020_no_{}"
    date_start = "2020-08-01"

    plot_model_output(template.format("vaccine.csv"),
                      template.format("vaccine.png"),
                      date_start=date_start,
                      ylabel="Počet prípadov",
                      title="Model - jeseň 2020",
                      )
    
    plot_comparison(csv_file=template.format("vaccine.csv"),
                    fig_location=template.format("vaccine_cases.png"),
                    ref_column="total_cases",
                    pred_column="quarantined",
                    date_start=date_start,
                    title="Prípady - jeseň 2020",
                    ylabel="Celkový počet prípadov"
                    )
    plot_comparison(csv_file=template.format("vaccine.csv"),
                    fig_location=template.format("vaccine_deaths.png"),
                    ref_column="total_deaths",
                    pred_column="dead",
                    date_start=date_start,
                    title="Úmrtia - jeseň 2020",
                    ylabel="Celkový počet úmrtí"
                    )


def calc_mean_cfr(date_start, date_end):
    """
    Calculate the mean CFR over a given time period based on the real data.
    """
    
    df = get_real_dataframe()
    mask = (df["date"] >= pd.to_datetime(date_start)
            ) & (df["date"] < pd.to_datetime(date_end))
    dfs = df[mask].copy()
    dfs["ratio"] = dfs["total_deaths"]/dfs["total_cases"]

    return dfs["ratio"].mean()

if __name__ == "__main__":
    calc_mean_cfr("2020-aug-01", "2021-jan-01")
    plot_2020_no_vaccine()
    # plot_2021_vaccine()
# %%
