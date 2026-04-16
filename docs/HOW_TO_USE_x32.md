## How to Use (x32dbg)

### 1. Analyze the binary

- Open **BinNexus.Probe**
- Load your target DLL / EXE
- Run analysis
- Identify interesting candidates

> [!TIP]
> Focus on high-score results and relevant API patterns (network, memory, loader)

---

### 2. Open binary in x32dbg

- Launch x32dbg
- Open the target executable or attach to process

---

### 3. Locate the function

Using the result from BinNexus.Probe:

- Find the function by **VA (Virtual Address)**

In x32dbg:

- Press `Ctrl + G`
- Enter the address:

````

```text
0x6CED3D2
````

````md
- Navigate to the function

---

### 4. Inspect behavior

Look for:

- API calls (`send`, `recv`, `LoadLibrary`, etc.)
- Control flow (branches, loops)
- Memory operations

> [!IMPORTANT]
> BinNexus.Probe gives you **entry points**, not full context.

---

### 5. Modify / patch

Typical workflow:

- NOP instructions
- Redirect jumps
- Hook function calls

Example:

- Disable condition
- Replace call
- Force return value

---

### 6. Validate changes

- Run the program
- Observe behavior
- Iterate if needed

---

## Workflow Summary

```text
Probe → Locate → Inspect → Patch
```
````

> [!TIP]
> Use BinNexus.Probe to avoid blind reversing.
