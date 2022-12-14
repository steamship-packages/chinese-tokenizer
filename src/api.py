"""Tokenizes Chinese text and adds transliterations and English translation."""
from typing import Optional, Type

from steamship import File, MimeTypes
from steamship.invocable import Config, Invocable, create_handler, post


class ChineseTokenizer(Invocable):
    """Package that transcribes audio to Markdown using in-audio formatting cues."""

    BLOCKIFIER_HANDLE = "whisper-s2t-blockifier"

    class ChineseTokenizerConfig(Config):
        """Config object containing required configuration parameters to initialize a AudioMarkdownPackage."""

        pass

    def config_cls(self) -> Type[Config]:
        """Return the Configuration class."""
        return self.ChineseTokenizerConfig

    @post("tokenize_markdown")
    def tokenize_markdown(self, content: str, mime_type: Optional[MimeTypes] = None):
        """Tokenize a Markdown text in Chinese."""
        file = File.create(self.client, content, mime_type=mime_type)
        task = file.blockify("markdown-blockifier-default-1.0")
        task.wait()
        cedict = self.client.use_plugin("cedict-tagger", "tagger")
        task = file.tag(cedict.handle)
        task.wait()
        file = file.refresh()
        return file.dict()


handler = create_handler(ChineseTokenizer)
