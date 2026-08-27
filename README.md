1. CSV Data Extraction

The csv library and csv.DictReader are used to read the depth values and point numbers from the provided CSV file.

2. Error Handling with Try/Except

A try/except block is used when converting depth readings into numbers, Because there is an invalid reading ##VALUE in the csv.

3. Lists for Data Storage

Lists are used throughout the program to store and organise data, including:

depth_data – valid depth readings
invalid_points – readings that could not be processed
suspicious_points – possible sensor errors/outliers
clean_data – data after suspicious readings are removed
smoothed_data – data after noise reduction
shallow_zone – points close to the shallowest area
rapid_changes – locations with rapid depth changes
4. Noise Cleaning


5.Suspicious Points: The program checks each reading against the readings immediately before and after it. If a reading differs from both neighbouring readings by more than 100 m, it is marked as suspicious. These points are then removed from the dataset before smoothing, helping prevent unusual sensor errors from affecting the final graph.

6.To reduce random sensor noise, the program uses a 5-reading moving average-which smooths out the graph 

The program also detects suspicious readings by comparing each reading with its neighbouring values and removes them before smoothing.

These are the limits and warning considered:
SAFE	Deepest/safest condition	Continue navigation
CAUTION	:Above -80 m	Monitor depth closelyWARNING	:Above -50 m	Reduce speed and prepare to change course
DANGER:	Above -20 m	Stop and change course immediately




I could not complete the second task code but i did make the circuit:(((

The Tinkercad circuit was designed using an Arduino, LCD, light sensor, PING))) distance sensor, push button, LED, and buzzer. The circuit wiring is included in circuit.png.
