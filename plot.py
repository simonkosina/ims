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

    ax.grid(visible=False, which='major', axis='x')
    ax.set_title(title)

    ax.set_ylabel(ylabel)
    ax.set_xlabel("Dátum")

    ax.xaxis.set_major_formatter(dates.DateFormatter("%d-%b"))

    ax.get_figure().tight_layout()
    ax.get_figure().savefig(fig_location)
    ax.get_figure().clf()


def plot_comparison(csv_file, fig_location, ref_column, pred_column, date_start, title, ylabel, ref_offset=0):
    df_pred = pd.read_csv(csv_file)

    ref_col = "Dáta" if ref_offset == 0 else f"Dáta - {ref_offset}"

    df_ref = get_real_dataframe()[["date", ref_column]].copy()
    df_ref.columns = ["date", ref_col]

    # offset the value
    df_ref[ref_col] = df_ref[ref_col] - ref_offset

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
                         value_vars=["Model", ref_col],
                         var_name="type")

    ax = sns.lineplot(
        data=df_cmp,
        x="date",
        y="value",
        style="type",
        hue="type"
    )

    ax.grid(visible=False, which='major', axis='x')
    ax.get_legend().set_title(None)

    ax.set_title(title)

    ax.set_ylabel(ylabel)
    ax.set_xlabel("Dátum")

    ax.xaxis.set_major_formatter(dates.DateFormatter("%d-%b"))

    ax.get_figure().tight_layout()
    ax.get_figure().savefig(fig_location)
    ax.get_figure().clf()


def get_total_cases(filename, vaccine_effectivity, date_start):
    """
    Get a dataframe with total cases for the given vaccine efficacy.
    """

    filename = filename.format(vaccine_effectivity)
    cases_col = f"{vaccine_effectivity}%"

    df = pd.read_csv(filename, usecols=["time", "quarantined"])

    df["time"] = df["time"].astype(int)
    df["date"] = pd.to_datetime(date_start)
    df.date = df.date + pd.to_timedelta(df.time, "D")
    df["diff"] = df["quarantined"].diff()
    df["diff"] = df["diff"].mask(df["diff"] < 0, 0)
    df[cases_col] = df["diff"].cumsum()

    return df[["date", cases_col]].copy()


def get_total_deaths(filename, vaccine_effectivity, date_start):
    """
    Get a dataframe with total cases for the given vaccine efficacy.
    """

    filename = filename.format(vaccine_effectivity)
    cases_col = f"{vaccine_effectivity}%"

    df = pd.read_csv(filename, usecols=["time", "dead"])

    df["time"] = df["time"].astype(int)
    df["date"] = pd.to_datetime(date_start)
    df.date = df.date + pd.to_timedelta(df.time, "D")
    df["diff"] = df["dead"].diff()
    df["diff"] = df["diff"].mask(df["diff"] < 0, 0)
    df[cases_col] = df["diff"].cumsum()

    return df[["date", cases_col]].copy()


def plot_deaths(title, col, ylabel, filename, fig_location, date_start, vals):
    df = get_total_deaths(filename, vals[0], date_start)

    for p in vals[1:]:
        df2 = get_total_deaths(filename, p, date_start)
        df = df.merge(df2, on="date", how="left")

    df = df.melt(id_vars=["date"], var_name=col)

    ax = sns.lineplot(
        data=df,
        x="date",
        y="value",
        hue=col
    )

    ax.grid(visible=False, which='major', axis='x')
    ax.set_title(title)

    ax.set_ylabel("Celkový počet úmrtí")
    ax.set_xlabel(ylabel)

    ax.xaxis.set_major_formatter(dates.DateFormatter("%d-%b"))

    ax.get_figure().tight_layout()
    ax.get_figure().savefig(fig_location)
    ax.get_figure().clf()

