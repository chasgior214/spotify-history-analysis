import pandas as pd
import matplotlib.pyplot as plt
plt.style.use('dark_background')

# Read the csv
df = pd.read_csv('all_data.csv')

# filter out songs that were played for less than 30 seconds
df = df[df['ms_played'] > 30000]

# Define some functions
def ms_played_to_minutes(df):
    df['minutes_played'] = df['ms_played'] / 1000 / 60
    return df
def ms_played_to_hours(df):
    df['hours_played'] = df['ms_played'] / 1000 / 60 / 60
    return df
def filter_by_artist(df, artist):
    return df[df['master_metadata_album_artist_name'] == artist]
def filter_by_track(df, track):
    return df[df['master_metadata_track_name'] == track]
# add a conversion for time to EST

# Count the ms_played by artist
df_artist = df.groupby('master_metadata_album_artist_name')['ms_played'].sum().reset_index()
df_artist = df_artist.sort_values('ms_played', ascending=False)
# convert ms_played to hours
df_artist = ms_played_to_hours(df_artist)
print('\nMost listened to artists:')
print(df_artist.head())

# plot the top 10 artists
plt.bar(df_artist['master_metadata_album_artist_name'][:10], df_artist['hours_played'][:10])
plt.ylabel('Hours Played')
plt.title('Top 10 Artists')
plt.show()

# Count the ms_played by track
df_track = df.groupby('master_metadata_track_name')['ms_played'].sum().reset_index()
df_track = df_track.sort_values('ms_played', ascending=False)
# convert ms_played to hours
df_track = ms_played_to_hours(df_track)
print('\nMost listened to tracks:')
print(df_track.head())

# plot the top 10 tracks
plt.bar(df_track['master_metadata_track_name'][:10], df_track['hours_played'][:10])
plt.ylabel('Hours Played')
plt.title('Top 10 Tracks')
plt.show()


# filter to 2023 only
df_2023 = df[df['ts'].str[0:4] == '2023']

# Count the ms_played by artist
df_artist_2023 = df_2023.groupby('master_metadata_album_artist_name')['ms_played'].sum().reset_index()
df_artist_2023 = df_artist_2023.sort_values('ms_played', ascending=False)
# convert ms_played to hours
df_artist_2023 = ms_played_to_hours(df_artist_2023)
print('\nMost listened to artists in 2023:')
print(df_artist_2023.head())

# plot the top 10 artists
plt.bar(df_artist_2023['master_metadata_album_artist_name'][:10], df_artist_2023['hours_played'][:10])
plt.ylabel('Hours Played')
plt.title('Top 10 Artists in 2023')
plt.show()

# Plot how much time was spent listening to a specific artist each month from the entire dataset
# filter to specific artist
artist_name = 'Sara Kays'
df_artist = df[df['master_metadata_album_artist_name'] == artist_name]

# Count the ms_played by month
df_artist['month'] = df_artist['ts'].str[0:7]
df_artist_month = df_artist.groupby('month')['ms_played'].sum().reset_index()
# convert ms_played to hours
df_artist_month = ms_played_to_hours(df_artist_month)
print(f'\nTime spent listening to {artist_name} each month:')
print(df_artist_month.head())

# plot time spent listening to a specific artist each month
plt.plot(df_artist_month['month'], df_artist_month['hours_played'])
plt.ylabel('Hours Played')
plt.xticks(rotation=90)
plt.title(f'Time Spent Listening to {artist_name} Each Month')
plt.show()

# Filter to a specific track
track_name = "I'm with You"
df_track = df[df['master_metadata_track_name'] == track_name]

# Count the ms_played by month
df_track['month'] = df_track['ts'].str[0:7]
df_track_month = df_track.groupby('month')['ms_played'].sum().reset_index()
# convert ms_played to minutes
df_track_month = ms_played_to_minutes(df_track_month)
print(f'\nTime spent listening to {track_name} each month:')
print(df_track_month.head())

# plot time spent listening to a specific track each month
plt.plot(df_track_month['month'], df_track_month['minutes_played'])
plt.ylabel('Minutes Played')
plt.xticks(rotation=90)
plt.title(f'Time Spent Listening to {track_name} Each Month')
plt.show()

# Determine number of equivalent full times the track was played per month
length_of_track_in_seconds = 3 * 60 + 43 # use the Spotify API to get this
df_track_month['times_played'] = df_track_month['ms_played'] / (length_of_track_in_seconds*1000)

# plot number of equivalent full times the track was played per month
plt.plot(df_track_month['month'], df_track_month['times_played'])
plt.ylabel('Times Played')
plt.xticks(rotation=90)
plt.title(f'Number of Equivalent Full Times {track_name} was Played Each Month')
plt.show()

# Plot total time spent listening to all tracks each month
# Count the ms_played by month
df['month'] = df['ts'].str[0:7]
df_month = df.groupby('month')['ms_played'].sum().reset_index()
# convert ms_played to hours
df_month = ms_played_to_hours(df_month)
print(df_month.head())

# plot time spent listening to all tracks each month
plt.plot(df_month['month'], df_month['hours_played'])
plt.ylabel('Hours Played')
plt.xticks(rotation=90)
plt.title('Time Spent Listening to All Tracks Each Month')
plt.show()

# Determine the day when the most time was spent listening to music
df['day'] = df['ts'].str[0:10]
df_day = df.groupby('day')['ms_played'].sum().reset_index()
# convert ms_played to hours
df_day = ms_played_to_hours(df_day).sort_values('hours_played', ascending=False)
print('\nDays with the most time spent listening to music:')
print(df_day.head())

# Determine the first times that a specific track was played
track_name = "Levels"
df_track = filter_by_track(df, track_name).sort_values('ts')
# # in case there are multiple artists with the same track name
# artist_name = "Avril Lavigne"
# df_track = filter_by_artist(df_track, artist_name)

print(f'\nFirst times {track_name} was played:')
print(df_track.head())