# -*- coding: utf-8 -*-
"""Combined T1/T2 Gradio demonstration (research use only)."""
from __future__ import annotations

import gradio as gr
import pandas as pd

from predict_t1 import score as score_t1
from predict_t2 import score as score_t2

DISCLAIMER = (
    "Research use only. This demonstration is not a diagnosis, does not replace pathology, "
    "and must not be used for referral, treatment, or discharge decisions. "
    "Fast mode uses two experts; full mode uses the locked five-expert ensemble."
)


def run_t1(file, mode):
    if file is None:
        return pd.DataFrame({"message": ["Please upload a T1 CSV."]})
    df = pd.read_csv(file.name if hasattr(file, "name") else file)
    return pd.concat([df.reset_index(drop=True), score_t1(df, mode=mode)], axis=1)


def run_t2(file, mode):
    if file is None:
        return pd.DataFrame({"message": ["Please upload a T2 CSV."]})
    df = pd.read_csv(file.name if hasattr(file, "name") else file)
    return pd.concat([df.reset_index(drop=True), score_t2(df, mode=mode)], axis=1)


with gr.Blocks(title="ACCORD-SL T1/T2 research demo") as demo:
    gr.Markdown(
        "# ACCORD-SL T1/T2 research demonstration\n"
        "**T1** is a low-burden pre-screen; **T2** is specialist-priority scoring. "
        "Not a medical device; not for clinical use."
    )
    with gr.Tab("T1 pre-screen"):
        f1 = gr.File(label="T1 input CSV (20 items + age)", file_types=[".csv"])
        m1 = gr.Radio(["fast", "full"], value="fast", label="Mode")
        b1 = gr.Button("Score T1")
        o1 = gr.Dataframe(label="T1 scores")
        b1.click(run_t1, inputs=[f1, m1], outputs=o1)
    with gr.Tab("T2 specialist priority"):
        f2 = gr.File(label="T2 input CSV (11 items + age)", file_types=[".csv"])
        m2 = gr.Radio(["fast", "full"], value="fast", label="Mode")
        b2 = gr.Button("Score T2")
        o2 = gr.Dataframe(label="T2 scores")
        b2.click(run_t2, inputs=[f2, m2], outputs=o2)
    gr.Markdown(DISCLAIMER)

if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", server_port=7862)
