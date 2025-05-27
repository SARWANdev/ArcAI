

from google import genai
from google.genai import types
client = genai.Client(api_key="AIzaSyC8L5ydAyyJcis54fhiUHBCKFemsRHu6b0")

inputText= '''Abstract—Remote Attestation (RA) has become a valuable security service for Internet of Things (IoT) devices, as the security
of these devices is often not prioritized during the manufacturing
process. However, traditional RA schemes suffer from a single
point of failure because they rely on a trusted verifier. To address
this issue, we propose a voting-based blockchain attestation
protocol that provides a reliable solution by eliminating the single
point of failure through distributed verification across all nodes.
In addition, it offers a traceable and immutable public history of
the attestation results, which can be verified by external auditors
at any time. Finally, we verify our proposed protocol on three
NVIDIA Jetson embedded devices hosting up to 15 attestation
nodes.'''

response = client.models.generate_content(
    model="gemini-2.0-flash",
    contents=["summarize this abstarct: "+ inputText],
    config=types.GenerateContentConfig(
        max_output_tokens=500,
        temperature=0.0
    )
)
print(response.text)

