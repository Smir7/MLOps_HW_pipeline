from diagrams import Diagram, Cluster
from diagrams.programming.language import Python
from diagrams.onprem.queue import Kafka
from diagrams.onprem.compute import Server
from diagrams.onprem.client import User

with Diagram("Video Face Blurring Parallel Architecture", show=False, direction="LR"):
    video_in = User("Source Video File")

    with Cluster("Processing Pipeline"):
        reader = Python("Frame Reader\n(Producer)")
        queue = Kafka("Frames Queue")

        with Cluster("Parallel Workers"):
            workers = [
                Server("Worker 1"),
                Server("Worker 2"),
                Server("Worker 3")
            ]

        writer = Python("Video Writer\n(Consumer)")

    video_in >> reader >> queue >> workers >> writer