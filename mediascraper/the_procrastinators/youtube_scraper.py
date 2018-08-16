from pathlib import Path
import requests
import json
import yaml
from pprint import pprint
from typing import List, Tuple
import re
import datetime
from dataclasses import dataclass
from pytools.timetools import Duration
shownotes_regex = ""

@dataclass
class Shownote:
	timestamp: Duration
	title: str
	link: str

def extract_description(text:str)->str:
	description, *junk = text.split('PCP Episode')
	description = description.strip()
	return description

def extract_shownotes(lines:List[str])->List[Shownote]:
	""" Extracts the timestamps, titles, and links of each shownote."""
	regex = re.compile("[\d]+:[\d]+(?:[:][\d]+)?")
	shownotes = list()
	for current_line, next_line in zip(lines[:-1], lines[1:]):
		if regex.match(current_line):
			_time, *_title = current_line.split(' ')

			timestamp = Duration.from_string(_time)
			title = " ".join(_title)
			link = next_line
			shownote = Shownote(timestamp, title, link)
			shownotes.append(shownote)
	return shownotes


if __name__ == "__main__":
	sample = Path(__file__).parent / "Tourist Trap Stockholm Syndrome - The Pro Crastinators Podcast, Episode 119-toHfm6RyLYo.info.json"
	data = json.loads(sample.read_text())
	description = data['description']
	#print(description)
	pprint(extract_shownotes(description.split('\n')))

