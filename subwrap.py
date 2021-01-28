#!/usr/bin/env python3

import sys
import logging
import os
import glob
import collections
import subprocess

logger = logging.getLogger("subwrap")

EXTS = ('srt','ssa','ass')
LANGS = {
    'en': ('en','eng'),
    'chs': ('chs','cn','sc_v2', 'sc','SC','uni_gb','gb','gbk'),
    'cht': ('cht','chi','tc','uni_big5'),
}

def play(path):
    logger.info("playing %s", path)
    path = os.path.abspath(path)
    logger.debug("Full path: %s", path)

    dirname = os.path.dirname(path)
    basename = os.path.basename(path)
    logger.debug("Dir: %s", dirname)
    logger.debug("Basename: %s", basename)

    (name, ext) = os.path.splitext(basename)
    logger.debug("Name: %s", name)
    logger.debug("Extension: %s", ext)

    subtitles = collections.defaultdict(list)
    for otherfile in os.listdir(dirname):
        if otherfile == basename: continue
        if otherfile.startswith(name):
            (othername, otherext) = os.path.splitext(otherfile)
            otherext = otherext.lower()
            if otherext.startswith('.'): otherext = otherext[1:]
            if otherext in EXTS:
                (othername2, otherext2) = os.path.splitext(othername)
                otherext2 = otherext2.lower()
                if otherext2.startswith('.'): otherext2 = otherext2[1:]
                logger.debug("other: %s %s", othername2, otherext2)

                sublang = None
                for lang, exts in LANGS.items():
                    if otherext2 in exts:
                        sublang = lang
                        break
                if sublang is None:
                    for lang, exts in LANGS.items():
                        for ext in exts:
                            if otherext2.startswith(ext):
                                sublang = lang
                                break
                        if sublang is not None: break
                if sublang is None: sublang = 'unknown'
                logger.debug("Language: %s", sublang)

                subtitles[sublang].append(otherfile)

    for sublang, subfiles in subtitles.items():
        for subfile in subfiles:
            logger.info("lang %s: %s", sublang, subfile)

    chosen = None
    chosen_lang = 'unknown'
    for lang in LANGS:
        if lang in subtitles:
            chosen = subtitles[lang][0]
            chosen_lang = lang
            break

    if chosen is None:
        if subtitles:
            chosen = list(subtitles.values())[0][0]

    if chosen is None:
        logger.error("Fail to found a subtitle for %s", path)
        subprocess.check_call(["mpv", path])
    else:
        logger.info("Chosen %s, lang %s", chosen, chosen_lang)
        chosen = os.path.join(dirname, chosen)
        subprocess.check_call(["mpv", "--sub-file=%s" % chosen, path])


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    if len(sys.argv) < 2:
        logger.error("Usage: %s <media file>", sys.argv[0])
        sys.exit(1)

    path = sys.argv[1]
    play(path)
