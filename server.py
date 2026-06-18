"""
server.py
MCP server exposing resume-vs-job-description matching tools.

Tools:
- match_score: semantic similarity + skill overlap between resume & JD
- generate_gap_chart: visual chart of matched/missing skills
- suggest_bullet_points: suggest resume bullet phrasing for missing skills
"""

import os
from mcp.server.fastmcp import FastMCP
from matcher import analyze_match
from chart_generator import generate_gap_chart

mcp = FastMCP("resume-matcher")

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "output")


@mcp.tool()
def match_score(resume_text: str, job_description: str) -> dict:
    """
    Compare a resume against a job description.

    Returns semantic similarity score (0-100), matched skills,
    missing skills (present in JD but not resume), and extra skills
    (in resume but not required by JD).
    """
    return analyze_match(resume_text, job_description)


@mcp.tool()
def generate_gap_chart_tool(resume_text: str, job_description: str, filename: str = "gap_chart.png") -> str:
    """
    Generate a visual bar chart showing which JD-required skills are
    present (green) or missing (red) in the resume.

    Returns the file path to the generated PNG image.
    """
    analysis = analyze_match(resume_text, job_description)
    output_path = os.path.join(OUTPUT_DIR, filename)
    return generate_gap_chart(analysis, output_path)


@mcp.tool()
def suggest_bullet_points(missing_skills: list[str], experience_summary: str) -> str:
    """
    Given a list of missing skills and a summary of the user's actual
    experience, suggest how to phrase resume bullet points to highlight
    relevant (even tangential) experience with those skills.

    Note: This tool returns a structured prompt; the calling model (Claude)
    should use it to generate the actual bullet suggestions based on the
    user's real project history.
    """
    skills_str = ", ".join(missing_skills) if missing_skills else "none"
    return (
        f"The job description requires these skills not currently visible "
        f"on the resume: {skills_str}.\n\n"
        f"Here is a summary of the candidate's actual experience:\n"
        f"{experience_summary}\n\n"
        f"For each missing skill, suggest a resume bullet point ONLY if there is "
        f"genuine relevant experience to highlight (do not fabricate experience). "
        f"If no relevant experience exists for a skill, note it as a learning gap instead."
    )


if __name__ == "__main__":
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    mcp.run()
