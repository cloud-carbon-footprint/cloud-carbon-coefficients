# https://www.cloudcarbonfootprint.org/docs/methodology#memory
MEMORY_COEFFICIENT = 0.000392 # kWh / Gb

# Manufacturing emissions for a mono socket, low DRAM, no local storage 
# commodity rack server
BASE_MANUFACTURING_EMISSIONS = 1000 # kgCO2eq

# Commodity rack server lifespan
RACK_SERVER_LIFESPAN = 4 # years

# Hourly manufacturing emissions conversion factor - linearly amortised
MANUFACTURING_EMISSIONS = BASE_MANUFACTURING_EMISSIONS / RACK_SERVER_LIFESPAN / 12 / 30 / 24 # gCO2eq/hour

# DRAM Threshold to unlock additional Scope 3 emissions
DRAM_THRESHOLD = 16 # GB

# Manufacturing emissions for the threshold DRAM amount
# Based on Dell PowerEdge R740 Life-Cycle Assessment
# https://docs.google.com/spreadsheets/d/1YhtGO_UU9Hc162m7eQKYFQOnV4_yEK5_lgHYfl02JPE/edit#gid=954946016
# = 533 kgCO₂eq for 12*32GB DIMMs Memory (384 GB).
DRAM_MANUFACTURING_EMISSIONS = (533 / 384) * DRAM_THRESHOLD

# Manufacturing emissions per additional CPU
CPU_MANUFACTURING_EMISSIONS = 100 # kgCO2eq

# Manufacturing emissions per additional HDD
HDD_MANUFACTURING_EMISSIONS = 50 # kgCO2eq

# Manufacturing emissions per additional SSD
SSD_MANUFACTURING_EMISSIONS = 100 # kgCO2eq

# Manufacturing emissions per additional GPU Card
GPU_MANUFACTURING_EMISSIONS = 150 # kgCO2eq
