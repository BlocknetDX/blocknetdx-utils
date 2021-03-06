## BlocknetDX Utils Recent Changelog

- Re-enabled some skipped tests.
- Log files are now always written to the relative log folder (support platform independent paths).
- Code cleanings.
- Added unit tests for dxGetOrderbook.
- Added unit tests for dxGetTradeHistory.


# Running the tests

1. Make sure your wallet is encrypted.

2. Update the tests.conf file with your credential parameters, and adjust the options to control some
behaviors of the program.

    - If some required parameters are not filled, the program will stop.
    - Also set the number of runs you want launch by default, when command line parameters are not provided.
    - Make sure the **tests.conf** file is in the same directory as the main program.
    - Some APIs require the wallet decryption passphrase, so fill the appropriate field in the tests.conf file. If this field is not set or the supplied passphrase is not correct, the relevant tests will be either skipped or will fail.

3. Run the python with or without the optional parameters.

    - If you don't specify the optional parameters, those in the **tests.conf** file will be used.
    - If you specify them, they have priority over the ones in the **tests.conf** file.

```
python build_time_tests.py
python build_time_tests.py --unittest=10 --sequence=100
```

4. Check the logs (log and Excel files) to analyze results.
The console will wrongly show assertions errors. These can be safely ignored.

# Tests.conf file

- Remark ! ** Do not put quotes ** when you input the parameters.

```
[CONNECTION]
IP = 127.0.0.1:41414
LOGIN = Your_login
PASSWORD = Your_password

[WALLET]
wallet_decryption_passphrase = mypwd

[OUTPUT]
LOG_DIR = C:\Users\...\Blocknet_unit_tests\test_outputs\

[DEFAULT_NUMBER_OF_RUNS]
SEQUENCE_TESTS_NB_OF_RUNS = 1
UNIT_TESTS_NB_OF_RUNS = 10
SUB_TESTS_NB_OF_RUNS = 10
MAX_CHAR_LENGTH_TO_DISPLAY = 50
```

# Tests.conf recommendations

- If you want for example run only unittests, just put **--unittest=10 --sequence=0**.
or set them accordingly in the **tests.conf** file.
- Do not set the unittest parameter too high, because subtests are automatically generated from some unit test groups ; the number of subtests will therefore increase exponentially as the parameter is increased.
- set **MAX_CHAR_LENGTH_TO_DISPLAY=50** if you want to maintain clarity in the log file. Set **MAX_CHAR_LENGTH_TO_DISPLAY = 0** if you don't want the test suite to output the parameters
in case of assertion errors or other errors.


# Optional command-Line options for build-time automation

All arguments are optional.- Use *-s* or *--sequence* argument to specify the number of sequence tests to run.- Use *-u* or *--unittest* argument to specify the number of unit tests to run.You can avoid using these parameters if you set the **tests.conf** file properly.

# Requirements

- This code won't run on Python < 3.4 because of the use of subtests and exception chaining.

# Testing model

- The code uses randomness to generate various groups of data and scenarios and mix them together (valid, invalid, out-of-bounds data).
So the longer the tests are run, the better.

- It is therefore **strongly** advised to run these tests continuously for days to let the program generate a very high number of combinations of scenarios.

- It would also be advisable to run them on a periodic basis. Because the newly run tests will *always* be different from the previous ones (due to the randomness nature).

- Randomness is used for the following variables:
  - call order in the sequence.
  - size of parameters sent to the API.
  - content type (hexadecimal, numeric, alpha-numeric, garbage data, or a mix of them).
  - valid / invalid nature of parameter.

# Testing groups

- Unit tests for each API.
- Various random multi API sequences.

# Program outputs

- A log file will be generated reporting all errors. It will also tell you the number of tests run, and the number of assertions errors.
- Sequence tests generate an Excel file with the timing distribution.
- If the walletpassphrase unit tests run, you will also see some dumped wallet.dat files.


# Current known issues

- Popups will appear when using the client.
- Some APIs require the returned values to be reviewed, so that the assertion tests are tightened.

# TODO

- Add unit tests with valid data present in the dex once it's loaded.
- Running tests and analyzing results.
- When the code of the RPC calls are settled, apply the same structure for the client.
- Documentation.


