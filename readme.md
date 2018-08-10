 Coding Challenge:
 Company automatically flags comments and messages that are deemed offensive.
 This is done by detecting key phrases in the text and assigning it a score.
 If the score is over a certain threshold, it is flagged as offensive.

 Write a program in Go or PHP, or any language you feel skilled in (e.g. Ruby, Python)
 that reads input files of potentially offensive text and writes to an output file with
 scores for each of the text files (details below).

 You are given two files with lists of offensive phrases.
 One file contains "low risk" phrases and the other, "high risk" phrases, one phrase per line.
 You are also given a set of 15 input files, each one containing
 some possibly offensive text that your program will score.

 The offensive score is defined as:
 (number of low risk phrases) + (number of high risk phrases * 2)

 Your program should write out one output file containing
 the scores of each input file in order, in the format:
 <input-filename-1>:<score-1>
 <input-filename-2>:<score-2>

 ASSUMPTIONS
 1. Comment scoring is not case sensitive. ShOOter will be scored as shooter.
 2. Input files will have input<number>.txt pattern.
 3. If file doesn't exist, it's score will be set to zero in the output.
 4. Only exact phrase is matched. Leading and Trailing characters around
 the offensive phrase are not ignored.
 It was necessary to avoid incorrectly scoring comment when
 a offensive keyword like sick will be detected in words like "homesick".
 Example: kkkittenn will not be detected as kitten.

 NOTES
 showPrompt function needs improvements.

 SOLUTION
 Since the scale of problem is small, dictionary lookup, 
 the regex matching and count methods work in short time. 
 After timing the all three using timeit, I found Dict Lookup to be the fastest.
 So after this analysis, I decided to use it to solve the challenge
