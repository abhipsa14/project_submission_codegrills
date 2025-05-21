#!/usr/bin/env python3
"""
Telegram .onion Link Extractor

This script connects to a Telegram channel using the Telethon library
and extracts .onion links from recent messages.
"""

import os
import re
import json
import asyncio
import logging
from datetime import datetime
from telethon import TelegramClient, errors
from telethon.tl.types import PeerChannel

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("telegram_extractor.log"),
        logging.StreamHandler()
    ]
)

class TelegramOnionExtractor:
    """Extracts .onion links from Telegram channels."""

    def __init__(self, api_id, api_hash, channel_username='toronionlinks', 
                 output_file='onion_links.jsonl', last_id_file='last_message_id.txt'):
        """Initialize the extractor with API credentials and target channel."""
        self.api_id = api_id
        self.api_hash = api_hash
        self.channel_username = channel_username
        self.output_file = output_file
        self.last_id_file = last_id_file
        
       
        self.onion_pattern = re.compile(
            r'(https?:\/\/)?([a-zA-Z0-9\-\.]+)\.onion(\/[a-zA-Z0-9\-\.\/\?\=\&\%]*)?',
            re.IGNORECASE
        )

    async def connect(self):
        """Connect to Telegram API."""
        self.client = TelegramClient('onion_link_session', self.api_id, self.api_hash)
        await self.client.start()
        logging.info(f"Connected to Telegram API")

    def get_last_message_id(self):
        """Get the last processed message ID from file."""
        try:
            if os.path.exists(self.last_id_file):
                with open(self.last_id_file, 'r') as f:
                    return int(f.read().strip())
            return 0
        except Exception as e:
            logging.error(f"Error reading last message ID: {e}")
            return 0

    def save_last_message_id(self, message_id):
        """Save the last processed message ID to file."""
        try:
            with open(self.last_id_file, 'w') as f:
                f.write(str(message_id))
            logging.info(f"Saved last message ID: {message_id}")
        except Exception as e:
            logging.error(f"Error saving last message ID: {e}")

    def extract_onion_links(self, text):
        """Extract .onion links from text using regex."""
        if not text:
            return []
            
        matches = self.onion_pattern.findall(text)
        links = []
        
        for match in matches:
           
            protocol = match[0] if match[0] else 'http://'
            domain = match[1] + '.onion'
            path = match[2] if match[2] else ''
            full_url = protocol + domain + path
            links.append(full_url)
            
        return links

    def save_link(self, url):
        """Save a link to the output file in JSON format."""
        now = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
        entry = {
            "source": "telegram",
            "url": url,
            "discovered_at": now,
            "context": f"Found in Telegram channel @{self.channel_username}",
            "status": "pending"
        }
        
        try:
            with open(self.output_file, 'a') as f:
                f.write(json.dumps(entry) + '\n')
        except Exception as e:
            logging.error(f"Error saving link to file: {e}")

    async def process_messages(self, limit=100):
        """Process recent messages from the channel and extract .onion links."""
        try:
         
            channel = await self.client.get_entity(self.channel_username)
            if not channel:
                logging.error(f"Channel @{self.channel_username} not found")
                return
                
            logging.info(f"Processing messages from channel @{self.channel_username}")
            
   
            last_id = self.get_last_message_id()
            logging.info(f"Last processed message ID: {last_id}")
            
         
            highest_id = last_id
            
          
            if last_id == 0:
                open(self.output_file, 'w').close()
                
        
            async for message in self.client.iter_messages(channel, limit=limit):
                try:
                 
                    if message.id <= last_id:
                        logging.debug(f"Skipping already processed message {message.id}")
                        continue
                        
                    if message.id > highest_id:
                        highest_id = message.id
                        
                  
                    if message.text:
                   
                        links = self.extract_onion_links(message.text)
                        
                        for link in links:
                            logging.info(f"Found .onion link: {link}")
                            self.save_link(link)
                            
                except Exception as e:
                    logging.error(f"Error processing message {message.id}: {e}")
                    continue
                    
         
            if highest_id > last_id:
                self.save_last_message_id(highest_id)
                
        except errors.FloodWaitError as e:
            logging.error(f"Rate limited by Telegram. Need to wait {e.seconds} seconds")
        except Exception as e:
            logging.error(f"Error processing messages: {e}")

    async def run(self):
        """Run the extractor."""
        try:
            await self.connect()
            await self.process_messages()
        finally:
            await self.client.disconnect()
            logging.info("Disconnected from Telegram API")


async def main():
    """Main function to run the extractor."""
    
    api_id = os.environ.get('TELEGRAM_API_ID')
    api_hash = os.environ.get('TELEGRAM_API_HASH')
    
    if not api_id or not api_hash:
        print("Please provide your Telegram API credentials:")
        api_id = input("API ID: ")
        api_hash = input("API Hash: ")
    
    channel = os.environ.get('TELEGRAM_CHANNEL', 'toronionlinks')
    

    extractor = TelegramOnionExtractor(
        api_id=int(api_id),
        api_hash=api_hash,
        channel_username=channel
    )
    
    await extractor.run()


if __name__ == "__main__":
    asyncio.run(main())