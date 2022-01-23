# sqlalchemy-challenge

## Step 1 - Climate Analysis

After importing the required libraries, we create a DB reflection by using "Base = automap_base()" followed by "Base.prepare(engine.reflect=True)".

We view the classes and see 'measurement' and 'station', and store both classes into their own variables to call later. We then open a session link.

To understand the design of the "measurement" we did a query of the first row. Then used the "order_by & desc" functions on 'date' to find the most recent date in the dataset.

### Precipitation Analysis

Using the 'datetime' library, we determined the year back from the most recent date, then queried all the data, applying a fliter to ensure that the dates fell within the year long range. This data was placed into a Pandas DataFrame and then plotted to show how much precipitation there was on each day over the year. We also performed the .describe() function on the DataFrame to calculate summary statistics.

### Station Analysis

To determine the number of stations in the dataset, we performed a "group_by & count()" function on the "station" column in the 'measurement' dataset.

To list and find the most active station, we queried both the station id's and counted each occurrence of a station id in the dataset, using the func.count function, then grouped_by the station ids and ordered_by the func.count values desc.

To store the most active station ID, rather than ending the above function with "all()" we changed it to "first()", then did a session execute and scalar function to store just the name rather than a tuple.

We then created variables for the lowest, highest, and average temperature values, then ran a single session query using the func.min,func.max and func.avg functions respectively, then applied a filter to "station" to ensure that it matches out most active station.

We then used the same time period as we did in "Precipitation Analysis" to gather the TOBS data from the last 12 months, and plotted it into a histogram with bins=12.

The session was then closed.

## Step 2 - Climate App

### Routes
#### /
Created a home route that lists all the other routes that are available, and what they return

#### /api/v1.0/precipitation
Queried the database to find the date and corresponding precipitation amount out of the 'measurement' class, for final year available in the dataset. This data is unpacked into a list to be JSONified, using a for loop that pulls the corresponding date and prcp values from the tuples.

#### /api/v1.0/stations
Queried the database to pull each station name from the "Station" class. The list of names is then converted from a tuple into a regular list, which is JSONified.

#### /api/v1.0/tobs
Similar to the precipitation activity, however it queries the date and corresponding tobs value from 'measurement' class, and adds the filter of the most active station. Which is found using the same code we used in Step 1.

#### /api/v1.0/<start>
We query the 'measurement' class and perform the func.min,func.avg and func.max functions on the 'tobs' values, and filter by the given start date, providing all values from the start to the end of the dataset. Similar to previous routes, the data is unpacked into a list using a for loop, then JSONified

#### /api/v1.0/<start>/<end>
Same as last route, with added filter for the input end date, for which the data is pulled from between the start and end date given.