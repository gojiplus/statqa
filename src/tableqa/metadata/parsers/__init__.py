"""Codebook parsers for various formats."""

from tableqa.metadata.parsers.base import BaseParser
from tableqa.metadata.parsers.csv import CSVParser
from tableqa.metadata.parsers.text import TextParser


__all__ = ["BaseParser", "CSVParser", "TextParser"]
