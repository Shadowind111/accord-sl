# -*- coding: utf-8 -*-
"""Gradio batch demonstration for T2-ACCORD-SL (research use only)."""
from __future__ import annotations

import tempfile
from pathlib import Path

import gradio as gr
import pandas as pd

from predict_t2 import score

DISCLAIMER = (
    "Research use only. This demonstration is not a diagnosis, does not replace pathology, "
    "and must not be used for referral, treatment, or discharge decisions. "
    "The fast mode is a reduced two-expert approximation, not the locked five-expert ensemble."
)


def run(file, mode: str):
    if file is None:
        return pd.DataFrame({"message": ["Please upload a CSV file."]}), DISCLAIMER
    df = pd.read_csv(file.name if hasattr(file, "name") else file)
    out = pd.concat([df.reset_index(drop=True), score(df, mode=mode)], axis=1)
    return out, DISCLAIMER


with gr.Blocks(title="T2-ACCORD-SL research demo") as demo:
    gr.Markdown(
        "# T2-ACCORD-SL research demonstration\n"
        "Batch scoring of the 11-item T2 contract plus age. "
        "**Not a medical device; not for clinical use.**"
    )
    with gr.Row():
        inp = gr.File(label="Input CSV", file_types=[".csv"])
        mode = gr.Radio(["fast", "full"], value="fast", label="Mode")
    btn = gr.Button("Score")
    out = gr.Dataframe(label="Scores")
    note = gr.Markdown(DISCLAIMER)
    btn.click(run, inputs=[inp, mode], outputs=[out, note])

if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", server_port=7860)
