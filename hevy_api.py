import os
import requests
from typing import Optional, Dict, List
from dotenv import load_dotenv

load_dotenv()

class HevyClient:
    def __init__(self, api_key: Optional[str] = None):
        self.base_url = "https://api.hevyapp.com/v1"
        self.api_key = api_key or os.getenv("HEVY_API_KEY")

        if not self.api_key:
            raise ValueError("Kein API-Key gefunden. Setze die Umgebungsvariable HEVY_API_KEY.")

        self.session = requests.Session()
        self.session.headers.update({
            "accept": "application/json",
            "api-key": self.api_key
        })

    def _handle_response(self, response: requests.Response) -> Dict:
        #print(f"[DEBUG] Status Code: {response.status_code}")
        #print(f"[DEBUG] Response Text: {response.text}")

        if response.status_code == 200:
            return response.json()
        elif response.status_code == 401:
            raise Exception("❌ Ungültiger API-Key (401)")
        elif response.status_code == 404:
            raise Exception(f"❌ Endpunkt nicht gefunden (404): {response.url}")
        else:
            raise Exception(f"❌ Fehlerhafte Anfrage: {response.status_code} - {response.text}")

    def _get_workouts_page(self, page: int, pageSize: int) -> Dict:
        url = f"{self.base_url}/workouts?page={page}&pageSize={pageSize}"
        #print(f"[DEBUG] Anfrage an URL: {url}")
        response = self.session.get(url)
        return self._handle_response(response)

    def get_workouts(self) -> Dict:
        all_workouts = []
        page = 1
        pageSize = 1

        while True:
            try:
                response = self._get_workouts_page(page=page, pageSize=pageSize)

                resp_page = response.get('page', 1)
                resp_page_size = response.get('page_count', 1)

                #print(f"[DEBUG] Seite: {resp_page}, Seitengröße: {resp_page_size}")

                workouts = response.get('workouts', [])
                if not workouts:
                    break  # Keine weiteren Workouts
                all_workouts.extend(workouts)
                page += 1
                if page > resp_page_size:
                    break # Alle Seiten abgearbeitet
                
            except Exception as e:
                print(f"[ERROR] {e}")
                break

        print(all_workouts)

        return {
            'total_workouts': len(all_workouts),
            'workouts': all_workouts
        }
