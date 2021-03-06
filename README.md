# Tour-Scheduler
Algorithm to schedule tours based on tour guide availability.

## Usage
This program was created to automate tour scheduling to assist current and future Head Engineering Guides. Using the availibilites and day preferences of the tour guides, the algorithm assigns guides to tours with even distribution.

### Input
Follow the prompts:
 - Google Forms spreadsheet exported as a comma-delimited csv file
 - Columns of the csv to drop
 - The names of the Head Guides
 - Max number of tours to assign to the Head Guides
 - Number of weeks to schedule for
 - Number of guides for each tour

### Output
A schedule with the guides assigned to each day is outputted.

### Factors
When deciding who to assign to a tour on a given day, weight is given to (1) guides that have not yet been paired up for a tour prior to that point in the program and (2) guides who, at that point in the program, have been assigned to fewer tours than their peers.

## Other Applications
This algoirthm can be generalized to scheduling shifts of any kind.
