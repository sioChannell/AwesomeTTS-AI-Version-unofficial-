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

"""Local kokoro"""

from .base import Service
from .common import Trait
import requests
__all__ = ['Kokoro']


class Kokoro(Service):
    """Provides a Service implementation for Local kokoro."""

    __slots__ = []

    VOICE_CODES = [
        (0, "af_alloy, en-US"),
        (1, "af_aoede, en-US"),
        (2, "af_bella, en-US"),
        (3, "af_heart, en-US"),
        (4, "af_jadzia, en-US"),
        (5, "af_jessica, en-US"),
        (6, "af_kore, en-US"),
        (7, "af_nicole, en-US"),
        (8, "af_nova, en-US"),
        (9, "af_river, en-US"),
        (10, "af_sarah, en-US"),
        (11, "af_sky, en-US"),
        (12, "af_v0, en-US"),
        (13, "af_v0bella, en-US"),
        (14, "af_v0irulan, en-US"),
        (15, "af_v0nicole, en-US"),
        (16, "af_v0sarah, en-US"),
        (17, "af_v0sky, en-US"),
        (18, "am_adam, en-US"),
        (19, "am_echo, en-US"),
        (20, "am_eric, en-US"),
        (21, "am_fenrir, en-US"),
        (22, "am_liam, en-US"),
        (23, "am_michael, en-US"),
        (24, "am_onyx, en-US"),
        (25, "am_puck, en-US"),
        (26, "am_santa, en-US"),
        (27, "am_v0adam, en-US"),
        (28, "am_v0gurney, en-US"),
        (29, "am_v0michael, en-US"),
        (30, "bf_alice, en-GB"),
        (31, "bf_emma, en-GB"),
        (32, "bf_lily, en-GB"),
        (33, "bf_v0emma, en-GB"),
        (34, "bf_v0isabella, en-GB"),
        (35, "bm_daniel, en-GB"),
        (36, "bm_fable, en-GB"),
        (37, "bm_george, en-GB"),
        (38, "bm_lewis, en-GB"),
        (39, "bm_v0george, en-GB"),
        (40, "bm_v0lewis, en-GB"),
        (41, "ef_dora, Spanish"),
        (42, "em_alex, Spanish"),
        (43, "em_santa, Spanish"),
        (44, "ff_siwis, French"),
        (45, "hf_alpha, Hindi"),
        (46, "hf_beta, Hindi"),
        (47, "hm_omega, Hindi"),
        (48, "hm_psi, Hindi"),
        (49, "if_sara, Italian"),
        (50, "im_nicola, Italian"),
        (51, "jf_alpha, ja-JP"),  # only japanese english
        (52, "jf_gongitsune, ja-JP"),
        (53, "jf_nezumi, ja-JP"),
        (54, "jf_tebukuro, ja-JP"),
        (55, "jm_kumo, ja-JP"),
        (56, "pf_dora, Brazilian Portuguese"),
        (57, "pm_alex, Brazilian Portuguese"),
        (58, "pm_santa, Brazilian Portuguese"),
        (59, "zf_xiaobei, zh-CN"),  # only chinese english
        (60, "zf_xiaoni, zh-CN"),
        (61, "zf_xiaoxiao, zh-CN"),
        (62, "zf_xiaoyi, zh-CN"),
        (63, "zm_yunjian, zh-CN"),
        (64, "zm_yunxi, zh-CN"),
        (65, "zm_yunxia, zh-CN"),
        (66, "zm_yunyang, zh-CN")
    ]

    VOICE_LOOKUP = dict(VOICE_CODES)

    NAME = "Kokoro"

    TRAITS = [Trait.INTERNET]

    def desc(self):
        """Returns a static description."""

        return "Kokoro Local TTS"

    def options(self):
        """Returns an option to select the voice."""
        return [
            dict(
                key='voice',
                label="Voice",
                values=[(key, description)
                        for key, description in self.VOICE_CODES],
                transform=lambda value: value,
                default=0,
            ),
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
        ]

    def run(self, text, options, path):
        base_url = options['api']
        voice_index = options['voice']
        voice = self.VOICE_CODES[voice_index][1].split(",")[0]
        speed = options['speed']

        headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer your_api_key_here"
        }

        data = {
            "model": "kokoro",
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

