# from qwen_agent.agents import Agent
# # from qwen_agent.llm import LLM
# from qwen_agent.memory import Memory
# from qwen_agent.prompt import SystemPrompt
# from tools.form_tools import *
# from mongo import MongoMemoryStore
# from tools.llm_wrapper import VLLMWrapper
# import config
# from ..schemas import FormRequest
# from fastapi.responses import StreamingResponse
# # # -------------------------
# # # SETUP LLM + AGENT
# # # -------------------------

# # llm = LLM(
# #     model="qwen2.5-32b-instruct",   
# #     stream=True                   # streaming questions
# # )

# system_prompt = SystemPrompt("""
# You are a Form-Filling Assistant.

# Your job has two responsibilities:

# ======================================================================
# 1) ASK QUESTIONS (One Field at a Time)
# ======================================================================

# You receive:
# - a session_id
# - metadata describing every field in the form
# - a description of the form’s purpose

# For each step, you must output ONE question for the NEXT field only.

# QUESTION RULES:
# - Ask exactly ONE question at a time.
# - The question must be SHORT, SIMPLE, and CLEAR.
# - Use the field metadata (type, required/optional, constraints, enums).
# - If optional → mention the user can skip.
# - If required → ask directly.
# - If enum → present choices naturally.
# - No technical words, no metadata, no explanations.
# - DO NOT output anything except the single question.
# - DO NOT repeat the question.
# - DO NOT generate multiple questions.
# - DO NOT include JSON or metadata in the output.

# ======================================================================
# 2) VALIDATE USER ANSWERS
# ======================================================================

# When the user answers a question:

# You act as a **strict form answer parser**.
# Extract ONLY the value for the current field.

# VALIDATION RULES:
# - Return value must match the field type:
#   - number → return a number
#   - string → return a string
#   - date → return an ISO date
#   - boolean → return true/false
#   - array → return an array
#   - enum → return ONLY one allowed value
# - If the user says “skip”, “none”, "no", “not applicable”:
#   - If optional → return null
#   - If required → return a valid empty fallback (false, "", or null depending on type). DO NOT invent realistic data.

# ======================================================================
# 3) TOOL USAGE FOR VALIDATION
# ======================================================================

# Before accepting a value:
# - Call the validation tool with parsed value and field metadata.
# - If the tool reports the value is valid → accept it.
# - If invalid → ask the SAME field question again.
#   (Still follow the question rules above.)

# ======================================================================
# 4) FORM COMPLETION
# ======================================================================

# After all fields have been individually collected and validated:

# 1. Perform a **final validation of the entire form**:
#    - Call the form validation tool with all collected field values.
#    - If the form is invalid, identify the problematic field(s) and ask the user to correct them one by one.
#    - Continue until the entire form passes validation.

# 2. Once the full form is verified as valid:
#    - Call the backend save tool with the final completed form data.
#    - Output a friendly confirmation message to the user indicating successful submission.

# 3. Restrictions:
#    - Do not display metadata, JSON, or internal reasoning.
#    - Only show validation prompts, correction questions, or final success message.

# ======================================================================
# GLOBAL RESTRICTIONS
# ======================================================================

# - Do NOT output metadata, JSON, or internal reasoning.
# - Do NOT show tool arguments or tool results to the user.
# - Only show:
#   1. A question
#   2. Or a validation message
#   3. Or a final success message after save.
# """)

# engine_args = AsyncEngineArgs(
#         model=config.QWEN_MODEL,
#         tensor_parallel_size=1,
#         gpu_memory_utilization=0.2,
#         trust_remote_code=True,
#     )
    
# llm_engine = AsyncLLMEngine.from_engine_args(engine_args)

# wrapped_llm = VLLMWrapper(llm_engine)

# class LLMService:
#     def __init__(self,session_id):
#         self.llm = wrapped_llm
#         self.agent = Agent(
#             llm=wrapped_llm,
#             system=system_prompt,
#             memory=Memory(store=MongoMemoryStore(session_id=session_id))
#         )

#     def start_form_filling(self, form:FormRequest):
#         """Starts interactive session with the user."""
#         print(f"🔵 Starting form: {form.form_key}, ID: {form.unique_id}")

#         # initial trigger for the agent
#         agent_response = self.agent.run(
#             f"""Start filling the form. formKey={form.form_key}, uniqueId={form.unique_id}.
#             form_metadata={form.form_metadata}
#             form_description={form.form_description}
#             """
#         )
#         return agent_response;
#         # while True:
#         #     for chunk in agent_response:

