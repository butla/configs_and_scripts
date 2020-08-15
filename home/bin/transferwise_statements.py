#!/usr/bin/env python3

# TODO get gbp and USD for previous month (if it's before 10) or current (if after 10)
# take month as param
# name them, put in dropbox folder (separete function for that)
# tests
import os
import sys
from typing import List

import requests

token = os.environ['TRANSFERWISE_TOKEN']


def main():
    date = sys.argv[1]
    amount = float(sys.argv[2])

    profile_id = get_profile_id()
    account_id = get_account_id(profile_id)

    # TODO
    resp = requests.get(
        f'"https://api.transferwise.com/v3/profiles/{profile_id}/borderless-accounts/{account_id}/statement.csv?currency=GBP&intervalStart=2020-07-01T00:00:00.000Z&intervalEnd=2020-08-01T00:00:00.000Z"',
        headers={'Authorization': f'Bearer {token}'},
    )
    if not resp.ok:
        print('ERROR! Request failed! Response:')
        print(resp.text)

    pln_to_gbp_rate = float(resp.json()[0]['rate'])
    exchanged_amount = amount * pln_to_gbp_rate
    print(amount, 'PLN *', pln_to_gbp_rate, '=', exchanged_amount)


def get_profile_id() -> int:
    resp = requests.get(
        'https://api.transferwise.com/v1/profiles',
        headers={'Authorization': f'Bearer {token}'},
    )
    resp.raise_for_status()

    profiles: List[dict] = resp.json()
    business_profile = next(profile for profile in profiles if profile['type'] == 'business')
    return business_profile['id']


def get_account_id(profile_id: int) -> int:
    resp = requests.get(
        f'https://api.transferwise.com/v1/borderless-accounts?profileId={profile_id}'
        headers={'Authorization': f'Bearer {token}'},
    )
    resp.raise_for_status()

    accounts: List[dict] = resp.json()
    business_account = accounts[0]
    return business_account['id']

if __name__ == '__main__':
    main()
