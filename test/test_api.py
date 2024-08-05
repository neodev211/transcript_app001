import unittest
import json
import requests
# from api import get_video_id  # Mantenemos la importación de get_video_id

class TestYoutubeTranscriptionAPI(unittest.TestCase):

    def setUp(self):
        self.base_url = "http://localhost:5000"  # Asumiendo que tu API corre en este puerto

    # def test_get_video_id(self):
    #     url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
    #     self.assertEqual(get_video_id(url), "dQw4w9WgXcQ")

    #     url = "https://youtu.be/dQw4w9WgXcQ"
    #     self.assertEqual(get_video_id(url), "dQw4w9WgXcQ")

    #     url = "https://www.youtube.com/invalid"
    #     self.assertIsNone(get_video_id(url))

    def test_transcribe_video_success(self):
        response = requests.post(f"{self.base_url}/transcribe", 
                                 json={"url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ"})
        self.assertEqual(response.status_code, 200)
        data = response.json()
        # print("data", data)
        self.assertIn("transcription", data)
        self.assertIsInstance(data["transcription"], str)
        self.assertGreater(len(data["transcription"]), 0)

    def test_transcribe_video_no_url(self):
        response = requests.post(f"{self.base_url}/transcribe", json={})
        self.assertEqual(response.status_code, 400)
        data = response.json()
        self.assertIn("error", data)
        self.assertEqual(data["error"], "No se proporcionó URL")

    def test_transcribe_video_invalid_url(self):
        response = requests.post(f"{self.base_url}/transcribe", 
                                 json={"url": "https://www.youtube.com/invalid"})
        self.assertEqual(response.status_code, 400)
        data = response.json()
        self.assertIn("error", data)
        self.assertEqual(data["error"], "URL de YouTube inválida")

if __name__ == '__main__':
    unittest.main()