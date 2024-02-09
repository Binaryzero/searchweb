import streamlit as st


def translate_cvss31_vector(cvss_vector):
    explanations = {
        "AV": {
            "N": ("Network", "The vulnerability can be exploited over the network."),
            "A": (
                "Adjacent Network",
                "The attack can be launched from adjacent networks.",
            ),
            "L": ("Local", "The attack is executed locally."),
            "P": ("Physical", "The attack requires physical access to the device."),
        },
        "AC": {
            "L": (
                "Low",
                "Attack complexity is low, meaning the attack can be conducted easily.",
            ),
            "H": (
                "High",
                "Attack complexity is high, requiring more effort from the attacker.",
            ),
        },
        "PR": {
            "N": ("None", "No privileges are required to exploit the vulnerability."),
            "L": ("Low", "Low-level privileges are required."),
            "H": ("High", "High-level privileges are required."),
        },
        "UI": {
            "N": (
                "None",
                "No user interaction is required to exploit the vulnerability.",
            ),
            "R": (
                "Required",
                "User interaction is required to exploit the vulnerability.",
            ),
        },
        "S": {
            "U": (
                "Unchanged",
                "The scope remains unchanged, meaning the exploited vulnerability does not affect resources beyond its security scope.",
            ),
            "C": (
                "Changed",
                "The scope changes, indicating the exploited vulnerability can affect resources beyond its security scope.",
            ),
        },
        "C": {
            "H": (
                "High",
                "Confidentiality impact is high, leading to total information disclosure.",
            ),
            "L": (
                "Low",
                "Confidentiality impact is low, resulting in partial information disclosure.",
            ),
            "N": ("None", "There is no impact on confidentiality."),
        },
        "I": {
            "H": (
                "High",
                "Integrity impact is high, leading to a total compromise of system integrity.",
            ),
            "L": (
                "Low",
                "Integrity impact is low, resulting in partial modification of data.",
            ),
            "N": ("None", "There is no impact on integrity."),
        },
        "A": {
            "H": (
                "High",
                "Availability impact is high, leading to a total shutdown of the affected resource.",
            ),
            "L": (
                "Low",
                "Availability impact is low, resulting in reduced performance.",
            ),
            "N": ("None", "There is no impact on availability."),
        },
    }
    # # Check if the input format is correct
    if not cvss_vector.startswith("CVSS:3.1/"):
        return None, "Invalid format. Please start with 'CVSS:3.1/'"

    metrics = cvss_vector.replace("CVSS:3.1/", "").split("/")
    translated = {}
    for metric in metrics:
        if ":" not in metric:
            return (
                None,
                f"Invalid format in '{metric}'. Expected format: 'Metric:Value'.",
            )
        key, value = metric.split(":")
        if key not in explanations or value not in explanations[key]:
            return None, f"Invalid metric or value in '{metric}'."
        description, explanation = explanations[key][value]
        translated[key] = (description, explanation)
    return translated, ""


# Streamlit app UI enhancements
st.title("CVSS 3.1 Vector Translator with Detailed Explanations")

# Example CVSS Vector Button and User Input Field
user_input = st.text_input("Enter CVSS 3.1 Vector String", "")

if user_input:  # Ensure translation logic is executed only if there's user input
    # Translate dynamically
    translated_metrics, error_message = translate_cvss31_vector(user_input)
    if translated_metrics:
        st.write("Translated CVSS Vector Components with Explanations:")
        # Explanation Toggle
        if st.checkbox("Show Detailed Explanations"):
            for key, (description, explanation) in translated_metrics.items():
                st.markdown(f"**{key} ({description}):** {explanation}")
        else:
            for key, (description, _) in translated_metrics.items():
                st.markdown(f"**{key}:** {description}")
    elif error_message:
        st.error(error_message)
else:
    # Optionally, provide guidance when no input is detected
    st.write(
        "Please enter a CVSS 3.1 vector string above to see its translation and detailed explanations."
    )

# Note on the Clipboard Copy feature
import pyperclip

# Clipboard Copy Button
if st.button("Copy Translation to Clipboard"):
    translation_text = ""
    if translated_metrics:
        for key, (description, explanation) in translated_metrics.items():
            translation_text += f"{key} ({description}): {explanation}\n"
        pyperclip.copy(translation_text)
        st.success("Translation copied to clipboard!")
    else:
        st.warning(
            "No translation to copy. Please enter a valid CVSS 3.1 vector string."
        )
