## Metaprogramming

[MIT 6.NULL - Metaprogramming](https://missing.csail.mit.edu/2020/metaprogramming/)

### Build systems

概念：dependencies, targets, rules

`make`和`Makefile`
* 根据modify time确定什么文件需要regenerate
```shell
target: prerequisite1 prerequisite2 ...
	command1
	command2 (需要tab)
```
```shell
paper.pdf: paper.tex plot-data.png
	pdflatex paper.tex

plot-%.png: %.dat plot.py
	./plot.py -i $*.dat -o $@
```


```shell
# specify all source files here
SRCS = hw.c helper.c

# specify target here (name of executable)
TARG = hw

# specify compiler, compile flags, and needed libs
CC   = gcc
OPTS = -Wall -O
LIBS = -lm

# this translates .c files in src list to .o’s
OBJS = $(SRCS:.c=.o)

# all is not really needed, but is used to generate the target, default directive
all: $(TARG)

# this generates the target executable
$(TARG): $(OBJS)
	$(CC) -o $(TARG) $(OBJS) $(LIBS)
	
# this is a generic rule for .o files
%.o: %.c
  $(CC) $(OPTS) -c $< -o $@

# and finally, a clean line
.PHONY: clean
clean:
	rm -f $(OBJS) $(TARG)
```
* 第一个directive是default goal
* indent后面的命令是建立依赖的语句
* [.PHONY](https://www.gnu.org/software/make/manual/html_node/Phony-Targets.html)避免clean和名为clean的文件冲突

```shell
SUBDIRS = foo bar baz

.PHONY: subdirs $(SUBDIRS)

subdirs: $(SUBDIRS)

$(SUBDIRS):
        $(MAKE) -C $@

foo: baz
```



### Dependency management
概念：repository, versioning, version number, [semantic versioning](https://semver.org/)

- If a new release does not change the API, increase the patch version.
- If you *add* to your API in a backwards-compatible way, increase the minor version.
- If you change the API in a non-backwards-compatible way, increase the major version.

lock file: a file that lists the exact version you are *currently* depending on of each dependency

* vendoring: copy all the code of your dependencies into your own project

makedepend工具能帮助寻找依赖

### Continuous integration(CI) systems

“stuff that runs whenever your code changes”

* e.g. Travis CI, Azure Pipelines, and GitHub Actions
* Pages is a CI action that runs the Jekyll blog software on every push to `master` and makes the built site available on a particular GitHub domain

**testing**

- Test suite: a collective term for all the tests
- Unit test: a “micro-test” that tests a specific feature in isolation
- Integration test: a “macro-test” that runs a larger part of the system to check that different feature or components work *together*.
- Regression test: a test that implements a particular pattern that *previously* caused a bug to ensure that the bug does not resurface.
- Mocking: the replace a function, module, or type with a fake implementation to avoid testing unrelated functionality. For example, you might “mock the network” or “mock the disk”.