#         #         if chunk["type"] == "output":
#         #             print(chunk["text"], end="", flush=True)
#         #             yield chunk["text"]

#         #         elif chunk["type"] == "tool_call":
#         #             tool_name = chunk["tool"]
#         #             args = chunk["arguments"]
#         #             print(f"\n🛠 Tool call: {chunk['tool']}")
#         #             # run the tool
#         #             result = run_tool(tool_name, args)

#         #             # Continue agent with tool result
#         #             agent_response = self.agent.run({
#         #                 "tool": tool_name,
#         #                 "result": result
#         #             })
#         #             break  # restart outer while-loop

#         #     else:
#         #         # no more chunks → agent finished
#         #         break

#         # # streaming output loop
#         # for chunk in agent_response:
#         #     if chunk.get("type") == "output":
#         #         print(chunk["text"], end="", flush=True)
#         #     elif chunk.get("type") == "tool_call":
#         #         print(f"\n🛠 Tool call: {chunk['tool']}")
#         #     elif chunk.get("type") == "tool_result":
#         #         print(f"\n📄 Tool result received")

#         # print("\n\n✔️ Form session complete.\n")
#         # return StreamingResponse(agent_stream(), media_type="text/plain")


#     def filling_up_form(self, user_query):
#         agent_response = self.agent.run(user_query)
#         return agent_response
        
# # if __name__ == "__main__":
# #     start_form_filling("registrationForm", "abc-123")


# from qwen_agent.agents import Agent
# from qwen_agent.memory import Memory
# from vllm import AsyncEngineArgs, AsyncLLMEngine

# from ..tools.form_tools import (
#     ValidateSingleFieldTool,
#     ValidateFormTool,
#     SaveFormDataTool,
# )
#         # tools/form_tools.py
# from ..db.mongo import MongoMemoryStore   # db/mongo.py
# from ..services.llm_wrapper import VLLMWrapper
# from ..schemas import FormRequest
# from fastapi.responses import StreamingResponse
# import config

# # -------------------------
# # SYSTEM PROMPT (plain string, no SystemPrompt object)
# # -------------------------

# SYSTEM_PROMPT = """
# You are a Form-Filling Assistant.

# Your job has two responsibilities:

# ======================================================================
# 1) ASK QUESTIONS (One Field at a Time)
# ======================================================================

# You receive:
# - a session_id
# - metadata describing every field in the form
# - a description of the form’s purpose

# For each step, you must output ONE question for the NEXT field only.

# QUESTION RULES:
# - Ask exactly ONE question at a time.
# - The question must be SHORT, SIMPLE, and CLEAR.
# - Use the field metadata (type, required/optional, constraints, enums).
# - If optional → mention the user can skip.
# - If required → ask directly.
# - If enum → present choices naturally.
# - No technical words, no metadata, no explanations.
# - DO NOT output anything except the single question.
# - DO NOT repeat the question.
# - DO NOT generate multiple questions.
# - DO NOT include JSON or metadata in the output.

# ======================================================================
# 2) VALIDATE USER ANSWERS
# ======================================================================

# When the user answers a question:

# You act as a **strict form answer parser**.
# Extract ONLY the value for the current field.

# VALIDATION RULES:
# - Return value must match the field type:
#   - number → return a number
#   - string → return a string
#   - date → return an ISO date
#   - boolean → return true/false
#   - array → return an array
#   - enum → return ONLY one allowed value
# - If the user says “skip”, “none”, "no", “not applicable”:
#   - If optional → return null
#   - If required → return a valid empty fallback (false, "", or null depending on type). DO NOT invent realistic data.

# ======================================================================
# 3) TOOL USAGE FOR VALIDATION
# ======================================================================

# Before accepting a value:
# - Call the validation tool with parsed value and field metadata.
# - If the tool reports the value is valid → accept it.
# - If invalid → ask the SAME field question again.
#   (Still follow the question rules above.)

# ======================================================================
# 4) FORM COMPLETION
# ======================================================================

# After all fields have been individually collected and validated:

# 1. Perform a **final validation of the entire form**:
#    - Call the form validation tool with all collected field values.
#    - If the form is invalid, identify the problematic field(s) and ask the user to correct them one by one.
#    - Continue until the entire form passes validation.

# 2. Once the full form is verified as valid:
#    - Call the backend save tool with the final completed form data.
#    - Output a friendly confirmation message to the user indicating successful submission.

# 3. Restrictions:
#    - Do not display metadata, JSON, or internal reasoning.
#    - Only show validation prompts, correction questions, or final success message.

