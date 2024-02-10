import streamlit as st


def translate_cvss31_vector(cvss_vector):
    explanations = {
        "AV": {
            "N": (
                "Network",
                "The vulnerability can be exploited from anywhere on the network, without any need for user interaction or prior access to the vulnerable system.",
                "Implement network level access controls and firewalls to limit access to the system.",
            ),
            "A": (
                "Adjacent Network",
                "The vulnerability can be exploited from the same physical or logical network, but not over the internet. This could include local Wi-Fi networks or VPNs.",
                "Implement network level access controls and firewalls to limit access to the system.",
            ),
            "L": (
                "Local",
                "The vulnerability can only be exploited by an attacker who has either physical access to the device, or access over a local network.",
                "Implement physical security controls and network level access controls to limit access to the system.",
            ),
            "P": (
                "Physical",
                "The vulnerability can only be exploited by an attacker who has physical access to the device.",
                "Implement physical security controls to limit access to the system.",
            ),
        },
        "AC": {
            "L": (
                "Low",
                "The attack can be conducted easily with no special conditions or circumstances required. The attacker does not require any specialized knowledge or resources.",
                "Implement the principle of least privilege and apply regular security updates.",
            ),
            "H": (
                "High",
                "The attack requires certain conditions that may be difficult to meet. The attacker may need specialized knowledge or resources, or there may be a high likelihood of the attack being detected.",
                "Implement the principle of least privilege, apply regular security updates, and monitor for suspicious activity.",
            ),
        },
        "PR": {
            "N": (
                "None",
                "The attacker does not require any privileges or access rights to exploit the vulnerability.",
                "Apply regular security updates and monitor for suspicious activity.",
            ),
            "L": (
                "Low",
                "The attacker requires privileges or access rights that are easy to obtain, such as those granted to ordinary users.",
                "Apply regular security updates, monitor for suspicious activity, and implement the principle of least privilege.",
            ),
            "H": (
                "High",
                "The attacker requires privileges or access rights that are difficult to obtain, such as those granted to system administrators.",
                "Apply regular security updates, monitor for suspicious activity, and implement the principle of least privilege.",
            ),
        },
        "UI": {
            "N": (
                "None",
                "The vulnerability can be exploited without any interaction from any user. The attack can be completely automated.",
                "Apply regular security updates and implement network level access controls.",
            ),
            "R": (
                "Required",
                "The vulnerability requires some form of interaction from a user. This could include clicking a link, opening a file, or entering information.",
                "Apply regular security updates, implement network level access controls, and educate users about security best practices.",
            ),
        },
        "S": {
            "U": (
                "Unchanged",
                "The exploited vulnerability does not affect resources beyond its security scope. The impact of the attack is limited to the vulnerable component itself.",
                "Apply regular security updates and monitor for suspicious activity.",
            ),
            "C": (
                "Changed",
                "The exploited vulnerability can affect resources beyond its security scope. The impact of the attack can extend to other components in the system.",
                "Apply regular security updates, monitor for suspicious activity, and implement network level access controls.",
            ),
        },
        "C": {
            "H": (
                "High",
                "The confidentiality impact is high. A successful exploit could lead to all data in the affected system or component being disclosed to the attacker.",
                "Implement encryption and access controls to protect sensitive data. Apply regular security updates.",
            ),
            "L": (
                "Low",
                "The confidentiality impact is low. A successful exploit could lead to some data being disclosed, but not all.",
                "Implement encryption and access controls to protect sensitive data. Apply regular security updates.",
            ),
            "N": (
                "None",
                "There is no impact on confidentiality. The attack does not result in any data being disclosed.",
                "Apply regular security updates and monitor for suspicious activity.",
            ),
        },
        "I": {
            "H": (
                "High",
                "The integrity impact is high. A successful exploit could allow the attacker to modify all data in the affected system or component.",
                "Implement integrity checks and access controls to protect data. Apply regular security updates.",
            ),
            "L": (
                "Low",
                "The integrity impact is low. A successful exploit could allow the attacker to modify some data, but not all.",
                "Implement integrity checks and access controls to protect data. Apply regular security updates.",
            ),
            "N": (
                "None",
                "There is no impact on integrity. The attack does not result in any data being modified.",
                "Apply regular security updates and monitor for suspicious activity.",
            ),
        },
        "A": {
            "H": (
                "High",
                "The availability impact is high. A successful exploit could render the affected system or component completely unavailable, either by crashing it or by making it so slow as to be unusable.",
                "Implement redundancy and failover systems to maintain availability. Apply regular security updates.",
            ),
            "L": (
                "Low",
                "The availability impact is low. A successful exploit could reduce the performance of the affected system or component, but not render it completely unavailable.",
                "Implement redundancy and failover systems to maintain availability. Apply regular security updates.",
            ),
            "N": (
                "None",
                "There is no impact on availability. The attack does not affect the usability of the system or component.",
                "Apply regular security updates and monitor for suspicious activity.",
            ),
        },
    }
    full_names = {
        "AV": "Attack Vector",
        "AC": "Attack Complexity",
        "PR": "Privileges Required",
        "UI": "User Interaction",
        "S": "Scope",
        "C": "Confidentiality",
        "I": "Integrity",
        "A": "Availability",
        # Add more if needed
    }

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
        description, explanation, mitigation = explanations[key][value]
        full_name = full_names.get(key, key)
        translated[full_name] = (description, explanation, mitigation)
    return translated, ""


# Streamlit app UI enhancements
st.title("CVSS 3.1 Vector Translator")

# Example CVSS Vector Button and User Input Field
user_input = st.text_input("Enter CVSS 3.1 Vector String", "")

if user_input:  # Ensure translation logic is executed only if there's user input
    # Translate dynamically
    translated_metrics, error_message = translate_cvss31_vector(user_input)
    if translated_metrics:
        st.write("Translated CVSS Vector Components:")
        # Explanation Toggle

        for key, (description, explanation, mitigation) in translated_metrics.items():
            st.markdown(
                f"**{key}:** *{description}*  \n{explanation}\n\n**Mitigation:** {mitigation}"
            )
    elif error_message:
        st.error(error_message)
else:
    st.write(
        "Please enter a CVSS 3.1 vector string above to see its translation and detailed explanations."
    )

# Note on the Clipboard Copy feature
import pyperclip

# Clipboard Copy Button
if st.button("Copy Translation to Clipboard"):
    translation_text = ""
    if translated_metrics:
        for key, (description, explanation, mitigation) in translated_metrics.items():
            translation_text += (
                f"{key} ({description}): {explanation}\n\nMitigation:{mitigation}\n"
            )
        pyperclip.copy(translation_text)
        st.success("Translation copied to clipboard!")
    else:
        st.warning(
            "No translation to copy. Please enter a valid CVSS 3.1 vector string."
        )
