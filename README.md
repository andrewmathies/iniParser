generic ERD reader/writer with controls of useful types

I can type the name of an ERD
    after each input, run a regex through each string in the approved ERD list
    accumulate a list of the first n that match
    display a list of those n ERDs with the matched characters bolded

I can select an ERD from the list or press the search button
    retrieve the ERD name that was selected or searched for
    get a map of field names to types for each field of the ERD
    if any field names are in the map of adapters, then add controls with the values from that map to the map of field names to types
    grab references to controls of the correct type for each value in the map of field names
    set them to visible
    set their position in a vertical list with consistent spacing
    set their captions as the ERD name . field name (in the case of adapters do ERD name. field name. adapter ?)

I can press a button to read from those ERDs
    hex strings for ERDs are retrieved from FGV
    read command is sent on GEA bus with hex strings
    get a response on bus
    parse response via JSON
    adapter layer converts some of the response
    the controls are populated with converted data

I can press a button to write to those ERDs
    the values in the controls of the correct types are collected and mapped to labels
    adapter layer converts values in assigned controls to hidden controls
    convert data to hex string
    write command is sent on GEA bus with converted data