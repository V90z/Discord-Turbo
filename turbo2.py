#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from time import sleep
from io import BytesIO
from threading import Thread
from random import getrandbits
from ipaddress import IPv4Address
from colorama import init

import json, requests
import random, certifi, os, pycurl

spinners = ["/", "-", "\\", "|"]
dir_path = os.path.dirname(os.path.realpath(__file__))
DISCORD_WEBHOOK_URL = "https://discordapp.com/api/webhooks/738425869948682320/ZPUV_q8d-lDryiROKaK4iMtwfnTnb-F3je9uwUk6e1gA-9GO71Ew6epKQ74T6TRNphSB"
bad_responses = [
    "/challenge/", # Account is email/phone locked
    "consent_required", # Most likely GDPR
    "feedback_required", # Spamblock :(
    "login_required",
    "few minutes",# Expired/invalid/revoked session
    "nother account" # Fucked up fucked up fucked up
]

ERROR = "[\x1b[31m-\x1b[39m]"
WHITE = "\033[1;37;40m"
BLUE = "\033[1;36;40m"
SUCCESS = "[\x1b[32m+\x1b[39m]"
INFO = "[\x1b[33m?\x1b[39m]"
INPUT = "[\x1b[35m*\x1b[39m]"

with open(os.getcwd() + '/sessions.txt', 'r') as fd:
    accountpool = fd.read().splitlines()

def discord(username, attempt):
    return "nonce" in http_request(DISCORD_WEBHOOK_URL, [
        "Accept: */*",
        "User-Agent: Turbo/v1",
        "Content-Type: application/json",
        "Authorization: "
    ], json.dumps({
        "embed":
        {
            "title": "S",
            "description": "uh",
            "color": 1193835,
            "fields": [
            {
                "name": "Username",
                "value": username,
                "inline": True
            },
            {
                "name": "Attempts",
                "value": "{:,}".format(attempt),
                "inline": True
            }],
            "thumbnail":
            {
                "url": "https://imgur.com/APs8FWn.gif"
            },
            "footer":
            {
                "text": "arab#0002",
                "icon_url": "https://imgur.com/rqOqDbN"
            }
        }
    }))

def http_request(url, headers, data=None, proxy=None):
    curl = pycurl.Curl()
    response = b''

    curl.setopt(pycurl.URL, url)
    # curl.setopt(pycurl.WRITEDATA, response)
    curl.setopt(pycurl.HTTPHEADER, headers)

    if data:
        curl.setopt(pycurl.POST, True)
        curl.setopt(pycurl.POSTFIELDS, data)

    if proxy:
        curl.setopt(pycurl.PROXY, proxy)
        curl.setopt(pycurl.CONNECTTIMEOUT, 1)
        curl.setopt(pycurl.PROXYTYPE, pycurl.PROXYTYPE_HTTP)

    try:
        response = curl.perform_rb()
    except:
        pass
    finally:
        curl.close()

    return response.decode("utf-8")

class Instagram(object):
    def __init__(self):
        super(Instagram, self).__init__()
        self.claimed = False
        self.running = True
        self.attempts = 0
        self.rl = 0.0
        self.rs = 0

    def random_session(self):
        # username:password
        return random.choice(self.sessions).split(":")

    def remove_session(self, session):
        if session not in self.sessions:
            return

        self.sessions.remove(session)

        if len(self.sessions) == 0:
            self.running = False
            return

        print("\n".join(self.sessions), file=open(dir_path + "/sessions.txt".format(dir_path), "w"))

    def check_username(self, username):
        session = self.random_session()
        response = http_request("https://i.instagram.com/api/v1/accounts/set_username/", [
            "Accept: */*",
            "User-Agent: Instagram 5.9.2 Android (29/10; 420dpi; 1080x1794; Google/google; Android SDK built for x86_64; generic_x86_64; ranchu; en_US; 132081655)",
            "Content-Type: application/x-www-form-urlencoded; charset=UTF-8",
            "Cookie: sessionid=" + session[4]
        ], "username=" + username, random.choice(self.proxies))

        if not response:
            return False

        if "This username isn't available. Please try another." in response:
            print("{} This user is swappable. \n".format(SUCCESS))
        elif "This username isn't available." in response:
            print("{} This user isn't swappable. \n".format(ERROR))

            return False

    def claim_username(self, username):
        session = self.random_session()
        response = http_request("https://i.instagram.com/api/v1/accounts/set_username/", [
            "Accept: */*",
            "Accept-Language: en-US",
            "User-Agent: Instagram 5.9.2 Android (29/10; 420dpi; 1080x1794; Google/google; Android SDK built for x86_64; generic_x86_64; ranchu; en_US; 132081655)",
            "Content-Type: application/x-www-form-urlencoded; charset=UTF-8",
            "Cookie: sessionid=" + session[4]
        ], "username=" + username, random.choice(self.proxies))
        #print(response)
        if not response:
            return False


        if "isn't" in response:
            self.attempts += 1
        elif "few minutes" in response:
            self.rl += 1
        elif "\"status\": \"ok\"" in response:
            self.email = session[2]
            self.passw = session[1]
            self.id = session[4]
            return True
        elif any(i in response for i in bad_responses):
            self.remove_session(":".join(session))

        return False


