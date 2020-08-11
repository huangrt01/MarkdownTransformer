### Ray: 动态可编程分布式计算框架

请阅读 [Ray支持ML动态编程需求的分析](https://bytedance.feishu.cn/docs/doccn5NqhYdlPtHOmDKMSDSKCfe#)  ，并读一些Ray的代码/文献。 谈一谈：1) Ray是什么？ 2) 目前工业界一般怎么使用Ray？  3) Ray对应我们的系统中的哪一个/哪一些层次？  4) 最值得我们借鉴的地方有哪些？



1.Ray是一个动态可编程的分布式计算框架，支持分布式训练，主要体现在以下几方面：

丰富的本地训练场景（清晰指派local/remote的任务/角色，task无状态，actor有状态）

灵活训练规划pipeline（用户可以在Actor里自定义逻辑，包括循环、计时器等）

灵活数据源（流批处理融合，支持简单的数据处理chain）

2.目前工业界主要使用Ray的方式分两种，一是用Ray的上游生态lib，二是用Ray的底层能力深入自研框架

（1）Ray的上游生态：

* 强化学习库(RLLib)

* 超参调优库(Tune):  支持任意ML框架：PyTorch，XGBoost， MXNet， Keras，集成了很多优化器的库和算法， 通过TensorBoard做显示，可以和Ray Serve无缝结合
* Training with RaySGD: 优势在于能和其它Ray lib无缝结合，并且实现了分布式的dataset

（2）Ray的底层能力：大厂结合Ray自研框架的lecture在这里：[蚂蚁金服Ray Forward推广](https://tech.antfin.com/community/activities/698/review)，还没来得及听

3.Ray对应于我们系统中的多个层次，它的底层能力对应于资源管理层REAM (包括Flink, Yarn等)，上游生态对应于我们的LagrangeX

4.最值得我们借鉴的地方有哪些？

底层：

* Ray实现了高效的系统间数据传输， "在底层hack了python的内存对象，和Redis内存共享，实现Numpy、Pandas等数据格式序列化/反序列化时候zero-copy，没有损耗"，是否可以引入这一思想减小我们model serving/training过程中序列化/反序列化的开销
* Ray的结构非常优雅，global scheduler调度全部任务，local scheduler调度同一Node内共享内存的worker，object store支持Node之间的通信。

易用性：

Ray是用户友好的分布式计算框架，具体体现在

1）轻量级的API，几乎不提高代码复杂性。只用在函数前加`@ray.remote`，就能通过remote调用，使task在其它ray集群执行。

2）支持ray dashboard，利于debugging and profiling



官方doc：https://docs.ray.io/en/latest/installation.html

开源史海钩沉系列 [1] Ray：分布式计算框架 - 高策的文章 - 知乎 https://zhuanlan.zhihu.com/p/104022670