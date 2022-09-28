# FRIENDBRW

### A reciprocity-based method for improving community detection on directed friendship networks

Friendship Reciprocal Inclusivity-Emphasizing Never Does Backtrack Random Walk (FRIENDBRW) is an extension of existing community detection algorithms to enhance results for sociological networks of friendship relations. This method is ***embarrassingly parallelizable*** and is motivated by the importance of information cycles and the reciprocal nature of friendships in forming communities. The algorithm can be adjusted to change how inclusive detected friend groups are, as measured by the prevalence of non-reciprocal edges. Communities detected by our algorithm are more tightly-knit and realistically sized for sociological data compared to those found by the undirected Louvain algorithm.

1. Begin with a directed network data
1. Translate into a [Networkx object](https://networkx.org/documentation/stable/reference/readwrite/index.html)
1. Determine the inclusivity value in the range (0,1) based on your application. Smaller inclusivity will result in smaller communities, including singletons. Larger inclusivity will reduce the number of singletons detected.
1. Running the [FRIENDBRW algorithm]() will add weights to your original networkx object
1. Run [directed Louvain algorithm](https://github.com/nicolasdugue/DirectedLouvain) on your FRIENDBRW weighted network. This will return the desired communities.



-----------
Please email if you have questions: sfeuer45@gmail.com, davidarollo@outlook.com

