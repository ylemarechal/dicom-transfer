# coding: utf-8
from typing import Dict, List


def build_query_payloads(list_of_acession_number: List[str]) -> List[Dict]:
    query_payloads = []

    for acession_number in list_of_acession_number:
        query_payloads.append(
            {"Level": "Study", "Query": {"AccessionNumber": acession_number}}
        )

    return query_payloads