class Turbo(Thread):
    def __init__(self, instagram, target):
        super(Turbo, self).__init__()
        self.instagram = instagram
        self.target = target

    def run(self):
        while self.instagram.running:
            if self.instagram.claim_username(self.target):
                self.instagram.claimed = True
                self.instagram.running = False

            sleep(0.001)

class RequestsPS(Thread):
    def __init__(self, instagram):
        super(RequestsPS, self).__init__()
        self.instagram = instagram

    def run(self):
        while self.instagram.running:
            before = self.instagram.attempts
            sleep(1) # Wait 1 second, calculate the difference
            self.instagram.rs = self.instagram.attempts - before

if __name__ == "__main__":
    instagram = Instagram()
    print("{}{} Sai's Instagram Target Turbo\n".format(WHITE, SUCCESS))
    print("{} Sessions loaded: {}{}{}\r\n".format(SUCCESS, BLUE, len(accountpool), WHITE))
    try:
        instagram = Instagram()
        instagram.sessions = [i.strip() for i in open(dir_path + "/sessions.txt", "r") if i]
        instagram.proxies = [i.strip() for i in open(dir_path + "/proxies.txt", "r") if i]
    except Exception as ex:
        print(ex)
        exit(1)

    threads = int(input("{} Threads: ".format(INPUT)))
    target = input("{} Target: ".format(INPUT)).strip().lower()
    instagram.check_username(target)
    pycurl.global_init(pycurl.GLOBAL_ALL)

    for _ in range(threads):
        thread = Turbo(instagram, target)
        thread.setDaemon(True)
        thread.start()

    rs_thread = RequestsPS(instagram)
    rs_thread.setDaemon(True)
    rs_thread.start()

    print("\n{} All threads successfully initialized".format(SUCCESS))

    try:
        while instagram.running:
            for spinner in spinners:
                print("[\x1b[33m{}\x1b[37m] {:,} attempts | RL: {:,} | R/s: {:,}".format(spinner, instagram.attempts, instagram.rl, instagram.rs), end="\r", flush=True)
                sleep(0.1) # Update attempts every 100ms
    except KeyboardInterrupt:
        instagram.running = False
        print("\r{} Turbo stopped, exiting after {:,} attempts...".format(ERROR, instagram.attempts))
        pass

    if instagram.claimed:
        print("\r{} Claimed username \x1b[32m@{}\x1b[37m after \x1b[32m{:,}\x1b[37m attempts".format(SUCCESS, target, instagram.attempts + 1))
        discord(target, instagram.attempts + 1)
        print("{} Account that claimed: \x1b[32m{}\x1b[37m".format(INFO, instagram.id))
        print(f"{SUCCESS} password: {instagram.passw}")
    elif len(instagram.sessions) == 0:
        print("\r{} Ran out of accounts after \x1b[31m{:,}\x1b[37m attempts".format(ERROR, instagram.attempts))

    sleep(0.1)
    pycurl.global_cleanup()
