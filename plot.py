# %%
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

if __name__ == "__main__":
    df = pd.read_csv("seir.csv")
    dfm = df.melt(id_vars=["time"], var_name="subset")

    sns.lineplot(
        data=dfm,
        x="time",
        y="value",
        hue="subset"
    )
    
    plt.savefig("seir.png");
