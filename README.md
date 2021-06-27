# Cloud Carbon Coefficients

This notebook calculates the coefficients used in [Cloud Carbon
Footprint](https://www.cloudcarbonfootprint.org/), an application that
estimates the energy (kilowatt hours) and carbon emissions (metric tons CO2e)
from public cloud provider utilization.

These values are based on the [SPECpower_ssj2008
results](https://www.spec.org/power_ssj2008/results/). New data is released
every quarter so [the notebook](coefficients.ipynb) helps calculate updated
coefficients. The full results are in [data/](data/).

## Updating the SPECpower results

1. Copy the new lines from the full results table into the CSV.
2. Ensure the "CPU Description" column is clean. [The
   notebook](coefficients.ipynb) explains how the data should be cleaned.
3. Run the notebook to calculate the new values.
4. The final section of the notebook explains where to insert the values into
   the main Cloud Carbon Footprint project.
