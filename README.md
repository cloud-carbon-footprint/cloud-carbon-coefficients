# Cloud Carbon Coefficients (ccfcoef)

This tool calculates the coefficients used in [Cloud Carbon
Footprint](https://www.cloudcarbonfootprint.org/), an application that
estimates the energy (kilowatt hours) and carbon emissions (metric tons CO2e)
from public cloud provider utilization.

These values are based on the [SPECpower_ssj2008
results](https://www.spec.org/power_ssj2008/results/). 

## Outputs

The outputs of this tool used in Cloud Carbon Footprint are two:

1. **Use stage coefficients:** Values are calculated within the notebook and
   output in-line for Azure (min watts, max watts, GB/chip), AWS (min watts, max
   watts, GB/chip) and GCP (min watts, max watts). The file to drop them into in
   CCF is indicated in the notebook. A CSV is created in `output/` with the
   values for each CPU architecture, currently for reference only.

2. **Embodied emissions coefficients:** Values are calculated within the
   notebook and output to CSV in `output/` for each instance type for each cloud
   platform in `kgCO2e`.

## Setup

This command line is writen in Python and manages its dependencies through
[poetry](https://python-poetry.org/). Steps: 

* Ensure you have or install Python 3.10 with `python3 --version`
* If you don't have it, install poetry: `curl -sSL https://install.python-poetry.org | python3 -`
* Run `poetry install` to install dependencies
* Run `poetry run ccfcoef --help` to see the available commands or `poetry shell` to enter a virtualenv and then `ccfcoef --help`

## Basic usage

Looking at the help output, you can see the available commands:

```bash
$ poetry run ccfcoef --help

Usage: ccfcoef [OPTIONS] COMMAND [ARGS]...

Options:
  --spec-version TEXT  The SPECpower version to use, use "ccfcoef list-specs"
                       to see available versions.
  --help               Show this message and exit.

Commands:
  cpu-averages           Display the calculated power usage averages for...
  embodied-coefficients  Calculate the embodied coefficients for each...
  filter-spec            Filter SPECpower file by CPU family.
  list-specs             Display all available SPECpower results files.
  show-constants         Display all constants available to ccfcoef.
  show-families          Display all CPU families available to ccfcoef.
  tag-spec               Tag SPECpower results with CPU family.
  update-specpower       Will fetch a new version of the SPECpower...
  usage-coefficients     Calculate the usage coefficients for each cloud...
```

### Generating the coefficients

* `usage-coefficients`: This command will calculate the usage coefficients for
  each cloud provider and output them to CSV in `output/`.

```bash
$ poetry run ccfcoef usage-coefficients -w

Calculating usage coefficients...
Using SPECpower results file: SPECpower-2023-05-01.csv

Azure
Missing: Unknown
Writing to output/coefficients-azure-use.csv, 8 entries.

GCP
Writing to output/coefficients-gcp-use.csv, 8 entries.

AWS
Missing: 8375C
Writing to output/coefficients-aws-use.csv, 11 entries.
```

* `embodied-coefficients`: This command will calculate the embodied coefficients
  for each cloud provider and output them to CSV in `output/`.

```bash
$ poetry run ccfcoef embodied-coefficients -w

Calculating embodied coefficients...
Azure
Writing to output/coefficients-azure-embodied.csv, 595 entries.
GCP
Writing to output/coefficients-gcp-embodied.csv, 277 entries.
GCP (mean)
Writing to output/coefficients-gcp-embodied-mean.csv, 126 entries.
AWS
Writing to output/coefficients-aws-embodied.csv, 621 entries.
```

### Updating the SPECpower results

* `update-specpower`: This command will fetch a new version of the SPECpower
  results file from the SPEC website and save it to `data/`.

```bash
$ poetry run ccfcoef update-specpower

Updating SPECpower data...
Found 830 results
Writing SPECpower-2023-05-01.csv
```

## Advanced usage

Other commands are available to help investigate the data and the coefficients. Use
`poetry run ccfcoef COMMAND --help` for more information.

### SPECpower versioning

`ccfcoef` uses the last available SPECpower results file by default. You can
specify a different version with the `--spec-version` option. This is a global
option and will set the SPECpower version for all commands.

* `list-specs`: This command will display all available SPECpower results files
  in `data/`. See example below.

```bash
$ poetry run ccfcoef list-specs

Available SPECpower results files:
file: SPECpower-2023-05-01.csv version:2023-05-01
file: SPECpower-2023-04-28.csv version:2023-04-28
file: SPECpower-2023-04-27.csv version:2023-04-27
file: SPECpower-2023-04-06.csv version:2023-04-06
file: SPECpower-2022-03-01.csv version:2022-03-01

$ poetry run ccfcoef --spec-version 2022-03-01 cpu-averages --family intel-coffeelake

Using SPECpower results file: SPECpower-2022-03-01.csv

Averages for: Coffee Lake
Average: Min Watts = 1.14
Average: Max Watts = 5.42
Average: Max Watts (GCP) = 5.41
Average: GB/chip = 19.56
```
