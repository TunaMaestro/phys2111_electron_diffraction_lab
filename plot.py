from scipy import stats
import numpy as np
import scipy.optimize as opt
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

def uncertainty(df: pl.DataFrame):
    x=df["x"].to_numpy()
    y=df["y"].to_numpy()
    y_err=df["y_err"].to_numpy()
    # Define a linear model: y = m*x + c
    def linear_model(x, m, c):
        return m * x + c

    # Perform weighted least squares fitting
    popt, pcov = opt.curve_fit(linear_model, x, y, sigma=y_err, absolute_sigma=True)
    m_fit, c_fit = popt  # Fitted slope and intercept
    m_err, c_err = np.sqrt(np.diag(pcov))  # Standard errors of parameters

    # Compute Chi-Squared statistic
    residuals = y - linear_model(x, *popt)
    chi2 = np.sum((residuals / y_err) ** 2)
    dof = len(y) - len(popt)  # Degrees of freedom (n - number of parameters)
    chi2_red = chi2 / dof  # Reduced chi-squared

    # Compute R-squared
    ss_total = np.sum((y - np.mean(y)) ** 2)
    ss_residual = np.sum(residuals ** 2)
    r_squared = 1 - (ss_residual / ss_total)

    # Print results
    print(f"\tFitted Parameters: m = {m_fit:.3f} ± {m_err:.3f}, c = {c_fit:.3f} ± {c_err:.3f}")
    print(f"\tChi-Squared: {chi2:.3f}, Reduced Chi-Squared: {chi2_red:.3f}")
    print(f"\tR-Squared: {r_squared:.3f}")

    # Confidence Interval Calculation (95%)
    alpha = 0.05
    t_val = stats.t.ppf(1 - alpha / 2, dof)
    m_conf = t_val * m_err
    c_conf = t_val * c_err
    print(f"\t95% Confidence Interval for m: ±{m_conf:.3f}, for c: ±{c_conf:.3f}")
    print(f"\tRelative uncertainty for m: {m_conf / m_fit}")

def process_n(df: pl.DataFrame):
    """Performs linear regression and returns the slope with proper units."""
    linear_regression: stats.LinRegressResult = stats.linregress(
        x=df["x"].to_numpy(),
        y=df["y"].to_numpy(),
    )
    
    return linear_regression


def compute_d_values(df: pl.DataFrame):
    """Processes each unique n-group and computes d_n values."""
    results = []
    for (n,), series in df.group_by("n"):
        linregress = process_n(series)
        m = linregress.slope  # Slope (m * sqrt(V))
        d_n = (m * Constants.coeff ** 2) ** 0.5
        results.append((n, series, d_n, linregress))
        print(f"d_{n} = {d_n:.3e}")
    return results


def plot_results(results, configure, finalise, errors):
    """Plots the series for different n-values on the same graph."""
    fig, ax = plt.subplots(figsize=(8, 6))

    for n, series, _, regression in results:
        x = series["x"].to_numpy()
        y = series["y"].to_numpy()
        ax.errorbar(
            x,
            y,
            yerr=errors(x, y),
            marker="+",
            linestyle="",
            label=f"n={n}",
        )
        if regression:
            best_fit_y = regression.slope * x + regression.intercept
            ax.plot(x, best_fit_y, linestyle="-", label=f"Fit n={n}")

    ax.legend()
    ax.grid(True)

    configure(ax)

    finalise(plt)

def configure_analysis_graph(ax):
    ax.set_xlabel("Voltage (V)")
    ax.set_ylabel("Ring radius$^{-2}$ (m$^{-2}$)")
    ax.set_title("Electron Diffraction: Analysis curve")
    
def configure_raw_graph(ax):
    ax.set_xlabel("Voltage (V)")
    ax.set_ylabel("Ring radius (mm)")
    ax.set_title("Electron Diffraction Rings in Wehnelt Cylinder")
    

def write(path):
    def do_write(plt):
        plt.savefig(path)
    return do_write


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


    raw = [
        (n, series.select(
            pl.col("voltage").alias("x"),
            pl.col("r").alias("y"),
        ), None, None)
        for (n,), series in df.group_by(pl.col('n'))
    ]

    print(f"{raw=}")


    results = compute_d_values(df)
    plot_results(raw, configure_raw_graph, write("plots/raw.png"), lambda x, y: 1e-3)
    plot_results(results, configure_analysis_graph, write("plots/analysis.png"), lambda x, y: y * 5 / 100)

    for (n,), series in df.group_by(pl.col('n')):
        series = series.with_columns((pl.col("y") * 5 / 100).alias("y_err"))
        print(f"Uncertainty for n={n}")
        uncertainty(series)


if __name__ == "__main__":
    main()
