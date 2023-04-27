import numpy as np
import pandas as pd
import pytest

from ccfcoef.aws.coefficients import AWSCoefficients
from ccfcoef.azure.coefficients import AzureCoefficients
from ccfcoef.cli import DATA_DIR, to_dataframe
from ccfcoef.gcp.coefficients import GCPCoefficients


@pytest.fixture(scope='module')
def gcp_cpus():
    return pd.read_csv(DATA_DIR.joinpath('gcp-instances-cpus.csv'))


@pytest.fixture(scope='module')
def aws_cpus():
    return pd.read_csv(DATA_DIR.joinpath('aws-instances-cpus.csv'))


def test_sample_azure(gcp_cpus):
    azure = AzureCoefficients.instantiate(DATA_DIR.joinpath('azure-instances.csv'))
    azure_embodied = to_dataframe(azure.embodied_coefficients(gcp_cpus))

    # Pick some random instances to test the results are as expected
    result = azure_embodied.query('type == "A1 v2"')
    assert np.isclose(result['additional_memory'], 66.62)
    assert np.isclose(result['additional_storage'], 50.0)
    assert np.isclose(result['additional_cpus'], 100.0)
    assert np.isclose(result['additional_gpus'], 0.0)
    assert np.isclose(result['total'], 1216.62)

    result = azure_embodied.query('type == "NC24s v3"')
    assert np.isclose(result['additional_memory'], 599.62)
    assert np.isclose(result['additional_storage'], 50.0)
    assert np.isclose(result['additional_cpus'], 100.0)
    assert np.isclose(result['additional_gpus'], 600.0)
    assert np.isclose(result['total'], 2349.62)

    result = azure_embodied.query('type == "S896om"')
    assert np.isclose(result['additional_memory'], 51145.79)
    assert np.isclose(result['additional_storage'], 50.0)
    assert np.isclose(result['additional_cpus'], 100.0)
    assert np.isclose(result['additional_gpus'], 0.0)
    assert np.isclose(result['total'], 52295.79)


def test_sample_aws(aws_cpus):
    aws = AWSCoefficients.instantiate(DATA_DIR.joinpath('aws-instances.csv'))
    aws_embodied = to_dataframe(aws.embodied_coefficients(aws_cpus))

    # Pick some random instances to test the results are as expected
    result = aws_embodied.query('type == "a1.medium"')
    assert np.isclose(result['additional_memory'], 22.21)
    assert np.isclose(result['additional_storage'], 0)
    assert np.isclose(result['additional_cpus'], 0)
    assert np.isclose(result['additional_gpus'], 0)
    assert np.isclose(result['total'], 1022.21)

    result = aws_embodied.query('type == "c3.xlarge"')
    assert np.isclose(result['additional_memory'], 61.07)
    assert np.isclose(result['additional_storage'], 200.0)
    assert np.isclose(result['additional_cpus'], 100.0)
    assert np.isclose(result['additional_gpus'], 0)
    assert np.isclose(result['total'], 1361.07)

    result = aws_embodied.query('type == "g4dn.xlarge"')
    assert np.isclose(result['additional_memory'], 510.79)
    assert np.isclose(result['additional_storage'], 200.0)
    assert np.isclose(result['additional_cpus'], 100.0)
    assert np.isclose(result['additional_gpus'], 1200.0)
    assert np.isclose(result['total'], 3010.79)


def test_sample_gcp(gcp_cpus):
    gcp = GCPCoefficients.instantiate(DATA_DIR.joinpath('gcp-instances.csv'))
    gcp_embodied = to_dataframe(gcp.embodied_coefficients(gcp_cpus))

    # Pick some random instances to test the results are as expected
    result = gcp_embodied.query('type == "e2-standard-2" and microarchitecture == "Skylake"')
    assert np.isclose(result['additional_memory'], 155.46)
    assert np.isclose(result['additional_storage'], 0)
    assert np.isclose(result['additional_cpus'], 100.0)
    assert np.isclose(result['additional_gpus'], 0)
    assert np.isclose(result['total'], 1255.46)

    result = gcp_embodied.query('type == "n2-standard-4" and microarchitecture == "Cascade Lake"')
    assert np.isclose(result['additional_memory'], 688.46)
    assert np.isclose(result['additional_storage'], 100.0)
    assert np.isclose(result['additional_cpus'], 100.0)
    assert np.isclose(result['additional_gpus'], 0)
    assert np.isclose(result['total'], 1888.46)

    result = gcp_embodied.query('type == "a2-highgpu-8g" and microarchitecture == "Cascade Lake"')
    assert np.isclose(result['additional_memory'], 1865.5)
    assert np.isclose(result['additional_storage'], 100.0)
    assert np.isclose(result['additional_cpus'], 100.0)
    assert np.isclose(result['additional_gpus'], 2400)
    assert np.isclose(result['total'], 5465.5)

    gcp_mean = to_dataframe(gcp.embodied_coefficients_mean(gcp_embodied))

    # Pick some random instances to test the results are as expected
    result = gcp_mean.query('type == "e2-standard-2"')
    assert np.isclose(result['total_mean'], 1230.46)

    result = gcp_mean.query('type == "n2-standard-4"')
    assert np.isclose(result['total_mean'], 1888.46)

    result = gcp_mean.query('type == "a2-highgpu-8g"')
    assert np.isclose(result['total_mean'], 5465.5)
