from Classes.Account import Account
from Utils.Utils import *
import sys

def main():
    if len(sys.argv) < 5:
        print("please enter an tx_sender, msg_signer, ASN, and its address to add to ASNMap")
        sys.exit(-1)

    tx_sender_name = str(sys.argv[1])
    msg_signer_namer = str(sys.argv[2])
    inASN = int(sys.argv[3])
    inAddress = Web3.toChecksumAddress(sys.argv[4])

    # create accounts
    tx_sender = Account(AccountType.TransactionSender, tx_sender_name)
    tx_sender.load_account_keys()

    msg_sender = Account(AccountType.MessageSender, msg_signer_namer)
    msg_sender.load_account_keys()

    tx_sender.generate_transaction_object("IANA", "IANA_CONTRACT_ADDRESS")

    # data to hash and sign
    data_types = ['uint32', 'address']
    data = [inASN, inAddress]
    
    # sign and hash data
    signed_message, err = msg_sender.hash_and_sign_message(data_types, data)
    if err:
        print("ERROR: failed to hash and sign message")
        sys.exit(-1)

    # generate signed message validation data
    tx_sender.generate_signature_validation_data_from_signed_message(signed_message)

    # generate contract transaction
    tx = tx_sender.tx.sc_addASN(tx_sender.get_nonce(), inASN, inAddress)

    # sign and execute transaction
    tx_hash, tx_receipt, err = tx_sender.tx.sign_and_execute_transaction(tx)
    if TxErrorType(err) != TxErrorType.OK:
        print("ERROR: " + str(TxErrorType(err)) + ". Transaction NOT executed")
        
    print("SUCCESS: ASN<=>Address added")


if __name__ == "__main__":
    main()