# potok
Protocol Over Transmission Of Knowledge

My homemade HTTP-like protocol

## Structure
POTOK message is made up of `segments`  
Each segment begins with the its `-name-`  
Name is followed by segment content, this can be raw or structurized data

### BEGIN - Segment
Identifier of POTOK

```
-BEGIN-
POTOK <--- Name of protocol
0.1   <--- Version
GET   <--- Method
```

### HEAD - Segment
This segment contains additional information  
Each line is a key-value pair

```
-HEAD-
Target: example
Origin: here
Location: home
```

### BODY - Segment
Request payload   
The data should be escaped, by replacing `-` with `\-`

```
-BODY-
rawdatabytes...
ewerfer56t4g43f
4364g3r3t5yvwvd
8net357u67453bh
```

### Example
```
-BEGIN-
POTOK
0.1
GET
-HEAD-
Target: example
Origin: here
-BODY-
rawdatabytes...
ewerfer56t4g43f
4364g3r3t5yvwvd
8net357u67453bh
```