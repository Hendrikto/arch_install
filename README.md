# arch_install
Interactively install a list of Arch packages.

## Input Format
This is an example input file containing a comment, a line with only whitespace, and an empty line, as well as a line with a package name.

```
# comment
  

package1
```

### Rules
1. Leading and trailing whitespace is discarded from every line
2. Lines are discarded if
	* they are empty
	* they start with a `#`
3. Remaining lines are interpreted as package names
