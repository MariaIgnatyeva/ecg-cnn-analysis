import warnings
warnings.filterwarnings(action='ignore')

import os
import wfdb
from model import ECGModel


def record_input(records):
    while True:
        print('Enter record number:', end=' ')
        record = input()
        if record in records:
            break
        else:
            print('Invalid record number: should be one of', records)

    return record


def samps_input():
    while True:
        try:
            print('Enter samples interval:', end=' ')
            samples_str = input()
            if samples_str.find(' ') < 0:
                print('You should enter 2 numbers: sampfrom sampto')
            else:
                sampfrom_str, sampto_str = samples_str.split()
                sampfrom, sampto = int(sampfrom_str), int(sampto_str)
                if 0 <= sampto <= 650000 \
                        and 0 <= sampfrom < sampto <= 650000:
                    break
                else:
                    print('sampfrom should < sampto and numbers should be 0 < n <= 650000')
        except ValueError:
            print('Inputs should be 2 integers')

    return sampfrom, sampto


if __name__ == '__main__':
    os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

    records = wfdb.get_record_list('mitdb')

    model = ECGModel('model')

    while True:
        record = record_input(records)
        sampfrom, sampto = samps_input()

        model.evaluate(record, '', sampfrom, sampto)

    # TODO: cheat code
