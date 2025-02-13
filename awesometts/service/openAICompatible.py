# -*- coding: utf-8 -*-

# AwesomeTTS text-to-speech add-on for Anki
# Copyright (C) 2010-Present  Anki AwesomeTTS Development Team
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""OpenAI-compatible api"""

from .base import Service
from .common import Trait
import requests
__all__ = ['OpenAICompatible']


class OpenAICompatible(Service):
    __slots__ = []

    NAME = "OpenAICompatible"

    TRAITS = [Trait.INTERNET]

    def desc(self):
        """Returns a static description."""

        return "OpenAI Compatible TTS"

    def options(self):
        """Returns an option to select the voice."""
        return [
            dict(
                key='speed',
                label="Speed",
                values=(0.25, 4),
                transform=float,
                default=1,
            ),
        ]

    def extras(self):
        return [
            dict(key='api', label="API EndPoint", required=True),
            dict(
                key='model',
                label="Model",
                required=True
            ),
            dict(
                key='voice',
                label="Voice",
                required=True
            ),
        ]

    def run(self, text, options, path):
        model = options['model']
        base_url = options['api']
        voice = options['voice']
        speed = options['speed']

        headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer your_api_key_here"
        }

        data = {
            "model": model,
            "voice": voice,
            "input": text,
            "response_format": "mp3",
            "speed": speed
        }

        try:
            with requests.post(base_url, headers=headers, json=data, stream=True) as response:
                response.raise_for_status()

                if response.headers['Content-Type'] != 'audio/mpeg':
                    print("Error: Expected audio/mpeg, but got {}".format(response.headers['Content-Type']))
                    exit()

                with open(path, "wb") as f:
                    for chunk in response.iter_content(chunk_size=8192):  # 8KB chunks
                        f.write(chunk)

            print("saved to output.mp3")

        except requests.exceptions.RequestException as e:
            print(f"bad request: {e}")
        except Exception as e:
            print(f"error: {e}")

