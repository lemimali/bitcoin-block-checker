# Bitcoin Block Checker

I watched some videos about Bitcoin mining and got interested to know more on how this stuff actually works.
After some more research I thought it would be fun to create my own block verifier. So here it is :)

How it works:

Program calculates the hash and checks if it matches with the hash the block creator has sent.
It also checks if creators hash value is equal or smaller than target bits value.
Program needs block's hash as a parameter to make the needed work. Best way to get a hash is to go to
blockchain.com's explorer section and choose a block from there. Then copy hash value from block's info page.

For example:

Go to https://www.blockchain.com/btc/block/0 and copy Hash value to your clipboard.

After that just run the program: python BitcoinBlockChecker.py <hash_value>
