import discord
import secrets

from Markov import Chains, Punctuations, Filters

class MarkovBot (discord.Client):
    
    def __init__(self):
        super().__init__(intents = discord.Intents(
            guilds         = True,
            guild_messages = True,
        ))

        self.name               = "Markov"

        self.max_recursion      = 3
        self.discord_char_limit = 2000
        self.punctuations       = Punctuations.default
        self.filters            = Filters.default \
                                + [(r"\bMarkov\b", "eu"), (r"\bmarkov\b", "eu")]

        self.markov_chains = Chains \
            ( self.max_recursion
            , self.discord_char_limit
            , self.punctuations
            , self.filters
            , {}
            , "data.json"
            )

    async def on_ready(self):
        print("Markov: Running...")

    async def on_message(self, event):
        if event.author == self.user: return

        print("=== [Descriptor] ===")

        author   = event.author
        message  = event.content
        channel  = event.channel
        mentions = event.mentions

        print(f"Markov: Received message from \"{author.name}\" at \"{channel.name}\": \"{message}\".")

        if self.name in message \
        or self.user in mentions:
            print("Markov: Mentioned, sending text.")
            await channel.send( self.markov_chains.generate() )

        print(f"Markov: Learning from last message.")
        result = self.markov_chains.feed(message)
        print(f"Markov: Success?={result}")

        print(f"Markov: Saving progress at \"{self.markov_chains.file_name}\".")
        self.markov_chains.save()

if __name__ == "__main__" \
    : MarkovBot().run(secrets.AUTH_TOKEN) ; exit(0)
