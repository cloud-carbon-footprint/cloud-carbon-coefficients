import re

from ccfcoef.aws.coefficients import AWSCoefficients
from ccfcoef.cli import DATA_DIR


def test_aws_platforms():
    aws = AWSCoefficients.instantiate(DATA_DIR.joinpath('aws-instances.csv'))
    aws_platforms = [re.sub('((Xeon Platinum)|Xeon)', '', p).strip()
                     for p in aws.instances['Platform CPU Name'].unique()]

    # We expect to detect the following platforms
    # Based on https://docs.google.com/spreadsheets/d/1YhtGO_UU9Hc162m7eQKYFQOnV4_yEK5_lgHYfl02JPE/edit#gid=1695769209
    assert 'E5-2666 v3' in aws_platforms
    assert 'E5-2676 v3' in aws_platforms
    assert 'E5-2686 v4' in aws_platforms
    assert 'E5-2650' in aws_platforms
    assert 'E5-2665' in aws_platforms
    assert 'E5-2670' in aws_platforms
    assert 'E5-2651 v2' in aws_platforms
    assert 'E5-2670 v2' in aws_platforms
    assert 'E5-2680 v2' in aws_platforms
    assert 'E7-8880 v3' in aws_platforms
    assert '8124M' in aws_platforms
    assert '8151' in aws_platforms
    assert '8175M' in aws_platforms
    assert '8176M' in aws_platforms
    assert '8252C' in aws_platforms
    assert '8259CL' in aws_platforms
    assert '8275CL' in aws_platforms
    # Commented out due to lack of Ice Lake SPECpower results
    # assert '8375C' in aws_platforms
    assert 'EPYC 7571' in aws_platforms
    assert 'EPYC 7R32' in aws_platforms
    assert 'Graviton' in aws_platforms
    assert 'Graviton2' in aws_platforms
    assert 'Core i7-8700B' in aws_platforms
