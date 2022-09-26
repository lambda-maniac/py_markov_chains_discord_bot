import discord
import secrets
import json

from markov import *

class Bot (discord.Client):
    prefix      = "markov"
    specials    = specials = { prefix: "eu" }
    punctuation = [".", ",", ":", ";", "!", "?"]

    with open("data.json", "r") as file:
        data = json.loads(''.join(file.readlines()))

        print(f":: Loaded data: {data}")

    async def on_ready(self):
        print(":: Initializing...")

    async def on_message(self, event):
        if event.author.name == self.user.name: return
        
        message = event.content.lower()

        if self.prefix in message:
            await event.channel.send(generate(self.data, self.punctuation))

        self.data = learn(tokenize(message, self.specials, self.punctuation), self.data)

        with open("data.json", "w+") as file:
            file.write(json.dumps(self.data, indent = 4))

    async def exit(self):
        print(":: Closing connection...")
        await self.close()
        print(":: Done.")

if __name__ == '__main__' \
    : Bot().run(secrets.AUTH_TOKEN) ; exit(0)
