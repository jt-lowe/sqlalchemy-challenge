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