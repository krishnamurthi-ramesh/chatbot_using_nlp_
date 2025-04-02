import requests
from datetime import datetime
import json
from colorama import Fore, Style, init
import subprocess
import os
import re

# Initialize colorama
init()

def test_ollama():
    """Test Ollama connection."""
    try:
        # Test with a simple prompt
        test_prompt = "Hello, how are you?"
        # Use the correct path to ollama
        ollama_path = r"C:\Users\Krishnamurthi\AppData\Local\Programs\Ollama\ollama.exe"
        response = subprocess.run(
            [ollama_path, 'run', 'llama2', test_prompt],
            capture_output=True,
            text=True
        )
        
        if response.returncode != 0:
            print(f"{Fore.RED}Ollama returned error code: {response.returncode}{Style.RESET_ALL}")
            print(f"{Fore.RED}Error output: {response.stderr.strip()}{Style.RESET_ALL}")
            return False
        
        # Check if we got any response
        if not response.stdout.strip():
            print(f"{Fore.RED}No response received from Ollama{Style.RESET_ALL}")
            return False
            
        return True
    except FileNotFoundError:
        print(f"{Fore.RED}Ollama executable not found. Please make sure Ollama is installed and added to PATH.{Style.RESET_ALL}")
        return False
    except Exception as e:
        print(f"{Fore.RED}Error testing Ollama: {str(e)}{Style.RESET_ALL}")
        return False

def get_time():
    """Get current time and date."""
    now = datetime.now()
    return f"Current time: {now.strftime('%H:%M:%S')}\nDate: {now.strftime('%Y-%m-%d')}"

def solve_math(expression):
    """Solve basic math problems."""
    try:
        # Handle square root
        if "square root" in expression:
            number = expression.replace("square root of", "").strip()
            try:
                result = float(number) ** 0.5
                return f"Result: {result}"
            except ValueError:
                return "Invalid number for square root."
            
        # Handle basic operations
        try:
            # Replace words with operators
            expression = expression.replace("plus", "+")
            expression = expression.replace("minus", "-")
            expression = expression.replace("times", "*")
            expression = expression.replace("divided by", "/")
            
            # Evaluate the expression
            result = eval(expression)
            return f"Result: {result}"
        except:
            return "Invalid math expression."
            
    except Exception as e:
        return f"Error solving math: {str(e)}"

def analyze_sentiment(text):
    """Analyze sentiment using Ollama."""
    try:
        prompt = f"""You are a sentiment analyzer. Analyze the following text:
        Text: {text}
        
        Is it positive, negative, or neutral? Provide a clear explanation."""
        
        # Use the correct path to ollama
        ollama_path = r"C:\Users\Krishnamurthi\AppData\Local\Programs\Ollama\ollama.exe"
        response = subprocess.run(
            [ollama_path, 'run', 'llama2', prompt],
            capture_output=True,
            text=True
        )
        # Clean the response
        cleaned_response = re.sub(r'\[.*?\]', '', response.stdout)
        cleaned_response = re.sub(r'\(.*?\)', '', cleaned_response)
        cleaned_response = cleaned_response.strip()
        
        if not cleaned_response:
            return "I couldn't analyze the sentiment. Could you please rephrase your question?"
            
        return cleaned_response
    except Exception as e:
        return f"Error analyzing sentiment: {str(e)}"

def get_information(query):
    """Get information using Ollama's Llama2."""
    try:
        # Format the query for better responses
        prompt = f"""You are a helpful and knowledgeable assistant. 
        Answer the following question in a clear and concise manner:
        
        Question: {query}
        
        If you don't know the answer, say "I'm not sure about that. Could you please rephrase your question?" 
        instead of making something up."""
        
        # Use the correct path to ollama
        ollama_path = r"C:\Users\Krishnamurthi\AppData\Local\Programs\Ollama\ollama.exe"
        response = subprocess.run(
            [ollama_path, 'run', 'llama2', prompt],
            capture_output=True,
            text=True
        )
        
        # Clean the response
        cleaned_response = re.sub(r'\[.*?\]', '', response.stdout)
        cleaned_response = re.sub(r'\(.*?\)', '', cleaned_response)
        cleaned_response = cleaned_response.strip()
        
        # Check if response contains the question itself
        if query.lower() in cleaned_response.lower():
            cleaned_response = cleaned_response.replace(query, "").strip()
        
        if not cleaned_response:
            return "I'm not sure about that. Could you please rephrase your question?"
            
        return cleaned_response
    except Exception as e:
        return f"Error getting information: {str(e)}"

def chatbot_response(user_input):
    """Generate chatbot response."""
    try:
        # Clean user input
        user_input = user_input.strip()
        
        # Check for specific commands
        if "time" in user_input.lower():
            return get_time()
        
        elif any(op in user_input.lower() for op in ["+", "-", "*", "/", "square root"]):
            return solve_math(user_input)
        
        # Check for sentiment analysis
        if any(word in user_input.lower() for word in ["sentiment", "mood", "feeling"]):
            return analyze_sentiment(user_input)
        
        # Use Ollama for general responses
        try:
            query = user_input.strip()
            query = query.replace("?", "").strip()
            
            response = get_information(query)
            
            if not response.strip():
                response = "I'm not sure about that. Could you please rephrase your question?"
            
            return response
        except Exception as e:
            return f"Error getting response: {str(e)}"
    
    except Exception as e:
        return f"Error: {str(e)}"

def main():
    """Main function to run the chatbot."""
    # Check if Ollama is running
    if not test_ollama():
        print(f"{Fore.RED}Error: Ollama is not running or Llama2 model is not available.{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}Please make sure Ollama is running and Llama2 model is downloaded.{Style.RESET_ALL}")
        return
    
    print(f"{Fore.CYAN}Welcome to the Chatbot!{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}Type 'exit' to quit.{Style.RESET_ALL}\n")
    
    while True:
        try:
            user_input = input(f"{Fore.GREEN}You: {Style.RESET_ALL}").strip()
            
            if user_input.lower() == 'exit':
                print(f"{Fore.YELLOW}Goodbye!{Style.RESET_ALL}")
                break
            
            response = chatbot_response(user_input)
            print(f"{Fore.BLUE}Chatbot: {Style.RESET_ALL}{response}\n")
        
        except KeyboardInterrupt:
            print(f"\n{Fore.YELLOW}Goodbye!{Style.RESET_ALL}")
            break
        except Exception as e:
            print(f"{Fore.RED}Error: {str(e)}{Style.RESET_ALL}")

if __name__ == "__main__":
    main()
