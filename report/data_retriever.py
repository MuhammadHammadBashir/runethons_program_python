import json

class DataRetriever:
    athlete_data_path = "athlete_data/athlete_info.json"
    athlete_conversations_path = "athlete_data/athlete_conversations.json"
    expert_conversations_path = "athlete_data/expert_conversations.json"

    @staticmethod
    def get_athlete_data():
        with open(DataRetriever.athlete_data_path, 'r') as file:
            athlete_data = json.load(file)
        
        # Remove unwanted keys safely
        keys_to_remove = {"hub", "loadingCurrentPlans", "report", "archive", "password"}
        filtered_athlete_data = {k: v for k, v in athlete_data.items() if k not in keys_to_remove}

        return filtered_athlete_data
    
    @staticmethod
    def get_athlete_conversations():
        with open(DataRetriever.athlete_conversations_path, 'r') as file:
            conversations = json.load(file)
        return {"messages": [msg["message_text"] for msg in conversations]}
        # for values in conversations:
        #     allowed_keys = {"name", "age", "sport"}  # Replace with the keys you want to keep
        #     conversations_keys = set(values.keys())
    
        #     for key in conversations_keys - allowed_keys:
        #         values.pop(key, None)        
        # return conversations
    
    @staticmethod
    def get_expert_conversations():
        with open(DataRetriever.expert_conversations_path, 'r') as file:
            conversations = json.load(file)

        return {"messages": [msg["message_text"] for msg in conversations]}
        # for values in conversations:
        #     allowed_keys = {"name", "age", "sport"}  # Replace with the keys you want to keep
        #     conversations_keys = set(values.keys())
    
        #     for key in conversations_keys - allowed_keys:
        #         values.pop(key, None)        
        # return conversations
    
    @staticmethod
    def get_all_data(athlete_email):
        athlete_data = DataRetriever.get_athlete_data()
        athlete_conversations = DataRetriever.get_athlete_conversations()
        expert_conversations = DataRetriever.get_expert_conversations()
        
        return {
            "athlete": athlete_data,
            "athleteConversations": athlete_conversations,
            "expertConversations": expert_conversations
        }