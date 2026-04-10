"""
Functions to display results in the CLI.
"""

header = "# MBQS protocol\n"

protocol_text = [
    "J = {J:.3g} rad / µs",
    "State = {state}",
]

size_text = [
    "L = {L}",
    "Time = {time:.3g} µs",
    "Correlation indices: {corr_idx}",
]

rydberg_text = [
    "Level = {level}",
    "a = {a:.3g} µm",
]

pulses_text = [
    "Ω = {Omega:.3g} rad / µs",
    "δ = {delta:.3g} rad / µs",
]


def join_with_prefix(text_list: list[str], prefix: str) -> str:
    """
    Join a list of strings with a prefix for each item.
    """

    return "\n".join([prefix + text for text in text_list])


def combine_text(protocol_data: dict) -> str:
    """
    Combine the texts for one or several protocols.
    """

    text = header + "\n"
    text += "\n".join(protocol_text).format(**protocol_data)

    if "rydberg" in protocol_data:
        text += "\n\nRydberg data\n"
        text += join_with_prefix(rydberg_text, "- ").format(**protocol_data["rydberg"])

    if "sizes" in protocol_data:
        for size_data in protocol_data["sizes"]:
            text += "\n\n## "
            text += join_with_prefix(size_text, "- ")[2:].format(**size_data)
            if "pulses" in size_data:
                text += "\n- Pulses:\n"
                text += join_with_prefix(pulses_text, "  - ").format(
                    **size_data["pulses"]
                )

    return text


def combine_text_single(protocol_data: dict) -> str:
    """
    Combine the texts for one or several protocols.
    """

    text = header + "\n"
    text += join_with_prefix(protocol_text, "- ").format(**protocol_data)
    text += join_with_prefix(size_text, "- ").format(**protocol_data)

    if "rydberg" in protocol_data:
        text += "\n- Rydberg data:\n"
        text += join_with_prefix(rydberg_text, "  - ").format(
            **protocol_data["rydberg"]
        )
        text += "\n"
        text += join_with_prefix(pulses_text, "  - ").format(**protocol_data["pulses"])

    return text
