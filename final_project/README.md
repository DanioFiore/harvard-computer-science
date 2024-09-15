# ChatGPT Chrome Extension

This Chrome extension enables users to interact with ChatGPT directly from their browser using the OpenAI API. Users can configure their API key and chat with ChatGPT through a simple popup interface.

## Features

- **API Key Setup**: Enter and save your OpenAI API key for authenticating requests to the ChatGPT API.
- **Chat Interface**: Send messages to ChatGPT and receive responses directly within the popup interface.
- **Persistent Storage**: The API key is saved using Chrome's storage API, so you don't need to re-enter it every time you use the extension.

## Files

- **`manifest.json`**: The manifest file for the Chrome extension. It specifies metadata about the extension, permissions, background scripts, and popup settings.
  - **Key Sections**:
    - `manifest_version`: Specifies the version of the manifest file format.
    - `name`, `version`, `description`: Basic information about the extension.
    - `permissions`: Requests permissions needed by the extension, such as `storage` and `activeTab`.
    - `background`: Defines the background script for handling messages and API requests.
    - `action`: Configures the extension's popup UI.

- **`background.js`**: Handles background tasks for the extension. It listens for messages from the popup, makes requests to the OpenAI API, and processes responses.
  - **Key Functions**:
    - Listens for messages of type `chatgpt`.
    - Makes API requests to OpenAI and handles responses and errors.

- **`popup.html`**: Defines the HTML structure of the popup interface that appears when the extension icon is clicked.
  - **Key Elements**:
    - Input field for the API key.
    - Buttons for saving the API key and sending messages.
    - Text area for displaying ChatGPT responses.

- **`popup.js`**: Manages user interactions within the popup. It handles saving the API key, toggling between setup and chat views, and sending messages to the background script.
  - **Key Functions**:
    - Retrieves and saves the API key from Chrome's storage.
    - Sends chat messages to the background script and displays responses.
    - Handles visibility of setup and chat interfaces based on API key presence.

## Installation

1. **Clone**: Clone this repository.
2. **Open Chrome**: Navigate to `chrome://extensions/` in your browser.
3. **Enable Developer Mode**: Toggle the "Developer mode" switch in the top right corner.
4. **Load Extension**: Click "Load unpacked" and select the directory where you have the extension files.

## Usage

1. **Set Up API Key**:
   - Click on the extension icon in your browser toolbar.
   - Enter your OpenAI API key in the provided input field and click "Save".
   - The extension will switch to the chat interface if the API key is successfully saved.

2. **Start Chatting**:
   - Type a message into the input field in the chat interface.
   - Click "Send" to submit the message.
   - The response from ChatGPT will be displayed below the input field.

## Troubleshooting

- **Quota Exceeded**: If you receive an "insufficient_quota" error, check your OpenAI account usage and ensure that your API key is valid and has sufficient quota.
- **API Key Issues**: Verify that the API key is correctly entered and saved. Ensure there are no extra spaces or errors in the key.

