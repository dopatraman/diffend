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
        return json.loads(response.text)["files"]
    return None

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

def run_after_diff(diff):
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": f"You are a succinct communicator. You have the diff between two branches. {json.dumps(diff)}. Explain it as concisely as possible."},
            {"role": "user", "content": "Transform your explanation into a JSON where the key is the file name, and the value is a JSON that contains the explanation as well as the text of the diff. Please remove the markdown formatting and just return serializable json."},
        ],
    )
    message = response.choices[0].message
    # print(message.model_dump_json(indent=2))

    response_ = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": f"You are a succinct communicator. You have the diff between two branches. {json.dumps(diff)}. Explain it as concisely as possible."},
            {"role": "user", "content": "Transform your explanation into a JSON where the key is the file name, and the value is a JSON that contains the explanation as well as the text of the diff. Please remove the markdown formatting and just return serializable json."},
            message,
            {"role": "user", "content": "Now group the changes by the type of change performed. Name the type of change performed a phrase that represents the group. Create a JSON where the key is the group name and the value is a list of JSON objects that contain the file names that belong to the group, an explanation, AND the plaintext patch. Please remove the backtick heading from the top of the output."}
        ],
    )
    message_ = response_.choices[0].message
    print(message_.content)

def end_conversation():
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are done with this conversation. It is time to say goodbye."},
        ]
    )
    message = response.choices[0].message
    print(message.model_dump_json(indent=2))

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
                if diff is not None:
                    run_after_diff(diff)
                    return

    end_conversation()

run_conversation()
