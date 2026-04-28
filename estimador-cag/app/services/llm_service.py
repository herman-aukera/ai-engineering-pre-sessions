from openai import OpenAI
from app.config import settings, get_model_config
from app.context.examples import ESTIMATION_EXAMPLES


def build_system_prompt() -> str:
    examples_text = "\n\n---\n\n".join([
        f"TRANSCRIPCIÓN:\n{ex['meeting_summary']}\n\nESTIMACIÓN GENERADA:\n{ex['estimation']}"
        for ex in ESTIMATION_EXAMPLES
    ])

    return f"""Eres un estimador de software senior con 15 años de experiencia.
Generas estimaciones detalladas basándote en transcripciones de reuniones.

Reglas:
- Desglosa en tareas concretas (horas por tarea)
- Incluye total de horas, equipo recomendado y duración estimada
- Sé realista, no optimista
- Usa markdown para la estimación

Ejemplos de referencia:

{examples_text}"""


def estimate(transcription: str, tier: str = None) -> dict:
    system_prompt = build_system_prompt()
    client, model = get_model_config(tier)

    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"TRANSCRIPCIÓN DE REUNIÓN:\n{transcription}"}
        ],
        temperature=0.3,
        max_tokens=2000
    )

    content = response.choices[0].message.content

    return {
        "estimation": content,
        "model": model,
        "tier": tier or settings.llm_tier,
        "input_tokens": response.usage.prompt_tokens,
        "output_tokens": response.usage.completion_tokens
    }