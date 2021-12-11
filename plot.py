# %%
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# date_start = "2020-08-01" # 2020 no vaccine fall
date_start = "2021-08-01"  # 2021 vaccine fall


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


def plot_comparison(csv_file, fig_location, ref_column, pred_column, ref_offset=0):
    df_pred = pd.read_csv(csv_file)

    df_ref = get_real_dataframe()[["date", ref_column]].copy()
    df_ref.columns = ["date", "reference"]

    # offset the value
    df_ref["reference"] = df_ref["reference"] - ref_offset

    # convert floats to intengers
    df_pred.time = df_pred.time.astype(int)

    # add dates
    df_pred["date"] = pd.to_datetime(date_start)
    df_pred.date = df_pred.date + pd.to_timedelta(df_pred.time, "D")

    df_pred = df_pred[["date", pred_column]].copy()
    df_pred["diff"] = df_pred[pred_column].diff()
    df_pred["diff"] = df_pred["diff"].mask(df_pred["diff"] < 0, 0)
    df_pred["predicted"] = df_pred["diff"].cumsum()

    df_cmp = df_pred.merge(df_ref, on="date", how="left")
    df_cmp = df_cmp.melt(id_vars=["date"],
                         value_vars=["predicted", "reference"],
                         var_name="type")

    g = sns.lineplot(
        data=df_cmp,
        x="date",
        y="value",
        style="type",
        hue="type"
    )

    g.get_figure().savefig(fig_location)
    g.get_figure().clf()


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

    plot_model_output(template.format("vaccine.csv"),
                      template.format("vaccine.png"))
    plot_comparison(csv_file=template.format("vaccine.csv"),
                    fig_location=template.format("vaccine_cases.png"),
                    ref_column="total_cases",
                    ref_offset=1_680_000,
                    pred_column="quarantined"
                    )
    plot_comparison(csv_file=template.format("vaccine.csv"),
                    fig_location=template.format("vaccine_deaths.png"),
                    ref_column="total_deaths",
                    ref_offset=30_369,
                    pred_column="dead"
                    )


def plot_2020_no_vaccine():

    template = "out/cr_2020_no_{}"

    plot_model_output(template.format("vaccine.csv"),
                      template.format("vaccine.png"))
    plot_comparison(csv_file=template.format("vaccine.csv"),
                    fig_location=template.format("vaccine_cases.png"),
                    ref_column="total_cases",
                    pred_column="quarantined"
                    )
    plot_comparison(csv_file=template.format("vaccine.csv"),
                    fig_location=template.format("vaccine_deaths.png"),
                    ref_column="total_deaths",
                    pred_column="dead"
                    )


if __name__ == "__main__":
    # plot_2020_no_vaccine()
    plot_2021_vaccine()
# %%
