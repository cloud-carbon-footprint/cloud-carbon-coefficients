import pytest

from ccfcoef.cli import CPU_FAMILIES, calculate_cpus_families_power

# Expected values for each family in the order of CPU_FAMILIES
# family, min_watts, max_watts, max_watts_gcp_adjusted, gb_chip
EXPECTED_AVERAGE_POWER = [
    (CPU_FAMILIES[0].name, 0.82, 2.55, 2.49, 89.60),
    (CPU_FAMILIES[1].name, 0.47, 1.69, 1.58, 129.78),
    (CPU_FAMILIES[2].name, 0.45, 2.02, 1.87, 128.00),
    (CPU_FAMILIES[3].name, 2.17, 8.58, 8.55, 16.48),
    (CPU_FAMILIES[4].name, 3.04, 8.25, 8.20, 14.93),
    (CPU_FAMILIES[5].name, 1.90, 6.01, 5.97, 27.31),
    (CPU_FAMILIES[6].name, 0.71, 3.69, 3.39, 69.65),
    (CPU_FAMILIES[7].name, 0.64, 4.19, 3.90, 80.43),
    (CPU_FAMILIES[8].name, 0.64, 3.97, 3.64, 98.12),
    (CPU_FAMILIES[9].name, 1.14, 5.42, 5.41, 19.56),
]


@pytest.fixture(scope='module')
def average_power():
    return calculate_cpus_families_power(CPU_FAMILIES)


@pytest.mark.parametrize('family, min_watts, max_watts, max_watts_gcp_adjusted, gb_chip', EXPECTED_AVERAGE_POWER)
def test_cpu_average(family, min_watts, max_watts, max_watts_gcp_adjusted, gb_chip, average_power):
    assert float('{:,.2f}'.format(average_power[family].min_watts)) == min_watts
    assert float('{:,.2f}'.format(average_power[family].max_watts)) == max_watts
    assert float('{:,.2f}'.format(average_power[family].max_watts_gcp_adjusted)) == max_watts_gcp_adjusted
    assert float('{:,.2f}'.format(average_power[family].gb_chip)) == gb_chip
