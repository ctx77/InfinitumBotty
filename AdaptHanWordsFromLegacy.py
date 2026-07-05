#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from faustbot.model.HanDatabaseProvider import HanDatabaseProvider
import csv

HanDBProvider = HanDatabaseProvider()
wordList = open("logs/HangmanLog")
wordListWords = csv.reader(wordList, delimiter=";", quotechar="|")
randomChoicePool = []
for word in wordListWords:
    print(word)
    print(word[1].strip())
    no = False
    for char in ["ä", "ü", "ö", "ß"]:
        if char.upper() in word[1].strip().upper():
            no = True
    if not no:
        HanDBProvider.addWord(word[1].strip())
