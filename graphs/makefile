GOAL = regex.pdf
FLAG = -Tpdf
SRC  = 0.gv
OUT  = 0.pdf

$(GOAL): $(SRC)
	dot $(FLAG) $< -o $(OUT)

.PHONY: clear

clear:
	rm -rf *.pdf *.gv
