"""source （ DataFetcher type）。"""

from shared.datafetcher.sources.entities import EntitySource
from shared.datafetcher.sources.knowledge import KnowledgeSource
from shared.datafetcher.sources.vocab import VocabSource

__all__ = ["EntitySource", "KnowledgeSource", "VocabSource"]