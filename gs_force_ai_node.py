from uagents import Agent, Context, Model, Protocol
from pydantic import Field
from ai_engine import UAgentResponse, UAgentResponseType
import os
from os_helpers import load_env_file
from req_helpers import request_ollama

load_env_file(dotenv_path='.env')

AGENT_SEED = os.environ["AGENT_SEED"]
AGENT_MAILBOX_KEY = os.environ["AGENT_MAILBOX_KEY"]

class GsForceAiRequest(Model):
    user_prompt: str = Field(description="Ask AI anything you want")

GsForceAiNode = Agent(
    name="Ollama Agent", 
    seed=AGENT_SEED,
    mailbox=f"{AGENT_MAILBOX_KEY}@https://agentverse.ai")

gs_force_ai_protocol = Protocol("GS Force AI")

@gs_force_ai_protocol.on_message(model=GsForceAiRequest, replies={UAgentResponse})
async def call_gs_node(ctx: Context, sender: str, msg: GsForceAiRequest):
    ctx.logger.info(msg.user_prompt)
    result = request_ollama(prompt=msg.user_prompt)
    raw_result = result['response']
    ctx.logger.info(raw_result)
    await ctx.send(
        sender, UAgentResponse(message=raw_result, type=UAgentResponseType.FINAL)
    )

GsForceAiNode.include(gs_force_ai_protocol, publish_manifest=True)
GsForceAiNode.run()