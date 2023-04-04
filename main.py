# coding: utf-8

import sys
import time
import pyorthanc
from alive_progress import alive_bar

import conf
import creds
from exams import ACCESSION_NUMBERS
from src import communication, data

studies_checked = []
access_num_checked = []

if __name__ == "__main__":

    local_orthanc = pyorthanc.Orthanc(creds.ORTHANC_LOCAL_HOST)
    onco_orthanc = pyorthanc.Orthanc(creds.ORTHANC_HOST)
    onco_orthanc.setup_credentials(creds.ORTHANC_USER, creds.ORTHANC_PASSWD)

    clinic_pacs = pyorthanc.RemoteModality(local_orthanc, creds.PACS_AET)

    if not communication.does_communication_with_given_modality_works(
            clinic_pacs, verbose=True
    ):
        exit("DICOM communication with distant PACS has failed (C-ECHO)")

    print("Loading studies cache ...")
    params = {"expand": "true"}
    studies = onco_orthanc.get_studies(params=params)
    with alive_bar(len(studies), dual_line=True, title='Loading studies') as loading_bar:
        for study in studies:
            studies_checked.append(study["ID"])
            access_num_checked.append(study["MainDicomTags"]["AccessionNumber"])
            loading_bar()

    with alive_bar(len(ACCESSION_NUMBERS), dual_line=True, title='Accession number') as bar:
        for query_payload in data.build_query_payloads(ACCESSION_NUMBERS):
            start = time.perf_counter()
            bar.text = f'-> Sending study {query_payload["Query"]["AccessionNumber"]}. Waiting for confirmation' \
                       f'{time.perf_counter() - start:0.2f} for sec'

            bar()
            if query_payload["Query"]["AccessionNumber"] in access_num_checked:
                print(f'INFO    : Study {query_payload["Query"]["AccessionNumber"]} already in destination PACS')
                continue

            local_orthanc.delete_queries()

            try:
                communication.query(clinic_pacs, query_payload, verbose=False)
            except Exception as e:
                print(e)
                sys.exit("DICOM communication with distant PACS has failed")

            pacs_retour = local_orthanc.get_query_answers(local_orthanc.get_queries()[0])
            if pacs_retour is not None and len(pacs_retour) > 0:

                communication.move(clinic_pacs, creds.TARGET_AET, verbose=False)

                while 1:
                    bar.text = f'-> Sending study {query_payload["Query"]["AccessionNumber"]}. ' \
                               f'Waiting for confirmation ...'
                    accession_numbers = []
                    studies = onco_orthanc.get_studies()

                    for study in studies:

                        if study not in studies_checked:
                            study_info = onco_orthanc.get_study_information(study)
                            access_num_checked.append(
                                study_info["MainDicomTags"]["AccessionNumber"]
                            )
                            studies_checked.append(study_info["ID"])

                    stop = time.perf_counter()
                    if (
                            query_payload["Query"]["AccessionNumber"]
                            in set(access_num_checked)
                    ):
                        print(f'SUCCESS : Study {query_payload["Query"]["AccessionNumber"]} '
                              f'sent in {stop - start:0.2f} sec')
                        break
                    if stop - start >= conf.TIMEOUT:
                        print(f'FAIL    : Study {query_payload["Query"]["AccessionNumber"]} not '
                              f'received by destination after {stop - start:0.2f} sec')
                        break

                    time.sleep(conf.WAITING_TIME)

            else:
                print(f'WARN    : Study {query_payload["Query"]["AccessionNumber"]} NOT FOUND')

    print("Script finished ...")
