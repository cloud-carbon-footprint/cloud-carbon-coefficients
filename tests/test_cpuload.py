import ccfcoef.cpu_load as cpu_load


def test_load_check():
    cpus_amd_epyc_gen1 = cpu_load.load_append_list('amd-epyc-gen1.csv')
    assert 'EPYC 7601' in cpus_amd_epyc_gen1
    cpus_amd_epyc_gen2 = cpu_load.load_append_list('amd-epyc-gen2.csv')
    assert 'EPYC 7742' in cpus_amd_epyc_gen2
    cpus_amd_epyc_gen3 = cpu_load.load_append_list('amd-epyc-gen3.csv')
    assert 'EPYC 75F3' in cpus_amd_epyc_gen3
    cpus_intel_sandybridge = cpu_load.load_append_list('intel-sandybridge.csv')
    assert 'E5-4610' in cpus_intel_sandybridge
    cpus_intel_ivybridge = cpu_load.load_append_list('intel-ivybridge.csv')
    assert 'E5-2609 v2' in cpus_intel_ivybridge
    cpus_intel_haswell = cpu_load.load_append_list('intel-haswell.csv')
    assert 'E5-2630 v3' in cpus_intel_haswell
    cpus_intel_broadwell = cpu_load.load_append_list('intel-broadwell.csv')
    assert 'E5-2683 v4' in cpus_intel_broadwell
    cpus_intel_skylake = cpu_load.load_append_list('intel-skylake.csv')
    assert 'Platinum 8160T' in cpus_intel_skylake
    cpus_intel_cascadelake = cpu_load.load_append_list('intel-cascadelake.csv')
    assert 'Gold 6230R' in cpus_intel_cascadelake
    cpus_intel_coffeelake = cpu_load.load_append_list('intel-coffeelake.csv')
    assert 'E-2246G' in cpus_intel_coffeelake
