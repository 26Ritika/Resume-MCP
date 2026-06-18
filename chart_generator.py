import matplotlib
matplotlib.use("Agg")  # non-interactive backend, needed for server use
import matplotlib.pyplot as plt
import os


def generate_gap_chart(analysis: dict, output_path: str) -> str:
    """
    Create a horizontal bar chart showing matched vs missing skills.

    analysis: dict returned by matcher.analyze_match()
    output_path: where to save the PNG
    Returns: the output_path
    """
    matched = analysis["matched_skills"]
    missing = analysis["missing_skills"]

    labels = matched + missing
    colors = ["#4CAF50"] * len(matched) + ["#E53935"] * len(missing)
    values = [1] * len(labels)  # presence indicator

    if not labels:
        labels = ["No skills detected"]
        colors = ["#9E9E9E"]
        values = [1]

    fig, ax = plt.subplots(figsize=(8, max(3, len(labels) * 0.4)))
    y_pos = range(len(labels))

    ax.barh(y_pos, values, color=colors)
    ax.set_yticks(y_pos)
    ax.set_yticklabels(labels)
    ax.set_xticks([])
    ax.invert_yaxis()
    ax.set_title(
        f"Resume vs JD Skill Match — {analysis['similarity_score']}% semantic similarity\n"
        f"({analysis['matched_count']}/{analysis['jd_skill_count']} JD skills matched)"
    )

    # Legend
    matched_patch = plt.Rectangle((0, 0), 1, 1, fc="#4CAF50")
    missing_patch = plt.Rectangle((0, 0), 1, 1, fc="#E53935")
    ax.legend(
        [matched_patch, missing_patch],
        ["Matched skill", "Missing skill (in JD, not in resume)"],
        loc="lower right",
    )

    plt.tight_layout()
    os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)
    plt.savefig(output_path, dpi=120)
    plt.close(fig)

    return output_path
