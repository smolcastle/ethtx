from typing import List
from ethtx.models.decoded_model import DecodedBalance, DecodedEvent, AddressInfo, DecodedTransfer

from .nfts import nfts


'''
Cryptopunk: check if event contains either PunkTransfer or PunkBought event. If so, follow the logic below. 
1. transferPunk call emits Transfer(from, to, 1) and PunkTransfer events. Capture PunkTransfer(from, to, punkIndex) event
2. buyPunk calls emit Transfer(from, to, 1) and PunkBought events. Capture PunkBought(punkIndex, msg.value, from, to) event
3. acceptBidForPunk calls emit Transfer(from, to, 1) and PunkBought events. Capture Transfer event to track 
addresses and PunkBought to track index. In this case, PunkBought has toAddress set to 0x0

Note: Transfer event is is at -1 index in case of acceptBidForPunk call.

Above cases can handle any transaction which contains a CryptoPunk.Transfer event.
'''


def handle_balances(event: DecodedEvent, events: List[DecodedEvent], balances: List[DecodedBalance]) -> List[DecodedBalance]:
    if event.event_name == "PunkTransfer":
        fromAddress = event.parameters[0].value.address
        toAddress = event.parameters[1].value.address
        punkIndex = event.parameters[2].value
    else:
        if events[events.index(event)-1].event_name == "Transfer": # acceptBidForPunk call
            fromAddress = events[events.index(event)-1].parameters[0].value.address
            toAddress = events[events.index(event)-1].parameters[1].value.address
            punkIndex = event.parameters[0].value
        else: # buyPunk call
            fromAddress = event.parameters[2].value.address
            toAddress = event.parameters[3].value.address
            punkIndex = event.parameters[0].value

    buyerExists, sellerExists = False, False
    for balance in balances:
        if balance.holder.address ==  fromAddress:
            balances[balances.index(balance)].tokens.append(
                {
                    "token_address": nfts["cryptopunk"] + "?a=%i" % punkIndex + "#inventory",
                    "token_symbol": "NFT %i" % punkIndex,
                    "token_standard": "PUNK00",
                    "balance": "-1.0000",
                }
            )
            sellerExists = True
        elif balance.holder.address == toAddress:
            balances[balances.index(balance)].tokens.append(
                {
                    "token_address": nfts["cryptopunk"] + "?a=%i" % punkIndex + "#inventory",
                    "token_symbol": "NFT %i" % punkIndex,
                    "token_standard": "PUNK00",
                    "balance": "1.0000",
                }
            )
            buyerExists = True
        
    else:
        # if addresses don't exist in the balances, add them
        if not sellerExists:
            balances.append(
                DecodedBalance(
                    holder=AddressInfo(
                        address=fromAddress,
                        name=fromAddress,
                        badge=None
                    ),
                    tokens=[
                        {
                            "token_address": nfts["cryptopunk"] + "?a= %i" % punkIndex + "#inventory",
                            "token_symbol": "NFT %i" % punkIndex,
                            "token_standard": "PUNK00",
                            "balance": "-1.0000",
                        }
                    ]
                )
            )
        if not buyerExists:
            balances.append(
                DecodedBalance(
                    holder=AddressInfo(
                        address=toAddress,
                        name=toAddress,
                        badge=None
                    ),
                    tokens=[
                        {
                            "token_address": nfts["cryptopunk"] + "?a=%i" % punkIndex + "#inventory",
                            "token_symbol": "NFT %i" % punkIndex,
                            "token_standard": "PUNK00",
                            "balance": "1.0000",
                        }
                    ]
                )
            )
    return balances


def handle_transfers(event: DecodedEvent, events: List[DecodedEvent], transfers: List[DecodedTransfer]) -> List[DecodedTransfer]:
    if event.event_name == "PunkTransfer":
        fromAddress = event.parameters[0].value.address
        toAddress = event.parameters[1].value.address
        punkIndex = event.parameters[2].value
    else:
        if events[events.index(event)-1].event_name == "Transfer": # acceptBidForPunk call
            fromAddress = events[events.index(event)-1].parameters[0].value.address
            toAddress = events[events.index(event)-1].parameters[1].value.address
            punkIndex = event.parameters[0].value
        else: # buyPunk call
            fromAddress = event.parameters[2].value.address
            toAddress = event.parameters[3].value.address
            punkIndex = event.parameters[0].value

    transfers.append(
        DecodedTransfer(
            from_address=AddressInfo(
                address=fromAddress,
                name=fromAddress,
                badge=None
            ),
            to_address=AddressInfo(
                address=toAddress,
                name=toAddress,
                badge=None
            ),
            token_address=nfts['cryptopunk'] + "?a=%i" % punkIndex + "#inventory",
            token_symbol="NFT %i" % punkIndex,
            token_standard="PUNK00",
            value="1.0000",
        )
    )

    return transfers