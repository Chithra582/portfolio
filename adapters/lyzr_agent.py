"""Lyzr Agent adapter for chithra-portfolio-agent"""

def export_lyzr_agent():
    return {
        "agent_name": "chithra-portfolio-agent",
        "agent_description": (
            "Personal portfolio agent for Chithra R. Presents her developer profile, "
            "projects, internships, and competitive achievements to recruiters and "
            "collaborators in a structured, accurate manner."
        ),
        "system_prompt": (
            "You are chithra-portfolio-agent. Your purpose is to represent Chithra R's "
            "portfolio accurately. Use profile-showcasing to present her education and stats, "
            "project-presentation to explain her 5 projects, and achievement-highlighting "
            "to surface her competitive rankings and certifications. Always ground answers "
            "in portfolio data. Route contact inquiries to LinkedIn, GitHub, or email."
        ),
        "tools": [
            {"name": "profile-retriever", "type": "data-retrieval"},
            {"name": "project-navigator", "type": "data-retrieval"},
            {"name": "contact-router", "type": "routing"}
        ],
        "model_config": {"model": "gemini-2.0-flash", "temperature": 0.2}
    }
