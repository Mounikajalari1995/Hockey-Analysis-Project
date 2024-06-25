# Hockey Analytics Data Analysis

## Introduction
This repository contains Python scripts for analyzing hockey game data using pandas, numpy, and matplotlib libraries. The dataset includes event-level details from a hockey game, focusing on shot attempts, goals, player statistics, and Expected Goals (xG) values.

## Files
- **DA_Tutorial_24.csv**: Contains detailed event data from a hockey game.
- **DA_Tutorial_24_xg.csv**: Includes xG values associated with shot attempts.

## Requirements
To run the scripts, ensure you have Python 3.x installed along with the following libraries:
- pandas
- numpy
- matplotlib

## Analysis Overview
### 1. Determining Game Outcome
- **Question 1a**: Identifies the winning team and their score.
- **Question 1b**: Plots shot attempts by the winning team in the period of the winning goal, highlighting the goal.

### 2. Player Analysis
- **Question 2a**: Identifies the player who scored the winning goal.
- **Question 2b**: Plots powerplay shot attempts for the player who scored the winning goal.
- **Question 2c**: Adjusts shot attempt coordinates for a player (simulated as Alex Ovechkin) to "Ovi's Office".

### 3. Team Performance Metrics
- **Question 3a**: Visualizes even strength pass completion rates by zone.
- **Question 3b**: Analyzes the most challenging zone for pass completions.
- **Question 3c**: Calculates slot save percentage for each goalie.

### 4. Shot Analysis
- **Question 4a**: Calculates average shot distance for each team to the center of the net from outside the north-west play section.
- **Question 4b**: Determines Goals Saved Above Expected (GSAx) for each goalie from the outside north-west play section.

### 5. Shot Assist and xG Creation
- **Question 5a**: Identifies shot attempts assisted for a specific player.
- **Question 5b**: Determines which player created the most xG through shot assists.
- **Question 5c**: Plots shot assists (pass to reception) and corresponding shots (reception to shot).

### 6. xG Battle and Game Analysis
- **Question 6a**: Determines which team won the xG battle and their xG total.
- **Question 6b**: Provides insights into the game outcome based on xG and goals scored.

### 7. Predictors of Goal
- **Question 7a**: Uses statistical techniques to identify predictors of a goal (for xG model creation).
- **Question 7b**: Discusses findings and insights from the analysis relevant to coaching strategy.

## How to Use
1. Clone the repository to your local machine.
2. Ensure Python and required libraries are installed.
3. Run the Python scripts to perform analysis and generate visualizations.

## Conclusion
This project provides detailed insights into hockey game dynamics through statistical analysis and visualization of event data. The findings can be used to understand team performance, player contributions, and factors influencing goal scoring probabilities in hockey games.
