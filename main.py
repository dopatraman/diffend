import openai

client = openai.OpenAI()

# Find a way to generate these tool descriptions
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
    },
]

def run_conversation():
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are an extremely succinct communicator with experience using the Github API."},
            {
                "role": "user",
                "content": "I need to get a diff of two branches. Both exist. Get the diff of main and prakash-456789.",
            },
        ],
        tools=tools,
    )

    message = response.choices[0].message

    print(message.model_dump_json(indent=2))

run_conversation()
