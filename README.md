# Enigma Machine Assignment
## Introduction
This notebook contains the full instructions for each part of the assignment, but it assumes you already have an understanding of the assignment and the basics of how an Enigma machine works.

This notebook also includes instructions for how to format your code and some test cells like the ones you have seen in the exercise sheets. These are not exhaustive and outside of matching the names in the specified tests you are welcome to choose how you structure your code. We have tried to offer a good balance between being able to test your code, offering structure for the assignment, and also offering flexibility for you to be able to show off your own design ability.

The earlier stages of this assignment contain more guidance than the later ones. You are encouraged to research and use Python features that you have not been taught in the unit, and this can add to the quality of your code. Remember also that advanced work which goes beyond the specification and is well documented will be rewarded (see the final section below).

## Part One – Simulation
In this part you will be producing a simulation of an Enigma machine using Python. Your code must be object-oriented, i.e. it must use classes. Some names of classes and methods will be specified in test cells, and you must match these where this is the case. Otherwise it is up to you how you implement the functionality and how you design your class structure.

**For all parts, you must write all of your Enigma machine code in separate files, i.e. not in the notebook cells.** In the cell below we have included an import statement `from enigma import *`. This will import the definitions (functions and classes) in a file called `enigma.py` which is located in the same directory, and a file is provided to get you started. If you wish to use a different file name, you can change this line and our tests will still run. Your code can be split across multiple files if you like, and you can include multiple import statements.


```python
from enigma_machine import *
```

### Plug Leads
Let's start simulating the Enigma machine with the plugboard, specifically the leads. Each lead in the enigma machine connects two plugs in the plugboard. If we think of the functionality of the plugboard itself in terms of how it encodes a single character, the plugboard *aggregates* the leads, so it makes sense to make a class to represent the lead objects.

Write a class called `PlugLead`. The constructor should take a string of length two, which represents the two characters this lead should connect. So the following code:
```python3
lead = PlugLead("AG")
```
creates a lead which connects A to G. Remember leads are reversible so this lead also connects G to A. 

If you are still new to object-oriented design, when you are first conceptualising a class, you should take some time to think about what attributes it has and what methods it has. Some will be required by this specification, but you are always free to add more of your own.

As part of the specification, you must implement a method called `encode(c)` on your lead, which takes a single character `c`, and returns the result of this lead on this character. 

So, with the `lead` object we created above, `lead.encode("G")` should return `"A"`.

`lead.encode("D")` should return `"D"` – this lead had no impact on the letter D, it only connects A and G. 

Of course even though it would have no effect, it should not be possible to connect a letter to itself – there is only one plug for each letter on the plugboard. For this assignment you should write your code to be robust, obeying the physical limitations of the Engima machine (at least for part one; you may decide to lift these in your extension material). 

In general “robustness” is left up to your interpretation and discretion, but in this instance we will help out by suggesting your code should `raise` an error if someone tries to construct an invalid lead. You are welcome to include your own errors as custom classes, but in this case a `ValueError` would also be appropriate.

***Note:*** at this point we'll note that, of course, whenever the Enigma machine *encodes*, it also *decodes* for the exact same settings. We'll still use the method name `encode(…)` throughout our tests, and take it as assumed that the same method is used for encoding and decoding.


```python
lead = PlugLead("AG")
assert(lead.encode("A") == "G")
assert(lead.encode("D") == "D")

lead = PlugLead("DA")
assert(lead.encode("A") == "D")
assert(lead.encode("D") == "A")
```

### Plugboard
Naturally we now need the plugboard itself to house our leads. 

An interesting part of object-oriented design is the idea that the *interface* of the object is really all an outsider needs to know. In the previous part we asked you to ensure a lead object supports `.encode("A")`, but how you achieve that is up to you.

Of course in this assignment we will be looking at your code, not just running automated tests. So two different implementations that both work could get different grades. But this is a programming unit and so it is part of the learning outcomes to learn how to write good code. In later units, you might be asked to show you are able to select and implement AI algorithms – not to test your ability to code, but to show you understand the techniques. Code quality is still important, it might even be worth marks, but it is not the primary goal.

With all that in mind, I am now going to ask you to write a class called `Plugboard`. The plugboard should accept leads which connect plugs via the method `.add(…)` as demonstrated below.

Like the leads, the plugboard should have an `.encode(…)` method as well, which should return the result of passing the character through the entire plugboard. 

These are the only interface requirements, but you are encouraged to elaborate on these with additional methods and/or constructor keywords. 

Remember that the Enigma machine only came with 10 leads to connect plugs. From now onwards, we will not always specifically point out the physical limitations that you need to model for robustness – you are expected to think of these and include them yourself. You do not need to know arcane details about how Enigma machines work, but from the information presented you can think of obvious incompatibilities and handle them.


```python
plugboard = Plugboard()

plugboard.add(PlugLead("SZ"))
plugboard.add(PlugLead("GT"))
plugboard.add(PlugLead("DV"))
plugboard.add(PlugLead("KU"))

assert(plugboard.encode("K") == "U")
assert(plugboard.encode("A") == "A")
```

### Rotors
The number of possible combinations due to the plugboard is staggering, making brute force attempts to break a code extremely difficult. But using it alone would result in a simple substitution cipher – easily cracked with techniques like frequency analysis. The next step in the process, the rotors, allow the letter substitution to change mechanically every time a key is pressed, which prevents simple frequency analysis.

Over time, rotors with many different wiring patterns were developed, and different Enigma machines supported different types and numbers of rotors. We are not necessarily looking for exact historical accuracy in this assignment – for your extension material you might choose to be much more accurate or much less accurate! For this part, you should work on the following specification.

Your Enigma machine must support *three or four* rotors and one reflector – notice that a reflector is really just a type of rotor where the characters line up in 13 perfect pairs. The rotors will be numbered *from right to left*, which is the “path” the current takes when first entering the rotors. The signal goes through each rotor in turn, hits the reflector, then goes through the rotors again in reverse order (left to right). When it goes through the rotors in reverse order, it uses the *reverse* wiring. So if A is mapped to L when going from right to left, then L is mapped to A on the reverse journey (of course it is not possible to actually hit the same wire on the way back – a letter cannot encode into itself in the machine as a whole).

