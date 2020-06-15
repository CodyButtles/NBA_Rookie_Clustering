# NBA_Rookie_Clustering

## Overview
This project focuses on attempting to evaluate NBA players' rookie season performance. I look at every player's rookie season stats going back to the 1979-1980 NBA season and compare them against each other to see the best and worst of rookie players for the past 40 years. There are some interesting questions this may be able to answer.... Which NBA players were the best rookies? How good was the very hyped Zion Williamson? Which NBA players were the most similar to each other as rookies? Do certain clusters of players show a trend that could be used for future predictions or career projections? Some of the results may surprise you.

## Resources Used
-Python with Spyder IDE.
-Tableau
-Basketball Reference

## Methodology
The steps I took to complete this project included web scraping multiple pages on Basketball Reference to create a dataset. I scraped NBA rookie season stats, per 36 min stats, and the advanced stats. I then joined the names and age from each rookie season with the statistics that matched those players in the per 36 and advanced stats pages. This dataset is the All_Rookies csv in this repository.

Once I had all the data put together I kept rookies that played more then 9 games in their rookie season and then rookies that played more than 90 total minutes. This dataset is the Kept_Rookies csv that is in this repository. At this point I have 45 columns that represent different statistics for each players performance and then 4 columns describing the player which includes their name, team, age, and position.





