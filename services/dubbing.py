"""
Dubbing Service - ElevenLabs Integration

Provides AI voice dubbing and text-to-speech with:
- Multi-language dubbing
- Voice cloning
- Lip-sync support
- Multiple voice options
"""

from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
from dataclasses import dataclass, field
from pathlib import Path
import logging
import asyncio
import httpx

logger = logging.getLogger(__name__)


@dataclass
class Voice:
    """Voice configuration."""
    id: str
    name: str
    language: str
    description: str = ""
    preview_url: Optional[str] = None
    labels: Dict[str, str] = field(default_factory=dict)


@dataclass
class DubbingResult:
    """Result of dubbing operation."""
    audio_path: str
    language: str
    voice_id: str
    duration: float
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class TTSResult:
    """Text-to-speech result."""
    audio_data: bytes
    format: str = "mp3"
    duration: float = 0
    metadata: Dict[str, Any] = field(default_factory=dict)


class DubbingService(ABC):
    """Abstract base for dubbing services."""

    @abstractmethod
    async def get_voices(self, language: str = None) -> List[Voice]:
        """Get available voices."""
        pass

    @abstractmethod
    async def text_to_speech(
        self,
        text: str,
        voice_id: str,
        **kwargs
    ) -> TTSResult:
        """Convert text to speech."""
        pass

    @abstractmethod
    async def dub_audio(
        self,
        audio_path: str,
        target_language: str,
        voice_id: str = None,
        **kwargs
    ) -> DubbingResult:
        """Dub audio to target language."""
        pass


class ElevenLabsService(DubbingService):
    """
    ElevenLabs dubbing and TTS service.

    Features:
    - High-quality voice synthesis
    - Multi-language support
    - Voice cloning
    - Emotional voice control
    """

    def __init__(
        self,
        api_key: str,
        default_voice_id: str = "21m00Tcm4TlvDq8ikWAM",  # Rachel
        timeout: int = 60
    ):
        """
        Initialize ElevenLabs service.

        Args:
            api_key: ElevenLabs API key
            default_voice_id: Default voice to use
            timeout: Request timeout in seconds
        """
        self.api_key = api_key
        self.default_voice_id = default_voice_id
        self.timeout = timeout
        self._base_url = "https://api.elevenlabs.io/v1"

    def _get_headers(self) -> Dict[str, str]:
        """Get API headers."""
        return {
            "xi-api-key": self.api_key,
            "Accept": "application/json"
        }

    async def get_voices(self, language: str = None) -> List[Voice]:
        """
        Get available voices.

        Args:
            language: Filter by language (optional)

        Returns:
            List of Voice objects
        """
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            response = await client.get(
                f"{self._base_url}/voices",
                headers=self._get_headers()
            )
            response.raise_for_status()
            data = response.json()

        voices = []
        for v in data.get("voices", []):
            voice = Voice(
                id=v["voice_id"],
                name=v["name"],
                language=v.get("labels", {}).get("language", "en"),
                description=v.get("description", ""),
                preview_url=v.get("preview_url"),
                labels=v.get("labels", {})
            )

            # Filter by language if specified
            if language is None or voice.language == language:
                voices.append(voice)

        return voices

    async def text_to_speech(
        self,
        text: str,
        voice_id: str = None,
        model_id: str = "eleven_multilingual_v2",
        stability: float = 0.5,
        similarity_boost: float = 0.75,
        **kwargs
    ) -> TTSResult:
        """
        Convert text to speech.

        Args:
            text: Text to synthesize
            voice_id: Voice ID (uses default if None)
            model_id: TTS model ID
            stability: Voice stability (0-1)
            similarity_boost: Voice similarity (0-1)

        Returns:
            TTSResult with audio data
        """
        voice_id = voice_id or self.default_voice_id

        logger.info(f"TTS: {len(text)} chars with voice {voice_id}")

        async with httpx.AsyncClient(timeout=self.timeout) as client:
            response = await client.post(
                f"{self._base_url}/text-to-speech/{voice_id}",
                headers={
                    **self._get_headers(),
                    "Content-Type": "application/json"
                },
                json={
                    "text": text,
                    "model_id": model_id,
                    "voice_settings": {
                        "stability": stability,
                        "similarity_boost": similarity_boost
                    }
                }
            )
            response.raise_for_status()

        return TTSResult(
            audio_data=response.content,
            format="mp3",
            metadata={
                "voice_id": voice_id,
                "model_id": model_id,
                "text_length": len(text)
            }
        )

    async def dub_audio(
        self,
        audio_path: str,
        target_language: str,
        voice_id: str = None,
        source_language: str = "en",
        **kwargs
    ) -> DubbingResult:
        """
        Dub audio to target language.

        Uses ElevenLabs dubbing API for full audio translation.

        Args:
            audio_path: Path to source audio
            target_language: Target language code
            voice_id: Voice ID for dubbing
            source_language: Source language code

        Returns:
            DubbingResult with dubbed audio path
        """
        voice_id = voice_id or self.default_voice_id
        path = Path(audio_path)

        logger.info(f"Dubbing {path.name} to {target_language}")

        async with httpx.AsyncClient(timeout=300) as client:  # Longer timeout for dubbing
            with open(path, "rb") as f:
                response = await client.post(
                    f"{self._base_url}/dubbing",
                    headers=self._get_headers(),
                    files={"file": (path.name, f, "audio/mpeg")},
                    data={
                        "target_lang": target_language,
                        "source_lang": source_language,
                        "voice_id": voice_id
                    }
                )
                response.raise_for_status()

        # Save dubbed audio
        output_path = path.with_stem(f"{path.stem}_{target_language}")
        output_path.write_bytes(response.content)

        return DubbingResult(
            audio_path=str(output_path),
            language=target_language,
            voice_id=voice_id,
            duration=0,  # Would need to analyze audio to get duration
            metadata={
                "source_language": source_language,
                "source_file": str(path)
            }
        )

    async def clone_voice(
        self,
        name: str,
        audio_files: List[str],
        description: str = ""
    ) -> Voice:
        """
        Clone a voice from audio samples.

        Args:
            name: Name for the cloned voice
            audio_files: List of audio file paths
            description: Voice description

        Returns:
            Created Voice object
        """
        files = []
        for path in audio_files:
            with open(path, "rb") as f:
                files.append(("files", (Path(path).name, f.read(), "audio/mpeg")))

        async with httpx.AsyncClient(timeout=120) as client:
            response = await client.post(
                f"{self._base_url}/voices/add",
                headers=self._get_headers(),
                files=files,
                data={
                    "name": name,
                    "description": description
                }
            )
            response.raise_for_status()
            data = response.json()

        return Voice(
            id=data["voice_id"],
            name=name,
            language="en",
            description=description
        )


