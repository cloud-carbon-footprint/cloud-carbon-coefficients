import io
import re

import pandas as pd
import requests

# Search parameters are at the end of this file.
SPEC_FETCH_SEARCH_URL = 'https://www.spec.org/cgi-bin/osgresults?'


def compose_url():
    parameters = '&'.join(SPEC_FETCH_PARAMS.split('\n')[1:-1])
    return SPEC_FETCH_SEARCH_URL + parameters


def fetch_spec_results():
    result = requests.get(compose_url())
    if result.status_code != 200:
        raise ValueError(f'Failed to fetch spec results {result.status_code}')
    return io.BytesIO(result.content)


def spec_results():
    df = pd.read_csv(fetch_spec_results())

    # Remove whitespace from column names
    df.columns = df.columns.str.strip()

    # Remove 'Disclosures' column which cannot be removed through parameters request
    df.drop(['Disclosures'], axis=1, inplace=True)

    # Rename columns to the names used in the original notebook
    df.rename(columns={
        '# Chips': 'Chips',
        'Memory (GB)': 'Total Memory (GB)',
        'Average watts @ active idle': 'avg. watts @ active idle',
        'Average watts @ 100% of target load': 'avg. watts @ 100%',
        'Processor': 'CPU Description',
    }, inplace=True, errors='raise')

    # Remove any row which the 'Chips' is 0, which means that
    # later we will divide by 0 when calculating the average watts because
    # 'Total Threads' will be 0
    df = df[df['Chips'] != 0]

    # Remove all results that are non-compliant, in the CSV format this is
    # represented by a '0' in the 'Result' column
    df = df[df['Result'] != 0]

    # Memory information comes with some HTML links, remove them
    df['Total Memory (GB)'] = df['Total Memory (GB)'].str.extract(r'(\d+)').astype(int)

    # 'Total Threads' shows up on the website, but not in the CSV so we need to calculate it
    df['Total Threads'] = df['Chips'] * df['# Threads Per Core'] * df['# Cores Per Chip']

    # Remove any row which the ratio between idle power and threads is too high
    # We spotted some outliers with this ratio being 200+
    filter_ratio = 100
    df = df[df['avg. watts @ active idle'] / df['Total Threads'] < filter_ratio]

    # Clean the processor description so that it can be matched later against
    # the CPU families
    df['CPU Description'] = df['CPU Description'].apply(clean_server_data)

    return df


def clean_server_data(cpu_desc):
    # Remove text following '@'
    cpu_desc = cpu_desc.split('@')[0].strip()

    # Remove parenthesis containing 'GHz'
    cpu_desc = re.sub(r'\(.*GHz.*\)', '', cpu_desc).strip()

    # Remove any string containing 'GHz'
    cpu_desc = re.sub(r'\w+\.\w+', '', cpu_desc).strip()

    # Remove any string containing 'GHz', 'Ghz', or 'ghz'
    cpu_desc = ' '.join(
        [x for x in cpu_desc.split() if not re.search(r'Ghz', x, re.IGNORECASE)])
    return cpu_desc


'''
The following is all parameters used in the search form of SPEC website. 
Strangely enough, omitting entries with =0 will sometimes fetch them anyway. While
this is not a big problem we try to keep the file small and manageable if needs
to be inspected manually.

To check what the parameters means, create the URL and replace
'format=csvdump' with just 'format=csv' SPECpower website will
show the form and the parameters selected.
'''
SPEC_FETCH_PARAMS = '''
conf=power_ssj2008
op=fetch
proj-BMKVERS=0
proj-COMPANY=256
proj-SYSTEM=256
proj-NODES=0
proj-FORMFACTOR=0
proj-TESTMETHOD=0
proj-PEAK=256
proj-OPSAT100=0
proj-OPSAT90=0
proj-OPSAT80=0
proj-OPSAT70=0
proj-OPSAT60=0
proj-OPSAT50=0
proj-OPSAT40=0
proj-OPSAT30=0
proj-OPSAT20=0
proj-OPSAT10=0
proj-WATTSAT100=256
proj-WATTSAT90=0
proj-WATTSAT80=0
proj-WATTSAT70=0
proj-WATTSAT60=0
proj-WATTSAT50=0
proj-WATTSAT40=0
proj-WATTSAT30=0
proj-WATTSAT20=0
proj-WATTSAT10=0
proj-WATTSATAA=256
proj-PPAT100=0
proj-PPAT90=0
proj-PPAT80=0
proj-PPAT70=0
proj-PPAT60=0
proj-PPAT50=0
proj-PPAT40=0
proj-PPAT30=0
proj-PPAT20=0
proj-PPAT10=0
proj-CORES=0
proj-CHIPS=256
proj-CORESCHP=256
proj-THREADS=256
proj-CPU=256
proj-CPU_MHZ=256
proj-CPUCHAR=0
proj-NCPUORD=0
proj-CACHE1=0
proj-CACHE2=0
proj-CACHE3=0
proj-OCACHE=0
proj-MEMORY=256
proj-OS=0
proj-OSVERS=0
proj-FS=0
proj-DIMMS=0
proj-MEMDESC=0
proj-NETCTRL=0
proj-NCTRLCON=0
proj-NCTRLFRM=0
proj-NCTRLOS=0
proj-NETSPEED=0
proj-JVMVENDOR=0
proj-JVMVERS=0
proj-JVMINST=0
proj-JVMAFF=0
proj-JVMBIT=0
proj-JVMOPT=0
proj-HEAPINI=0
proj-HEAPMAX=0
proj-SOURCE=0
proj-DESIGNATION=0
proj-PROVISION=0
proj-DISK=0
proj-DISKCTL=0
proj-PWRMAN=0
proj-PSUDESC=0
proj-PSUINSTALL=0
proj-PSURATE=0
proj-HWAVAIL=0
crit2-HWAVAIL=Jan
proj-SWAVAIL=0
crit2-SWAVAIL=Jan
proj-LICENSE=0
proj-TESTER=0
proj-SPONSOR=0
proj-TESTDAT=0
crit2-TESTDAT=Jan
proj-PUBLISH=0
crit2-PUBLISH=Jan
proj-UPDATE=0
crit2-UPDATE=Jan
proj-FDRURL=0
dups=1
duplist=COMPANY
duplist=SYSTEM
duplist=FORMFACTOR
duplist=TESTMETHOD
duplist=CORES
duplist=CHIPS
duplist=CORESCHP
duplist=THREADS
duplist=CPU
duplist=CPU_MHZ
duplist=CPUCHAR
duplist=NCPUORD
duplist=CACHE1
duplist=CACHE2
duplist=CACHE3
duplist=OCACHE
duplist=MEMORY
duplist=OSVERS
duplist=FS
duplist=DIMMS
duplist=MEMDESC
duplist=NETCTRL
duplist=NCTRLCON
duplist=NCTRLFRM
duplist=NCTRLOS
duplist=NETSPEED
duplist=JVMVERS
duplist=HEAPINI
duplist=HEAPMAX
duplist=SOURCE
duplist=DESIGNATION
duplist=PROVISION
duplist=DISK
duplist=DISKCTL
duplist=PWRMAN
duplist=PSUDESC
duplist=PSUINSTALL
duplist=PSURATE
duplist=HWAVAIL
duplist=SWAVAIL
duplist=LICENSE
duplist=UPDATE
dupkey=PUBLISH
latest=Dec-9999
sort1=COMPANY
sdir1=1
sort2=SYSTEM
sdir2=1
sort3=PSURATE
sdir3=1
format=csvdump
'''
