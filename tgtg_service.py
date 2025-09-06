from tgtg import TgtgClient
from typing import List, Dict, Set, Tuple


class TgtgService:
    @staticmethod
    def get_item_key(item: Dict) -> str:
        """Create unique identifier for an item"""
        return f"{item['store']['store_name']}_{item['item']['item_id']}"

    @staticmethod
    def create_client(credentials: Dict) -> TgtgClient:
        """Create authenticated TgtgClient"""
        return TgtgClient(
            access_token=credentials['access_token'],
            refresh_token=credentials['refresh_token'],
            cookie=credentials['cookie']
        )

    @staticmethod
    def process_items(current_items: List[Dict], last_notified_items: Set[str]) -> Tuple[List[Dict], List[Dict], Set[str]]:
        """Process items and identify new ones"""
        currently_available_items = set()
        all_available_items = []
        new_items = []

        for item in current_items:
            available = item.get('items_available', 0)

            if available > 0:
                item_key = TgtgService.get_item_key(item)
                currently_available_items.add(item_key)

                store_name = item['store']['store_name']
                item_name = item['item']['name']
                price = item['item']['item_price']['minor_units'] / 100
                address = item['pickup_location']['address']['address_line']

                item_data = {
                    'store': store_name,
                    'item': item_name,
                    'available': available,
                    'price': price,
                    'address': address,
                    'key': item_key,
                    'is_new': item_key not in last_notified_items
                }

                all_available_items.append(item_data)

                if item_key not in last_notified_items:
                    new_items.append(item_data)

        return all_available_items, new_items, currently_available_items
