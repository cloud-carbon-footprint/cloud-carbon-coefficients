# Cloud Carbon Coefficients

This notebook calculates the coefficients used in [Cloud Carbon
Footprint](https://www.cloudcarbonfootprint.org/), an application that
estimates the energy (kilowatt hours) and carbon emissions (metric tons CO2e)
from public cloud provider utilization.

These values are based on the [SPECpower_ssj2008
results](https://www.spec.org/power_ssj2008/results/). New data is released
every quarter so [the notebook](coefficients.ipynb) helps calculate updated
coefficients. The full results are in [data/](data/).

## Setup - Deepnote (recommended)

The recommended way to use this notebook is in Deepnote, which provides free
environments and has a good UI. 

1. Click the button below to create a a copy of the project in Deepnote.
2. Open the `coefficients.ipynb` file in Deepnote, then press the "Run notebook"
   button at the top.

[<img
src="https://deepnote.com/buttons/launch-in-deepnote-white.svg">](https://deepnote.com/launch?url=https://github.com/davidmytton/cloud-carbon-coefficients)

## Setup - VS Code

A `.devcontainer` is provided if you want to run this inside a container or
using GitHub Codespaces. This will automatically set up the environment with
Python 3.9. You can then open the `coefficients.ipynb` file in VS Code and press
the `Run all cells` button.

## Setup - Manual

The notebook requires Python 3.9 and [Jupyter (Lab or
Notebook)](https://jupyter.org/install). Install both of these for your platform
and then open `coefficients.ipynb`.

## Updating the SPECpower results

1. Copy the new lines from the [full
   results](https://www.spec.org/power_ssj2008/results/power_ssj2008.html) table
   into the CSV.
2. Ensure the "CPU Description" column is clean by following the instructions in
   [the notebook](coefficients.ipynb).
3. Run the notebook to calculate the new values.
4. The final three sections of the notebook - Azure, AWS, GCP - explain where to
   place the values from the output tables.
