from typing import List, Optional, Tuple


def validate_tracks_length(
    tracks_length: Tuple[int],
    indices: List[int],
    total_length: int,
    tracks_count: int,
):
    tracks_list = tuple(tracks_length[i] for i in indices)
    if sum(tracks_list) == total_length and tracks_count == len(tracks_list):
        return True
    return False


def check_tracks_length(
    tracks_length: List[int], concert_premiere_length: int, tracks_count: int = 3
):
    if len(tracks_length) < tracks_count:
        return False

    valid_tracks_length = tuple(
        length for length in tracks_length if length < concert_premiere_length
    )

    track_length_size = len(valid_tracks_length)
    if track_length_size < tracks_count:
        return False

    indices = list(range(tracks_count))
    if validate_tracks_length(
        valid_tracks_length, indices, concert_premiere_length, tracks_count
    ):
        return True

    while True:
        for i in reversed(range(tracks_count)):
            if indices[i] != i + track_length_size - tracks_count:
                break
        else:
            return False
        indices[i] += 1
        for j in range(i + 1, tracks_count):
            indices[j] = indices[j - 1] + 1

        if validate_tracks_length(
            valid_tracks_length, indices, concert_premiere_length, tracks_count
        ):
            return True


if __name__ == "__main__":
    assert check_tracks_length([2, 3], 5) is False
    assert check_tracks_length([1, 2, 6], 6) is False
    assert check_tracks_length([1, 2, 3], 6) is True
    assert check_tracks_length([1, 2, 3, 4, 30, 20], 54) is True
