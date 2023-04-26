import pytest

from ccfcoef.specpower import SPECPower

import pandas as pd


def test_servers():
    with pytest.raises(ValueError, match="Data not clean, servers contains Ghz"):
        SPECPower(pd.DataFrame({'CPU Description': ['Intel Ghz']}))
    # should not raise an exception
    SPECPower(pd.DataFrame({'CPU Description': ['Intel']}))
