#!/usr/bin/env python3

import os
import shlex
import random
import string



# Test input generation

def random_string(r = range(0, 12)):
    return ''.join(random.choice(string.ascii_lowercase) for _ in range(random.choice(r)))

def generate_random_json_inputs(n = 5):
    header = "{'username': '"
    middle = "', 'password': '"
    footer = "'}"
    return [(header + random_string() + middle + random_string() + footer) for _ in range(n)]

def generate_random_http_inputs(n = 5):
    header = "GET /echo?a="
    middle = "&b="
    footer = " HTTP/1.1\r\nHost: reqbin.com\r\nAccept: */*"
    return [(header + random_string() + middle + random_string() + footer) for _ in range(n)]

def generate_random_long_http_inputs(n = 5):
    inputs = []
    for _ in range(n):
        username = random_string(range(4, 12))
        password = random_string(range(6, 18))
        user_agent_version = random.choice(string.digits) + "." + random.choice(string.digits)
        payload = "username=" + username + "&password=" + password
        inputs.append("POST /cgi-bin/process.cgi HTTP/1.1\r\nUser-Agent: Mozilla/" + user_agent_version + "\r\nHost: 10.60.0.1\r\nContent-Type: application/x-www-form-urlencoded\r\nContent-Length: " + str(len(payload)) + "\r\nAccept-Language: en-us\r\nAccept-Encoding: gzip, deflate\r\nConnection: Keep-Alive\r\n\r\n" + payload)
    return inputs


def generate_bad_random_long_http_inputs(n = 5):
    inputs = []
    for _ in range(n):
        username = random_string(range(4, 12))
        password = "' OR 1=1; --"
        user_agent_version = "5.6"
        payload = "username=" + username + "&password=" + password
        inputs.append("POST /cgi-bin/process.cgi HTTP/1.1\r\nUser-Agent: Mozilla/" + user_agent_version + "\r\nHost: 10.60.0.1\r\nContent-Type: application/x-www-form-urlencoded\r\nContent-Length: " + str(len(payload)) + "\r\nAccept-Language: en-us\r\nAccept-Encoding: br, gzip, deflate\r\nConnection: Keep-Alive\r\n\r\n" + payload)
    return inputs



def main():
    # inputs = "\n".join(generate_random_json_inputs(1000))
    # print(inputs)
    inputsA = generate_random_long_http_inputs(100)
    # Write inputs to tests/long_http_200 ffolder, one per file
    for i in range(len(inputsA)):
        with open("tests/long_http_200/" + str(i) + ".txt", "w") as f:
            f.write(inputsA[i])
    inputsB = generate_bad_random_long_http_inputs(100)
    # Write inputs to tests/long_http_200 folder, one per file
    for i in range(len(inputsB)):
        with open("tests/long_http_200/" + str(i + 100) + ".txt", "w") as f:
            f.write(inputsB[i])


if __name__ == "__main__":
    main()