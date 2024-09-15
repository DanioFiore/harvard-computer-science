chrome.runtime.onMessage.addListener((request, sender, send_response) => {
    if (request.type === 'chatgpt') {
        fetch('https://api.openai.com/v1/chat/completions', {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${request.apiKey}`,
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                model: 'gpt-3.5-turbo',
                messages: [
                    {
                        role: 'user',
                        content: request.message
                    }
                ]
            })
        }).then(response => response.json()).then(data => {
            send_response({ 
                reply: data.choices[0].message.content 
            });
        }).catch(error => {
            send_response({ 
                reply: `Error: Failed to fetch chat response. Please check your API key and try again.  Error details: ${error.message}`
            });
        });

        return true;
    }
});