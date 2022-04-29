# HeapViewer

This is a command line tool the uses PANDA to visualize heap usage of a target program and detect when a heap corruption attack is possible or has occurred. It is a fork of [lacraig2's pandaheapinspect](https://github.com/lacraig2/pandaheapinspect) with a few key differences: 
* The ability to analyze any target program that uses libc's malloc() function to allocate memory chunks
* Output the information in a way that is easy to understand and shows how the chunks are stored in memory
* Detect when a memory leak or corruption attack has taken place 

## Overview

This section will detail some prerequisites, goals, motivation, high-level implementation details, and some testing. If you would like to try the 
tool for youself, skip to the [Getting Started](#getting-started) section. 

### Prerequisites

While this tool is meant to be easy to use, in order to get the most out of it you should have some background knowdlege. There are a few topics
that are core to this project, and information can be found about them here: 
* [What is the heap?](https://opendsa-server.cs.vt.edu/OpenDSA/Books/CS2/html/HeapMem.html#:~:text=%E2%80%9CHeap%E2%80%9D%20memory%2C%20also%20known,is%20different%20in%20every%20way.)
* [How does libc manage the heap?](https://azeria-labs.com/heap-exploitation-part-1-understanding-the-glibc-heap-implementation/)
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

### Testing 

Testing this program relied heavily on my understanding of the heap and knowing what the expected output should be. I wrote test programs, which can be found in the scripts folder and are detailed more below, and tested my tool using those programs. Each one demonstrates some aspect of libc's memory handling, such as first checking the tcache bin for chunks or showing that the fastbin is used after the tcache bin. All of the output that I have observed are in line with what I expected based on the research I have done, but if you find any unexpected behavior let me know!


## Getting Started

The only other dependency besides python to run this program will be PANDA. The easiest way to get access to panda is through docker. The command to install PANDA's container on your system is 

```
docker pull pandare/panda
```

Or you can clone thier github repo using the command 

```
git clone https://github.com/panda-re/panda.git
```
More information about installing PANDA can be found [here.](https://panda.re/)

If you used the docker container to access panda, then you will have to have to have access to this repo from within the container. The 
easiest way to do that is, after cloning the repo and making it your working directory, running the following command
```
docker run --rm -v $(pwd):/host -it pandare/panda
```

## Running the program

The only file that you will have to run is the PANDAHeapInspect.py file. The help message outputs the options available to you, and looks like this 

<img width="1072" alt="Screen Shot 2022-04-29 at 5 21 45 PM" src="https://user-images.githubusercontent.com/66029105/166070882-b0a89621-cf7f-4faa-9e5b-a4c93f836d9d.png">


If no option is specified, the program will output chunk information through diagrams. If you find that there are too many chunks and want just the raw data, then you can specify the --raw option. <br> 
The --script flag is optional, and if it is not specified then it will run the program named 'simple' in the /scripts folder. This is where you can write your own C program, compile it, and place it into the /scripts folder. Then specify the name of the executable and you will be able to analyze it. <br> 
If the --all flag is set, then information about all heap usage will be displayed, not just from the target program

### Note 
The first time you run this program, PANDA will have to download a large .qcow2 file. This will take a few minutes, and is normal. The message you get will look like this 

<img width="876" alt="Screen Shot 2022-04-29 at 5 27 05 PM" src="https://user-images.githubusercontent.com/66029105/166071510-838ea355-3ff3-4bf8-b6e6-6b5af5224972.png">


## Output

Here is some sample output from running different programs already in the /scripts folder.

```
python PANDAHeapInspect.py --script tcache 
```
The first section of output will look like 
<img width="1344" alt="Screen Shot 2022-04-29 at 5 29 16 PM" src="https://user-images.githubusercontent.com/66029105/166071679-1d6f3034-7bad-428d-bb1c-939dd8edb125.png">
This is because our analysis runs on every malloc() call, but bins only get populated on calls to free(). Therefore there will be a series of initial hooks that do not return any data. The first meaningful output will look like this: 

<img width="967" alt="image" src="https://user-images.githubusercontent.com/66029105/166071799-ea3f00c7-c3fc-4ca9-a072-1279b27ec08a.png">

Some tcache bins have been populated with freed chunks, and information about those chunks is not displayed. The first tcache bin that is not empty is holding chunks of size 0x21 bytes, and is a singly linked list since there are multiple chunks of that size. Since it is just singly linked, there is no back pointer or prev_size, and they are displayed as 0x0. <br>

There are two more tcache bins with 1 chunk each, the first of these has a chunk of 0x51 bytes and the second has a chunk of 0x61 bytes. The source code for the tcache executable is available in the /scripts folder, so this program can be better understood. 
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

* **Gabe Holmes** - *Initial work* - [PurpleBooth](https://github.com/PurpleBooth)

See also the list of [contributors](https://github.com/your/project/contributors) who participated in this project.

## License

This project is free to use and build apon

## Acknowledgments

* Big acknowledgement to lacraig2 for their original project 
* Inspiration
* etc
