import pandas as pd
import matplotlib.pyplot as plt
plt.style.use('dark_background')
import spotify_API_fns as sp_API_fns
import filter_fns
import plot_fns

# Read the csv
df = pd.read_csv('all_data.csv')
# filter out songs played for less than 20 seconds
df = filter_fns.filter_by_minimum_secs_played(df, 20)

# df = filter_fns.filter_non_spotify_tracks(df)

# Time by artist
df_artists = df.groupby('master_metadata_album_artist_name')['hours_played'].sum().reset_index()
df_artists = df_artists.sort_values('hours_played', ascending=False)
print('\nMost listened to artists:')
print(df_artists.head())

plot_fns.plot_top_n(df_artists, 10, 'master_metadata_album_artist_name', 'hours_played', x_label='Artist', y_label='Hours Played')

# Time by track

# custom df so that it ignores live versions, etc
# take out the following from the track name:
"""
radio edit
live
acoustic
acoustic version
anniversary edition
year remaster
remaster year
remaster
year remastered
remastered year
remastered
single version
live in...
live at...
live from...
"""
# better way to do it: take current filter, and then if the artist has a track that starts with the same name as another one of their tracks, merge the hours_played_sums
df_tracks = df

df_tracks = df_tracks.groupby(['master_metadata_track_name', 'master_metadata_album_artist_name']).agg(hours_played_sum=('hours_played', 'sum')).reset_index()
df_tracks = df_tracks.sort_values('hours_played_sum', ascending=False)
print('\nMost listened to tracks:')
print(df_tracks.head())
df_tracks['track_artist'] = df_tracks['master_metadata_track_name'] + '\n' + df_tracks['master_metadata_album_artist_name']
plot_fns.plot_top_n(df_tracks, 10, 'track_artist', 'hours_played_sum', x_label='Track and Artist', y_label='Hours Played', title='Top 10 Tracks')

# Specific year time by artist
year = 2020
df_year = filter_fns.filter_to_year(df, year)

df_artist_year = df_year.groupby('master_metadata_album_artist_name')['hours_played'].sum().reset_index()
df_artist_year = df_artist_year.sort_values('hours_played', ascending=False)

n = 10
plot_fns.plot_top_n(df_artist_year, n, 'master_metadata_album_artist_name', 'hours_played', title=f'Top {n} Artists in {year}')

# Time listening to specific artist each month over entire dataset
artist_name = 'Avril Lavigne'
df_artist = filter_fns.filter_by_artist_string(df, artist_name)

df_artist['month'] = df_artist['ts'].str[0:7]
df_artist_month = df_artist.groupby('month')['hours_played'].sum().reset_index()

plot_fns.plot_time_series(df_artist_month, 'month', 'hours_played', title=f'Time Spent Listening to {artist_name} Each Month', rotate_x_labels=True)

# Time with specific track
track_name = "Sk8er Boi"
artist_name = 0 # if listened to multiple artists with the same track name
df_track = filter_fns.filter_by_track_string(df, track_name, artist_name)

# Time by month
df_track['month'] = df_track['ts'].str[0:7]
df_track_month = df_track.groupby('month')['minutes_played'].sum().reset_index()

plot_fns.plot_time_series(df_track_month, 'month', 'minutes_played', title=f'Time Spent Listening to {track_name} Each Month', rotate_x_labels=True)

# Number of equivalent full times the track was played per month
track_length_s = sp_API_fns.get_track_length_s(sp_API_fns.get_track_uris(track_name, artist_name)[0])
df_track_month['times_played'] = df_track_month['minutes_played'] / (track_length_s / 60)

plot_fns.plot_time_series(df_track_month, 'month', 'times_played', title=f'Number of Equivalent Full Times {track_name} was Played Each Month', rotate_x_labels=True)


# time listening to all tracks by month
df['month'] = df['ts'].str[0:7]
df_months = df.groupby('month')['hours_played'].sum().reset_index()

plot_fns.plot_time_series(df_months, 'month', 'hours_played', title='Time Spent Listening to All Tracks Each Month', rotate_x_labels=True)

# Days when the most time was spent listening to music
df['day'] = df['ts'].str[0:10]
df_day = df.groupby('day')['hours_played'].sum().reset_index().sort_values('hours_played', ascending=False)
print('\nDays with the most time spent listening to music:')
print(df_day.head())

# Determine the first times that a specific track was played
track_name = "Levels"
artist_name = None # if listened to multiple artists with the same track name
df_track = filter_fns.filter_by_track_string(df, track_name, artist_name).sort_values('ts')

print(f'\nFirst times {track_name} was played:')
print(df_track.head())