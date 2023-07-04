import sys

ACCESSION_NUMBERS = [
    "PATIENT_ACC_NUM1",
    "PATIENT_ACC_NUM2"
]


def get_accession_numbers():
    number_of_args = len(sys.argv)

    if number_of_args == 1:  # Correspond to the executed python file
        return ACCESSION_NUMBERS

    elif number_of_args == 2:
        with open(sys.argv[1]) as file:
            lines = file.readlines()
            lines = lines[1:]

            return [line.replace('\n', '') for line in lines]

    raise ValueError('Too many arguments')
