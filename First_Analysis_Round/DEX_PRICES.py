import requests
from web3 import Web3
import web3
import json
import time
from decimal import Decimal
import csv

# Function to fetch transactions for a given token address
def fetch_transactions(token_address, api_key, start_block, end_block):
    url = f"https://api.gnosisscan.io/api?module=account&action=txlist&startblock={start_block}&endblock={end_block}&address={token_address}&sort=asc&apikey={api_key}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()['result']
    else:
        return None

# Function to fetch transaction data using its hash
def fetch_transaction_data(tx_hash, api_key):
    url = f"https://api.gnosisscan.io/api?module=proxy&action=eth_getTransactionByHash&txhash={tx_hash}&apikey={api_key}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()['result']
    else:
        return None

# Function to decode transaction input data
def decode_transaction_input(web3, contract_abi, input_data):
    contract = web3.eth.contract(abi=contract_abi)
    return contract.decode_function_input(input_data)

# Function to calculate exchange rate
def calculate_exchange_rate(web3,decoded_input, value,methodExecuted):
    sellTokenAddress = decoded_input[1]['path'][0]
    buyTokenAddress = decoded_input[1]['path'][-1]
    if methodExecuted == "<Function swapExactTokensForETH(uint256,uint256,address[],address,uint256)>":
        amountSold = web3.from_wei(decoded_input[1]['amountIn'],'ether')
        amountBought = web3.from_wei(decoded_input[1]['amountOutMin'],'ether')
        ER = amountBought / amountSold if amountSold != 0 else None

        if ER != None:
            return (sellTokenAddress, buyTokenAddress,float(format(ER, '.7g')))
        else:
            return None
    
    elif methodExecuted == "<Function swapExactETHForTokens(uint256,address[],address,uint256)>":
        amountSold = web3.from_wei(value,'ether')
        amountBought = web3.from_wei(decoded_input[1]['amountOutMin'],'ether')
        ER = amountBought / amountSold if amountSold != 0 else None

        if ER != None:
            return (sellTokenAddress, buyTokenAddress,float(format(ER, '.7g')))
        else:
            return None
        
    elif methodExecuted == "Function: swapExactTokensForTokens(uint256 amountIn, uint256 amountOutMin, address[] path, address to, uint256 deadline)":
        amountSold = web3.from_wei(decoded_input[1]['amountIn'],'ether')
        amountBought = web3.from_wei(decoded_input[1]['amountOutMin'],'ether')
        ER = amountBought / amountSold if amountSold != 0 else None

        if ER != None:
            return (sellTokenAddress, buyTokenAddress,float(format(ER, '.7g')))
        else:
            return None
    elif methodExecuted == "Function: swapTokensForExactTokens(uint256 amountOut, uint256 amountInMax, address[] path, address to, uint256 deadline)":
        amountSold = web3.from_wei(decoded_input[1]['amountInMax'],'ether')
        amountBought = web3.from_wei(decoded_input[1]['amountOut'],'ether')
        ER = amountBought / amountSold if amountSold != 0 else None

        if ER != None:
            return (sellTokenAddress, buyTokenAddress,float(format(ER, '.7g')))
        else:
            return None
    elif methodExecuted == "Function: swapTokensForExactETH(uint amountOut, uint amountInMax, address[] calldata path, address to, uint deadline)":
        
        amountSold = web3.from_wei(decoded_input[1]['amountInMax'],'ether')
        amountBought = web3.from_wei(decoded_input[1]['amountOut'],'ether')

        ER = amountBought / amountSold if amountSold != 0 else None

        if ER != None:
            return (sellTokenAddress, buyTokenAddress,float(format(ER, '.7g')))
        else:
            return None
        
    elif methodExecuted == "Function: swapETHForExactTokens(uint amountOut, address[] calldata path, address to, uint deadline)":
        amountSold = web3.from_wei(value,'ether')
        amountBought = web3.from_wei(decoded_input[1]['amountOut'],'ether')
        ER = amountBought / amountSold if amountSold != 0 else None

        if ER != None:
            return (sellTokenAddress, buyTokenAddress,float(format(ER, '.7g')))
        else:
            return None
