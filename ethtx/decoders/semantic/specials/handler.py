from typing import List
from ethtx.models.decoded_model import DecodedBalance, DecodedEvent, DecodedTransfer

from . import cryptopunk
from .nfts import nfts

def update_missing_balances(events: List[DecodedEvent], balances: List[DecodedBalance]) -> List[DecodedBalance]:
  for event in events:
    # For cryptopunk
    if event.contract.address == nfts["cryptopunk"] and event.event_name in ["PunkTransfer", "PunkBought"]:
      balances: List[DecodedBalance] = cryptopunk.handle_balances(event, events, balances)

  return balances


def update_missing_transfers(events: List[DecodedEvent], transfers: List[DecodedTransfer]) -> List[DecodedTransfer]:
  for event in events:
    # For cryptopunk
    if event.contract.address == nfts["cryptopunk"] and event.event_name in ["PunkTransfer", "PunkBought"]:
      transfers: List[DecodedTransfer] = cryptopunk.handle_transfers(event, events, transfers)

  return transfers