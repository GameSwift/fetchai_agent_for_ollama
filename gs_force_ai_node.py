from uagents import Agent, Context, Model, Protocol
from ai_engine import UAgentResponse, UAgentResponseType
from pydantic.v1 import Field
import os
from os_helpers import load_env_file
from req_helpers import request_ollama

load_env_file(dotenv_path='.env')

AGENT_SEED = os.environ["AGENT_SEED"]
AGENT_MAILBOX_KEY = os.environ["AGENT_MAILBOX_KEY"]
OLLAMA_MODEL = os.environ["OLLAMA_MODEL"]
OLLAMA_HOST = os.environ["OLLAMA_HOST"]

class GsForceAiRequest(Model):
    user_prompt: str = Field("What you would like to ask GS Force AI?")

GsForceAiNode = Agent(
    name="GS FORCE AI", 
    seed=AGENT_SEED,
    mailbox=f"{AGENT_MAILBOX_KEY}@https://agentverse.ai")

gs_force_ai_protocol = Protocol(name="GS Force AI", version="0.1")

print("Fetch network address: ", GsForceAiNode.wallet.address())
print("uAgent address: ", GsForceAiNode.address)

@gs_force_ai_protocol.on_message(model=GsForceAiRequest, replies={UAgentResponse})
async def call_gs_node(ctx: Context, sender: str, msg: GsForceAiRequest):
    ctx.logger.info(msg.user_prompt)
    result = request_ollama(prompt=msg.user_prompt, model=OLLAMA_MODEL, host=OLLAMA_HOST)
    raw_result = result['response']
    ctx.logger.info(raw_result)
    await ctx.send(
        sender, UAgentResponse(message=raw_result, type=UAgentResponseType.FINAL)
    )

GsForceAiNode.include(gs_force_ai_protocol, publish_manifest=True)
GsForceAiNode.run()