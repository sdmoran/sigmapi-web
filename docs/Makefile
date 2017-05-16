
SRC=$(shell find src/ -name *.md)
HTML=$(subst src/,html/,$(subst .md,.html,$(SRC)))

all: $(HTML)

$(HTML): $(SRC)
	mkdir -p $(subst src/,html/,$(<D))
	markdown $< > $(subst src/,html/,$(subst .md,.html,$<))

clean:
	rm -rf html/
