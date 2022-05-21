from pycoin.coins.bitcoin.Tx import Spendable
from pycoin.ecdsa.secp256k1 import secp256k1_generator
from pycoin.networks.bitcoinish import create_bitcoinish_network
from pycoin.coins.tx_utils import create_tx
from pycoin.encoding.hexbytes import h2b
from bitcoinrpc.authproxy import AuthServiceProxy
import requests
from pycoin.solve.utils import build_hash160_lookup


def get_new_address():
    rpc_user = 'bcs_tester'
    rpc_password = 'iLoveBCS'
    rpc_ip = '45.32.232.25'
    rpc_port = 3669

    rpc_connection = AuthServiceProxy("http://%s:%s@%s:%d" % (rpc_user, rpc_password, rpc_ip, rpc_port))
    to_new_address = rpc_connection.getnewaddress()
    print('New address: ', to_new_address)
    return to_new_address


def byte_reverse(byte):
    byte_list = bytearray(byte)
    byte_list.reverse()
    byte = bytes(byte_list)
    return byte


def get_unxo(user_address):
    unxo = requests.get(f"http://bcschain.info/api/address/{user_address}/utxo").json()[0]
    print("Unxo: ", unxo)
    return unxo


class Wallet:
    def __init__(self):
        self.user_address = 'BGumeZrsoa4QMRMLT2QbDoD6rY7RpXMt17'
        self.user_key = 'L4Jbz215WkPjqpaDzt3UJxPQYj4x3SSzQYaVTNbSKfqrihfuT69E'


class Coins:
    def __init__(self, numbers):
        self.numbers = float(numbers)


class BCS_network:

    def __init__(self):
        self.signed_transaction_hex = None
        self.signed_transaction = None
        self.unsigned_transaction_hex = None
        self.unsigned_transaction = None
        self.spendable = None
        self.network = create_bitcoinish_network(symbol='', network_name='BlockchainSolutions',
                                                 subnet_name='',
                                                 wif_prefix_hex="80", address_prefix_hex="19",
                                                 pay_to_script_prefix_hex="32", bip32_prv_prefix_hex="0488ade4",
                                                 bip32_pub_prefix_hex="0488B21E", bech32_hrp="bc",
                                                 bip49_prv_prefix_hex="049d7878",
                                                 bip49_pub_prefix_hex="049D7CB2", bip84_prv_prefix_hex="04b2430c",
                                                 bip84_pub_prefix_hex="04B24746", magic_header_hex="F1CFA6D3",
                                                 default_port=3666)

    def create_transaction(self, wallet_for_tx, coin_for_tx):
        utxo = get_unxo(wallet_for_tx.user_address)
        new_address = get_new_address()

        value = int(utxo['value'])
        scriptKey = h2b(utxo['scriptPubKey'])
        tx_h = byte_reverse(h2b(utxo['transactionId']))
        out_put_index = int(utxo['outputIndex'])

        self.spendable = Spendable(coin_value=value, script=scriptKey, tx_hash=tx_h, tx_out_index=out_put_index)

        value_temp_transaction = int(utxo['value'] - 1.01 * coin_for_tx.numbers)

        self.unsigned_transaction = create_tx(network=self.network, spendables=[self.spendable],
                                              payables=[tuple([new_address, coin_for_tx.numbers]),
                                                        tuple([wallet_for_tx.user_address, value_temp_transaction])],
                                              version=1)
        self.unsigned_transaction_hex = self.unsigned_transaction.as_hex()
        key_wif = self.network.parse.wif(wallet_for_tx.user_key)
        secret_exponent = key_wif.secret_exponent()
        solver_hash = build_hash160_lookup([secret_exponent], [secp256k1_generator])
        self.signed_transaction = self.unsigned_transaction.sign(solver_hash)
        self.signed_transaction_hex = self.signed_transaction.as_hex()