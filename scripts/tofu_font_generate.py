#!/usr/bin/env fontforge -lang=py -script
# -*- coding: utf-8 -*-
#
# michinari.nukazawa@ "project daisy bell"
# (michinari.nukazawa@gmail.com)
# License: BSD class-2
# 
# Special Thanks
# mashabow＠しろもじ作業室（http://shiromoji.net, mashabow@shiromoji.net）
# koruri(lindwurm)
# https://gist.github.com/lindwurm/b24657c335bb11a520c4/9461c1690188ddd2b6d721467653e6e0072689b8
# Import SVGs
# http://mshio.b.sourceforge.jp/2010/10/15/how2import-2/
#

#
# test: fontforge -lang=py -script ./font_generate.py RuneAMN_Pro_BlackletterPLow 0.001 500 1000 100 no
#

import sys
import fontforge
import os

def sfnt_names(fontname, weight, version):
	return (
		('English (US)', 'Copyright',
		'TofuFont: Copylight (c) 2015-, daisy bell.'),
		('English (US)', 'Family', fontname + ' {0}'.format(weight)),
		('English (US)', 'SubFamily', weight),
		('English (US)', 'Fullname', fontname + '-{0}'.format(weight)),
		('English (US)', 'Version', version),
		('English (US)', 'PostScriptName', fontname + '-{0}'.format(weight)),
		('English (US)', 'Vendor URL', 'http://michinari-nukazawa.com/'),
		('English (US)', 'Preferred Family', fontname),
		('English (US)', 'Preferred Styles', weight),
		('Japanese', 'Preferred Family', fontname),
		('Japanese', 'Preferred Styles', weight),
	)
	
def copyReferenceOfRange(font, ucSrc, top, tail):
	print("copy start: {0} {1}".format(top, tail))
	for i in range(top, tail):
		if 0 == (i % 0xFFF):
			print("copying...: %d" % i)
		if i == ucSrc:
			continue
		ucDst =  i
		font.selection.select(ucSrc)
		font.copyReference()
		font.selection.select(ucDst)
		font.paste()

def main():
	print("start TofuFont Script.")
	
	if(not(3 == len(sys.argv))):
		print("error: args length :%d\n" % len(sys.argv))
		sys.exit(-1)
	
	version  = sys.argv[1]
	familyname = "TofuFont"
	fontnameSub = sys.argv[2]
	fontName = familyname + fontnameSub
	width	= 500
	height   = 1000
	baseline = 100	
	
	fontFilename = fontName + "_" + version
	fontFilenameOfLatest = fontName + "_latest"
	
	# create new font.
	font = fontforge.font()
	
	# エンコードにUnicodeを指定
#	font.encoding = "unicode"
	font.encoding = "unicode4"
#	font.encoding = "ISO-10646-1" # できない

	# 半角文字の高さ／深さ(ベースライン)設定
	# set Baseline
	font.em = 1000
	font.descent = baseline
	font.ascent = height - baseline

	# created .notdef
	glyphSpace = font.createChar(0x0000)
	glyphSpace.glyphname = ".notdef"


	font.os2_use_typo_metrics = True

	font.hhea_ascent_add = False
	font.hhea_descent_add = False
	font.os2_typoascent_add = False
	font.os2_typodescent_add = False
	font.os2_winascent_add = False
	font.os2_windescent_add = False

	#descent
	font.os2_typodescent = (-baseline)
	font.os2_windescent = baseline
	font.hhea_descent = (-baseline)
	
	# ascent
	font.os2_typoascent = height - baseline
	font.os2_winascent = height - baseline
	font.hhea_ascent = height - baseline

	# フォント情報設定

	font.sfnt_names = sfnt_names(fontName, "Regular", version)	
	font.fontname = fontName
	font.familyname = fontName
	font.fullname = fontName
	font.weight = "Regular"
	font.copyright = "© 2015 Michinari.Nukazawa"
	font.version = version


	# source glyph
	ucSrc =  (0x0041) # A

	# importing tofu SVG
	pathTofuSvg = "./FontSources/TofuFont/A.svg"
	font.createChar(ucSrc)
	font[ucSrc].importOutlines(pathTofuSvg)

	# 大文字を小文字に(リファレンス)コピーする
	# en_US
	copyReferenceOfRange(font, ucSrc, 0x0001, 0x00FF)
	if "_ja" == fontnameSub:
		# U+3040～U+309F	平仮名用に割り当てられたコードポイント
		copyReferenceOfRange(font, ucSrc, 0x3040, 0x309F)
		# U+30A0～U+30FF	片仮名用に割り当てられたコードポイント
		copyReferenceOfRange(font, ucSrc, 0x30A0, 0x30FF)
		# U+31F0～U+31FF	片仮名の音声用用拡張コードポイント
		copyReferenceOfRange(font, ucSrc, 0x31F0, 0x31FF)
		# U+FF00～U+FFEF	全角 ASCII 、半角カタカナ、半角ハングルおよび、全角シンボル のコードポイント
		copyReferenceOfRange(font, ucSrc, 0xFF00, 0xFFEF)
		# CJK統合漢字 unicode1.0.1
		copyReferenceOfRange(font, ucSrc, 0x4e00, 0x9FFF)
		copyReferenceOfRange(font, ucSrc, 0xF900, 0xFAFF) # CJK互換漢字
		copyReferenceOfRange(font, ucSrc, 0x3400, 0x4DB5) # CJK統合漢字拡張A集合
	elif "" == fontnameSub: # full
		copyReferenceOfRange(font, ucSrc, 0x0100, 0xFFF0)

	# 半角スペース作成
	glyphSpace = font.createChar(0x0020)
	glyphSpace.clear()
	glyphSpace.width = width

	# 全角スペース作成
	glyphSpace = font.createChar(0x3000)
	glyphSpace.clear()
	glyphSpace.width = 1000


	## デザイン上の各種設定
	font.selection.none()
	font.selection.all()
	# パスの統合
	# print("before removeOverlap")
	# とてもたくさんの内部エラーを吐き出す。
	font.removeOverlap()
	# 整数値に丸める
	font.round()
	# アウトラインの向きを修正
	font.correctDirection()
	
	font.selection.none()
	font.selection.select(("ranges",None), 0x0020, 0x007e)
	for glyph in font.selection.byGlyphs:
		# 自動ヒント有効化
		glyph.autoHint()
		
		# 半角文字の文字幅設定
		glyph.vwidth = 1000
		glyph.width = width	
	
	# .sfd を出力
	#font.save("releases/" + fontFilename + ".sfd") 
	
	font.generate("releases/" + fontFilename + ".otf", '', ('short-post', 'opentype', 'PfEd-lookups'))
	font.generate("releases/" + fontFilenameOfLatest + ".otf", '', ('short-post', 'opentype', 'PfEd-lookups'))

	print ("generated: "+ fontFilename)

	font.close()



if __name__ == '__main__':
	main()

