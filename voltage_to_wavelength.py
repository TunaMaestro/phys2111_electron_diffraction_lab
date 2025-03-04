from plot import Constants

def wavelength(u):
    return Constants.h / (2 * Constants.m_e * Constants.e_c * u) ** 0.5

with open("/dev/stdin") as f:
    for line in f.readlines():
        print(f"{wavelength(float(line.strip())):.3g}")
