import pandas as pd
import matplotlib.pyplot as plt
plt.style.use('dark_background')
import spotify_API_fns as sp_API_fns

# Read the csv
df = pd.read_csv('all_data.csv')

# filter out songs that were played for less than 20 seconds
df = df[df['ms_played'] > 20000]

# Define some functions
def ms_played_to_minutes(df):
    df['minutes_played'] = df['ms_played'] / 1000 / 60
    return df
def ms_played_to_hours(df):
    df['hours_played'] = df['ms_played'] / 1000 / 60 / 60
    return df
def filter_by_artist_string(df, artist):
    return df[df['master_metadata_album_artist_name'] == artist]
def filter_by_track_string(df, track):
    return df[df['master_metadata_track_name'] == track]
def filter_by_track_uri(df, track_uri):
    return df[df['master_metadata_track_uri'] == track_uri]
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


# 2023 only
df_2023 = df[df['ts'].str[0:4] == '2023']

# Count time by artist
df_artist_2023 = df_2023.groupby('master_metadata_album_artist_name')['ms_played'].sum().reset_index()
df_artist_2023 = df_artist_2023.sort_values('ms_played', ascending=False)
df_artist_2023 = ms_played_to_hours(df_artist_2023)

# plot the top 10 artists
plt.bar(df_artist_2023['master_metadata_album_artist_name'][:10], df_artist_2023['hours_played'][:10])
plt.ylabel('Hours Played')
plt.title('Top 10 Artists in 2023')
plt.show()



# Time spent listening to specific artist each month from the entire dataset
artist_name = 'Avril Lavigne'
df_artist = df[df['master_metadata_album_artist_name'] == artist_name]
df_artist['month'] = df_artist['ts'].str[0:7]
df_artist_month = df_artist.groupby('month')['ms_played'].sum().reset_index()
df_artist_month = ms_played_to_hours(df_artist_month)

plt.plot(df_artist_month['month'], df_artist_month['hours_played'])
plt.ylabel('Hours Played')
plt.xticks(rotation=90)
plt.title(f'Time Spent Listening to {artist_name} Each Month')
plt.show()

# Filter to a specific track
track_name = "Sk8er Boi"
df_track = df[df['master_metadata_track_name'] == track_name]
# in case there are multiple artists with the same track name
artist_name = "Avril Lavigne"
df_track = filter_by_artist_string(df_track, artist_name)

# Count time by month
df_track['month'] = df_track['ts'].str[0:7]
df_track_month = df_track.groupby('month')['ms_played'].sum().reset_index()
df_track_month = ms_played_to_minutes(df_track_month)

# plot time spent listening to a specific track each month
plt.plot(df_track_month['month'], df_track_month['minutes_played'])
plt.ylabel('Minutes Played')
plt.xticks(rotation=90)
plt.title(f'Time Spent Listening to {track_name} Each Month')
plt.show()

# Determine number of equivalent full times the track was played per month
track_length_s = sp_API_fns.get_track_length_s(sp_API_fns.get_track_uris(track_name, artist_name)[0])
df_track_month['times_played'] = df_track_month['ms_played'] / (track_length_s*1000)

# plot number of equivalent full times the track was played per month
plt.plot(df_track_month['month'], df_track_month['times_played'])
plt.ylabel('Times Played')
plt.xticks(rotation=90)
plt.title(f'Number of Equivalent Full Times {track_name} was Played Each Month')
plt.show()


# time listening to all tracks by month
df['month'] = df['ts'].str[0:7]
df_month = df.groupby('month')['ms_played'].sum().reset_index()
df_month = ms_played_to_hours(df_month)

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
track_name = "Sk8er Boi"
df_track = filter_by_track_string(df, track_name).sort_values('ts')
# # in case there are multiple artists with the same track name
# artist_name = "Avril Lavigne"
# df_track = filter_by_artist_string(df_track, artist_name)

print(f'\nFirst times {track_name} was played:')
print(df_track.head())