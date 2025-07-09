# pylint: disable=invalid-name, missing-module-docstring
# pylint: disable=bad-indentation, line-too-long, trailing-whitespace
# pylint: disable=missing-function-docstring, unused-variable, unbalanced-tuple-unpacking, wrong-import-order
import asyncio
import re
from fuzzywuzzy import process
from emoji import EMOJI_DATA
from deep_translator import GoogleTranslator
import lyricsgenius
import os

emoji_keywords = []
emoji_map = {}

for emj, data in EMOJI_DATA.items():
	keywords = data.get("en", "")
	if isinstance(keywords, str):
		keywords = keywords.split()
	for kw in keywords:
		emoji_keywords.append(kw)
		emoji_map[kw] = emj

genius = lyricsgenius.Genius("N8_ueLWGTvss_0tZIruMSFdtUhYiU2hPr63LMAI9c7fMD0f-Z92P8uVcHS4Phv9S", timeout=15)
genius.verbose = False


async def get_song(title, artist):
	song = genius.search_song(title, artist)
	if song:
		os.makedirs("lyrics", exist_ok=True)
		path = f"lyrics/{title}.txt"
		with open(path, "w", encoding="utf_8") as f:
			f.write(song.lyrics)
		return path
	return None


def translate_to_english(word, src_lang='auto'):
	return GoogleTranslator(source=src_lang, target='en').translate(word).lower()


def match_emoji(line):
	match = re.search(r"\b\w+\b(?=\s*$)", line, re.UNICODE)
	if match:
		last_word = match.group()
		translated = translate_to_english(last_word)
		best_match, _ = process.extractOne(translated, emoji_keywords)
		emoji_char = emoji_map.get(best_match)
		return last_word, emoji_char
	return None, None


async def main():
	title = input("🌍 PLEASE ENTER TITLE'S NAME:\n")
	artist = input("🌍 PLEASE ENTER ARTIST'S NAME:\n")
	
	path = await get_song(title, artist)
	if not path:
		print("❌ Song not found.")
		return
	
	with open(path, "r", encoding="utf_8") as f:
		for line in f:
			line = line.strip()
			if not line:
				continue
			word, translated, emoji_char = match_emoji(line)
			if emoji_char:
				print(f"{line} {emoji_char}")


if __name__ == "__main__":
	asyncio.run(main())
