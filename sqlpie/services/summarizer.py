# -*- coding: utf-8 -*-
"""

SQLpie License (MIT License)
Copyright (c) 2011-2016 André Lessa, http://sqlpie.com
See LICENSE file.

"""

#
# Text Summarization Service
#

from flask import g
import sqlpie
import json

from stemming.porter2 import stem
from collections import Counter
import re, math
from string import punctuation

class Summarizer(object):
    ALL_FIELDS = "ALL_FIELDS"
    MAX_SENTENCES = 10
    MAX_SUMMARY_SIZE = 6000
    MAX_SUMMARY_PERCENT = 80
    MAX_KEYWORDS = 5
    MAX_ENTITIES = 10

    def __init__(self, bucket, document_ids, documents):
        if bucket is not None and document_ids is not None:
            documents = []
            bucket_id = sqlpie.Bucket(bucket).bucket_id
            for doc_id in document_ids:
                hexed_doc_id = sqlpie.Util.to_sha1(unicode(doc_id))
                documents.append(sqlpie.Document.get(bucket_id, hexed_doc_id).document)
        self.documents = documents

    def word_tokenize(self, sentence):
        words = re.split('\W+', sentence)
        return words

    def tokenize(self, text, use_stem=True):
        if use_stem:
            tokens = [stem(w.lower()) for w in self.word_tokenize(text) if w not in punctuation and not sqlpie.global_cache[sqlpie.Config.STOPWORDS].get(w.lower()) and re.match('[A-Z0-9]', w, re.IGNORECASE)]
        else:
            tokens = [w.lower() for w in self.word_tokenize(text) if w not in punctuation and not sqlpie.global_cache[sqlpie.Config.STOPWORDS].get(w.lower()) and re.match('[A-Z0-9]', w, re.IGNORECASE)]
        return tokens

    def sent_tokenize(self, text):
        sentence_delimiters = re.compile(ur"""
            (?:
              (?<=[(\s)+.!?])
            | (?<=[(\s)+.!?]['"])
            )
            (?<! a\.m\. )
            (?<! b\.a\. )
            (?<! b\.s\. )
            (?<! d\.d\.s\. )
            (?<! dr\. )
            (?<! e\.g\. )
            (?<! etc\. )
            (?<! ft\. )
            (?<! gen\. )
            (?<! hon\. )
            (?<! i\.e\. )
            (?<! in\. )
            (?<! inc\. )
            (?<! jr\. )
            (?<! mr\. )
            (?<! mrs\. )
            (?<! prof\. )
            (?<! sr\. )
            (?<! m\.a\. )
            (?<! m\.d\. )
            (?<! ms\. )
            (?<! ph\.d\. )
            (?<! p\.m\. )
            (?<! rep\. )
            (?<! rev\. )
            (?<! sen\. )
            (?<! st\. )
            (?<! ste\. )
            (?<! u\.k\. )
            (?<! u\.s\. )
            (?<! u\.s\.a\. )
            (?<! v\.s\. )
            \s+
            """,
            re.IGNORECASE | re.VERBOSE | re.UNICODE)
        sentenceList = [s.replace(u"\u2018", u"'").replace(u"\u2019", u"'").replace( u'\u201c', u'"').replace( u'\u201d', u'"') \
                         for s in sentence_delimiters.split(text)]
        return sentenceList

    def split_to_sentences(self, text):
        sentences = self.sent_tokenize(text)
        t1 = []
        for s in sentences:
            t1.extend(s.split("\n \n"))

        sentences = [(idx, s.replace('\r',' ').replace('\n',' ').replace('\t',' ').replace('  ',' ').strip()) for idx, s in enumerate(t1)]
        return sentences

    def token_frequency(self,text, use_stem=True):
        frequencies = {}
        for token in self.tokenize(text, use_stem=use_stem):
            frequencies[token] = frequencies.get(token, 0) + 1
        return frequencies

    def ngrams(self, l, ngrams, min_occurrences, text):
        new_list = zip(*[l[i:] for i in range(ngrams)])
        list_with_counts = Counter(new_list)
        return [k for v,k in sorted([(v,k) for k,v in list_with_counts.items()],reverse=True) if list_with_counts[k] >= min_occurrences and " ".join(k) in text.lower()]

    def ngram_frequency(self, text, min_occurrences):
        words = [w.lower() for w in self.word_tokenize(text) if w not in punctuation and not sqlpie.global_cache[sqlpie.Config.STOPWORDS].get(w.lower()) and re.match('[A-Z0-9]', w, re.IGNORECASE)]

        # only n-grams that appear min_occurrences+ times
        bigrams = self.ngrams(words, 2, min_occurrences, text)
        trigrams = self.ngrams(words, 3, min_occurrences, text)
        return (bigrams, trigrams)

    def entity_extractor(self, text, max_entities):
        frequencies = {}
        for s in self.split_to_sentences(text):
            sentence = s[1]
            possible_tokens = self.word_tokenize(sentence)
            candidates = [(i, w) for i, w in enumerate(possible_tokens) if len(w) > 1 and w[0].isupper() and \
                            not w[1].isupper() ]
            entity_candidates = []
            prev_index = -1
            ec = []
            for i, c in enumerate(candidates):
                phrase = " ".join(ec+[c[1]])
                if i == 0 or c[0] == (prev_index+1):
                    if len(phrase.strip()) > 0 and phrase in sentence:
                        ec.append(c[1])
                    else:
                        entity_candidates.append(ec)
                        ec = []
                        ec.append(c[1])
                else:
                    entity_candidates.append(ec)
                    ec = []
                    ec.append(c[1])
                prev_index = c[0]
            if len(ec) > 0:
                entity_candidates.append(ec)

            entities = []
            for ec in entity_candidates:
                phrase = " ".join(ec)
                if phrase in text and not sqlpie.global_cache[sqlpie.Config.STOPWORDS].get(phrase.lower()) and \
                    len(ec) < (len(sentence.split()) * 0.75):
                    entities.append(phrase)

            for entity in entities:
                frequencies[entity] = frequencies.get(entity, 0) + 1

        sorted_frequencies = [k for v,k in sorted([(v,k) for k,v in frequencies.items()],reverse=True)]
        if len(sorted_frequencies) > max_entities:
            sorted_frequencies = sorted_frequencies[:max_entities]
        return sorted_frequencies

    def sentence_score(self,sentence):
        if self.sentences_num > 1:
            pos_weight =  math.cos(sentence[0] * 2 * math.pi / (self.sentences_num - 1)) + 1
        else:
            pos_weight = 0.0
        sentence_bigrams, sentence_trigrams = self.ngram_frequency(sentence[1], 1)
        bigram_matches = 0
        trigram_matches = 0
        for bigram in self.top_bigrams:
            if bigram in sentence_bigrams:
                bigram_matches = bigram_matches + 1
        for trigram in self.top_trigrams:
            if trigram in sentence_trigrams:
                trigram_matches = trigram_matches + 1
        ngram_weight = (bigram_matches + (2 * trigram_matches)) / float(1 + (len(self.top_bigrams) + (2 * len(self.top_trigrams))))
        score = sum((self.frequencies[token] for token in self.tokenize(sentence[1])))
        pos_weighted_score = score + (score * pos_weight)
        ngram_score = pos_weighted_score + (pos_weighted_score * ngram_weight)
        final_score = float("{0:.6f}".format(ngram_score))
        return final_score

    def cleanup(self, sentence):
        idx, text = sentence[0], sentence[1]
        starts_with_symbol = False
        for punct in punctuation: # string.punctuation:   '!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~'
            #punct that's ok to start sentence
            if not punct in ['$','%',]:
                if text.startswith(punct):
                    starts_with_symbol = True
                    break
        if starts_with_symbol:
            text = text[1:]
        text = text.strip()
        return (idx, text)

    def is_sentence_novel(self, summary, sentence):
        is_sentence_novel = True
        s1_score = set(sentence.lower().split())
        for s in summary:
            s2_score = set(s[1].lower().split())
            diff_score = len(s1_score.intersection(s2_score)) / ((len(s1_score)+len(s2_score)) / 2.0)
            if diff_score > 0.8:
                is_sentence_novel = False
        return is_sentence_novel

    def create_summary(self,sentences, max_sentences, max_length, max_summary_percent):
        summary = []
        size = 0
        for sentence in sentences:
            size += len(sentence[1])
            if not self.is_sentence_novel(summary, sentence[1]) or \
              (len(summary) == max_sentences or size >= max_length or size >= (self.text_size * (max_summary_percent / 100.0))):
               break
            # Clean up sentence for presentations
            sentence = self.cleanup(sentence)
            summary.append(sentence)
        if len(summary) == 0 and len(sentences) > 0:
            sentence = self.cleanup(sentences[0])
            summary.append(sentence)
        # Re-sort selected sentences back to their original order
        summary.sort(key=lambda s: s[0])
        return [(s[1], self.sentence_score(s)) for s in summary]

    def summarize(self, options):
        if "max_sentences" in options:
            max_sentences = options["max_sentences"]
        else:
            max_sentences = sqlpie.Summarizer.MAX_SENTENCES
        if "max_summary_size" in options:
            max_summary_size = options["max_summary_size"]
        else:
            max_summary_size = sqlpie.Summarizer.MAX_SUMMARY_SIZE
        if "max_summary_percent" in options:
            max_summary_percent = options["max_summary_percent"]
        else:
            max_summary_percent = sqlpie.Summarizer.MAX_SUMMARY_PERCENT
        if "max_keywords" in options:
            max_keywords = options["max_keywords"]
        else:
            max_keywords = sqlpie.Summarizer.MAX_KEYWORDS
        if "max_entities" in options:
            max_entities = options["max_entities"]
        else:
            max_entities = sqlpie.Summarizer.MAX_ENTITIES
        if "fields_to_summarize" in options:
            fields_to_summarize = options["fields_to_summarize"]
        else:
            fields_to_summarize = sqlpie.Summarizer.ALL_FIELDS

        self.text = {}
        for doc in self.documents:
            contents = sqlpie.util.walk(doc)
            for content_type_from_walk, content_key_from_walk, content_value_from_walk in contents:
                if fields_to_summarize == sqlpie.Summarizer.ALL_FIELDS or \
                  content_key_from_walk in [k+"." for k in fields_to_summarize]:
                    self.text.setdefault(content_key_from_walk[:-1],[]).append(content_value_from_walk)

        summary = {}
        field_keywords = {}
        field_entities = {}
        for key in self.text.keys():
            text = "\n\n".join(self.text[key])
            self.frequencies = self.token_frequency(text)
            self.top_bigrams, self.top_trigrams = self.ngram_frequency(text, 2)
            entities = self.entity_extractor(text, max_entities)
            topics = self.token_frequency(text, use_stem=False)
            for trigram in self.top_trigrams:
                t1, t2, t3 = trigram[0], trigram[1], trigram[2]
                if t1 in topics and t2 in topics and t3 in topics:
                    if text.count(t1+" "+t2+" "+t3) > text.count(t1+" "+t2) and text.count(t1+" "+t2+" "+t3) > text.count(t2+" "+t3):
                        topics[t1+" "+t2+" "+t3] = topics[t1]+topics[t2]+topics[t3]
                        del topics[t1]
                        del topics[t2]
                        del topics[t3]
            for bigram in self.top_bigrams:
                t1, t2 = bigram[0], bigram[1]
                if t1 in topics and t2 in topics:
                    topics[t1+" "+t2] = topics[t1]+topics[t2]
                    del topics[t1]
                    del topics[t2]
            for feature in entities:
                topics[feature.lower()] = topics.get(feature.lower(), 1) + 1
            self.topics = list(sorted(topics, key=topics.__getitem__, reverse=True))
            if len(self.topics) > max_keywords:
                self.topics = self.topics[:max_keywords]
            else:
                self.topics
            sentences = self.split_to_sentences(text)
            self.sentences_num = len(sentences)
            self.text_size = len(text.strip())
            #
            # Re-sort selected sentences based on their scores
            #
            sentences.sort(key=lambda s: self.sentence_score(s), reverse=1)
            summary[key] = self.create_summary(sentences, max_sentences, max_summary_size, max_summary_percent)
            field_keywords[key] = self.topics
            field_entities[key] = entities
        return {"fields" : summary, "field_keywords" : field_keywords, "field_entities" : field_entities}
