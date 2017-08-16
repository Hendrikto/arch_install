# arch_install
Interactively install a list of Arch packages.

## Input Format
This is an example input file containing a comment, a line with only whitespace, and an empty line, as well as a line with a package name.

```
# comment
  

package1
```

### Rules
* empty lines are ignored
* lines containing only whitespace are ignored
* lines beginning with `#` are ignored
* all other lines are interpreted as package names
