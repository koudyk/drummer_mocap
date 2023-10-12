from pathlib import Path
from ast import literal_eval
import pandas as pd
import numpy as np


def load_lr_heel_data():
    l_filename = Path().resolve().parent / "data" / "data-prep_mocap-of-heels_left.csv"
    lh = pd.read_csv(l_filename, index_col=0).astype(object)

    r_filename = Path().resolve().parent / "data" / "data-prep_mocap-of-heels_right.csv"
    rh = pd.read_csv(r_filename, index_col=0).astype(object)

    for col in lh.columns:
        lh[col] = lh[col].apply(literal_eval)
        rh[col] = rh[col].apply(literal_eval)
    return lh, rh


def load_cop_data():
    filepath = (
        Path().resolve().parent
        / "data"
        / "data-prep_force-plate-center-of-pressure.csv"
    )
    df = pd.read_csv(filepath).astype(object)
    for col in ["cop_x", "cop_y"]:
        df[col] = df[col].apply(literal_eval)
    return df    


def xdim():
    return 0


def ydim():
    return 1


def zdim(): # up and down
    return 2


def load_participant_numbers():
    return np.arange(1, 10) # numbers 1 to 9


def load_song_genres():
    return {
    "Bloodline": "Heavy metal",
    "GoIntoTheWater": "Heavy metal",
    "BackInBlack": "Rock",
    "TheOcean": "Rock",
    "Juju": "Jazz",
    "SoWhat": "Jazz",
    }


def load_song_names():
    song_genres = load_song_genres()
    return list(song_genres.keys())


def load_song_numbers():
    song_numbers = {}
    for i, name in enumerate(load_song_names()):
        song_numbers[name] = i
    return song_numbers
       

def load_song_labels_for_figures():
    song_genres = load_song_genres()
    return ["%s\n(%s)"%(song, genre) for song, genre in song_genres.items()]


def get_figures_folder():
    return Path().resolve().parent / "figures"


def get_participants_data_folders():
    data_folder = Path().resolve().parent / "data" / "final_data"
    return sorted(list(data_folder.glob("*-Filled-In")))


def path_to_song_number(path):
    file_name = str(path)
    i_song_number = file_name.rfind('-0') + 2
    return int(file_name[i_song_number : i_song_number + 1])


def path_to_song_name(path):
    file_name = str(path)
    i_song_name = file_name.rfind('-0') + 4
    return file_name[i_song_name :-11]


def path_to_participant_number(path):
    file_name = str(path)
    i_participant_number = file_name.rfind('-P') + 2
    return int(file_name[i_participant_number: i_participant_number + 1])


def get_start_end_frames(song_name, participant_number):
    # file with the start times for each participant and song
    start_times_csv_path = Path().resolve().parent / "data" / "final_data" / "StartTimes.csv"
    start_times = pd.read_csv(start_times_csv_path)
    start_times = start_times[start_times["Participant"] > 0] # the pilot data is ptp 0

    # song lengths
    song_lengths_sec = {
        "Bloodline": 25,
        "GoIntoTheWater": 24.250,
        "BackInBlack": 21.5,
        "TheOcean":21,
        "Juju":25.187,
        "SoWhat": 28,
    }

    frames_per_second = 300
    song_lengths = {}
    for song, len_sec in song_lengths_sec.items():
        song_lengths[song] = int(np.floor(len_sec * frames_per_second))
    start_times_ptp = start_times[start_times['Participant'] == participant_number]
    start_times_ptp_song = start_times_ptp[start_times_ptp["Song"] == song_name]
    start_frame = int(start_times_ptp_song['Start frame'])
    end_frame = start_frame + song_lengths[song_name]
    return start_frame, end_frame



def load_channel_name_mapping():
    # rename the channels, based on the c3d manual
    # https://www.c3d.org/HTML/default.htm?turl=Documents%2Ftype24.htm
    # ours is a TYPE-4 force platform
    return {
        "Channel_01": "Force_x",
        "Channel_02": "Force_y",
        "Channel_03": "Force_z",
        "Channel_04": "Moment_x",
        "Channel_05": "Moment_y",
        "Channel_06": "Moment_z",
    }

























