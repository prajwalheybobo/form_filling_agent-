# # from qwen_agent.llm.base import LLM
# # from vllm import AsyncLLMEngine

# # class VLLMWrapper(LLM):
# #     def __init__(self, engine: AsyncLLMEngine):
# #         self.engine = engine

# #     async def generate(self, prompt, **kwargs):
# #         # For non-streaming generation
# #         result = await self.engine.generate(prompt, **kwargs)
# #         return result[0].outputs[0].text

# #     async def stream(self, prompt, **kwargs):
# #         # Streaming responses
# #         async for out in self.engine.stream(prompt, **kwargs):
# #             yield out.outputs[0].text


# from qwen_agent.llm.base import LLM
# from vllm import AsyncLLMEngine


# class VLLMWrapper(LLM):
#     def __init__(self, engine: AsyncLLMEngine):
#         self.engine = engine

#     async def generate(self, prompt, **kwargs):
#         """Non-streaming generation."""
#         result = await self.engine.generate(prompt, **kwargs)
#         return result[0].outputs[0].text

#     async def stream(self, prompt, **kwargs):
#         """Streaming generation."""
#         async for out in self.engine.stream(prompt, **kwargs):
#             yield out.outputs[0].text
