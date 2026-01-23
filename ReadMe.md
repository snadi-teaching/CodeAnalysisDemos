# About

This repo contains a bunch of demos related to tools for analyzing source code. These are simple tools & use cases just to demonstrate available options and how to get started.

The demos are prepared by [Sarah Nadi](https://sarahnadi.org) and mainly used for various levels of courses related to Mining Software Repositories and Software Analytics.

# Running the Demos

The repo comes with a Dockerfile that takes care of using the correct version of Java and setting up dependencies, including compiling the various projects into jar files to use.

To build the Docker image (this may take a bit of time):

```
docker build --tag=ca-demo:f23 .
```

To run the docker image:

```
docker run --name CADemo -it --rm ca-demo:f23 /bin/bash
```

Unless otherwise specified, all instructions for analyzing Java programs below are based on running from within the Docker image (which means that all most code for the demos has been compiled already)

For the Python demo, instructions provided below and no additional dependencies are needed. Just make sure to have Python installed.

## Using JDT for AST Processing

**NOTE: this currently produces an error on the Docker container (See Issue [#2](https://github.com/snadi/CodeAnalysisDemos/issues/2)). Fixes welcome. In the meantime, you can run this demo locally by first compiling the project with `mvn clean package assembly:single`**

We use the Eclipse JDT APIs to process the AST of corresponding code. The `MethodInvPrinter` prints out all invocations found in `resources/test-inv.java`. The `MethodiInvocationCounter` counts how many times each method is called. `VarDeclCounter` prints out all declarations found in `resources/test.java`.

```
/ca-demo# cd ASTDemos/
/ca-demo/ASTDemos# java -cp target/AST_JDT-1.0-SNAPSHOT-jar-with-dependencies.jar MethodInvPrinter
test:
	st_test.indexOf(["ell"])
	st_test.substring([2, 4])
test2:
	arrayList.add(["Hello"])
	arrayList.add([1, "World"])
	arrayList.get([0])
	testStr.substring([2, 4])

/ca-demo/ASTDemos# java -cp target/AST_JDT-1.0-SNAPSHOT-jar-with-dependencies.jar MethodInvocationCounter
add is called 2 times
indexOf is called 1 times
substring is called 2 times

/ca-demo/ASTDemos# java -cp target/AST_JDT-1.0-SNAPSHOT-jar-with-dependencies.jar VarDeclCounter
Declaration of 'i' at line2
Declaration of 'j' at line3
Declaration of 'al' at line4
```


## GumTreeDiff Demo

[GumTree](https://github.com/GumTreeDiff/gumtree) can analyze two versions of a piece of code, map nodes from one version to the other, and detecte the change operations that occurred. The current demo simply prins the edit actions that occurred between programs `examples/Version1.java` and  `examples/Version2.java`

```
/ca-demo# cd GumTreeDiffDemo/
/ca-demo/GumTreeDiffDemo# java -jar target/GumTreeDiffDemo-1.0-SNAPSHOT-jar-with-dependencies.jar

===
insert-tree
---
MethodDeclaration [113,177]
    Modifier: private [113,120]
    SimpleName: newMethod [128,137]
    ClassOrInterfaceType [121,127]
        SimpleName: String [121,127]
    BlockStmt [139,177]
        ExpressionStmt [143,174]
            MethodCallExpr [143,173]
                FieldAccessExpr [143,153]
                    NameExpr [143,149]
                        SimpleName: System [143,149]
                    SimpleName: out [150,153]
                SimpleName: println [154,161]
                StringLiteralExpr: I'm new! [162,172]
to
ClassOrInterfaceDeclaration [26,99]
at 3
===
update-node
---
SimpleName: foo [59,62]
replace foo by boo
===
insert-tree
---
ExpressionStmt [97,107]
    VariableDeclarationExpr [97,106]
        VariableDeclarator [101,106]
            PrimitiveType: int [97,100]
            SimpleName: x [101,102]
            IntegerLiteralExpr: 5 [105,106]
to
BlockStmt [64,97]
at 1
```

## Spoon Examples

Check out ReadMe in [https://github.com/SpoonLabs/spoon-examples](https://github.com/SpoonLabs/spoon-examples).

## BOA Demo

Not part of the Docker container

Boa homepage is [http://boa.cs.iastate.edu](http://boa.cs.iastate.edu) and contains all necessary documentation. You need an account to run queries.

1. View the example at [http://boa.cs.iastate.edu/examples/index.php#null-check](http://boa.cs.iastate.edu/examples/index.php#null-check)
2. Run the example on the small dataset (so it finishes quickly)
3. Go to your list of jobs to view the result

## Python Examples

Check `PythonDemos/analyze_exception_handling.py` which uses the python ast module to parse an AST to find exception handling nodes. It then analyzes the body of the except clause to determine code smells for exception handling.

To run:

```
cd PythonDemos
python analyze_exception_handling.py test_program.py
```

Try passing in a path to a project you are interested in analyzing and see how good that project is at excetion handling.