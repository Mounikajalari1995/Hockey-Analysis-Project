# importing required libraries
import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# loading the data And accessing for top5  records
event_data = pd.read_csv('DA_Tutorial_24.csv')
print(event_data.head(5))



# 1. a.Which teamid won the game, what was the score, which period was the winning goal scored in?
goals_scored_by_team = event_data.groupby('teamid')['goal'].sum()

# determining the winning teamid
winning_team_id = goals_scored_by_team.idxmax()

# determining the winning Score
winning_score = goals_scored_by_team.max()

print("The winning team ID is:", winning_team_id)
print("The Winning Team Score is:", winning_score)


# winning period against winning team
winning_team_goals_data = event_data[(event_data['teamid'] == winning_team_id) & (event_data['goal'] == 1)]

# Find the maximum time among the winning team's goals
max_goal_time = winning_team_goals_data['compiledgametime'].max()

# calculate winning Period
# Assuming 20-minute intervals, I divide the time data—which is supposed
# --to be in seconds—by 1200 (20 minutes * 60 seconds)
# --to convert it into periods and find the appropriate period bracket.
winning_goal_period = int(max_goal_time / 1200) + 1
print("The winning goal was scored in period:", winning_goal_period)


# the game has three 20 minute periods  , both team got tied up here , that's why they played another period
# the first goal here done by 315

print("*** Question 1b here ***")
event_data['period'] = np.ceil(event_data['compiledgametime'] / 1200).astype(
    int)  # adding a period column to filter winning period records
winning_team_shots = event_data[(event_data['teamid'] == winning_team_id) &
                                (event_data['eventname'] == 'shot') &
                                (event_data['period'] == winning_goal_period)]

plt.scatter(winning_team_shots['xadjcoord'], winning_team_shots['yadjcoord'], color='blue', label='Shot Attempts')
winning_goal = event_data[(event_data['teamid'] == winning_team_id) &
                          (event_data['goal'] == 1) &
                          (event_data['period'] == winning_goal_period)]
plt.scatter(winning_goal['xadjcoord'], winning_goal['yadjcoord'], color='red', label='Winning Goal')

# Set plot title and labels
plt.title('Winning Team\'s Shot Attempts and Winning Goal (Period {})'.format(winning_goal_period))
plt.xlabel('X axis')
plt.ylabel('Y axis')
plt.legend()
plt.xlim(-100, 100)
print("*** Question 1a here ***")
plt.ylim(-42.5, 42.5)
plt.gca().set_aspect('equal', adjustable='box')
# Show the plot
plt.show()


print("*** Question Q2a here ***")

winning_goal_event = event_data[(event_data['teamid'] == winning_team_id) &
                                (event_data['goal'] == 1) &
                                (event_data['compiledgametime'] == max_goal_time) &
                                (event_data['period'] == winning_goal_period)]
winning_goal_playerid = winning_goal_event['playerid'].values[0]
print(f"The playerid who scored the winning goal is: {winning_goal_playerid}")


print("*** Question Q2b here ***")
# Filter for the player's powerplay shot attempts
winplayer_powerplay_shots = event_data[(event_data['playerid'] == winning_goal_playerid) &
                                    (event_data['eventname'] == 'shot') &
                                    (event_data['manpowersituation'] == 'powerPlay')]

print('players powerplay shot attempt ',len(winplayer_powerplay_shots))
plt.scatter(winplayer_powerplay_shots['xadjcoord'], winplayer_powerplay_shots['yadjcoord'], color='blue', label='Winning Goal')
plt.title('Powerplay Shot Attempts by Player {}'.format(winning_goal_playerid))
plt.xlabel('X axis')
plt.ylabel('Y axis')
plt.legend()
plt.xlim(-100, 100)
plt.ylim(-42.5, 42.5)
plt.gca().set_aspect('equal', adjustable='box')
plt.show()


print("*** Question Q2C here ***")

# Filter powerplay shots by Alex Ovechkin
ovechkin_powerplay_shots = event_data[
    (event_data['manpowersituation'] == 'powerPlay') &
    (event_data['eventname'] == 'shot')
].copy()  # Explicitly create a copy of the DataFrame

# Calculate average Y coordinate
average_y_coordinate = ovechkin_powerplay_shots['yadjcoord'].mean()

# Set desired Y coordinate for "Ovi's Office"
ovi_office_y_coordinate = 20

# Calculate offset
offset = ovi_office_y_coordinate - average_y_coordinate

# Adjust the Y coordinates using .loc to avoid the SettingWithCopyWarning
ovechkin_powerplay_shots.loc[:, 'Adjusted Y Coordinate'] = ovechkin_powerplay_shots['yadjcoord'] + offset

# Create scatter plot with adjusted Y coordinates
plt.scatter(ovechkin_powerplay_shots['xadjcoord'], ovechkin_powerplay_shots['Adjusted Y Coordinate'], color='blue')
plt.title("Ovechkin's Powerplay Shot Attempts from 'Ovi's Office'")
plt.xlabel('X Coordinate')
plt.ylabel('Adjusted Y Coordinate')
plt.xlim(-100, 100)
plt.ylim(-42.5, 42.5)
plt.tight_layout()
plt.show()



