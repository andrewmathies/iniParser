# Parsing data from inis
Python

- read ini file text
- run regex
- convert to maps 
    - PhysicalProperties => model
    - Communication => addresses
    - RelayMap => relays

# Building the database
Python, pscygopg2

### create table
    - appliance
    - ui type
    - cooktop type
    - model
    - address
    - relay
    
where appliance, ui type, and cooktop types are serving as enums for values in model
one modelid, shared between model, address, and relay

### insert
fill enum tables as values are found
one ini file contains one model

# Future goals
- Labview code that will call this on each ini file and fill the database
- Labview client code to make SQL select join commands on db
