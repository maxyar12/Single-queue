# Single-queue
A simple single-queue single-server system based on discrete event simulation
This was written for teaching the discrete event simulation course at Baruch Zicklin School of Business

Usage and Comments

This code is mostly for pedalogical purposes following the arrival and departure logic from the textbook Discrete Event Simulation by Banks et. al. Therefore, variable names such as the future event-notice list (FEL), coincide with the names given in the textbook. This way I feel like the code may be more readable for students who read this textbook. 

I believe that python is excellent for "quick and dirty" implementations of models. This code is based on that principle. However, it would be non-trivial (but possible) to extend this code to multiple lines (queueus) and servers. The main idea is to have a simple low-level implementation to be compared to the high level implementation in ARENA. The textbook has a low-level Java implementation of the same problem, however, I feel that python is more accessible and easier to learn, at least for those who do not intend to work as professional software engineers, so I wrote the python version.

List Operations

As the textbook (Banks) points out, the best data structure for the future event-notice list is a dynamic linked list. This way insertion and deletion methods that preserve time ordering are O(1). My implementation here uses arrays and is less efficient than the an optimal code. On the other hand arrays allow O(1) lookups, so there is always this trade-off. My understanding is that the major list operations are inserstions and removals for FEL, so dynamic linked list is the way its done for most simulation package software

I chose to use lambda sorting for time-ordering the FEL as this is easy to do in python. For this case, there can be a maximum of two events in the FEL so the lambda sorting is uneccessary and could simply be coded explicitly. However, using the lambda based attribute sort extends this code to possible uses where the FEL can contain a large number of notices. It is used to sort the queue ( which is modeled as "checkoutline" after removing the customer currently being served (if any))

Using the code

   This code runs pretty fast up to 1 million "minutes" of runtime. For example set TE = 1000000 and you should have a report generated in a few seconds. Different arrival distributions and parameters can bet set in the arrival time function atime() and the service time generation function stime().

