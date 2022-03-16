import operator
from typing import List, Optional, Tuple


def validate_tracks_length(
    tracks_length: Tuple[int],
    indices: List[int],
    min_length: int,
    max_length: int,
    tracks_count: int,
):
    tracks_list = tuple(tracks_length[i] for i in indices)
    length = sum(tracks_list)
    if (
        length >= min_length
        and length <= max_length
        and tracks_count == len(tracks_list)
    ):
        return True
    return False


def _check_tracks_length(
    tracks_length: List[int],
    min_length: int,
    max_length: int,
    tracks_count: int,
):
    lower = operator.lt
    if tracks_count == 1:
        lower = operator.le

    valid_tracks_length = tuple(
        length for length in tracks_length if lower(length, max_length)
    )

    track_length_size = len(valid_tracks_length)
    if track_length_size < tracks_count:
        return False

    indices = list(range(tracks_count))
    if validate_tracks_length(
        valid_tracks_length, indices, min_length, max_length, tracks_count
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
            valid_tracks_length, indices, min_length, max_length, tracks_count
        ):
            return True


def init_tracks_count(tracks_length: List[int], tracks_count: Optional[int]) -> range:
    res = [tracks_count]
    if not tracks_count:
        res = range(1, len(tracks_length) + 1)
    return res


def check_tracks_length(
    tracks_length: List[int],
    concert_premiere_length: int,
    tracks_count: Optional[int] = 3,
    delta: int = 0,
):
    if tracks_count and len(tracks_length) < tracks_count:
        return False

    min_length = concert_premiere_length - delta
    max_length = concert_premiere_length + delta

    for count in init_tracks_count(tracks_length, tracks_count):
        if (
            _check_tracks_length(
                tracks_length,
                min_length,
                max_length,
                count,
            )
            is True
        ):
            return True
    else:
        return False


if __name__ == "__main__":
    assert check_tracks_length([2, 3], 5) is False
    assert check_tracks_length([1, 2, 6], 6) is False
    assert check_tracks_length([1, 2, 3], 6) is True
    assert check_tracks_length([1, 2, 3], 8) is False
    assert check_tracks_length([1, 2, 3], 6, delta=2) is True
    assert check_tracks_length([1, 2, 3, 4, 30, 20], 54) is True
    assert check_tracks_length([1], 1, tracks_count=1) is True
    assert check_tracks_length([1], 2, tracks_count=1) is False
    assert check_tracks_length([1], 2, tracks_count=1, delta=1) is True
    assert check_tracks_length([1, 2, 3], 5, tracks_count=None, delta=1) is True