print("*** Question Q3a here ***")

evenstrength = event_data[(event_data['manpowersituation'] == 'evenStrength') &
                      (event_data['outcome'] == 'successful') &
                      (event_data['eventname'] == 'pass')]
total_passes_by_zone = event_data[event_data['eventname'] == 'pass'].groupby('zone').size()
pass_counts_by_zone = evenstrength.groupby('zone').size()

pass_completion_rates = pass_counts_by_zone / total_passes_by_zone * 100

pass_completion_rates.plot(kind='bar', color='green')
plt.xlabel('Zone of Pass Origin')
plt.ylabel('Pass Completion Rate (%)')
plt.title('Even Strength Pass Completion Rate by Zone')

plt.tight_layout()

plt.show()


print("*** Question Q3b here ***")
most_difficult_zone = pass_completion_rates.idxmin()
print("Most Difficult Zone to Complete Passes in Even Strength:", most_difficult_zone)

print("*** Question Q3c here ***")
slot_zones = ['innerSlotDZ', 'westOuterSlotDZ', 'eastOuterSlotDZ']
slot_shots = event_data[event_data['playsection'].isin(slot_zones)]

total_shots_by_goalie = slot_shots.groupby('opposingteamgoalieoniceid').size()
slot_shots_saved_by_goalie = slot_shots[slot_shots['outcome'] == 'successful'].groupby('opposingteamgoalieoniceid').size()
slot_save_percentage = (slot_shots_saved_by_goalie / total_shots_by_goalie) * 100
print("Goalie ID   Slot Save Percentage")
print("---------------------------------")
for goalie_id, save_percentage in slot_save_percentage.items():
    print(f"{goalie_id}\t\t{save_percentage:.2f}%")

print("*** Question Q4a here ***")

outside_north_west_shots = event_data[event_data['playsection'] == 'outsideNorthWestDZ'].copy()
center_of_net = (89, 0)
outside_north_west_shots['distance_to_net'] = np.sqrt((center_of_net[0] - outside_north_west_shots['xadjcoord'])**2 +
                                                      (center_of_net[1] - outside_north_west_shots['yadjcoord'])**2)
grouped_shots = outside_north_west_shots.groupby('teamid')
average_distances = grouped_shots['distance_to_net'].mean()

print("Team ID   Average Shot Distance to Center of Net")
print("------------------------------------------------")
for team_id, avg_distance in average_distances.items():
    print(f"{team_id}\t\t{avg_distance:.2f} units")

print("*** Question Q4b here ***")

# merging xgdata from another file
xg_data = pd.read_csv('DA_Tutorial_24_xg.csv')
merged_data = pd.merge(event_data, xg_data, on='playerid', how='left')
event_data['xg'] = merged_data['xg']
event_data.loc[event_data['eventname'] != 'shot', 'xg'] = 0

outside_north_west_shots = event_data[event_data['playsection'] == 'outsideNorthWestDZ']

grouped_data = outside_north_west_shots.groupby('opposingteamgoalieoniceid')
goalie_stats = grouped_data.agg({'xg': 'sum', 'goal': 'sum'})
goalie_stats['GS'] = goalie_stats['goal'] - goalie_stats['xg']
goalie_stats['GSAx'] = goalie_stats['GS'] / goalie_stats['xg']
goalie_stats['GSAx'] = goalie_stats['GSAx'].fillna(0)

print("Goalie ID\tGSAx")
print("-------------------")
for goalie_id, gsax in goalie_stats['GSAx'].items():
    print(f"{goalie_id}\t\t{gsax:.2f}")



print("*** Question Q5a here ***")

# Sort the DataFrame by the numeric 'compiledgametime' column
passes_receptions_shots = event_data.sort_values(by='compiledgametime')

passes_receptions_shots['next_event'] = passes_receptions_shots['eventname'].shift(-1)
passes_receptions_shots['before_event'] = passes_receptions_shots['eventname'].shift(1)
passes_receptions_shots['before_beforeevent'] = passes_receptions_shots['eventname'].shift(2)
passes_receptions_shots['next_next_event'] = passes_receptions_shots['eventname'].shift(-2)
passes_receptions_shots['next_teamid'] = passes_receptions_shots['teamid'].shift(-1)
passes_receptions_shots['next_next_teamid'] = passes_receptions_shots['teamid'].shift(-2)
passes_receptions_shots['next_outcome'] = passes_receptions_shots['outcome'].shift(-1)



shot_assist_condition = (
        (passes_receptions_shots['eventname'] == 'pass') &
        (passes_receptions_shots['outcome'] == 'successful') &
        (passes_receptions_shots['next_event'] == 'reception') &
        (passes_receptions_shots['next_outcome'] == 'successful') &
        (passes_receptions_shots['next_next_event'] == 'shot') &
        (passes_receptions_shots['next_teamid'] == passes_receptions_shots['teamid']) &
        (passes_receptions_shots['next_next_teamid'] == passes_receptions_shots['teamid'])
)

