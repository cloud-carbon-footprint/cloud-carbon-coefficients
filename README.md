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
2. Press the "Run notebook" button at the top (open `coefficients.ipynb`
   from the left menu if it does not open automatically).

[<img
src="https://deepnote.com/buttons/launch-in-deepnote-white.svg">](https://deepnote.com/launch?url=https://github.com/davidmytton/cloud-carbon-coefficients/blob/main/coefficients.ipynb)

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

## Tests

Basic tests exist in-line. They can also be executed from the terminal:

```
nbdev_test_nbs
```

## Git hooks

Git hooks from [`nbdev`](https://nbdev.fast.ai/) are used to clean notebooks
before they're committed. This avoids committing all the metadata that changes
on each run. See the [`nbdev` Git hooks
docs](https://nbdev.fast.ai/cli.html#Git-hooks) for more details.

Cleaning the notebook before commit can be done with `nbdev_clean_nbs`. 
Installing the Git hooks using `nbdev_install_git_hooks` will do this 
automatically on commit.