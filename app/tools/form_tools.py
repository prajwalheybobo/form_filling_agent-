# #from qwen_agent.tools import register_tool
# #from qwen_agent.tools import register_tools
# from qwen_agent.tools.base import Tool
# import requests

# NODE_URL = "http://151.243.146.133:3000/v1"   # your NestJS backend

# # @register_tool
# # def getFormData(formKey: str, uniqueId: str):
# #     """Fetch form structure and metadata."""
# #     response = requests.get(f"{NODE_URL}/form/{formKey}/{uniqueId}")
# #     return response.json()


# #@register_tool
# @Tool
# def validate_single_field(session_id: str, field_name: str, field_value: str):
#     """Validate a single field.
#     Args:
#         session_id (str): The session id.
#         field_name (str): The field name.
#         field_value (str): The field value.
#     Returns:
#         { "status":boolean, "message":str, "data":{ validationErrors: List[str], metadata:dict }|None }.
#         status is True means it contains "data" and tool called is success else the tool is failed,
#         data contains the validation errors and metadata
#     """
#     response = requests.post(
#         f"{NODE_URL}/form/transcribe/validate-field",
#         json={"sessionId":session_id,"fieldName":field_name,"fieldValue":field_value}
#     )
#     return response.json()

# #@register_tool
# @Tool
# def validate_form(session_id: str, data:dict):
#     """Validates a form, before save it to backend this tool is called to validate the form data.
#     if it is valid then it will be allowed to save otherwise the again the questions will be asked to user.
#     Args:
#         data (dict): The form data collect from user to validate.
#         session_id (str): The session id.
#     Returns:
#         { "status":boolean, "message":str, "data":{ validationErrors: List[str], metadata:dict }|None }.
#         status is True means it contains "data" and tool called is success else the tool is failed,
#         data contains the validation errors and metadata
#     """
#     response = requests.post(
#         f"{NODE_URL}/form/transcribe/validate-form",
#         json={"data":data,"sessionId":session_id}
#     )
#     return response.json()


# #@register_tool
# @Tool
# def save_form_data(session_id: str, data: dict):
#     """Save form data to backend. but only if it is valid, else return validation error.
#     Args:
#         data (dict): The form data collect from user to validate.
#         session_id (str): The session id.
#     Returns:
#         { "status":boolean, "message":str, "data":{ parsedData:dict }|{ValidationErrors: List[str] }|None }.
#         status is True means it is saved Successfully!, else it contains "ValidationErrors" or tool is failed,
#         data contains the parsed data or validation errors
#     """
#     response = requests.post(
#         f"{NODE_URL}/form/transcribe/save-form",
#         json={"data":data,"sessionId":session_id}
#     )
#     return response.json()


from qwen_agent.tools.base import BaseTool
import requests

NODE_URL = "http://151.243.146.133:3000/v1"   # your NestJS backend


class ValidateSingleFieldTool(BaseTool):
    name = "validate_single_field"
    description = "Validates a single field with backend validation."

    def call(self, session_id: str, field_name: str, field_value: str):
        response = requests.post(
            f"{NODE_URL}/form/transcribe/validate-field",
            json={"sessionId": session_id, "fieldName": field_name, "fieldValue": field_value}
        )
        return response.json()


class ValidateFormTool(BaseTool):
    name = "validate_form"
    description = "Validates the full form before saving."

    def call(self, session_id: str, data: dict):
        response = requests.post(
            f"{NODE_URL}/form/transcribe/validate-form",
            json={"data": data, "sessionId": session_id}
        )
        return response.json()


class SaveFormDataTool(BaseTool):
    name = "save_form_data"
    description = "Saves validated form data to backend."

    def call(self, session_id: str, data: dict):
        response = requests.post(
            f"{NODE_URL}/form/transcribe/save-form",
            json={"data": data, "sessionId": session_id}
        )
        return response.json()
