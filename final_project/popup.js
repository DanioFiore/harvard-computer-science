// Check if the API key is already saved
chrome.storage.sync.get(['openaiApiKey'], function(result) {
    if (result.openaiApiKey) {
        document.getElementById('setup').style.display = 'none';
        document.getElementById('chat').style.display = 'block';
    } else {
        document.getElementById('setup').style.display = 'block';
        document.getElementById('chat').style.display = 'none';
    }
});

// Save API Key
document.getElementById('saveApiKey').addEventListener('click', function() {
    const apiKey = document.getElementById('apiKey').value;
    if (apiKey) {
        chrome.storage.sync.set({ openaiApiKey: apiKey }, function() {
            alert('API Key saved!');
            document.getElementById('setup').style.display = 'none';
            document.getElementById('chat').style.display = 'block';
        });
    }
});

// Handle chat messages
document.getElementById('send').addEventListener('click', function () {
    const message = document.getElementById('input').value;

    if (!message) {
        alert('Please enter a message!');
        return;
    }

    // Get the API key from storage
    chrome.storage.sync.get(['openaiApiKey'], function(result) {
        if (result.openaiApiKey) {
            const apiKey = result.openaiApiKey;

            // Send the message to the background script
            chrome.runtime.sendMessage({ type: 'chatgpt', message: message, apiKey: apiKey }, function (response) {
                if (chrome.runtime.lastError) {
                    console.error(chrome.runtime.lastError.message);
                    alert('Error: ' + chrome.runtime.lastError.message);
                } else {
                    document.getElementById('response').innerText = response.reply;
                }
            });
        } else {
            alert('No API Key found!');
        }
    });
});