def plot_cases(title, ylabel, col, filename, fig_location, date_start, vals):
    df = get_total_cases(filename, vals[0], date_start)

    for p in vals[1:]:
        df2 = get_total_cases(filename, p, date_start)
        df = df.merge(df2, on="date", how="left")

    df = df.melt(id_vars=["date"], var_name=col)

    ax = sns.lineplot(
        data=df,
        x="date",
        y="value",
        hue=col
    )

    ax.grid(visible=False, which='major', axis='x')
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
    template = "{}/cr_2021_{}"
    date_start = "2021-09-01"

    plot_model_output(csv_file=template.format("out", "vaccine.csv"),
                      fig_location=template.format("img", "vaccine.png"),
                      ylabel="Počet prípadov",
                      title="Model - jeseň 2021",
                      date_start=date_start)

    plot_comparison(csv_file=template.format("out", "vaccine.csv"),
                    fig_location=template.format("img", "vaccine_cases.png"),
                    ref_column="total_cases",
                    ref_offset=1_647_761,
                    pred_column="quarantined",
                    date_start=date_start,
                    title="Prípady - jeseň 2021",
                    ylabel="Celkový počet prípadov"
                    )

    plot_comparison(csv_file=template.format("out", "vaccine.csv"),
                    fig_location=template.format("img", "vaccine_deaths.png"),
                    ref_column="total_deaths",
                    ref_offset=30_483,
                    pred_column="dead",
                    date_start=date_start,
                    title="Úmrtia - jeseň 2021",
                    ylabel="Celkový počet úmrtí"
                    )


def plot_2020_no_vaccine():

    template = "{}/cr_2020_no_{}"
    date_start = "2020-08-01"

    plot_model_output(template.format("out", "vaccine.csv"),
                      template.format("img", "vaccine.png"),
                      date_start=date_start,
                      ylabel="Počet prípadov",
                      title="Model - jeseň 2020",
                      )

    plot_comparison(csv_file=template.format("out", "vaccine.csv"),
                    fig_location=template.format("img", "vaccine_cases.png"),
                    ref_column="total_cases",
                    pred_column="quarantined",
                    date_start=date_start,
                    title="Prípady - jeseň 2020",
                    ylabel="Celkový počet prípadov"
                    )

    plot_comparison(csv_file=template.format("out", "vaccine.csv"),
                    fig_location=template.format("img", "vaccine_deaths.png"),
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
    sns.set_style("whitegrid")
    # calc_mean_cfr("2020-aug-01", "2021-dec-01")
    plot_2020_no_vaccine()
    plot_2021_vaccine()
    
    # Plot experiment 1 results
    plot_cases(
        title="Počet prípadov vzhľadom na efektívnosť vakcíny",
        col="Miera vakcinácie",
        ylabel="Celkový počet prípadov",
        filename="out/ex1_effectivity_{}.csv", 
        fig_location="img/ex1_cases.png",
        date_start="2021-sep-01",
        vals = [53, 63, 73, 83, 93]
        )
    
    
    plot_deaths(
        title="Počet úmrtí vzhľadom na efektívnosť vakcíny",
        col="Miera vakcinácie",
        ylabel="Celkový počet úmrtí",
        filename="out/ex1_effectivity_{}.csv",
        fig_location="img/ex1_deaths.png", 
        date_start="2021-sep-01",
        vals=[53, 63, 73, 83, 93]
        )
    
    
    # Plot experiment 2 results
    plot_cases(
        title="Počet prípadov vzhľadom na mieru vakcinácie populácie",
        filename="out/ex2_vaccination_{}.csv",
        fig_location="img/ex2_cases.png",
        col="Efektívnosť vakcín",
        ylabel="Celkový počet prípadov",
        date_start="2021-sep-01",
        vals=[40, 50, 60, 70, 80]
        )
    
    plot_deaths(
        title="Počet úmrtí vzhľadom na mieru vakcinácie populácie",
        col="Efektívnosť vakcín",
        ylabel="Celkový počet úmrtí",
        filename="out/ex2_vaccination_{}.csv",
        fig_location="img/ex2_deaths.png",
        date_start="2021-sep-01",
        vals=[40, 50, 60, 70, 80]
        )
    
    # Plot experiment 3 results
    for e in [53, 63, 73, 83, 93]:
        plot_cases(
            title=f"Prípady vzhľadom na mieru vakcinácie populácie, $\sigma$ = {100-e}%",
            col="Miera zaočkovania",
            ylabel="Celkový počet prípadov",
            filename=f"out/ex3_e_{e}" + "_v_{}.csv",
            fig_location=f"img/ex3_e_{e}_cases.png",
            date_start="2021-sep-01",
            vals=[40, 50, 60, 70, 80]
        )
        
        plot_deaths(
            title=f"Úmrtia vzhľadom na mieru vakcinácie populácie, $\sigma$ = {100-e}%",
            col="Miera zaočkovania",
            ylabel="Celkový počet úmrtí",
            filename=f"out/ex3_e_{e}" + "_v_{}.csv",
            fig_location=f"img/ex3_e_{e}_deaths.png",
            date_start="2021-sep-01",
            vals=[40, 50, 60, 70, 80]
        )

    ...
# %%