# ======================================================================
# GLOBAL RESTRICTIONS
# ======================================================================

# - Do NOT output metadata, JSON, or internal reasoning.
# - Do NOT show tool arguments or tool results to the user.
# - Only show:
#   1. A question
#   2. Or a validation message
#   3. Or a final success message after save.
# """

# # -------------------------
# # SETUP VLLM ENGINE + WRAPPER
# # -------------------------

# engine_args = AsyncEngineArgs(
#     model=config.QWEN_MODEL,
#     tensor_parallel_size=1,
#     gpu_memory_utilization=0.2,
#     trust_remote_code=True,
# )

# llm_engine = AsyncLLMEngine.from_engine_args(engine_args)
# wrapped_llm = VLLMWrapper(llm_engine)


# class LLMService:
#     def __init__(self, session_id: str):
#         self.llm = wrapped_llm
#         self.agent = Agent(
#             llm=self.llm,
#             system=SYSTEM_PROMPT,
#             memory=Memory(store=MongoMemoryStore(session_id=session_id)),
#             tools=[
#                 ValidateSingleFieldTool(),
#                 ValidateFormTool(),
#                 SaveFormDataTool(),
#             ],
#         )


#     def start_form_filling(self, form: FormRequest):
#         """Starts interactive session with the user."""
#         print(f"🔵 Starting form: {form.form_key}, ID: {form.unique_id}")

#         agent_response = self.agent.run(
#             f"""Start filling the form. formKey={form.form_key}, uniqueId={form.unique_id}.
#             form_metadata={form.form_metadata}
#             form_description={form.form_description}
#             """
#         )
#         return agent_response

#     def filling_up_form(self, user_query: str):
#         """Continue the form-filling conversation with a user reply."""
#         agent_response = self.agent.run(user_query)
#         return agent_response


from qwen_agent.agents import Agent
from qwen_agent.memory import Memory

from ..tools.form_tools import (
    ValidateSingleFieldTool,
    ValidateFormTool,
    SaveFormDataTool,
)
from ..db.mongo import MongoMemoryStore
from ..schemas import FormRequest
import config

SYSTEM_PROMPT = """
You are a Form-Filling Assistant.

Your job has two responsibilities:

======================================================================
1) ASK QUESTIONS (One Field at a Time)
======================================================================

You receive:
- a session_id
- metadata describing every field in the form
- a description of the form’s purpose

For each step, you must output ONE question for the NEXT field only.

QUESTION RULES:
- Ask exactly ONE question at a time.
- The question must be SHORT, SIMPLE, and CLEAR.
- Use the field metadata (type, required/optional, constraints, enums).
- If optional → mention the user can skip.
- If required → ask directly.
- If enum → present choices naturally.
- No technical words, no metadata, no explanations.
- DO NOT output anything except the single question.
- DO NOT repeat the question.
- DO NOT generate multiple questions.
- DO NOT include JSON or metadata in the output.

======================================================================
2) VALIDATE USER ANSWERS
======================================================================

After each answer:
- Extract ONLY the value for the current field.
- Validate via tool.
- If invalid → ask the SAME field question again.

======================================================================
3) FORM COMPLETION
======================================================================

Once all fields are collected:
- Validate whole form via tool.
- If invalid → ask corrections one by one.
- If valid → call save tool and send final success message.

======================================================================
GLOBAL RESTRICTIONS
======================================================================

- No JSON, no metadata, no reasoning, no internal details.
- Output only a question / validation message / or final success message.
"""

# Qwen-Agent will automatically route to DashScope or OpenAI depending on model name
LLM_CONFIG = {
    "model": config.QWEN_MODEL,
    "model_type": "qwen",
}


class LLMService:
    def __init__(self, session_id: str):
        self.agent = Agent(
            llm=LLM_CONFIG,
            system=SYSTEM_PROMPT,
            memory=Memory(store=MongoMemoryStore(session_id=session_id)),
            tools=[
                ValidateSingleFieldTool(),
                ValidateFormTool(),
                SaveFormDataTool(),
            ],
        )

    def start_form_filling(self, form: FormRequest):
        print(f"🔵 Starting form: {form.form_key}, ID: {form.unique_id}")

        agent_response = self.agent.run(
            f"""Start filling the form. formKey={form.form_key}, uniqueId={form.unique_id}.
            form_metadata={form.form_metadata}
            form_description={form.form_description}
            """
        )
        return agent_response

    def filling_up_form(self, user_query: str):
        agent_response = self.agent.run(user_query)
        return agent_response
