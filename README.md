# HeapViewer

This is a command line tool the uses PANDA to visualize heap usage of a target program and detect when a heap corruption attack is possible or has occurred. It is a fork of [lacraig2's pandaheapinspect](https://github.com/lacraig2/pandaheapinspect) with a few key differences: 
* The ability to analyze any target program that uses libc's malloc() function to allocate memory chunks
* Output the information in a way that is easy to understand and shows how the chunks are stored in memory
* Detect when a memory leak or corruption attack has taken place 

## Overview

This section will detail some prerequisites, my goals with the project, motivation, and high-level implementation details. If you would like to try the 
tool for youself, skip to the [Getting Started](#getting-started) section. 

### Prerequisites

While this tool is meant to be easy to use, in order to get the most out of it you should have some background knowdlege. There are a few topics
that are core to this project, and information can be found about them here: 
* [What is the heap?](https://opendsa-server.cs.vt.edu/OpenDSA/Books/CS2/html/HeapMem.html#:~:text=%E2%80%9CHeap%E2%80%9D%20memory%2C%20also%20known,is%20different%20in%20every%20way.)
* [How does lic manage the heap?](https://azeria-labs.com/heap-exploitation-part-1-understanding-the-glibc-heap-implementation/)
* [What are bins?](https://azeria-labs.com/heap-exploitation-part-2-glibc-heap-free-bins/)
* [Heap explotation ideas](https://heap-exploitation.dhavalkapil.com/attacks)

### Motivation and Goals 

Since starting to study cybersecurity, I have done many stack-based buffer overflow attacks. While I learned a lot when executing these attacks in a lab environment, these types of attacks are rarely seen in the real world. However, with C being so dominent and the responsibility of managing memory being shifted to programmers memory attacks are still very possible. Many of these attacks deal with the heap memory region, so I wanted to dive into this world
and learn more about attacking memory beyond basic buffer overflow exploits. This meant that before I had a project in mind, I had to learn how memory is 
handled in C, what happens behind the scenes that the programmer never sees, and how this can be exploited to possibly hijack control flow of a program. 
Once I passed this step, I was able to formulate a project with some clear goals in mind:
* Create a tool that takes in a compiled C program and outputs information about its heap usage 
* Have this output mimic how chunks are stored in memory 
* Detect when bins have been corrupted in some way 
* Use PANDA to make the tool platform independent 

### PANDA and My Approach

PANDA is a tool that uses QEMU to emulate a entire system, and then provides, among other things, a python interface to analyze this system. This makes it 
possible to run a compiled program through PANDA and use python to analyze its heap usage. More specifically, we register a callback whenever PANDA detects libc's malloc() function being called and run our analysis code. A callback allows us to specify code that will run whenever a certain event happens in our emeulatd system. In this case, the event is malloc() being called by a process and we tell PANDA to then run our analysis code. The user can choose to analyze all malloc() calls, or just calls that happen within the target process. To learn more about PANDA, click [here.](https://panda.re/)

## Getting Started

A step by step series of examples that tell you how to get a development env running

Say what the step will be

```
Give the example
```

And repeat

```
until finished
```

End with an example of getting some data out of the system or using it for a little demo

## Running the tests

Explain how to run the automated tests for this system

### Break down into end to end tests

Explain what these tests test and why

```
Give an example
```

### And coding style tests

Explain what these tests test and why

```
Give an example
```

## Deployment

Add additional notes about how to deploy this on a live system

## Built With

* [Dropwizard](http://www.dropwizard.io/1.0.2/docs/) - The web framework used
* [Maven](https://maven.apache.org/) - Dependency Management
* [ROME](https://rometools.github.io/rome/) - Used to generate RSS Feeds

## Contributing

Please read [CONTRIBUTING.md](https://gist.github.com/PurpleBooth/b24679402957c63ec426) for details on our code of conduct, and the process for submitting pull requests to us.

## Versioning

We use [SemVer](http://semver.org/) for versioning. For the versions available, see the [tags on this repository](https://github.com/your/project/tags). 

## Authors

* **Billie Thompson** - *Initial work* - [PurpleBooth](https://github.com/PurpleBooth)

See also the list of [contributors](https://github.com/your/project/contributors) who participated in this project.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

* Hat tip to anyone whose code was used
* Inspiration
* etc
