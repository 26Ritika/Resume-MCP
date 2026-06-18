"""
test_local.py
Quick local test of the matching + chart generation logic,
without going through the MCP server.
"""

from matcher import analyze_match
from chart_generator import generate_gap_chart

SAMPLE_RESUME = """
I am a beginner ML engineer with experience building full-stack AI
applications. I have worked with Python, FastAPI, React, PostgreSQL,
LangChain, and the Gemini API. I built a real-time interview coach using
WebSockets and trained ensemble models with scikit-learn. I am
comfortable with Docker and have deployed projects to Railway and Vercel.
I also practice data structures and algorithms on LeetCode.
"""

SAMPLE_JD = """
We are looking for a Machine Learning Engineer with strong Python skills.
Experience with PyTorch or TensorFlow, deep learning, and NLP is required.
Familiarity with AWS, Docker, Kubernetes, and CI/CD pipelines is a plus.
Knowledge of system design and data structures and algorithms is expected.
"""

if __name__ == "__main__":
    print("Analyzing resume vs job description...\n")
    result = analyze_match(SAMPLE_RESUME, SAMPLE_JD)

    print(f"Similarity score: {result['similarity_score']}%")
    print(f"Matched skills ({result['matched_count']}): {result['matched_skills']}")
    print(f"Missing skills: {result['missing_skills']}")
    print(f"Extra skills: {result['extra_skills']}")

    chart_path = generate_gap_chart(result, "output/gap_chart.png")
    print(f"\nChart saved to: {chart_path}")
