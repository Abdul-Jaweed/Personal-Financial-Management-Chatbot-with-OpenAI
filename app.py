import gradio as gr
import openai
import json
from dotenv import load_dotenv
import os

load_dotenv()
# Set up OpenAI API credentials
openai.api_key = os.environ["OPENAI_API_KEY"]

TRANSACTIONS_DATA = [
    {"date": "2021-01-01", "amount": 1000, "category": "income", "description": "salary"},
    {"date": "2021-01-02", "amount": -50, "category": "groceries", "description": "milk and eggs"},
    {"date": "2021-01-03", "amount": -100, "category": "entertainment", "description": "movie tickets"},
    {"date": "2021-01-04", "amount": -20, "category": "transportation", "description": "bus fare"},
    {"date": "2021-01-05", "amount": -200, "category": "bills", "description": "electricity bill"},
    {"date": "2021-01-06", "amount": -30, "category": "groceries", "description": "bread and cheese"},
    {"date": "2021-01-07", "amount": -150, "category": "clothing", "description": "new shoes"},
    {"date": "2021-01-08", "amount": -40, "category": "healthcare", "description": "prescription drugs"},
    {"date": "2021-01-09", "amount": -80, "category": "education", "description": "online course"},
    {"date": "2021-01-10", "amount": -60, "category": "entertainment", "description": "pizza delivery"},
    {"date": "2021-01-11", "amount": -25, "category": "transportation", "description": "taxi ride"},
    {"date": "2021-01-12", "amount": -300, "category": "bills", "description": "internet bill"},
    {"date": "2021-01-13", "amount": -50, "category": "groceries", "description": "fruits and vegetables"}
]

def analyze_transactions(transactions):
    total_income = 0
    total_expenses = 0
    categories = {}

    for transaction in transactions:
        amount = transaction['amount']
        category = transaction['category']

        if amount > 0:
            total_income += amount
        else:
            total_expenses += amount

        if category in categories:
            categories[category] += amount
        else:
            categories[category] = amount

    return {
        'total_income': total_income,
        'total_expenses': total_expenses,
        'categories': categories
    }

def generate_response(prompt):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a Personal Financial Manager."},
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content.strip()

def handle_query(query):
    insights = analyze_transactions(TRANSACTIONS_DATA)
    response = generate_response(query)
    return response

def chatbot_interface(query):
    response = handle_query(query)
    return response

# Run the Gradio interface
if __name__ == '__main__':
    iface = gr.Interface(fn=chatbot_interface, inputs="text", outputs="text", title="Personal Financial Management Chatbot", description="Ask me anything about your finances!")
    #iface.launch()            # For local URL
    iface.launch(share=True)   # For Public URL