class MockDubbingService(DubbingService):
    """
    Mock dubbing service for demo mode.
    """

    async def get_voices(self, language: str = None) -> List[Voice]:
        """Return mock voices."""
        voices = [
            Voice("voice-1", "Sarah (News Anchor)", "en", "Professional news anchor voice"),
            Voice("voice-2", "James (Reporter)", "en", "Field reporter voice"),
            Voice("voice-3", "Maria (Spanish)", "es", "Spanish female voice"),
            Voice("voice-4", "Pierre (French)", "fr", "French male voice"),
            Voice("voice-5", "Hans (German)", "de", "German male voice"),
        ]

        if language:
            return [v for v in voices if v.language == language]
        return voices

    async def text_to_speech(
        self,
        text: str,
        voice_id: str = None,
        **kwargs
    ) -> TTSResult:
        """Return mock TTS result."""
        await asyncio.sleep(0.5)

        # Generate mock audio data (just bytes for demo)
        mock_audio = b"MOCK_AUDIO_DATA_" + text[:50].encode()

        return TTSResult(
            audio_data=mock_audio,
            format="mp3",
            duration=len(text) * 0.05,  # Rough estimate
            metadata={"mock": True, "voice_id": voice_id}
        )

    async def dub_audio(
        self,
        audio_path: str,
        target_language: str,
        voice_id: str = None,
        **kwargs
    ) -> DubbingResult:
        """Return mock dubbing result."""
        await asyncio.sleep(1)

        output_path = f"{audio_path}.{target_language}.mp3"

        return DubbingResult(
            audio_path=output_path,
            language=target_language,
            voice_id=voice_id or "mock-voice",
            duration=60.0,
            metadata={"mock": True}
        )
