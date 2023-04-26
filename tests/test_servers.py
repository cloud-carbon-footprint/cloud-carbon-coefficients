import pytest

from ccfcoef.servers import Servers

import pandas as pd


def test_servers():
    with pytest.raises(ValueError, match="Data not clean, servers contains Ghz"):
        Servers(pd.DataFrame({'CPU Description': ['Intel Ghz']}))
    # should not raise an exception
    Servers(pd.DataFrame({'CPU Description': ['Intel']}))