def main():
    api_key = "censored"
    token_address = "0xb18d4f69627F8320619A696202Ad2C430CeF7C53"
    
    web3 = Web3(Web3.HTTPProvider('https://mainnet.infura.io/v3/YOUR_INFURA_KEY'))
    contract_abi = json.loads('[{"inputs":[{"internalType":"address","name":"_factory","type":"address"},{"internalType":"address","name":"_WETH","type":"address"}],"stateMutability":"nonpayable","type":"constructor"},{"inputs":[],"name":"WETH","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"tokenA","type":"address"},{"internalType":"address","name":"tokenB","type":"address"},{"internalType":"uint256","name":"amountADesired","type":"uint256"},{"internalType":"uint256","name":"amountBDesired","type":"uint256"},{"internalType":"uint256","name":"amountAMin","type":"uint256"},{"internalType":"uint256","name":"amountBMin","type":"uint256"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"addLiquidity","outputs":[{"internalType":"uint256","name":"amountA","type":"uint256"},{"internalType":"uint256","name":"amountB","type":"uint256"},{"internalType":"uint256","name":"liquidity","type":"uint256"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"token","type":"address"},{"internalType":"uint256","name":"amountTokenDesired","type":"uint256"},{"internalType":"uint256","name":"amountTokenMin","type":"uint256"},{"internalType":"uint256","name":"amountETHMin","type":"uint256"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"addLiquidityETH","outputs":[{"internalType":"uint256","name":"amountToken","type":"uint256"},{"internalType":"uint256","name":"amountETH","type":"uint256"},{"internalType":"uint256","name":"liquidity","type":"uint256"}],"stateMutability":"payable","type":"function"},{"inputs":[],"name":"factory","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountOut","type":"uint256"},{"internalType":"uint256","name":"reserveIn","type":"uint256"},{"internalType":"uint256","name":"reserveOut","type":"uint256"}],"name":"getAmountIn","outputs":[{"internalType":"uint256","name":"amountIn","type":"uint256"}],"stateMutability":"pure","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountIn","type":"uint256"},{"internalType":"uint256","name":"reserveIn","type":"uint256"},{"internalType":"uint256","name":"reserveOut","type":"uint256"}],"name":"getAmountOut","outputs":[{"internalType":"uint256","name":"amountOut","type":"uint256"}],"stateMutability":"pure","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountOut","type":"uint256"},{"internalType":"address[]","name":"path","type":"address[]"}],"name":"getAmountsIn","outputs":[{"internalType":"uint256[]","name":"amounts","type":"uint256[]"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountIn","type":"uint256"},{"internalType":"address[]","name":"path","type":"address[]"}],"name":"getAmountsOut","outputs":[{"internalType":"uint256[]","name":"amounts","type":"uint256[]"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountA","type":"uint256"},{"internalType":"uint256","name":"reserveA","type":"uint256"},{"internalType":"uint256","name":"reserveB","type":"uint256"}],"name":"quote","outputs":[{"internalType":"uint256","name":"amountB","type":"uint256"}],"stateMutability":"pure","type":"function"},{"inputs":[{"internalType":"address","name":"tokenA","type":"address"},{"internalType":"address","name":"tokenB","type":"address"},{"internalType":"uint256","name":"liquidity","type":"uint256"},{"internalType":"uint256","name":"amountAMin","type":"uint256"},{"internalType":"uint256","name":"amountBMin","type":"uint256"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"removeLiquidity","outputs":[{"internalType":"uint256","name":"amountA","type":"uint256"},{"internalType":"uint256","name":"amountB","type":"uint256"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"token","type":"address"},{"internalType":"uint256","name":"liquidity","type":"uint256"},{"internalType":"uint256","name":"amountTokenMin","type":"uint256"},{"internalType":"uint256","name":"amountETHMin","type":"uint256"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"removeLiquidityETH","outputs":[{"internalType":"uint256","name":"amountToken","type":"uint256"},{"internalType":"uint256","name":"amountETH","type":"uint256"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"token","type":"address"},{"internalType":"uint256","name":"liquidity","type":"uint256"},{"internalType":"uint256","name":"amountTokenMin","type":"uint256"},{"internalType":"uint256","name":"amountETHMin","type":"uint256"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"removeLiquidityETHSupportingFeeOnTransferTokens","outputs":[{"internalType":"uint256","name":"amountETH","type":"uint256"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"token","type":"address"},{"internalType":"uint256","name":"liquidity","type":"uint256"},{"internalType":"uint256","name":"amountTokenMin","type":"uint256"},{"internalType":"uint256","name":"amountETHMin","type":"uint256"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"},{"internalType":"bool","name":"approveMax","type":"bool"},{"internalType":"uint8","name":"v","type":"uint8"},{"internalType":"bytes32","name":"r","type":"bytes32"},{"internalType":"bytes32","name":"s","type":"bytes32"}],"name":"removeLiquidityETHWithPermit","outputs":[{"internalType":"uint256","name":"amountToken","type":"uint256"},{"internalType":"uint256","name":"amountETH","type":"uint256"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"token","type":"address"},{"internalType":"uint256","name":"liquidity","type":"uint256"},{"internalType":"uint256","name":"amountTokenMin","type":"uint256"},{"internalType":"uint256","name":"amountETHMin","type":"uint256"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"},{"internalType":"bool","name":"approveMax","type":"bool"},{"internalType":"uint8","name":"v","type":"uint8"},{"internalType":"bytes32","name":"r","type":"bytes32"},{"internalType":"bytes32","name":"s","type":"bytes32"}],"name":"removeLiquidityETHWithPermitSupportingFeeOnTransferTokens","outputs":[{"internalType":"uint256","name":"amountETH","type":"uint256"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"tokenA","type":"address"},{"internalType":"address","name":"tokenB","type":"address"},{"internalType":"uint256","name":"liquidity","type":"uint256"},{"internalType":"uint256","name":"amountAMin","type":"uint256"},{"internalType":"uint256","name":"amountBMin","type":"uint256"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"},{"internalType":"bool","name":"approveMax","type":"bool"},{"internalType":"uint8","name":"v","type":"uint8"},{"internalType":"bytes32","name":"r","type":"bytes32"},{"internalType":"bytes32","name":"s","type":"bytes32"}],"name":"removeLiquidityWithPermit","outputs":[{"internalType":"uint256","name":"amountA","type":"uint256"},{"internalType":"uint256","name":"amountB","type":"uint256"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountOut","type":"uint256"},{"internalType":"address[]","name":"path","type":"address[]"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"swapETHForExactTokens","outputs":[{"internalType":"uint256[]","name":"amounts","type":"uint256[]"}],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountOutMin","type":"uint256"},{"internalType":"address[]","name":"path","type":"address[]"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"swapExactETHForTokens","outputs":[{"internalType":"uint256[]","name":"amounts","type":"uint256[]"}],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountOutMin","type":"uint256"},{"internalType":"address[]","name":"path","type":"address[]"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"swapExactETHForTokensSupportingFeeOnTransferTokens","outputs":[],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountIn","type":"uint256"},{"internalType":"uint256","name":"amountOutMin","type":"uint256"},{"internalType":"address[]","name":"path","type":"address[]"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"swapExactTokensForETH","outputs":[{"internalType":"uint256[]","name":"amounts","type":"uint256[]"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountIn","type":"uint256"},{"internalType":"uint256","name":"amountOutMin","type":"uint256"},{"internalType":"address[]","name":"path","type":"address[]"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"swapExactTokensForETHSupportingFeeOnTransferTokens","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountIn","type":"uint256"},{"internalType":"uint256","name":"amountOutMin","type":"uint256"},{"internalType":"address[]","name":"path","type":"address[]"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"swapExactTokensForTokens","outputs":[{"internalType":"uint256[]","name":"amounts","type":"uint256[]"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountIn","type":"uint256"},{"internalType":"uint256","name":"amountOutMin","type":"uint256"},{"internalType":"address[]","name":"path","type":"address[]"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"swapExactTokensForTokensSupportingFeeOnTransferTokens","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountOut","type":"uint256"},{"internalType":"uint256","name":"amountInMax","type":"uint256"},{"internalType":"address[]","name":"path","type":"address[]"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"swapTokensForExactETH","outputs":[{"internalType":"uint256[]","name":"amounts","type":"uint256[]"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountOut","type":"uint256"},{"internalType":"uint256","name":"amountInMax","type":"uint256"},{"internalType":"address[]","name":"path","type":"address[]"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"swapTokensForExactTokens","outputs":[{"internalType":"uint256[]","name":"amounts","type":"uint256[]"}],"stateMutability":"nonpayable","type":"function"},{"stateMutability":"payable","type":"receive"}]')  # Replace with actual contract ABI
    print("started")

    currentStartBlock = 14061900
    blockIncrement = 100000
    endBlock = 32000000

    with open('transaction_data.csv', 'w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=['tx_hash', 'token_sold', 'token_bought', 'exchange_rate', 'timeStamp', 'block_number'])
        writer.writeheader()

        while currentStartBlock <= endBlock:
            print(currentStartBlock)
            transactions = fetch_transactions(token_address, api_key, currentStartBlock, currentStartBlock + blockIncrement)
            print(f'transaction length: {len(transactions)}')
            if transactions:
                for tx in transactions:
                    input_data = tx['input']
                    try:
                        decoded_input = decode_transaction_input(web3, contract_abi, input_data)
                        methodExecuted = str(decoded_input[0])
                        if methodExecuted[10:14]=="swap": 
                            
                            value = Decimal(tx['value'])
                            exchange_rate = calculate_exchange_rate(web3,decoded_input, value, methodExecuted)
                            if exchange_rate is not None:
                                transaction_info = {'tx_hash': tx['hash'], 'token_sold': exchange_rate[0], 'token_bought': exchange_rate[1], 'exchange_rate': exchange_rate[2], 'timeStamp': tx['timeStamp'], 'block_number': tx['blockNumber']}
                                writer.writerow(transaction_info)
                                # print(f"Transaction Hash: {tx['hash']}, Token Sold: {exchange_rate[0]}, Token Bought: {exchange_rate[1]}, Exchange Rate: {exchange_rate[2]}, timeStamp: {tx['timeStamp']}, block_number: {tx['blockNumber']}")
                    except Exception as e:
                        print(f"Error in transaction {tx['hash']}: {e}")
            currentStartBlock += blockIncrement + 1
            # print(f'current start block: {currentStartBlock}')

    print("done")

        
if __name__ == "__main__":
    main()