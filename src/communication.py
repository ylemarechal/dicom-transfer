# coding: utf-8
from typing import Dict

import pyorthanc


def does_communication_with_given_modality_works(
    modality: pyorthanc.RemoteModality, verbose: bool = False
) -> bool:
    if verbose:
        print("Testing communication with C-Echo ...", end="\r")

    if not modality.echo():
        return False

    if verbose:
        print("Testing communication with C-Echo ... C-Echo succeeded")

    return True


def query(
    clinic_pacs: pyorthanc.RemoteModality, query_data: Dict, verbose: bool = False
) -> None:
    if verbose:
        print("Performing Query ...", end="\r")

    clinic_pacs.query(query_data)

    if verbose:
        print("Performing Query ... Done")


def _move_query(
    clinic_pacs: pyorthanc.RemoteModality, query_identifier: str, target_modality: str
) -> None:
    clinic_pacs.move(
        query_identifier,
        cmove_data={"TargetAet": target_modality, "Synchronous": False},
    )


def move(
    clinic_pacs: pyorthanc.RemoteModality, target_modality: str, verbose: bool = False
) -> None:
    if verbose:
        print("Sending C-Move instruction to source AET ...", end="\r")

    for query_identifier in clinic_pacs.orthanc.get_queries():
        _move_query(clinic_pacs, query_identifier, target_modality)

    if verbose:
        print("Sending C-Move instruction to source AET ... Done")
