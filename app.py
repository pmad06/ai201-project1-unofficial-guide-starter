"""
app.py
======
Gradio web UI for the UF Unofficial Dining & Meal Plan Guide.

Layout:
  - Text input for the question
  - Submit button
  - Answer text box
  - Sources text box
"""

import gradio as gr
from embed import retrieve
from generate import generate

# ── Core pipeline ─────────────────────────────────────────────────────────────

def ask(query: str):
    """
    Full RAG pipeline: retrieve → generate → return answer + sources.
    Called by the Gradio interface on button click.
    """
    if not query or not query.strip():
        return "Please enter a question.", ""

    # Retrieve top-5 chunks from ChromaDB
    chunks = retrieve(query.strip())

    # Generate answer via Groq
    result = generate(query.strip(), chunks)

    answer  = result["answer"]
    sources = "\n".join(f"• {s}" for s in result["sources"])

    return answer, sources


# ── Gradio UI ─────────────────────────────────────────────────────────────────

with gr.Blocks(title="UF Dining & Meal Plan Guide") as demo:

    gr.Markdown(
        """
        # 🐊 UF Unofficial Dining & Meal Plan Guide
        Ask anything about UF meal plans, on-campus dining, or restaurants near campus.
        Answers are sourced from student articles, reviews, and official UF dining information.
        """
    )

    with gr.Row():
        question_input = gr.Textbox(
            label       = "Your Question",
            placeholder = "e.g. What meal plan should I get as a freshman?",
            lines       = 2,
            scale       = 4,
        )

    ask_btn = gr.Button("Ask", variant="primary")

    with gr.Row():
        answer_output = gr.Textbox(
            label      = "Answer",
            lines      = 8,
            interactive= False,
        )

    with gr.Row():
        sources_output = gr.Textbox(
            label      = "Sources",
            lines      = 4,
            interactive= False,
        )

    # Example questions
    gr.Examples(
        examples=[
            ["What meal plans are available for freshmen at UF?"],
            ["What are the best vegan restaurants near campus?"],
            ["How much does it cost to eat at Broward dining hall?"],
            ["What is the Bite Club meal plan?"],
            ["What off-campus restaurants are near UF?"],
        ],
        inputs=question_input,
    )

    # Wire up button
    ask_btn.click(
        fn      = ask,
        inputs  = [question_input],
        outputs = [answer_output, sources_output],
    )

    # Also trigger on Enter key
    question_input.submit(
        fn      = ask,
        inputs  = [question_input],
        outputs = [answer_output, sources_output],
    )


if __name__ == "__main__":
    demo.launch()