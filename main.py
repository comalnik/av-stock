import requests
from bs4 import BeautifulSoup
from discord_webhook import DiscordWebhook, DiscordEmbed
import os
import time

#TESTING ARCHIVE URLS
#MCT YES https://web.archive.org/web/20251113061156/https://astrovials.com/product/estradiol-enanthate/
#MCT NO https://web.archive.org/web/20260506184119/https://astrovials.com/product/estradiol-enanthate/
#
#CASTOR YES https://web.archive.org/web/20251124222353/https://astrovials.com/product/estradiol-enanthate-castor/
#CASTOR NO https://web.archive.org/web/20260606220916/https://astrovials.com/product/estradiol-enanthate-castor/
#

# URLs to monitor
PRODUCT_URLS = {
    "Estradiol Enanthate (MCT)": "https://astrovials.com/product/estradiol-enanthate/",
    "Estradiol Enanthate (Castor)": "https://astrovials.com/product/estradiol-enanthate-castor/"
}

#Discord Webhook URL
WEBHOOK_URL = os.environ.get("DISCORD_WEBHOOK_URL")

def check_stock():
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }
        
        for name, url in PRODUCT_URLS.items():
            response = requests.get(url, headers=headers)
            soup = BeautifulSoup(response.text, 'html.parser')
            body_text = soup.get_text()
            
            if "Out of stock" in body_text:
                print(f"{name}: OUT OF STOCK")
            else:
                print(f"{name}: IN STOCK! 🟢")
                
                # Send Discord notification
                if WEBHOOK_URL:
                    embed = DiscordEmbed(
                        title="Astrovials Stock Alert",
                        description=f"**{name} is back in stock!**\n[Order here]({url})",
                        color=0xF5A9B8 
                    )
                    
                    webhook = DiscordWebhook(url=WEBHOOK_URL, embeds=[embed])
                    webhook.execute()

    except Exception as e:
        print(f"Error checking stock: {e}")

if __name__ == "__main__":
    check_stock()
