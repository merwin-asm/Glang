
# Glang
A lang ment for game dev.

<p align="right"> <img src="https://komarev.com/ghpvc/?username=merwin-glang&label=Project%20views&color=0e75b6&style=flat" alt="darkmash-org" /> </p>

## Docs

 
- Glang (Extension `.ga`) ver. 1.0.0

- CLI Commands:
  ``` 
    Glang run <path>
    Glang help-cmd
    Glang help-lang
    Glang version
   ```

- Note:
    - > The files are located in /home/user/Glang
    - > Only 2D InBuild support
    - > Installer only for linux
- Extras:
     - > Internal Python Code execution (
            Put the code in {}.
            eg:
                {
                print("Hello World")
                }
                Make sure you don't write code in the same line in which "{" or "}" is present.
        )

### Making Vars:
    
    MAKE NAME = VALUE

### Operators:
        +
        -
        /
        *
        **
        etc
        (Uses PEMDAS rule)
        When redefining a var:
            UPDATE var = var + 1
### Function:
        Call <function name> [<args>] (calling a function)

        Func <function name> [var1,var2(Params-which-are-required)]
        (
        sum =  var1 + var2
        return sum
        )

### Internal Vars:
        STARTUPTIME , contains how long the program took to start.
        OS , contains the OS you are on.

### Loop:
        Loop
        (
        PRINT "hello"
        )
        use BREAK to end

### InBuild Functions:
       
       
        SET_BG [ 0,0,0]
        PRINT "TEXT"
        PRINTLN "TEXT"
        for colored printing:
        PRINTLN "[red]TEXT[/red]" or  PRINT "[red]TEXT[/red]"

        

## Authors

- [@Merwin](https://www.github.com/mastercodermerwin)

