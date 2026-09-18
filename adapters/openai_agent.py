"""OpenAI Agents SDK adapter for chithra-portfolio-agent"""

SYSTEM_PROMPT = """You are chithra-portfolio-agent, the AI representative of Chithra R's
personal developer portfolio. Present her education, projects, skills, internships,
and achievements accurately. Ground all responses in portfolio data. Route contact
inquiries to LinkedIn, GitHub, or email. Never fabricate credentials."""

TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "profile_retriever",
            "description": "Retrieve Chithra R's structured profile data",
            "parameters": {
                "type": "object",
                "properties": {
                    "detail_level": {"type": "string", "enum": ["summary", "full"]}
                }
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "project_navigator",
            "description": "List or describe portfolio projects",
            "parameters": {
                "type": "object",
                "properties": {
                    "project_name": {"type": "string"},
                    "domain": {"type": "string", "enum": ["web", "ml", "all"]}
                }
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "contact_router",
            "description": "Route contact inquiries to the correct channel",
            "parameters": {
                "type": "object",
                "properties": {
                    "inquiry_type": {"type": "string", "enum": ["hiring", "collaboration", "general", "technical"]}
                },
                "required": ["inquiry_type"]
            }
        }
    }
]

def export_openai_spec():
    return {"system_prompt": SYSTEM_PROMPT, "tools": TOOLS, "model": "gpt-4o-mini"}
