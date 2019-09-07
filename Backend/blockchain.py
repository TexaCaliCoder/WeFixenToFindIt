import hashlib
import requests
import sys
import time


# leave "Token" keyword and change to your api key below
# You must have a name and be in the right room to mine or you will incur a penalty
api_key = "Token 8271c9035b3a113a16111392722a7bb4d9278a2c"
header_info = {'Authorization': api_key,"Content-Type": "application/json" }

def proof_of_work(last_proof,difficulty):

    coins_mined = requests.get("https://lambda-treasure-hunt.herokuapp.com/api/bc/get_balance/", headers=header_info )
    coin_data = coins_mined.json()
    print(coin_data["messages"])
    print("Starting work on a new proof..")
    proof = 0

    while valid_proof(last_proof, proof,difficulty) is False :
        proof += 1
    print("Found Valid Proof... Attempting to mine...")
    return proof

def valid_proof(last_proof,proof,difficulty):
    
    difficultyZeros = ""
    for x in range(difficulty):
        x = "0"
        difficultyZeros += x

    guess = f'{last_proof}{proof}'.encode()
    guess_hash = hashlib.sha256(guess).hexdigest()
    beginning = guess_hash[0:difficulty]
    if beginning == difficultyZeros:
        return True
    else:
        return False


if __name__ == '__main__':

    while True:

    #   Last proof cooldown 1 sec
        proof_info = requests.get("https://lambda-treasure-hunt.herokuapp.com/api/bc/last_proof/", headers=header_info  )
        data = proof_info.json()
        difficulty = data['difficulty']
        last_proof =  str(data['proof'])
        time.sleep(data['cooldown'])
        new_proof = proof_of_work(last_proof,difficulty)

    #   check if last proof is still the same meaning another miner hasnt submitted a new proof to avoid penalty
        check_proof_info = requests.get("https://lambda-treasure-hunt.herokuapp.com/api/bc/last_proof/", headers=header_info  )
        check_data = check_proof_info.json()
        check_last_proof =  str(check_data['proof'])
        time.sleep(check_data['cooldown'])
        if last_proof == check_last_proof:
            proof_data = {'proof': new_proof}

            # mine_attempt cooldown 15 sec minimum
            mine_attempt = requests.post( "https://lambda-treasure-hunt.herokuapp.com/api/bc/mine/", headers=header_info, json = proof_data)
            mine_attempt_data = mine_attempt.json()
            print("Errors :", mine_attempt_data["errors"])
            print("messages :", mine_attempt_data["messages"])
            time.sleep(mine_attempt_data['cooldown'])