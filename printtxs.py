#!/usr/bin/env python3
import csv
import time

from authproxy import AuthServiceProxy

# Set the correct RPC access details below and uncomment:
# a = AuthServiceProxy("http://<username>:<password>@<IP address>:<port>")

START_BLOCK = 493032
NUM_BLOCKS = 144

with open('txs.csv', 'w') as csvfile:
    writer = csv.writer(csvfile)
    csvfile.write(','.join(['block_height', 'txid', 'vsize (bytes)', 'sum_ins (satoshi)', 'sum_outs (satoshi)', 'fee (satoshi)', 'fee_rate (satoshi/vbyte)', 'segwit']) + '\n')
    for b in range(START_BLOCK, START_BLOCK + NUM_BLOCKS):
        print("Processing block at height {}".format(b))
        print("Time: {}".format(time.strftime("%X")))
        block = a.getblock(a.getblockhash(b))

        for tx in block['tx']:
            t = a.getrawtransaction(tx, True)
            coinbase = False
            sum_ins = 0
            for txin in t['vin']:
                if 'coinbase' in txin:
                    coinbase = True
                    break
                sum_ins += a.getrawtransaction(txin['txid'], True)['vout'][txin['vout']]['value']
            sum_ins = int(sum_ins * 10 ** 8)

            sum_outs = 0
            for txout in t['vout']:
                sum_outs += txout['value']

            sum_outs = int(sum_outs * 10 ** 8)
            if not coinbase:
                fees = sum_ins - sum_outs
                fee_rate = fees // t['vsize']
            else:
                fees = 0
                fee_rate = 0

            csvfile.write('{},{},{},{},{},{},{},{}\n'.format(b, t['txid'], t['vsize'], sum_ins, sum_outs, fees, fee_rate, t['hash'] != t['txid']))
