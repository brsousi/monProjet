# -*- coding: utf-8 -*-
"""
Created on Sat Dec 28 20:09:30 2019

@author: brahim
"""
from hashlib import sha256
import json
import time


class Block:
    def __init__(self, index, transactions, timestamp, previous_hash):
        self.index = index
        self.transactions = transactions
        self.timestamp = timestamp
        self.previous_hash = previous_hash
        self.nonce = 0

    def calcul_hash(self):
        """
        la fonction qui renvoie le hachage du bloc.
        """
        block_string = json.dumps(self.__dict__, sort_keys=True)
        return sha256(block_string.encode()).hexdigest()


class Blockchain:
    # La difficulté de preuve de notre travail
    difficulty = 2

    def __init__(self):
        self.unconfirmed_transactions = []
        self.chain = []
        self.create_genesis_block()

    def create_genesis_block(self):
        """
        Une fonction pour générer un bloc de genèse et l'ajouter à
        la chaine. Le bloc a l'index 0, le hashage précedent(previous_hash) comme 0 et un hachage valide.
        """
        genesis_block = Block(0, [], time.time(), "0")
        genesis_block.hash = genesis_block.compute_hash()
        self.chain.append(genesis_block)

    @property
    def last_block(self):
        return self.chain[-1]

    def add_block(self, block, proof):
        """
        Une fonction qui ajoute le bloc à la chaîne après vérification.
        La vérification comprend:
        * Vérification de la validité de la preuve.
        * Le précédent_hash référencé dans le bloc et le hachage du dernier bloc
          dans la chaine
        """
        previous_hash = self.last_block.hash

        if previous_hash != block.previous_hash:
            return False

        if not self.is_valid_proof(block, proof):
            return False

        block.hash = proof
        self.chain.append(block)
        return True

    def is_valid_proof(self, block, block_hash):
        """
        Vérifiez si block_hash est un hachage valide du bloc et a bien satisfait
        les critères de difficulté.
        """
        return (block_hash.startswith('0' * Blockchain.difficulty) and
                block_hash == block.compute_hash())

    def proof_of_work(self, block):
        """
       Fonction qui essaie différentes valeurs de nonce pour obtenir un hachage
       qui répond à nos critères de difficulté.
        """
        block.nonce = 0

        computed_hash = block.compute_hash()
        while not computed_hash.startswith('0' * Blockchain.difficulty):
            block.nonce += 1
            computed_hash = block.compute_hash()

        return computed_hash

    def add_new_transaction(self, transaction):
        self.unconfirmed_transactions.append(transaction)

    def mine(self):
        """
        Cette fonction constitue une interface pour ajouter l'attente
        transactions à la blockchain en les ajoutant au bloc 
        et trouver une preuve de travail
        """
        if not self.unconfirmed_transactions:
            return False

        last_block = self.last_block

        new_block = Block(index=last_block.index + 1,
                          transactions=self.unconfirmed_transactions,
                          timestamp=time.time(),
                          previous_hash=last_block.hash)

        proof = self.proof_of_work(new_block)
        self.add_block(new_block, proof)

        self.unconfirmed_transactions = []
        return new_block.index
