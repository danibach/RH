# RH

Tools for exploring the Riemann zeta function on the critical line.

The current script samples

```text
s = 0.5 + i t
```

and plots the output values `zeta(s)` in the complex plane as `t` changes.

![Sample zeta plot](examples/zeta_critical_line_0_50.svg)

## Usage

This version uses only Python's standard library and writes an SVG file.

```bash
python3 plot_zeta_critical_line.py --t-min 0 --t-max 50 --points 1000 --output zeta_critical_line.svg
```

Open the generated `zeta_critical_line.svg` in a browser to view the plot.

Useful options:

```bash
python3 plot_zeta_critical_line.py \
  --sigma 0.5 \
  --t-min 0 \
  --t-max 100 \
  --points 2000 \
  --terms 128 \
  --output zeta_critical_line_0_100.svg
```

## How It Works

The script evaluates the zeta function via the Dirichlet eta function:

```text
zeta(s) = eta(s) / (1 - 2^(1 - s))
```

It then accelerates the alternating eta series with Euler's transformation.
For larger `t` ranges, increase `--terms` to improve numerical stability.

The SVG colors the curve by the input value `t`, with green marking the start
and red marking the end.

