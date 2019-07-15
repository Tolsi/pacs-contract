# pacs-contract

This is a smart contract for [the Vostok platform](https://vostok.io/), allows you to add authorized persons (for example, employees) and recognize them in photos and save all this information on the blockchain. For example, you can use this information to provide access to some service or secure location. All stages of this check are fully onchain i.e performed by network miners. Also in the repository there is a minimalistic backend for indexing information from the blockchain for the operation of the UI interface and scripts for the test of the contract.

You can build it and push to a local docker repository using

```
docker build -t pacs-contract .
docker image tag pacs-contract 127.0.0.1:5000/pacs-contract
docker push 127.0.0.1:5000/pacs-contract
```

Then you can start your private network, call create contract transaction with this contract, change a little the backend scripts and start it.