Ignoring reflectors, which never rotate, there are two types of rotating rotor, based on whether or not the rotor contains a *notch*. If the rotor contains a notch, then when it is on a certain position and is rotated, it will cause the rotor in the next slot to rotate as well. In addition, in a four slot Engima machine, the leftmost (fourth) rotor never rotates. Rotation will be explained in more detail shortly.

Each rotor can be chosen from a box containing seven possible wiring patterns. There are two rotors labelled `Beta` and `Gamma`. Then there are five rotors labelled with Roman numerals which do rotate: `I, II, III, IV, V`. You must also support three possible reflector wiring patterns, labelled `A, B, C`.

Note: the wiring patterns are all real, taken from [this page](https://en.wikipedia.org/wiki/Enigma_rotor_details). The page contains more rotors if you wish to consider them, or you can make up your own, but you must support the ones here. The following patterns all assume the rotors are in their default position, with their default ring setting, and going from right to left (the initial path).

<table><thead>
<tr><th></th><th colspan="26"><center>Mapping from letter</center></th></tr>
<tr><th style="text-align:left">Label</th><th>A</th><th>B</th><th>C</th><th>D</th><th>E</th><th>F</th><th>G</th><th>H</th><th>I</th><th>J</th><th>K</th><th>L</th><th>M</th><th>N</th><th>O</th><th>P</th><th>Q</th><th>R</th><th>S</th><th>T</th><th>U</th><th>V</th><th>W</th><th>X</th><th>Y</th><th>Z</th></tr></thead><tbody>
<tr><th style="text-align:left">Beta</th><td>L</td><td>E</td><td>Y</td><td>J</td><td>V</td><td>C</td><td>N</td><td>I</td><td>X</td><td>W</td><td>P</td><td>B</td><td>Q</td><td>M</td><td>D</td><td>R</td><td>T</td><td>A</td><td>K</td><td>Z</td><td>G</td><td>F</td><td>U</td><td>H</td><td>O</td><td>S</td></tr>
<tr><th style="text-align:left">Gamma</th><td>F</td><td>S</td><td>O</td><td>K</td><td>A</td><td>N</td><td>U</td><td>E</td><td>R</td><td>H</td><td>M</td><td>B</td><td>T</td><td>I</td><td>Y</td><td>C</td><td>W</td><td>L</td><td>Q</td><td>P</td><td>Z</td><td>X</td><td>V</td><td>G</td><td>J</td><td>D</td></tr>
<tr><th style="text-align:left">I</th><td>E</td><td>K</td><td>M</td><td>F</td><td>L</td><td>G</td><td>D</td><td>Q</td><td>V</td><td>Z</td><td>N</td><td>T</td><td>O</td><td>W</td><td>Y</td><td>H</td><td>X</td><td>U</td><td>S</td><td>P</td><td>A</td><td>I</td><td>B</td><td>R</td><td>C</td><td>J</td></tr>
<tr><th style="text-align:left">II</th><td>A</td><td>J</td><td>D</td><td>K</td><td>S</td><td>I</td><td>R</td><td>U</td><td>X</td><td>B</td><td>L</td><td>H</td><td>W</td><td>T</td><td>M</td><td>C</td><td>Q</td><td>G</td><td>Z</td><td>N</td><td>P</td><td>Y</td><td>F</td><td>V</td><td>O</td><td>E</td></tr>
<tr><th style="text-align:left">III</th><td>B</td><td>D</td><td>F</td><td>H</td><td>J</td><td>L</td><td>C</td><td>P</td><td>R</td><td>T</td><td>X</td><td>V</td><td>Z</td><td>N</td><td>Y</td><td>E</td><td>I</td><td>W</td><td>G</td><td>A</td><td>K</td><td>M</td><td>U</td><td>S</td><td>Q</td><td>O</td></tr>
<tr><th style="text-align:left">IV</th><td>E</td><td>S</td><td>O</td><td>V</td><td>P</td><td>Z</td><td>J</td><td>A</td><td>Y</td><td>Q</td><td>U</td><td>I</td><td>R</td><td>H</td><td>X</td><td>L</td><td>N</td><td>F</td><td>T</td><td>G</td><td>K</td><td>D</td><td>C</td><td>M</td><td>W</td><td>B</td></tr>
<tr><th style="text-align:left">V</th><td>V</td><td>Z</td><td>B</td><td>R</td><td>G</td><td>I</td><td>T</td><td>Y</td><td>U</td><td>P</td><td>S</td><td>D</td><td>N</td><td>H</td><td>L</td><td>X</td><td>A</td><td>W</td><td>M</td><td>J</td><td>Q</td><td>O</td><td>F</td><td>E</td><td>C</td><td>K</td></tr>
<tr><th style="text-align:left">A</th><td>E</td><td>J</td><td>M</td><td>Z</td><td>A</td><td>L</td><td>Y</td><td>X</td><td>V</td><td>B</td><td>W</td><td>F</td><td>C</td><td>R</td><td>Q</td><td>U</td><td>O</td><td>N</td><td>T</td><td>S</td><td>P</td><td>I</td><td>K</td><td>H</td><td>G</td><td>D</td></tr>
<tr><th style="text-align:left">B</th><td>Y</td><td>R</td><td>U</td><td>H</td><td>Q</td><td>S</td><td>L</td><td>D</td><td>P</td><td>X</td><td>N</td><td>G</td><td>O</td><td>K</td><td>M</td><td>I</td><td>E</td><td>B</td><td>F</td><td>Z</td><td>C</td><td>W</td><td>V</td><td>J</td><td>A</td><td>T</td></tr>
<tr><th style="text-align:left">C</th><td>F</td><td>V</td><td>P</td><td>J</td><td>I</td><td>A</td><td>O</td><td>Y</td><td>E</td><td>D</td><td>R</td><td>Z</td><td>X</td><td>W</td><td>G</td><td>C</td><td>T</td><td>K</td><td>U</td><td>Q</td><td>S</td><td>B</td><td>N</td><td>M</td><td>H</td><td>L</td></tr>
</tbody></table>

### Single Rotor Demonstration
From now on, the specification does not require you to follow specific class or method names, it is totally up to you.

Rotors still get bit more complicated when we introduce their settings and put multiple in the same machine. But you might want to take this opportunity to see if you can write some code to represent what we've seen so far.

In the cell below, you should demonstrate some basic rotor functionality using your classes. I have left some sample code in here in case you want to use it, either directly or for inspiration – I am not implying this is the only or best way to achieve it, and either way you will likely want to add to it. The idea is to show us that your rotors work with the concepts introduced so far.

This code cell is especially important if you end up struggling with the next part, to allow for partial credit.


```python
rotor = Rotor.from_label(RotorLabel.I)
assert(rotor.encode_right_to_left("A") == "E")
assert(rotor.encode_left_to_right("A") == "U")
```

### The Enigma Machine
To fully understand rotors, we need to imagine multiple of them in the Enigma machine itself. For this next part, you will need to model many more details of how the rotors work, and in addition work out how to incorporate them into a single machine that is capable of performing the full encoding path.

#### Multiple Rotors
For now, let's ignore the plugboard, and introduce the remaining details for the rotors.

It is common to see the selection of rotors specified in a single sequence from left to right, as the operator would see when looking down, such as on a [German code book](https://en.wikipedia.org/wiki/Enigma_machine#/media/File:Enigma_keylist_3_rotor.jpg). For example, on the top row of that linked image, you can see the rotors should be `I V III`. This means the first (rightmost) rotor is `III`, and so on. How you conceptualise the order inside your code is up to you providing it is consistent with the terminology here.

The code book also specifies each rotor's “ring setting” – in that image you can see the rotors on the top line should be set to `14 09 24` correspondingly. 

The rotor settings will be explained later, but let's first ensure you understand the way the wiring works with multiple rotors. We will show a worked example using three rotors, with all the settings in their default positions – this means you can read the character mappings directly from the table above.

Imagine a `III` rotor sat upright in the machine in the right hand position. The right hand side of the rotor has 26 *pins* and the left hand side has 26 *contacts*, one for each character. The pins on the right are connected to the contacts of the rotor housing which is wired into the plugboard. So if the plugboard sends a signal on the `A` contact of the housing, then this hits the `A` *pin* of the rotor, then this passes through the rotor's internal wiring (check the table for the `III` rotor) and we receive an output signal on the `B` *contact* of the rotor. This will now go into the next rotor: remember there are three or four rotors, followed by a reflector.

Suppose there is a `II` rotor in the middle position, a `I` rotor in the left position, and then a `B` reflector. Here is the full path when we send an `A` signal from the plugboard:
* `A` signal comes in
* `III` rotor receives signal on `A` pin, which connects to `B` contact
* `II` rotor receives signal on `B` pin, which connects to `J` contact
* `I` rotor receives signal on `J` pin, which connects to `Z` contact
* `B` reflector receives signal on `Z` connecting to `T` <br/>
  (now the signal goes backwards, hitting the *contacts* and coming out the *pins*)
* `I` rotor receives signal on `T` contact, which connects to `L` pin
* `II` rotor receives signal on `L` contact, which connects to `K` pin
* `III` rotor receives signal on `K` contact, which connects to `U` pin
* `U` signal is output

The final output for this `A` signal is a `U`. Make sure you can follow this using the table above, as things are about to get more complicated.

#### Rotation
As mentioned, the rightmost rotor (first in the order of the electrical circuit) rotates at *the start* of each keypress, i.e. *before* the character signal is passed through the circuit. This is what makes the Enigma machine more powerful than a fixed substitution cipher, one rotation causes a completely different circuit and substitution.

The rotation of the rotor advances a setting called the ***position*** of each rotor, which is visible through a window on the machine. This setting is marked on the rotor and is a character between `A` and `Z`, but it is helpful to think of this number as an *offset* rather than a *letter*. In the example above we assumed all of the rotors were set to position `A`. Rotating moves the *pins and the contacts* up by one position (`A` becomes `B`, etc).

We mentioned before that if we input `A` into the `III` rotor in its default position (which is labelled `A`) then it produces an output of `B`. In our full example we assumed that the rotors were set to `AAA`, but if we set them this way on the machine, then as soon as we press the `A` key the rightmost rotor would rotate giving `AAB`, and this is the circuit that would be made (rotation always happens first). Let's look at what happens in this setting.

Now if we input an `A` signal from the plugboard, it will come out of the `A` contact of the housing, but it will hit the `B` pin of the rotor due to its rotation by one position. The `B` *pin* is wired to the `D` *contact* (reading from the table).

***But*** the `D` contact has also been rotated one position inside the machine, so it actually lines up with the `C` *pin* of the next rotor in its default position. The other two rotors and the reflector work as normal, and on the way back rotor `II` sends a signal on its `E` pin. Since `III` is rotated, this hits the `F` contact which is wired to the `C` pin. But again since it is rotated, this his the `B` contact of the rotor housing, and is what is sent back to the plugboard.

Here is the full example again, now assuming the rotors are set to `AAB` instead of `AAA`:
* `A` signal comes in
* `III (B)` rotor receives signal on `B` pin, which connects to `D` contact 
* `II (A)` rotor receives signal on `C` pin, which connects to `D` contact
* `I (A)` rotor receives signal on `D` pin, which connects to `F` contact
* `B` reflector receives signal on `F` connecting to `S`
* `I (A)` rotor receives signal on `S` contact, which connects to `S` pin
* `II (A)` rotor receives signal on `S` contact, which connects to `E` pin
* `III (B)` rotor receives signal on `F` contact, which connects to `C` pin
* `B` signal is output

You can try using the Enigma machine emulator [on this page](https://www.101computing.net/enigma-machine-emulator/). It defaults to the same settings: rotors `I II III` all initially set to position `A`, so when you press the `A` key on the keyboard you should get `B`.

Make sure you can follow this path using the table of wirings to help you understand how you will implement the behaviour. If you simply do not follow, there are lots of explanations and videos online for Enigma machines. 

#### Ring Settings
In addition each rotor could be configured by changing the *ring setting*, which is a fixed offset that would apply between the internal wiring and the external markings. The ring settings were either given from `A-Z` or `01-26` – you saw the latter in the code book image linked above, and we'll use these too to avoid confusion with the *position* setting.

If a rotor's ring setting is set to `01` then nothing is changed, the wiring is exactly as written in the table above.

*Increasing* the ring setting has the exact same effect as *decreasing* the position setting. It shifts the internal wiring in the opposite direction.

Earlier we said `A` becomes `U` with the given rotors actually set to `AAA` – we'd have to start on `AAZ` to get this result on the machine, since the rotation happens first (try it on the emulator). Alternatively, we could set the ring position to `02` on the rightmost rotor and set the initial positions to `AAA`, and we'll get the same result for a single press (again you can try this on the emulator; it uses letters for ring settings, if you click the rotor you can set the ring setting to `B`).

If we keep pressing `A`, the two configurations will produce many of the same characters, but not always. We have detailed how the rightmost rotor rotates, but not the others, and this detail will eventually produce a difference between the two sets of settings above.

#### Turnover
The rotors labelled `I` to `V` have *notches*. If a rotor has a notch and is currently set to its notch position, then it will turn the next rotor on the next keypress (this is called *turnover*). Here are the notch positions:

<table><thead><tr><th>Rotor</th><th>Notch</th></tr></thead><tbody><tr><td style="text-align:center">I</td><td style="text-align:center">Q</td></tr><tr><td style="text-align:center">II</td><td style="text-align:center">E</td></tr><tr><td style="text-align:center">III</td><td style="text-align:center">V</td></tr><tr><td style="text-align:center">IV</td><td style="text-align:center">J</td></tr><tr><td style="text-align:center">V</td><td style="text-align:center">Z</td></tr></tbody></table>

So if a `II` rotor in the first, rightmost, slot of the machine is *currently set to* position `E` then when you press a key the first rotor will turn to position `F` *and* the rotor in the second position will turn as well, and then the electrical signal will be sent through the circuit.

If the `II` rotor had been in the second position, then it will obviously turn much more slowly. But if its position is set to `E` and a key is pressed then it will rotate and turn the rotor in the third position also. 

There is an important detail here called the *double step*. Normally the second rotor will only turn once every 26 turns of the rightmost rotor. But if the second rotor is *on* its notch setting, then it will turn again *as it turns the third rotor*. Obviously the second rotor must have just rotated to land on its notch, so it actually rotates for two keypresses in a row.

Suppose we have the rotors `I II III`, on positions `A C U`. Pressing a key turns the `III` rotor and we get `A C V`. Now the `III` rotor is on its notch, so pressing a key also turns `II` and we get `A D W`. If we continue pressing keys we'll get `A D X`, `A D Y`, `A D Z`, `A D A`, and so on. Several keypresses later we wrap round again and approach the notch on `III` again on setting `A D U`. When we press once we get `A D V`. Now `III` is on its notch so pressing again turns `II` and we get `A E W`. But now `II` is on its notch, so when we press again *all three* rotors rotate and we get `B F X` – `III` turns because it always turns, `II` turns because it is on its notch, and `I` turns because `II` turned on its notch (turnover).

Notice the *ring setting* is inconsequential in this turnover process – it only requires the current position to line up with the notch setting.

The four-rotor machines did not have a additional lever, and so whether the third rotor had a notch or not the fourth rotor would not turn. In addition if a notchless rotor (e.g. `Beta`) was in the first position, then it will never cause the second rotor to rotate. The rightmost rotor will still always rotate exactly once on every keypress. Notchless rotors can still be set to different position settings as part of the setup process.

If you are curious about the mechanism, you can see a video of a mock-up version of an Enigma machine in action [here](https://www.youtube.com/watch?v=hcVhQeZ5gI4), showing how the the ratchets, levers, and notches contribute towards the rotation on each keypress, and also demonstrating the double step (around 26 seconds into the video).

### Multiple Rotor Demonstration
You have free reign to model the rotors however you wish, and you are encouraged to think about how object-oriented design principles and features might apply.

In the cell below, demonstrate that your rotors work. The code is left entirely up to you, though you must ensure to demonstrate the following:
* With rotors `I II III`, reflector `B`, ring settings `01 01 01`, and initial positions `A A Z`, encoding an `A` produces a `U`.
* With rotors `I II III`, reflector `B`, ring settings `01 01 01`, and initial positions `A A A`, encoding an `A` produces a `B`.
* With rotors `I II III`, reflector `B`, ring settings `01 01 01`, and initial positions `Q E V`, encoding an `A` produces an `L`.
* With rotors `IV V Beta`, reflector `B`, ring settings `14 09 24`, and initial positions `A A A`, encoding an `H` produces a `Y`.
* With rotors `I II III IV`, reflector `C`, ring settings `07 11 15 19`, and initial positions `Q E V Z`, encoding a `Z` produces a `V`.


```python
assert (EnigmaMachine(EnigmaSetup.from_string("I-II-III B 01-01-01 A-A-Z")).encode_character('A') == 'U')
assert (EnigmaMachine(EnigmaSetup.from_string("I-II-III B 01-01-01 A-A-A")).encode_character('A') == 'B')
assert (EnigmaMachine(EnigmaSetup.from_string("I-II-III B 01-01-01 Q-E-V")).encode_character('A') == 'L')
assert (EnigmaMachine(EnigmaSetup.from_string("IV-V-Beta B 14-09-24 A-A-A")).encode_character('H') == 'Y')
assert (EnigmaMachine(EnigmaSetup.from_string("I-II-III-IV C 07-11-15-19 Q-E-V-Z")).encode_character('Z') == 'V')
```

### Enigma Machine Demonstration
Now in the cell below, demonstrate that you can put all of the elements together. Your full Engima machine should support a plugboard with up to 10 leads, three or four rotors, and a reflector. In addition it should be able to encode an entire string of characters made from the letters `A`-`Z`, correctly advancing the rotors.

Again the code is up to you, and you may want to include additional points to demonstrate your Enigma machine, but please ensure you include the following two examples at minimum:
#### Example 1
Set up your enigma machine with rotors `I II III`, reflector `B`, ring settings `01 01 01`, and initial positions `A A Z`.

The plugboard should map the following pairs: `HL MO AJ CX BZ SR NI YW DG PK`.

*The result of encoding the string* `HELLOWORLD` *should be* `RFKTMBXVVW`.

#### Example 2
Set up your enigma machine with rotors `IV V Beta I`, reflector `A`, ring settings `18 24 03 05`, and initial positions `E Z G P`. 

The plugboard should map the following pairs: `PC XZ FM QA ST NB HY OR EV IU`.

*Find the result of decoding the following string:* `BUPXWJCDPFASXBDHLBBIBSRNWCSZXQOLBNXYAXVHOGCUUIBCVMPUZYUUKHI`.

(You should run this string through your Enigma machine in the cell below; do not just include the result.)


```python
# Example 1
assert(EnigmaMachine(EnigmaSetup.from_string("I-II-III B 1-1-1 A-A-Z HL-MO-AJ-CX-BZ-SR-NI-YW-DG-PK")).encode("HELLOWORLD") == "RFKTMBXVVW")

# Example 2
assert(
    EnigmaMachine(EnigmaSetup.from_string("IV-V-Beta-I A 18-24-03-05 E-Z-G-P PC-XZ-FM-QA-ST-NB-HY-OR-EV-IU")).encode('BUPXWJCDPFASXBDHLBBIBSRNWCSZXQOLBNXYAXVHOGCUUIBCVMPUZYUUKHI') == "CONGRATULATIONSONPRODUCINGYOURWORKINGENIGMAMACHINESIMULATOR"
)
```

## Part Two – Code Breaking
In this part of the assignment you will be given some ciphertext that has been encrypted using an Enigma machine, an idea of what the original text might contain (a *crib*), and some partial information about the machine. Your goal will be to provide the original plaintext and the full machine settings.

The Bletchley codebreakers were able to combine weaknesses in the machine's encryption, mathematical techniques, and computing power to solve German codes. In this section you only need to use using computing power. You can *brute force* the settings by trying each one until you get the one you are looking for. 

The number of possible settings for Enigma is still too vast to break a code through brute force alone, but you can use the partial information to narrow the search into something feasible on a modern computer. Even on weaker hardware, none of the codes will require more than a few minutes maximum with suitable code.

There is a cell beneath this one for you to include your results for each of the decoded strings. You must include the full decoded message, plus the settings that were missing. You should also point us towards the code (in a separate file) which was used to crack these strings, with instructions for replicating your results. 

Marks are awarded for correct solutions, and for coding style, as outlined in the assignment instructions. Solutions which can be run without manual intervention (e.g. manually changing variables) are likely to receive more credit, but this is not a firm requirement. Any manual steps required must be explained clearly.

### Codes
Each code contains the ciphertext (the encrypted text), and a crib: a word or phrase that you think appears exactly *somewhere* within the original text.

You should use the usual rotors and reflectors specified in the table above unless the question specifies otherwise. So if the question does not specify a rotor, the valid options are only `Beta`, `Gamma`, `I`, `II`, `III`, `IV`, and `V`, the valid options for reflectors are just `A`, `B`, and `C`.

The machines in this section will only ever use 3 rotors – meaning 3 ring settings and 3 starting positions also.

It is possible that more than one set of Enigma machine settings will produce an output containing the crib word. In this case, you must deduce on your own which one is correct based on the output contents.

#### Code 1
You recovered an Enigma machine! Amazingly, it is set up in that day's position, ready for you to replicate in your software. But unfortunately the label has worn off the reflector. All the other settings are still in place, however. You also found a book with the title "SECRETS" which contained the following code, could it be so simple that the code contains that text?

* Code: `DMEXBMKYCVPNQBEDHXVPZGKMTFFBJRPJTLHLCHOTKOYXGGHZ`
* Crib: `SECRETS`


* Rotors: `Beta Gamma V`
* Reflector: Unknown
* Ring settings: `04 02 14`
* Starting positions: `MJM`
* Plugboard pairs: `KI XN FL`

#### Code 2
You leave the machine in the hands of the university. The team have cracked the day's settings thanks to some earlier codebreaking, but unfortunately, the initial rotor positions are changed for each message. For the message below, the team has no idea what the initial settings should be, but know the message was addressed to them. Help them out.

* Code: `CMFSUPKNCBMUYEQVVDYKLRQZTPUFHSWWAKTUGXMPAMYAFITXIJKMH`
* Crib: `UNIVERSITY`


* Rotors: `Beta I III`
* Reflector: `B`
* Ring settings: `23 02 10`
* Starting positions: Unknown
* Plugboard pairs: `VH PT ZG BJ EY FS`

#### Code 3
The department has intercepted a message from the admissions team. They know it contains the word "THOUSANDS" and they are worried it might relate to how many students are arriving next semester. But the admissions team are a bit unusual: they *love* even numbers, and *hate* odd numbers. You happen to know they will never use an odd-numbered rotor, ruling out `I`, `III`, and `V`. They will also never use a *ring setting* that has even a single odd digit: `02` is allowed but `11` is certainly not, and even `12` is banned.

* Code: `ABSKJAKKMRITTNYURBJFWQGRSGNNYJSDRYLAPQWIAGKJYEPCTAGDCTHLCDRZRFZHKNRSDLNPFPEBVESHPY`
* Crib: `THOUSANDS`


* Rotors: Unknown but restricted (see above)
* Reflector: Unknown
* Ring settings: Unknown but restricted (see above)
* Starting positions: `EMY`
* Plugboard pairs: `FH TS BE UQ KD AL`

#### Code 4
On my way home from working late as I walked past the computer science lab I saw one of the tutors playing with the Enigma machine. Mere tutors are not allowed to touch such important equipment! Suspicious, I open the door, but the tutor hears me, and jumps out of the nearest window. They left behind a coded message, but some leads have been pulled out of the machine. It might contain a clue, but I'll have to find the missing lead positions (marked with question marks in the settings below).

* Code: `SDNTVTPHRBNWTLMZTQKZGADDQYPFNHBPNHCQGBGMZPZLUAVGDQVYRBFYYEIXQWVTHXGNW`
* Crib: `TUTOR`


* Rotors: `V III IV`
* Reflector: `A`
* Ring settings: `24 12 10`
* Starting positions: `SWU`
* Plugboard pairs: `WP RJ A? VF I? HN CG BS`

#### Code 5
I later remembered that I had given the tutor permission to use the Enigma machine to solve some codes I'd received via email. As for the window, they are just a big fan of parkour, this is always how they leave the building. It seems they are stuck on one last code. It came in via email so we suspect it's just spam, probably related to a social media website, but you never know when you'll find a gem in that kind of stuff.

The tutor has narrowed the search and found most of the settings, but it seems this code was made with a non-standard reflector. Indeed, there was a photo attached to the email along with the code. It appears that the sender has taken a standard reflector, cracked it open, and swapped some of the wires – two pairs of wires have been modified, by the looks of the dodgy soldering job. 

To be clear, a single wire connects two letters, e.g. mapping `A` to `Y` and `Y` to `A`. The sender has taken two wires (fours pairs of letters), e.g. `A-Y` and `H-J`, and swapped one of the ends, so one option would be `H-Y` and `A-J`. They did this twice, so they modified eight letters total (they did not swap the same wire more than once). 

In your answer, include what the original reflector was and the modifications.

* Code: `HWREISXLGTTBYVXRCWWJAKZDTVZWKBDJPVQYNEQIOTIFX`
* Crib: the name of a social media website/platform


* Rotors: `V II IV`
* Reflector: Unknown and non-standard (see above)
* Ring settings: `06 18 07`
* Starting positions: `AJL`
* Plugboard pairs: `UG IE PO NX WT`

### Code breaking - solution

The Code Breaker solution is built as a collection of Test Cases, using the built-in `unittest` library in Python. The solution is driven by a standardised framework which provides a set of methods to generate variants, and test and verify assertions for each coding break scenario. The framework supports both serial and parallel code-breaking. The parallelization, in its turn, relies on the built-in `multiprocessing` library.

Furthermore, it takes into consideration a standard Enigma Machine that is defined in the parent `enigma` package. The source code of the Code Breaker can be found at `enigma/tests/code_breaker`. The framework itself is defined in the class `EnigmaCodeBreakerBase`, in the module `enigma/tests/code_breaker/enigma_code_breaker_base.py`.

From the project directory, all test cases can either be executed via IDE, e.g. PyCharm, or via command line, from the project directory, by running `python -m unittest tests/code_breaker/test_enigma_code_breaker_case_[#].py`, where `#` is the number of the test case from 1 to 5.

In each code breaking Test Case, a method `test_break_code` is responsible for taking the known Enigma Machine setup properties, and find the unknown configurations. This method can be executed individually, for running a specific breaking process.

If desired, it is possible to follow the code-breaking process in detail, by enabling the debug mode. For that, please set an environment variable `LOG_LEVEL=DEBUG`. If enabled, it generates a verbose output, which can be useful for pedagogical and troubleshooting purposes. The default log level, however, is `INFO`, hence only key messages will be logged.


### Code 1 - Answer

For this case, most of the configuration is known, except for the reflector.

The solution strategy is to test each possible reflector, decoding the given code. Then, it is checked if the crib is part of the decoded message. If so, the code breaker stops since it might be a potential valid setup. After successful execution, the correct configuration is used as assertion, completing a test case.

* Code: `DMEXBMKYCVPNQBEDHXVPZGKMTFFBJRPJTLHLCHOTKOYXGGHZ`
* Crib: `SECRETS`

* Rotors: `Beta Gamma V`
* Reflector: `C`
* Ring settings: `04 02 14`
* Starting positions: `MJM`
* Plugboard pairs: `KI XN FL`

**Decoded message**: `NICEWORKYOUVEMANAGEDTODECODETHEFIRSTSECRETSTRING`

**Reproduction instructions**

The source code can be found at `enigma/tests/code_breaker/test_enigma_code_breaker_case_1.py`. In this file, a method `test_code_breaker` is defined with the step-by-step coding break algorithm. It can be executed via IDE, e.g., PyCharm, or via command line, from the project directory, by running `python -m unittest tests/code_breaker/test_enigma_code_breaker_case_1.py`.

### Code 2 - Answer

Most of the configuration is known, except for the starting positions.

The solution strategy is to test all possible starting positions - generated by permutation of the English alphabet - and test it with the known configuration until the message contains the crib. If so, the code breaker stops since it might be a potential valid setup.

After successful execution, the correct configuration is used as assertion, completing a test case.

* Code: `CMFSUPKNCBMUYEQVVDYKLRQZTPUFHSWWAKTUGXMPAMYAFITXIJKMH`
* Crib: `UNIVERSITY`

* Rotors: `Beta I III`
* Reflector: `B`
* Ring settings: `23 02 10`
* Starting positions: `I M G`
* Plugboard pairs: `VH PT ZG BJ EY FS`

**Decoded message**: `IHOPEYOUAREENJOYINGTHEUNIVERSITYOFBATHEXPERIENCESOFAR`

**Code breaking details:**

The source code can be found at `enigma/tests/code_breaker/test_enigma_code_breaker_case_2.py`. In this file, a method `test_code_breaker` is defined with the step-by-step coding break algorithm. It can be executed via IDE, e.g., PyCharm, or via command line, from the project directory, by running `python -m unittest tests/code_breaker/test_enigma_code_breaker_case_2.py`.


### Code 3 - Answer

Most of the configuration is unknown, except for the starting positions and plugboard.

Firstly, to be able to find out all potential setups, the possible rotors are permuted. Secondly, the possible ring setting are also permuted. Lastly, all the reflectors are considered. The permutations take into the account the outlined restrictions.

Given these possible setups, in combination with the known configuration, each configuration is tested until the message contains the crib. If so, the code breaker stops since it might be a potential valid setup.

* Code: `ABSKJAKKMRITTNYURBJFWQGRSGNNYJSDRYLAPQWIAGKJYEPCTAGDCTHLCDRZRFZHKNRSDLNPFPEBVESHPY`
* Crib: `THOUSANDS`

* Rotors: `II GAMMA IV`
* Reflector: `C`
* Ring settings: `24-08-20`
* Starting positions: `EMY`
* Plugboard pairs: `FH TS BE UQ KD AL`

**Decoded message**: `SQUIRRELSPLANTTHOUSANDSOFNEWTREESEACHYEARBYMERELYFORGETTINGWHERETHEYPUTTHEIRACORNS`

**Reproduction instructions**

The source code can be found at `enigma/tests/code_breaker/test_enigma_code_breaker_case_3.py`. In this file, a method `test_code_breaker` is defined with the step-by-step coding break algorithm. It can be executed via IDE, e.g., PyCharm, or via command line by running, from the project directory, `python -m unittest tests/code_breaker/test_enigma_code_breaker_case_3.py`.

### Code 4 - Answer

Most of the configuration is known, except for the plugboard that has two missing leads.

Firstly, to be able to find out all potential setups, the possible complements are permuted based upon the English alphabet. Secondly, only the valid possible plugboards are considered. For that, a filter is applied by checking if a lead is already present in the proposed new plugboard.

Given these possible setups, in combination with the known configuration, each setup is tested until the message contains the crib. If so, the code breaker stops since it might be a potential valid setup.

For this scenario, `9` potential setups and messages were found. After human proofreading, an assertion was set for the test case.

* Code: `SDNTVTPHRBNWTLMZTQKZGADDQYPFNHBPNHCQGBGMZPZLUAVGDQVYRBFYYEIXQWVTHXGNW`
* Crib: `TUTOR`


* Rotors: `V III IV`
* Reflector: `A`
* Ring settings: `24 12 10`
* Starting positions: `SWU`
* Plugboard pairs: `WP-RJ-AT-VF-IK-HN-CG-BS`

**Decoded message**: `NOTUTORSWEREHARMEDNORIMPLICATEDOFCRIMESDURINGTHEMAKINGOFTHESEEXAMPLES`

**Reproduction instructions**

The source code can be found at `enigma/tests/code_breaker/test_enigma_code_breaker_case_4.py`. In this file, a method `test_code_breaker` is defined with the step-by-step coding break algorithm. It can be executed via IDE, e.g., PyCharm, or via command line, from the project directory, by running `python -m unittest tests/code_breaker/test_enigma_code_breaker_case_4.py`.

### Code 5 - Answer

Most of the configuration is known, except for the Reflector, that has been hacked.

The crib is also unknown and the code breaker take into account the most popular platforms to find a potential decoded message. The platforms considered are `INSTAGRAM, FLICKR, PINTEREST, TUMBLR`.

This case considers a non-standard reflector. A reflector, unlike a regular rotor, has only 13 pairs of leads (so if A is mapped to E, then E is also mapped to A).
Each swap affects two pairs, for example (A,D), (B,C), so if A is swapped with B, then (A,B), and so on (C,D).

If multiple swaps are required, a single wire can only be swapped once. Two swaps, for example, mean swapping two wires, which affects four pairs, because a single swap of each wire affects two pairs.

Given these possible setups, in combination with the known configuration, each setup is tested until the message contains the crib. If so, the code breaker stops since it might be a potential valid setup.

After human proofreading, an assertion was set for the test case, including the real crib that is `INSTAGRAM`.

* Code: `HWREISXLGTTBYVXRCWWJAKZDTVZWKBDJPVQYNEQIOTIFX`
* Crib: `INSTAGRAM`

* Rotors: `V II IV`
* Reflector: `B`
* Ring settings: `06 18 07`
* Starting positions: `AJL`
* Plugboard pairs: `UG IE PO NX WT`

**Decoded message**: `YOUCANFOLLOWMYDOGONINSTAGRAMATTALESOFHOFFMANN`

**Modified reflector wiring**: `PQUHRSLDYXNGOKMABEFZCWVJIT`

The source code can be found at `enigma/tests/code_breaker/test_enigma_code_breaker_case_5.py`. In this file, a method `test_code_breaker` is defined with the step-by-step coding break algorithm. It can be executed via IDE, e.g., PyCharm, or via command line, from the project directory, by running `python -m unittest tests/code_breaker/test_enigma_code_breaker_case_5.py`.

## Advanced Work
Finally, there are a small proportion of marks available to rewards those who push beyond the specification we have presented here, in any way you find interesting.

It is completely acceptable to leave this section blank. The assignment is still plenty of work without doing extra. This assignment is only worth a proportion of the unit, and this section is only worth a proportion of the assignment. We have designed the marking system such that doing well on the other parts of the unit will still be more than enough to get the highest possible classification without submitting anything here.

Academic excellence (the highest possible marks) requires going beyond what you have been directly been taught or asked to do. This will likely become an even bigger factor in later units. This section is an opportunity to demonstrate that ability if you wish.

Please use the text cell below to describe your additional work, pointing to where in your code you demonstrate the work. If you wish to develop your code in a way that would break any of the tests above, you can create a separate folder in your submission for the more advanced version of the code.

Of course, more advanced features will be worth more marks. Your ability to explain your work academically is also important, so consider your presentation style. In particular, considering the programming *theory* of what you are doing (e.g. complexity, mathematical correctness) rather than simply explaining *what* you did is worth more credit. Have fun!

## Code Breaking with Multiprocessing

In the section Part Two - Code Breaking, five cases are given. Each of them present a problem where a set of Enigma Machine setup properties are known and other are not and the goal is to find out what is missing. Naturally, depending on the undisclosed configuration, more or less code breaking attempts are necessary to find a suitable Enigma Machine setup. In some cases, just a few possibilities are there to test, while in others, there is an exorbitant number of possibilities to verify. The first and obvious way to think about solving such kind of problem is to test all possibilities one by one, one after another. In computer science, this is known as a [sequential algorithm](https://en.wikipedia.org/wiki/Sequential_algorithm) or serial algorithm; an algorithm that is executed sequentially – once through, from start to finish, without other processing executing. For numerous problems, in the IT industry and in the academia, this approach is totally acceptable and often even required. For example, for Rule-based classifiers, where a disjunctive set of rules is evaluated one after another.

On the other hand, there are also concurrent or [parallel algorithm](https://en.wikipedia.org/wiki/Parallel_algorithm). In computer science, a parallel algorithm, as opposed to a traditional serial algorithm, is an algorithm which can do multiple operations in a given time. Concurrency and parallelism are in general distinct concepts, but they often overlap – many distributed algorithms are both concurrent and parallel. Nevertheless, the formal definition of those are beyond the goal of this essay. Parallel algorithms typically will be faster than sequential algorithms when the task can be divided into sub-tasks that can be executed independently and without communication or shared resources. Certainly, it depends on many other factors, and it is not an absolute truth. [Amdahl's law](https://en.wikipedia.org/wiki/Amdahl%27s_law) is often used in parallel computing to predict the theoretical performance increase when using multiple processors.

In python, the [multiprocessing](https://docs.python.org/3/library/multiprocessing.html) package is used to run independent parallel processes by using subprocesses (instead of threads). Python also has a [threading](https://docs.python.org/3/library/threading.html#module-threading) package and both APIs are actually very similar, but serve different purposes. [Python’s Global Interpreter Lock (GIL)](https://wiki.python.org/moin/GlobalInterpreterLock) only allows one thread to be run at a time under the interpreter, which means there is no performance increase applying multithreading if the Python interpreter is required. However, this is not the case for processes. Because each process has its own interpreter, which executes the instructions assigned to it, multiple processes can run in parallel. Moreover, an Operating System (OS) would perceive a program as multiple processes and schedule them separately independently,  resulting in a larger share of total computer resources being allocated. Hence, multiprocessing is faster when the program is CPU-bound. On the other hand, when there is I/O tasks involved the program, threading may be more effective since most of the time, the program is holding up for the I/O to total.

For increasing the Code breaker performance, the simple framework written in the `EnigmaCodeBreakerBase` also uses the `multiprocessing` package to perform multiple Enigma Machine setup variant checks in parallel. Such implementation can be seen in the method `def __check_variants_in_parallel`. This method uses a Pool of processes. A Pool class represents a pool of worker processes, where a process is a potential setup check executable via the method `def _check_potential_setup`. Furthermore, the method `__check_variants_in_parallel` uses `starmap`; like map() except that the elements of the iterable are expected to be iterables that are unpacked as arguments. Starmap is relatively new and was introduced in Python 3.3. This method, in combination with the use of context manager, simplifies the use of the `multiprocessing` package, as it removes the need of closing a process and join them.

The Pool, in its turn, expects a number of processes to fan out to. By default, it is the number of cores available in the computer where it is running. The graph below shows the performance for each case scenario. Because the Case 5 is a hypotetical cased considering a hacked Enigma Machine, it is excluded from the analysis, since only sequential processing was done for this code breaking.

For the running the tests the device used has the following main especifications:

* Operational System (OS): `macOS Monterey 12.6`
* Device: `MacBook Pro (16-inch, 2019)`
* Processor: `2,6 GHz 6-Core Intel Core i7`
* Memory: `32 GB 2667 MHz DDR4`

![title](tests/code_breaker/img/code_breaking_sequential_x_parallel.png)


Overall, it is possible to see a better performance when the multiprocessing is used. The only exception is the Case 1. This is due to the computational costs of initialisation of the multiprocessing pool. For this case, it is more expensive than just running the 3 iterations, sequentially. For all the others, there is a clear performance improvement.


## Profiling Enigma Machine decoding

Deterministic profiling is meant to reflect the fact that all function call, function return, and exception events are monitored, and precise timings are made for the intervals between these events (during which time the user's code is executing). Statistical profiling, on the other hand, randomly samples the effective instruction pointer and deduces where time is spent. The latter solution is less invasive and hence involves less overhead because the code does not need to be instrumented, but it only offers relative indications of where time is spent.

In Python, since there is an interpreter active during execution, the presence of instrumented code is not required to do deterministic profiling. Python generates a hook (optional callback) for each event. Furthermore, because Python is interpreted, it adds so much complexity to execution that deterministic profiling only adds little processing overhead in common applications. As a consequence, deterministic profiling is very inexpensive while providing detailed run-time information regarding the execution of a Python application.

Call count statistics may be utilised to uncover code issues and potential inline-expansion spots (high call counts). Internal time statistics can be utilised to discover "hot loops" that should be tuned carefully. Cumulative time statistics should be utilised to uncover high-level problems in algorithm selection. It is worth noting that the profiler's peculiar handling of cumulative times allows statistics for recursive implementations of algorithms to be directly compared to iterative ones.

In general, then, Profiling helps to understand how much time is spent in different parts of a program when it runs. These can be simply source code lines, functions, loops, and so forth. Profiling information is obtained by using profiling tools. In Python it can be done using the cProfile package part of the standard library.

The Python library provides [cProfile](https://docs.python.org/3/library/profile.html#module-cProfile) and [profile](https://docs.python.org/3/library/profile.html#module-profile) for deterministic profiling programs. The module `cProfile` is recommended for most users; it’s a C extension with reasonable overhead that makes it suitable for profiling long-running programs. Based on lsprof, contributed by Brett Rosen and Ted Czotter.

For getting a more in-depth understanding of the implemented Enigma Machine decoding process, a simple profiler command-line tool was created. This tool measures a decoding process of a message. For illustration purposes, a profiling target. This profiling target is a simple class with a single static method that instantiates a Enigma Machime Setup and decodes a message `XABMTXRSXTLZEHCZEJBGUW`, which gives the output `ARTIFICIALINTELLIGENCE`.

The overall Egnima Machine setup is:

* Code: `XABMTXRSXTLZEHCZEJBGUW`
* Rotors: `I II III`
* Reflector: `B`
* Ring settings: `01 01 01`
* Starting positions: `A A Z`
* Plugboard pairs: `HL MO AJ CX BZ SR NI YW DG PK`

The profiler can be executed via CLI, like so: `python profiling/profiler.py` or simply `./profiling/profiler.py`.

In addition, the profiler makes use of two extra packages: [graphviz](https://pypi.org/project/graphviz/) and [gprof2dot](https://pypi.org/project/gprof2dot/). By running the command above, both should be installed automatically. If preferred, they can also be installed by running `pip -m install graphviz gprof2dot`. These are meant for visualisation for the statitics generated by the profiler. The package `graphviz` facilitates the creation and rendering of graph descriptions in the DOT language. The package `gprof2dot` converts the output from many profilers into a dot graph.

Below a graph of the decoding explained above:

![title](profiling/demo/graph.png)

Note: Perhaps the image is too small to visualise in the jupyter notebook. The image can also be opened in another tool for better experience.

From the graph, it is possible to see which functions are accessed more frequently, and how much time it takes between them. The colors give an idea of intensity, like a heat map. A deeper analysis is beyond the scope of this demonstration.
