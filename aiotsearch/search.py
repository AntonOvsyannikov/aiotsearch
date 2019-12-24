import asyncio
from typing import Dict, List, Tuple

# noinspection PyUnresolvedReferences
from .tokenizers import tokenize_naive, tokenize_pymorphy

# You can choose tokenizer here
tokenize = tokenize_pymorphy


class Search:
    class StateError(Exception):
        pass

    def __init__(self):
        # Dict[topic_name, List[tokenized_topic_phrase]]
        self.topics: Dict[str, List[set]] = {}

        # Dict[token, topic_names_set]
        self.reverse_index: Dict[str, set] = {}

        self.commited = False
        self.lock = asyncio.Lock()

    async def add_topics(self, topics: List[Tuple[str, List[str]]]):  # List[Tuple[topic_name, List[topic_phrase]]]

        def do_add_topics(topics):
            result = []

            for topic_name, topic_phrases in topics:
                self.topics[topic_name] = self.topics.get(topic_name, [])
                for phrase in topic_phrases:
                    phrase_tokenized = tokenize(phrase)
                    self.topics[topic_name].append(phrase_tokenized)
                    for token in phrase_tokenized:
                        self.reverse_index[token] = self.reverse_index.get(token, set())
                        self.reverse_index[token].add(topic_name)
                result.append(topic_name)

            return result

        async with self.lock:
            if self.commited:
                raise Search.StateError('Already commited')
            # do under lock!
            return await asyncio.get_event_loop().run_in_executor(None, do_add_topics, topics)

    async def commit(self):
        async with self.lock:
            if self.commited:
                raise Search.StateError('Already commited')
            self.commited = True

    async def search(self, phrase: str):
        async with self.lock:
            if not self.commited:
                raise Search.StateError('Not commited')

        def do_search(phrase: str):
            result_topics = []

            phrase_tokenized = tokenize(phrase)

            # find topic candidates using reverse index, i.e. topics where at least one token from search prase exists
            candidates = set()
            for token in phrase_tokenized:
                if token in self.reverse_index:
                    candidates = candidates.union(self.reverse_index[token])

            def is_in_topic(search_phrase: set, phrases: List[set]):
                for topic_phrase in phrases:
                    if topic_phrase.issubset(search_phrase):
                        return True
                return False

            # do search in candidates
            for topic in candidates:
                phrases = self.topics[topic]
                if is_in_topic(phrase_tokenized, phrases):
                    result_topics.append(topic)

            return result_topics

        return await asyncio.get_event_loop().run_in_executor(None, do_search, phrase)
