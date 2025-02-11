import json

# Load the data from 'utterances.json'
with open('utterances.json', 'r') as f:
    data = json.load(f)

def update_json(data):
    updated_data = []
    
    for entry in data:
        # Extract intent name and remove "Inquiry"
        intent_name = entry['intent'].replace('Inquiry', '').lower()
        
        # Find the intent word in the 'text' field
        text = entry['text']
        offset = text.find(intent_name)  # Find the first occurrence of the intent word in 'text'
        
        # If the word is found, update the 'offset' and 'length' in the entities list
        if offset != -1:
            length = len(intent_name)  # Length of the found word
            
            # Update the entities list with the new offset and length
            entry['entities'] = [{
                "category": "Category",
                "offset": offset,
                "length": length
            }]
        
        # Add the updated entry to the result list
        updated_data.append(entry)
    
    return updated_data

# Update the data
updated_data = update_json(data)

# Print the updated JSON to the console
print(json.dumps(updated_data, indent=4))

# Save the updated data to a new JSON file
with open('updated_utterances.json', 'w') as f:
    json.dump(updated_data, f, indent=4)
