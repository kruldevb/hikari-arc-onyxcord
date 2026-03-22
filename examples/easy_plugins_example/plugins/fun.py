"""Fun commands plugin."""

import random
import arc

# Create the plugin
fun_plugin = arc.GatewayPlugin("Fun")


@fun_plugin.include
@arc.slash_command("roll", "Roll a dice")
async def roll(
    ctx: arc.GatewayContext,
    sides: arc.Option[int, "Number of sides on the dice"] = 6
):
    """Roll a dice with specified number of sides."""
    result = random.randint(1, sides)
    await ctx.respond(f"🎲 You rolled a {result}!")


@fun_plugin.include
@arc.slash_command("coinflip", "Flip a coin")
async def coinflip(ctx: arc.GatewayContext):
    """Flip a coin."""
    result = random.choice(["Heads", "Tails"])
    await ctx.respond(f"🪙 {result}!")


@fun_plugin.include
@arc.slash_command("8ball", "Ask the magic 8-ball")
async def eightball(
    ctx: arc.GatewayContext,
    question: arc.Option[str, "Your question"]
):
    """Ask the magic 8-ball a question."""
    responses = [
        "Yes, definitely!",
        "It is certain.",
        "Without a doubt.",
        "Ask again later.",
        "Cannot predict now.",
        "Don't count on it.",
        "My sources say no.",
        "Outlook not so good."
    ]
    await ctx.respond(f"🎱 {random.choice(responses)}")
