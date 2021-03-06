import unittest
import random
import xbridge_logger
from bitcoinrpc.authproxy import AuthServiceProxy, JSONRPCException

from interface import xbridge_rpc
from utils import xbridge_utils
from utils import xbridge_custom_exceptions

import sys
sys.path.insert(0,'..')
import xbridge_config

subTest_count = xbridge_config.get_conf_subtests_run_number()
MAX_LOG_LENGTH = xbridge_config.get_param_max_char_length_to_display()

class Network_UnitTest(unittest.TestCase):
    def setUp(self):
        xbridge_utils.generate_new_set_of_data(data_nature=3, char_min_size=1, char_max_size=10000)

    # @unittest.skip("IN REVIEW")
    def test_addnode_invalid(self):
        if xbridge_config.get_wallet_decryption_passphrase() == "":
            return
        valid_passphrase = xbridge_config.get_wallet_decryption_passphrase()
        random_int = xbridge_utils.generate_random_int(1, 9999)
        for i in range(subTest_count):
            log_json = ""
            with self.subTest("comb"):
                try:
                    node = random.choice(xbridge_utils.set_of_invalid_parameters)
                    cmd = random.choice(xbridge_utils.set_of_invalid_parameters)
                    xbridge_rpc.walletpassphrase(valid_passphrase, random_int, False)
                    self.assertRaises(xbridge_custom_exceptions.ValidBlockNetException, xbridge_rpc.addnode, node, cmd)
                    log_json = {"group": "test_addnode_invalid", "success": 1, "failure": 0, "error": 0}
                    xbridge_utils.ERROR_LOG.append(log_json)
                except AssertionError as ass_err:
                    log_json = {"group": "test_addnode_invalid", "success": 0, "failure": 1, "error": 0}
                    xbridge_utils.ERROR_LOG.append(log_json)
                    xbridge_logger.logger.info('test_addnode_invalid FAILED: %s' % ass_err)
                    if MAX_LOG_LENGTH > 0:
                        xbridge_logger.logger.info('node: %s' % str(node)[:MAX_LOG_LENGTH])
                        xbridge_logger.logger.info('cmd: %s' % str(cmd)[:MAX_LOG_LENGTH])
                except JSONRPCException as json_excpt:
                    xbridge_logger.logger.info('test_addnode_invalid ERROR: %s' % str(json_excpt))
                    log_json = {"group": "test_addnode_invalid", "success": 0,  "failure": 0, "error": 1}
                    xbridge_utils.ERROR_LOG.append(log_json)
                    if MAX_LOG_LENGTH > 0:
                        xbridge_logger.logger.info('node: %s' % str(node)[:MAX_LOG_LENGTH])
                        xbridge_logger.logger.info('cmd: %s' % str(cmd)[:MAX_LOG_LENGTH])

    # getaddednodeinfo dns bool ( "node" )
    # getaddednodeinfo true
    # getaddednodeinfo true "192.168.0.201"
    # Returns information about the given added node, or all added nodes
    # If dns is false, only a list of added nodes will be provided, otherwise connected information will also be available.
    def test_getaddednodeinfo_invalid(self):
        log_json = ""
        if xbridge_config.get_wallet_decryption_passphrase() == "":
            return
        valid_passphrase = xbridge_config.get_wallet_decryption_passphrase()
        random_int = xbridge_utils.generate_random_int(-999999999999, 999999999999)
        xbridge_rpc.walletpassphrase(valid_passphrase, random_int, False)
        self.assertIsInstance(xbridge_rpc.rpc_connection.getaddednodeinfo(True), list)
        self.assertIsInstance(xbridge_rpc.rpc_connection.getaddednodeinfo(False), list)
        for i in range(subTest_count):
            log_json = ""
            with self.subTest("comb"):
                try:
                    dns = random.choice(xbridge_utils.set_of_invalid_parameters)
                    node = random.choice(xbridge_utils.set_of_invalid_parameters)
                    self.assertRaises(xbridge_custom_exceptions.ValidBlockNetException, xbridge_rpc.getaddednodeinfo, dns, node)
                    log_json = {"group": "test_getaddednodeinfo_invalid", "success": 1, "failure": 0, "error": 0}
                    xbridge_utils.ERROR_LOG.append(log_json)
                except AssertionError as ass_err:
                    log_json = {"group": "test_getaddednodeinfo_invalid", "success": 0, "failure": 1, "error": 0}
                    xbridge_utils.ERROR_LOG.append(log_json)
                    xbridge_logger.logger.info('test_getaddednodeinfo_invalid FAILED: %s' % ass_err)
                    if MAX_LOG_LENGTH > 0:
                        xbridge_logger.logger.info('dns: %s' % str(dns)[:MAX_LOG_LENGTH])
                        xbridge_logger.logger.info('node: %s' % str(dns)[:MAX_LOG_LENGTH])
                except JSONRPCException as json_excpt:
                    xbridge_logger.logger.info('test_getaddednodeinfo_invalid ERROR: %s' % str(json_excpt))
                    log_json = {"group": "test_getaddednodeinfo_invalid", "success": 0,  "failure": 0, "error": 1}
                    xbridge_utils.ERROR_LOG.append(log_json)
                    if MAX_LOG_LENGTH > 0:
                        xbridge_logger.logger.info('dns: %s' % str(dns)[:MAX_LOG_LENGTH])
                        xbridge_logger.logger.info('node: %s' % str(dns)[:MAX_LOG_LENGTH])
                    
    def test_get_connection_count(self):
        try:
            log_json = ""
            self.assertIsInstance(xbridge_rpc.rpc_connection.getconnectioncount(), int)
            self.assertGreater(xbridge_rpc.rpc_connection.getconnectioncount(), 1)
            log_json = {"group": "get_connectioncount", "success": 1, "failure": 0, "error": 0}
            xbridge_utils.ERROR_LOG.append(log_json)
        except AssertionError as ass_err:
            xbridge_logger.logger.info('test_get_connection_count FAILED: %s' % str(ass_err))
            log_json = {"group": "get_connectioncount", "success": 0, "failure": 1, "error": 0}
            xbridge_utils.ERROR_LOG.append(log_json)
        except JSONRPCException as json_excpt:
            log_json = {"group": "get_connectioncount", "success": 0, "failure": 0, "error": 1}
            xbridge_utils.ERROR_LOG.append(log_json)
            xbridge_logger.logger.info('test_get_connection_count ERROR: %s' % str(json_excpt))

    def test_get_node_list(self):
        try:
            log_json = ""
            node_list = xbridge_rpc.get_node_list()
            self.assertIsInstance(node_list, list)
            self.assertGreater(len(node_list), 200)
            log_json = {"group": "get_node_list", "success": 1,  "failure": 0, "error": 0}
            xbridge_utils.ERROR_LOG.append(log_json)
        except AssertionError as ass_err:
            xbridge_logger.logger.info('test_get_node_list FAILED: %s' % str(ass_err))
            log_json = {"group": "test_get_node_list", "success": 0,  "failure": 1, "error": 0}
            xbridge_utils.ERROR_LOG.append(log_json)
        except JSONRPCException as json_excpt:
            xbridge_logger.logger.info('test_get_node_list ERROR: %s' % str(json_excpt))
            log_json = {"group": "test_get_node_list", "success": 0,  "failure": 0, "error": 1}
            xbridge_utils.ERROR_LOG.append(log_json)

    def test_get_version(self):
        try:
            log_json = ""
            version_nb = xbridge_rpc.get_core_version()
            self.assertIsInstance(version_nb, int)
            self.assertGreater(version_nb, 3073600)
            log_json = {"group": "test_get_version", "success": 1,  "failure": 0, "error": 0}
            xbridge_utils.ERROR_LOG.append(log_json)
        except AssertionError as ass_err:
            xbridge_logger.logger.info('test_get_version FAILED: %s' % str(ass_err))
            log_json = {"group": "test_get_version", "success": 0,  "failure": 1, "error": 0}
            xbridge_utils.ERROR_LOG.append(log_json)
        except JSONRPCException as json_excpt:
            xbridge_logger.logger.info('test_get_version ERROR: %s' % str(json_excpt))
            log_json = {"group": "test_get_version", "success": 0,  "failure": 0, "error": 1}
            xbridge_utils.ERROR_LOG.append(log_json)

    def test_get_peer_info(self):
        try:
            log_json = ""
            peer = xbridge_rpc.rpc_connection.getpeerinfo()
            self.assertIsInstance(peer, list)
            self.assertGreater(len(peer), 0)
            log_json = {"group": "test_get_peer_info", "success": 1,  "failure": 0, "error": 0}
            xbridge_utils.ERROR_LOG.append(log_json)
        except AssertionError as ass_err:
            xbridge_logger.logger.info('test_get_peer_info FAILED: %s' % str(ass_err))
            log_json = {"group": "test_get_peer_info", "success": 0,  "failure": 1, "error": 0}
            xbridge_utils.ERROR_LOG.append(log_json)
        except JSONRPCException as json_excpt:
            xbridge_logger.logger.info('test_get_peer_info ERROR: %s' % str(json_excpt))
            log_json = {"group": "test_get_peer_info", "success": 0,  "failure": 0, "error": 1}
            xbridge_utils.ERROR_LOG.append(log_json)

# unittest.main()


"""
suite = unittest.TestSuite()
for i in range(50):
    # suite.addTest(accept_Tx_Test("test_addnode_invalid"))
    # suite.addTest(accept_Tx_Test("test_invalid_accept_tx_0a_noseq"))
    suite.addTest(Network_UnitTest("test_addnode_invalid"))
# suite.addTest(accept_Tx_Test("test_getrawmempool_valid"))
runner = unittest.TextTestRunner()
runner.run(suite)
"""