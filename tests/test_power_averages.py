import pytest

from ccfcoef.cli import CPU_FAMILIES, calculate_cpus_families_power


@pytest.fixture
def average_power():
    return calculate_cpus_families_power(CPU_FAMILIES)


def test_amd_epyc_gen1(average_power):
    assert float('{:,.2f}'.format(average_power['EPYC 1st Gen'].min_watts)) == 0.82
    assert float('{:,.2f}'.format(average_power['EPYC 1st Gen'].max_watts)) == 2.55
    assert float('{:,.2f}'.format(average_power['EPYC 1st Gen'].max_watts_gcp_adjusted)) == 2.49
    assert float('{:,.2f}'.format(average_power['EPYC 1st Gen'].gb_chip)) == 89.60
