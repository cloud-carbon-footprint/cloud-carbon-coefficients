import pytest

from ccfcoef.aws.coefficients import AWSCoefficients
from ccfcoef.azure.coefficients import AzureCoefficients
from ccfcoef.cli import calculate_cpus_families_power, CPU_FAMILIES, DATA_DIR, to_dataframe
from ccfcoef.gcp.coefficients import GCPCoefficients


@pytest.fixture(scope='module')
def average_power():
    return calculate_cpus_families_power(CPU_FAMILIES)


def test_azure_usage(average_power):
    azure = AzureCoefficients.instantiate(DATA_DIR.joinpath('azure-instances.csv'))
    coefficients = to_dataframe(azure.use_coefficients(average_power))

    assert float('{:,.2f}'.format(coefficients["Min Watts"].mean())) == 0.85
    assert float('{:,.2f}'.format(coefficients["Max Watts"].mean())) == 3.69
    assert float('{:,.2f}'.format(coefficients["GB/Chip"].mean())) == 80.30


def test_aws_usage(average_power):
    aws = AWSCoefficients.instantiate(DATA_DIR.joinpath('aws-instances.csv'))
    coefficients = to_dataframe(aws.use_coefficients(average_power))

    assert float('{:,.2f}'.format(coefficients["Min Watts"].mean())) == 1.14
    assert float('{:,.2f}'.format(coefficients["Max Watts"].mean())) == 4.34
    assert float('{:,.2f}'.format(coefficients["GB/Chip"].mean())) == 73.22


def test_gcp_usage(average_power):
    gcp = GCPCoefficients.instantiate(DATA_DIR.joinpath('gcp-instances.csv'))
    coefficients = to_dataframe(gcp.use_coefficients(average_power))

    assert float('{:,.2f}'.format(coefficients["Min Watts"].median())) == 0.68
    assert float('{:,.2f}'.format(coefficients["Max Watts"].median())) == 3.77
    assert float('{:,.2f}'.format(coefficients["GB/Chip"].median())) == 75.04
