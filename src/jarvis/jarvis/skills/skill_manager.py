# MIT License

# Copyright (c) 2019 Georgios Papachristou

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from jarvis.settings import GENERAL_SETTINGS
from jarvis.core.console_manager import ConsoleManager
import jarvis.engines as engines


class AssistantSkill:
    first_activation = True
    console_manager = ConsoleManager()
    tts_engine = engines.TTSEngine() if GENERAL_SETTINGS.get('response_in_speech') else engines.TTTEngine()

    @classmethod
    def response(cls, text):
        cls.tts_engine.assistant_response(text)

    @classmethod
    def _extract_tags(cls, voice_transcript, tags):
        transcript_words = voice_transcript.split()
        tags = tags.split(',')
        return set(transcript_words).intersection(tags)
