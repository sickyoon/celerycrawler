
# GoCelery

Python Distributed Task Queue in Go

# What is Celery?

Celery is distributed task queue that allows asynchronous task processing. Commonly used by python applications to offload expensive synchronous or asynchronous tasks to celery workers. Alternative technologies include gRPC. It is actively used in organizations such as Instagram and Mozilla.

# Why GoCelery?

Go is compiled, statistically typed language designed with concurrency in mind. Modern python provides a good way to implement asynchronous tasks (uvloop) but there are still some limitations (GIL Lock Issue).

By implementing compatible celery workers

# Reception

Unofficially contacted by Uber engineers and creator of Celery regarding the project.

# Challenges

* Celery uses pickle as default option for serdes. However since pickle is python-specific serdes, it is difficult to find stable go libraries that support it. Fortunately, Celery supports json as alternative format.

* Supporting all brokers. Celery supports many brokers that include paid service such as Amazon SQS. Without access to those services, it is difficult to support most brokers supported by Celery.

# Benchmark
 
As benchmark application, I created a simple python web crawler that uses distributed task queue to crawl my local hosted websites and parse the result. Unofficial benchmarks run on my 2013 Macbook Air running youtube.

