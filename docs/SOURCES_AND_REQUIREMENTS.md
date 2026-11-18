# Sources and course requirements

Reviewed November 17, 2026. Course pages require the team's KSU login. Course instructions establish deliverables. The proposal establishes the project's selected scope. Public primary sources support graph algorithm concepts and measurement APIs.

## Supplied proposal

`C:/Users/byrke/Documents/~ School stuff/algorithms class/Real_Algo Analysis Semester Project Proposal.docx`

The approved topic is Graph Traversal Techniques Comparative Analysis of BFS and DFS. Its research question asks how the algorithms compare in efficiency and usefulness on graph traversal tasks. It calls for Python, queue-based BFS, recursive or stack-based DFS, shared test inputs, runtime/visited-vertex/memory measurements, graph structure comparisons, connected components, unweighted shortest paths, Matplotlib figures, a report, a presentation, and a demo. It proposes VS Code and GitHub. This delivery provides local source and evidence ready for the team to place in its repository.

The proposal bibliography includes sorting, divide-and-conquer, minimax, and alpha-beta resources. Those are unrelated to the implemented comparison and should be removed from the final bibliography unless the final text actually discusses them. The Cormen, MIT graph lectures, and relevant Stanford graph material align with the project. Confirm the edition and pages of any textbook passages actually used before adding page-specific citations. Cormen et al. (2009), Introduction to Algorithms, third edition, MIT Press, Chapter 22, is the proposal's relevant textbook reference.

## D2L resources used

1. [Project topics in Module 1](https://kennesaw.view.usg.edu/d2l/le/content/4034518/Home). The Graph Traversal Techniques topic asks for BFS/DFS comparison with applications such as connected components, shortest paths, or topological sorting. This implementation follows the proposal's connected-component and shortest-path choices. Topological sorting is outside the approved implementation scope chosen here.
2. [Presentation outline](https://kennesaw.view.usg.edu/d2l/le/content/4034518/viewContent/64687586/View). It establishes the slide sections, minimum slide counts, runtime/complexity plots, live demo, conclusion, references, and 12-minute presentation plus 3-minute Q&A target.
3. [Final report outline](https://kennesaw.view.usg.edu/d2l/le/content/4034518/viewContent/64687587/View). It establishes report sections and the minimum methodology/results lengths.
4. [Presentation announcement](https://kennesaw.view.usg.edu/d2l/le/news/4034518/7149430/view). It establishes the November 9-21 live presentation window, eligible meeting times, Teams arrangement, group attendance, and camera requirement.
5. [Assignment submission list](https://kennesaw.view.usg.edu/d2l/lms/dropbox/dropbox.d2l?ou=4034518). The preceding review verified presentation upload due November 21 and final report due November 30 at 11:59 p.m. Eastern. Recheck the live folders before submitting.

## Public primary sources

- Demaine, E., Ku, J., and Solomon, J. (2020). [Lecture 9 Breadth-First Search](https://ocw.mit.edu/courses/6-006-introduction-to-algorithms-spring-2020/resources/mit6_006s20_lec9/). MIT OpenCourseWare, 6.006 Introduction to Algorithms. Supports the BFS, graph representation, and shortest-path background.
- Demaine, E., Ku, J., and Solomon, J. (2020). [Lecture 10 Depth-First Search](https://ocw.mit.edu/courses/6-006-introduction-to-algorithms-spring-2020/resources/mit6_006s20_lec10/). MIT OpenCourseWare. Supports DFS traversal, full search forests, connectivity, and O(V + E) background. The implementation's explicit iterator frames are our Python design choice.
- Python Software Foundation. [time documentation](https://docs.python.org/3/library/time.html#time.perf_counter_ns). Supports use of a high-resolution monotonic performance clock. The actual runtime environment and clock resolution are recorded in results/environment.json.
- Python Software Foundation. [tracemalloc documentation](https://docs.python.org/3/library/tracemalloc.html). Supports peak tracked Python allocation measurement. Traced allocation differs from the operating system's process memory metric.

The implementation, independent verification, generated graph definitions, benchmark configuration, and numerical results in this package are the evidence for its specific claims. Public sources establish algorithm concepts and API behavior, rather than the measured timing values.
