import math
import wave
import numpy as np
import sys

Files_path = "Recordings"
Num_of_recordings = 5 #one more


def get_frame_value(frame):
    """
    Recieves a frame od audio as a string and uses numpy to unpack the frame in hex format,
    then calculates the average value of the frame.
    :param frame: audio frame in hex format.
    :return: the average value of the frame.
    """
    arr = np.fromstring(frame, 'int16')
    return int(math.fabs((arr[0] + arr[1]) / 2))


def create_list(waves_len):
    """
    receives the amount of audio files that will be compared and then uses the zip function in order to
    create every possible comparison without any duplicated.
    :param waves_len: the length of the wave files list that will be compared.
    :return: a list of lists that contain tuples of all the comparisons that need to be made.
    """
    pairs = []
    count = 0
    while count != waves_len:
        pairs.append(zip([count + 1] * (waves_len - count - 2), range(count + 2, waves_len)))
        count += 1
    return pairs


def compare(index1, index2, waves):
    """
        This function receives 2 audio files index in the prepared audio files list and compares them to each other.
        The comparison in done using the get value function which calculates the amplitude of the sound every 1 ms and
        compares the integer values difference at the exact moment in both of the recordings.
        :param waves:
        :param index1: the first audio file index in the list
        :param index2: the second audio file index in the list
        :return: this function returns a dictionary where the key is the compared audio files (their index in the list
        => their keys) and the value is the difference that was calculated in float format.
    """
    wav1 = waves[index1]
    wav2 = waves[index2]
    min_length = min(wav1.getnframes(), wav2.getnframes())
    diff = 0
    for i in range(min_length):
        val1 = get_frame_value(wav1.readframes(1))
        val2 = get_frame_value(wav2.readframes(1))
        subtraction = math.fabs(val1 - val2)
        diff += subtraction

    waves[index1].setpos(0)
    waves[index2].setpos(0)
    return index1, index2, diff


def handle_compare(pairs, waves):
    result = {}
    for pack in pairs:
        for pair in pack:
            index1, index2, diff = compare(pair[0], pair[1], waves)
            result[str([index1, index2])] = diff
    return result


def get_max_diff(result):
    """
    Calculates the max difference between two recordings in audio frame values.
    :param result: A dictionary of differences between every two recordings.
    :return: max key = int, the dictionary key for the max diff key.
             max = int, the max difference
    """
    max = sys.maxsize * -1
    max_key = list(result.keys())[0]
    for key in result:
        if result[key] > max:
            max = result[key]
            max_key = key
    return max_key, max


def get_min_diff(result):
    """
    This function calculates the minimal difference between two recordings in audio frame values.
    :param result: A dictionary of differences between every two recordings.
    :return: min key = int, the dictionary key for the min diff key.
             min = int, the min difference
    """
    min = sys.maxsize
    min_key = list(result.keys())[0]
    for key in result:
        if result[key] < min:
            min = result[key]
            min_key = key
    return min_key, min


def average_diff(results):
    """
        this function calculates the average difference of audio frames from each other.
    :param results: a dictionary of pairs and differences between them.
    :return: float, average difference.
    """
    sum = 0
    counter = 0
    for diff in results:
        sum += results[diff]
        counter += 1
    average = (sum / counter)
    return average


def average_num(results, num, waves):
    """
    This Function Calculates the average difference of the audio frames values of a recording from the other recordings.
    :param results: a dictionary: the key is the audio file numbers that are being compared and the value is the
        difference between them.
    :param num: the compared recording's number
    :return: float, average difference of the audio frames value of a recording from the other recordings.
    """
    counter = 0
    sum = 0
    for i in range(1, len(waves) + 1):
        if i != num:
            key = str([num, i])
            if key in results:
                sum += results[key]
                counter += 1
            else:
                key = str([i, num])
                if key in results:
                    sum += results[key]
                    counter += 1
    avg = sum / counter
    print('average : {0} for num {1}'.format(avg, num))
    return avg


def calc_diff_from_median(median, differences):
    """
    this function receives the median value of the average difference of the audio frames values of a recording
        from the other recordings and those differences and identifies recordings that have a big value diffrence
        the median so they can be pointed out as other people's voices. The logic behind this is that if a diffrent
        person's voice recording will appear it will be very diffrent from the average voice frame values of the user,
        and that's how I can differentiate between other people's voices and the users voice.
    :param median: The median is the value separating the higher half of a data sample from the lower half.
        In our case: an integer value, the median value of the average difference between audio frames values of a
        recording from the other recordings.
    :param differences: a list containing floats. Those floats are the average differences of every recording that is
        being compared.
    :return: Boolean value: True: if the last recording belongs to that user, False otherwise.
        This function prints out the recording files numbers of the recordings that don't belong to the user.
    """
    base_line = []
    for i in range(3):
        base_line.append(differences[i])

    max_base_val = max(base_line)
    min_base_val = min(base_line)
    max_diff = math.fabs(max_base_val - min_base_val)
    print('max diff {0} belongs to recording number: {1}'.format(max_diff, differences.index(max_base_val)))
    for i in range(3, len(differences), 1):
        diff = math.fabs(differences[i] - median)
        print('diff of recording num {0} is {1}'.format(i + 1, diff))
        if diff > max_diff or math.fabs(diff - max_diff) < 50000:
            print(" ==> recording {0} isn't yours!".format(i + 1))
            return False
    return True


def main():
    waves = {i: wave.open(Files_path + '//{0}.wav'.format(i), 'r') for i in range(1, Num_of_recordings)}
    pairs_list = create_list(len(waves) + 1)
    r = handle_compare(pairs_list, waves)
    differences = []

    print('Max_Diff: ' + str((get_max_diff(r))))
    print('Min_Diff: ' + str((get_min_diff(r))))

    for i in range(1, len(waves) + 1):
        differences.append(average_num(r, i, waves))
    print('Differences : {0}'.format(differences))

    median = np.median(sorted(differences))
    print('Median sorted : {0}'.format(median))
    print('------ Results ------')
    recording_belongs_to_user = calc_diff_from_median(median, differences)
    if recording_belongs_to_user:
        return True
    else:
        return False


if __name__ == '__main__':
    result = main()
    print(result)
