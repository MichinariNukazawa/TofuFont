#
# make -f ./scripts/font.makefile all
#
# Want: sudo apt-get install fontforge -y
# Want: sudo apt-get install texlive -y
#

FontName=TofuFont
Version=0.23
FontFile=./releases/$(FontName)_$(Version).otf
BookFile=./releases/book_of_$(FontName).pdf
ZipFile=$(FontName)_$(Version).zip

# all: font
# all: font book
all: $(ZipFile)
font: $(FontFile)
book: $(BookFile)

$(ZipFile) : $(FontFile) $(BookFile) docs/etcs/*
	./scripts/mkzip_retail_distribution.sh $(FontName) $(Version)

$(FontFile) : FontSources/$(FontName)/A.svg
	# フォントファイル生成スクリプトを呼び出す
	fontforge -lang=py -script ./scripts/tofu_font_generate.py $(Version) "_en"
	fontforge -lang=py -script ./scripts/tofu_font_generate.py $(Version) "_ja"
	fontforge -lang=py -script ./scripts/tofu_font_generate.py $(Version) ""

$(BookFile) : docs/book/*.pdf
	pdflatex -halt-on-error -interaction=nonstopmode -file-line-error \
		./scripts/book_of_TofuFont.tex > tex.log
	mv book_of_TofuFont.pdf ./releases/
	rm book_of_TofuFont.aux
	rm book_of_TofuFont.log

