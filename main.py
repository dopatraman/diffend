import openai

client = openai.OpenAI()

tools = [
    {
        "type": "function",
        "function": {
            "name": "check_if_branch_exists",
            "description": "checks whether a branch exists",
            "parameters": {
                "type": "object",
                "properties": {"branch_name": {"type": "string"}},
                "required": ["branch_name"],
            },
        },
    },
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
    }
]

conversation_history = [
    {"role": "system", "content": "You are an extremely succinct communicator with experience using the Github API."}
]

def add_user_message(content):
    conversation_history.append({"role": "user", "content": content})

def add_assistant_message(content):
    conversation_history.append({"role": "assistant", "content": content})

def call_openai_with_context():
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=conversation_history,
        tools=tools
    )
    message = response.choices[0].message.content
    add_assistant_message(message)
    return response

def run_conversation():
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are an extremely succinct communicator with experience using the Github API."},
            {
                "role": "user",
                "content": "Check if main and prakash-456789 exist.",
            },
        ],
        tools=tools,
    )

    message = response.choices[0].message

    print(message.model_dump_json(indent=2))

    # In real life, the result of the tool call would be appended to the
    # conversation history instead of starting a new conversation with a new
    # system prompt.
    response2 = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You already checked the branches' existence."},
            {"role": "assistant", "content": (
                f"Branch 'main' existence: {True}. "
                f"Branch 'prakash-456789' existence: {True}."
            )},
            {"role": "user", "content": "Now get the diff of the two branches."},
        ],
        tools=tools
    )

    print(response2.choices[0].message.model_dump_json(indent=2))

run_conversation()
