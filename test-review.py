import requests
import asyncio
import aiohttp
import logging

# Configure logging to avoid exposing sensitive data
logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

# Base API URL (parameterized for better maintainability)
API_BASE_URL = "https://jsonplaceholder.typicode.com"


# Function to calculate the sum of a list (using sum() for better readability)
def calculate_sum(numbers):
    if not isinstance(numbers, list) or not all(isinstance(num, int) for num in numbers):  
        raise TypeError("Input must be a list of integers.")
    return sum(numbers)


# Function to fetch user data from an API with async handling   
async def fetch_user_data(session, user_id):
    try:
        url = f"{API_BASE_URL}/users/{user_id}"
        async with session.get(url) as response:
            if response.status != 200:
                raise Exception(f"API call failed with status {response.status}")
            data = await response.json()
            logging.info(f"User Data: {data}")  # Avoid logging sensitive information in production
            return data
    except Exception as e:
        logging.error(f"Error fetching user data: {str(e)}")
        return None


# Function to format a user's full name safely
def format_full_name(user):
    if not isinstance(user, dict) or "name" not in user:
        logging.warning("Invalid user object. Returning 'Unknown User'.")
        return "Unknown User"
    return user["name"]


# Function to process multiple users concurrently and calculate their total ID sum
async def process_users(user_ids):
    results = []
    
    # Use aiohttp to fetch multiple user details concurrently
    async with aiohttp.ClientSession() as session:
        tasks = [fetch_user_data(session, user_id) for user_id in user_ids]
        users = await asyncio.gather(*tasks)

    for user in users:
        if user:
            full_name = format_full_name(user)
            logging.info(f"Processed User: {full_name}")
            results.append({"id": user["id"], "fullName": full_name})

    total_id_sum = calculate_sum([user["id"] for user in results])
    logging.info(f"Total User ID Sum: {total_id_sum}")
    return results


# Test the functions asynchronously
if __name__ == "__main__":
    try:
        user_ids = [1, 2, 3]
        processed_users = asyncio.run(process_users(user_ids))
        logging.info(f"Processed Users: {processed_users}")
    except Exception as error:
        logging.error(f"Unexpected error during processing: {str(error)}")