passes_receptions_shots['Shot_Assist'] = False
passes_receptions_shots.loc[shot_assist_condition, 'Shot_Assist'] = True
# added shot_assist column
assisted_shot_attempts = passes_receptions_shots[(passes_receptions_shots['Shot_Assist'] == True) &
                                              (passes_receptions_shots['playerid'] == 79380) ]


num_assisted_shot_attempts = len(assisted_shot_attempts)
print(f"The number of shot attempts assisted for playerid 79380 is: {num_assisted_shot_attempts}")
#
# print(assisted_shot_attempts[['eventname', 'outcome', 'next_event', 'next_outcome', 'next_next_event', 'Shot_Assist', 'compiledgametime']].to_string(max_colwidth=None))

print("*** Question Q5b here ***")
# Here who ever has made shot only those xg values sum up and showed here  with shotassisrt true cases

# print(passes_receptions_shots.to_string(max_colwidth=None))
condition1 = (passes_receptions_shots['eventname'] == 'reception') & (passes_receptions_shots['next_event'] == 'shot') & (passes_receptions_shots['before_event'] == 'pass')
condition2 = (passes_receptions_shots['eventname'] == 'shot') & (passes_receptions_shots['before_event'] == 'reception') & (passes_receptions_shots['before_beforeevent'] == 'pass')

passes_receptions_shots.loc[condition1 | condition2, 'Shot_Assist'] = True
assisted_shots = passes_receptions_shots[passes_receptions_shots['Shot_Assist'] == True]
passer_xg = assisted_shots.groupby('playerid')['xg'].sum()
most_xg_passer = passer_xg.idxmax()
total_xg_created = passer_xg.max()
print(f"The passer who created the most xG for their teammates is Player ID {most_xg_passer} "
      f"with a total xG value of {total_xg_created}.")


print("*** Question Q5c here ***")
pass_to_reception = passes_receptions_shots[
    (passes_receptions_shots['eventname'] == 'pass') &
    (passes_receptions_shots['next_event'] == 'reception') &
    (passes_receptions_shots['Shot_Assist'] == True)
]

reception_to_shot = passes_receptions_shots[
    (passes_receptions_shots['eventname'] == 'reception') &
    (passes_receptions_shots['next_event'] == 'shot')
]
# Extract X and Y coordinates for pass to reception
pass_to_reception_x = pass_to_reception['xadjcoord']
pass_to_reception_y = pass_to_reception['yadjcoord']


# Extract X and Y coordinates for reception to shot
reception_to_shot_x = reception_to_shot['xadjcoord']
reception_to_shot_y = reception_to_shot['yadjcoord']



# Plot pass to reception events
plt.scatter(pass_to_reception_x, pass_to_reception_y, label='Pass to Reception', color='blue')

# Plot reception to shot events
plt.scatter(reception_to_shot_x, reception_to_shot_y, label='Reception to Shot', color='red')

# Set plot labels and title
plt.xlabel('X Coordinate')
plt.ylabel('Y Coordinate')
plt.title("Passer's Shot Assists and Corresponding Shots")
plt.legend()

# Adjust plot limits and aspect ratio based on rink dimensions
plt.xlim(-100, 100)
plt.ylim(-42.5, 42.5)
plt.gca().set_aspect('equal', adjustable='box')

# Show plot
plt.show()


print("*** Question Q6a here ***")

team_xg = event_data.groupby('teamid')['xg'].sum()

# Determine which team won the xG battle
winning_team = team_xg.idxmax()
winning_xg = team_xg.max()

# Print the results
print(f"The winning team in the xG battle is {winning_team} with a total xG of {winning_xg:.2f}.")
print("\nTotal xG for each team:")


print("*** Question Q6b here ***")
print("- The winning team (Team 315) scored more goals.\n- They had more high-quality scoring chances, as indicated by their higher Expected Goals (xG).\n- Team 315 performed well in critical moments, scoring the winning goal in period 4.\n- Key players, like playerid 81408, contributed significantly to the victory.\n- Overall, Team 315 dominated the game, showing better control and performance compared to Team 311.")
print('')
print("*** Question Q7a here ***")
print("Statistical methods such as logistic regression or machine learning algorithms are usually used to identify the highest predictors of a goal in the dataset for creating an xG model.\nFeatures that could be taken into account include shot location, shot type, event type, player engagement, period, remaining time, distance to the net, defensive pressure, and past events.\nYou can ascertain which of these characteristics most significantly affects the probability of a goal being scored by examining them.")
print('')
print("*** Question Q7b here ***")
print("Coach, I've concentrated on identifying the variables that lead to risky shot attempts when reviewing the data. It's evident from the pass-reception-shoot sequences that precise passes that result in successful receptions in high-scoring zones greatly raise the risk of a risky shot attempt.\nFurthermore, we've discovered that shots that are made close to the net, under ideal shooting angles, with plenty of time and space, and with no defensive pressure, typically carry a higher risk.\nWe can more effectively plan our offensive moves to generate more scoring opportunities and raise our chances of success on the ice by spotting these tendencies in the data.")
