import json
import openai
import os
import requests

client = openai.OpenAI()

def check_if_branch_exists(branch_name):
    token = os.environ["GITHUB_API_KEY"]
    if not token:
        raise Exception("You need a Github API Key")
    url = "/repos/dopatraman/diffend/branches/{branch_name}"
    headers = {
        'Authorization': 'token {token}'
    }
    response = requests.get(url, headers=headers)
    if response.status == 200:
        return True
    return False

def get_diff(base, head):
    token = os.environ["GITHUB_API_KEY"]
    if not token:
        raise Exception("You need a Github API Key")
    url = f"https://api.github.com/repos/dopatraman/diffend/compare/{base}...{head}"
    headers = {
        "Authorization": f"token {token}"
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return True
    return False

# Find a way to generate these tool descriptions
tools = [
    {
        "type": "function",
        "function": {
            "name": "get_diff",
            "description": "get a diff of two branches",
            "parameters": {
                "type": "object",
                "properties": {"base": {"type": "string"}, "head": {"type": "string"}},
                "required": ["base", "head"],
            },
        },
    },
]

def run_after_check_branch_exists():
    pass

def run_conversation():
    # Needs to be generated
    tool_lookup = {
        "get_diff": get_diff
    }
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are an extremely succinct communicator with experience using the Github API."},
            {
                "role": "user",
                "content": "I need to get a diff of two branches. Both exist. Get the diff of main and prakash-first-commit.",
            },
        ],
        tools=tools,
    )

    message = response.choices[0].message

    if message.content is None and len(message.tool_calls) > 0:
        for tool_call in message.tool_calls:
            if tool_call.function.name == "get_diff":
                arguments = json.loads(tool_call.function.arguments)
                base = arguments["base"]
                head = arguments["head"]
                diff = tool_lookup["get_diff"](base, head)
        

    print(message.model_dump_json(indent=2))

run_conversation()
