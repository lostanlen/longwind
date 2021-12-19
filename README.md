# longwind
Make an audio file (really) long-winded

```
Daily repetitions are an illusion anyway.
— Tristan Bath, Shilla Strelka
```

This Python script concatenates audio files in a directory. It depends on sox while circumventing one of its shortcomings: the number of arguments in a command such as `sox input output.wav` is limited to 100. Against this problem, longwind assembles audio files in small batches (default size = 50) recursively until all batches are recombined onto the same file.

Longwind has been used by composer Florian Hecker to produce `Syn As Tex [AC]`, a monumental computer music piece (51 hours). Listen at: https://etat.xyz/release/SynAsTexAC


Program made by Vincent Lostanlen, CNRS, in 2021. MIT License.