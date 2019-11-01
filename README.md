# rasa-jira
## Technologies
- Python
- Rasa
- Jira API
## Other Technologies Tested With
- Raspberry Pi
- Mycroft Speech-to-Text

## How it Works
Rasa defines the NLU and has preliminary training based on the intents, data slots, and stories to determine the overall flow of how the chat assisstant interacts with the user. This determines what to say next and what information to grab from the user's speech.

Rasa uses this information to walk users through adding, moving, and deleting cards from a JIRA board using JIRA's api. If the chat assisstant is missing any information to complete a task it will prompt the user for it, instead of resulting in an error.

One of the added benefits of using RASA, is that it allows for users to interact with your chat assistant during the training process, allowing you to see how the NLP interprets the text in terms of intent and values. If there are any misinterpretations you can select the correct intents and values, which then gets added to the training model.
