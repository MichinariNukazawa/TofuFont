#!/usr/bin/env fontforge -lang=py -script
# -*- coding: utf-8 -*-
#
# converted font format otf to ttf. (add gasp table).
#
# need: mkdir ttf
# all convert:  ls -1 | grep .otf | xargs -I{} fontforge --script font_extra.py {}

 
import fontforge
import sys
import os


def get_gasp():
	return (
	 (8, ('antialias',)),
	 (16, ('antialias', 'symmetric-smoothing')),
	 (65535, ('gridfit', 'antialias', 'symmetric-smoothing', 'gridfit+smoothing')),
	)


if (2 != len(sys.argv)):
	print 'Usage: # fontforge --script %s fontfile_path' % sys.argv[0]
	quit()

target_font_path = sys.argv[1]
print "target:" + target_font_path
target_font_name = os.path.basename(target_font_path)
target_font_name, ext = os.path.splitext(target_font_name)
font = fontforge.open(target_font_path)

# Grid Fittingを設定
font.gasp_version = 1
font.gasp = get_gasp()
font.generate("./ttf/" + target_font_name + ".ttf", '', ('short-post', 'opentype', 'PfEd-lookups'));
font.close()


