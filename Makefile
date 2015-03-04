Minimum-Font.bdf: Minimum-Font.png
	python png2bdf.py $< 4 8 > $@
