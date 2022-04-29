# HeapViewer
Tool to view heap usage and detect corruption

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

```
Give examples
```

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
