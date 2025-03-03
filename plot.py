from scipy import stats
from scipy import constants
import polars as pl
import matplotlib.pyplot as plt
from data import data


class Constants:
    R = 65e-3
    e = constants.electron_mass
    h = constants.Planck
    m_e = constants.electron_mass
    e_c = constants.elementary_charge
    coeff = 2 * R * h / ((2 * m_e * e_c) ** 0.5)

def process_n(df: pl.DataFrame):
    """Performs linear regression and returns the slope with proper units."""
    linear_regression: stats.LinRegressResult = stats.linregress(
        x=df["x"].to_numpy(),
        y=df["y"].to_numpy(),
    )
    return linear_regression.slope


def compute_d_values(df: pl.DataFrame):
    """Processes each unique n-group and computes d_n values."""
    results = []
    for (n,), series in df.group_by("n"):
        m = process_n(series)  # Slope (m * sqrt(V))
        d_n = (m * Constants.coeff ** 2) ** 0.5
        results.append((n, series, d_n))
        print(f"d_{n} = {d_n:.3e}")
    return results


def plot_results(results):
    """Plots the series for different n-values on the same graph."""
    fig, ax = plt.subplots(figsize=(8, 6))

    for n, series, _ in results:
        ax.plot(
            series["x"].to_numpy(),
            series["y"].to_numpy(),
            marker="o",
            linestyle="-",
            label=f"n={n}",
        )

    ax.set_xlabel("Voltage (V)")
    ax.set_ylabel("Ring radius$^{-2}$ (m$^{-2}$)")
    ax.set_title("Electron Diffraction Rings in Wehnelt Cylinder")
    ax.legend()
    ax.grid(True)

    plt.show()


def main():
    df = pl.DataFrame(
        data,
        schema={
            "n": pl.UInt32(),
            "voltage_kv": pl.Float64(),
            "diameter_outer": pl.Float64(),
            "diameter_inner": pl.Float64(),
        },
        orient="row",
    )
    df = df.with_columns(
        (pl.col("voltage_kv") * 1e3).alias("voltage"),
    )
    df = df.with_columns(
        pl.col("voltage").sqrt().alias("sqrt_voltage"),
        ((pl.col("diameter_outer") + pl.col("diameter_inner")) / 4 * 1e-3).alias("r"),
    )

    df = df.with_columns(
        (pl.col("voltage")).alias("x"),
        (1 / (pl.col("r") ** 2)).alias("y")
    )

    # df = df.with_columns(
    #     (1 / pl.col("x") ** 0.5).alias("x"),
    #     (1 / pl.col("y") ** 0.5).alias("y"),
    # )

    ds = df.select(
        pl.col("n"),
        1 / pl.col("r") * Constants.coeff * 1 / pl.col("sqrt_voltage")
    )


    print(df)

    print(f"{ds=}")
    avgs = ds.group_by(pl.col('n')).agg(pl.col('literal').mean())
    print(f"{avgs}")



    results = compute_d_values(df)
    plot_results(results)


if __name__ == "__main__":
    main()
