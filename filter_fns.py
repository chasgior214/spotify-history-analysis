import pandas as pd

# track filters
def filter_by_track_string(df, track, artist=None):
    """Filter the dataframe to only include rows where the master_metadata_track_name column is equal to track. Optionally, filter by artist as well.
    
    Args:
    - df: the dataframe to filter
    - track: the track name to filter by as a string (e.g. 'Complicated')
    - artist: optional. the artist name to filter by as a string (e.g. 'Avril Lavigne')"""
    if artist:
        df = df[df['master_metadata_album_artist_name'] == artist]
    return df[df['master_metadata_track_name'] == track]
def filter_by_track_uri(df, track_uri):
    """Filter the dataframe to only include rows where the master_metadata_track_uri column is equal to track_uri.
    
    Args:
    - df: the dataframe to filter
    - track_uri: the track uri to filter by as a string (e.g. 'spotify:track:00Mb3DuaIH1kjrwOku9CGU')"""
    return df[df['master_metadata_track_uri'] == track_uri]

# artist filters
def filter_by_artist_string(df, artist):
    """Filter the dataframe to only include rows where the master_metadata_album_artist_name column is equal to artist.
    
    Args:
    - df: the dataframe to filter
    - artist: the artist name to filter by as a string (e.g. 'Avril Lavigne')"""
    return df[df['master_metadata_album_artist_name'] == artist]

# time filters
def filter_to_time_range(df, start, end):
    """Filter the dataframe to only include rows where the ts column is between start and end.
    
    Args:
    - df: the dataframe to filter
    - start: the start of the time range in ISO 8601 format (e.g. '2023-01-01T00:00:00.000Z')
    - end: the end of the time range in ISO 8601 format (e.g. '2023-12-31T23:59:59.999Z')"""
    return df[(df['ts'] >= start) & (df['ts'] <= end)]
def filter_to_year(df, year):
    """Filter the dataframe to only include rows where the ts column is in the given year.
    
    Args:
    - df: the dataframe to filter
    - year: the year to filter by as an integer (e.g. 2023)"""
    return df[df['ts'].str[0:4] == str(year)]
def filter_to_month(df, month, year):
    """Filter the dataframe to only include rows where the ts column is in the given month and year.
    
    Args:
    - df: the dataframe to filter
    - month: the month to filter by as an integer (e.g. 1 for January)
    - year: the year to filter by as an integer (e.g. 2023)"""
    return df[df['ts'].str[0:7] == f'{year}-{str(month).zfill(2)}']

def filter_by_minimum_secs_played(df, min_played):
    """Filter the dataframe to only include rows where the ms_played column is greater than min_played.
    
    Args:
    - df: the dataframe to filter
    - min_secs_played: the minimum number of seconds played to filter by as an integer (e.g. 60)
    """
    return df[df['ms_played'] > min_played*1000]

# add a conversion for time to EST
