#!/usr/bin/env python3
"""
Context Reference Store Architecture Diagram
Shows the original efficient context management system built by Adewale
"""

from diagrams import Diagram, Cluster, Edge
from diagrams.onprem.inmemory import Redis
from diagrams.onprem.database import PostgreSQL
from diagrams.programming.language import Python
from diagrams.programming.flowchart import Decision, StartEnd
from diagrams.generic.storage import Storage
from diagrams.generic.blank import Blank
from diagrams.aws.storage import S3

graph_attr = {"ranksep": "1.2", "nodesep": "0.8", "splines": "ortho"}

with Diagram(
    "Context Reference Store - Original Architecture",
    filename="context_reference_store_architecture",
    direction="TB",
    show=False,
    graph_attr=graph_attr,
):

    # ────────────────────── Input Layer ─────────────────────
    with Cluster("Input - Large Contexts"):
        large_doc = StartEnd("Large Document\n(1M-2M tokens)")
        multimodal = StartEnd("Multimodal Content\n(Images, Audio, Video)")
        structured = StartEnd("Structured Data\n(JSON, XML)")

    inputs = [large_doc, multimodal, structured]

    # ────────────────────── Core Processing ─────────────────────
    with Cluster("Context Reference Store Core"):
        hash_gen = Python("SHA256 Hash\nGenerator")
        dedup = Decision("Duplicate\nDetection")
        metadata = Python("ContextMetadata\nProcessor")

    inputs >> hash_gen >> dedup
    dedup >> Edge(label="new content", color="green") >> metadata
    (
        dedup
        >> Edge(label="duplicate", color="orange", style="dashed")
        >> Blank("Return Ref")
    )

    # ────────────────────── Storage Layer ─────────────────────
    with Cluster("Multi-Tier Storage"):
        # Memory tier
        with Cluster("Memory Tier (Hot Data)"):
            memory_cache = Redis("LRU/LFU Cache\n(Small contexts)")
            binary_memory = Redis("Binary Cache\n(<1MB content)")

        # Disk tier
        with Cluster("Disk Tier (Cold Data)"):
            disk_storage = Storage("Local Disk\n(Large binaries ≥1MB)")
            context_store = Storage("In-Memory Store\n(Dict-based References)")

    metadata >> memory_cache
    metadata >> binary_memory
    metadata >> disk_storage
    metadata >> context_store

    # ────────────────────── Caching Strategies ─────────────────────
    with Cluster("Advanced Caching"):
        lru = Python("LRU\n(Least Recently Used)")
        lfu = Python("LFU\n(Least Frequently Used)")
        ttl = Python("TTL\n(Time To Live)")
        memory_pressure = Python("Memory Pressure\n(System-aware)")

    memory_cache >> [lru, lfu, ttl, memory_pressure]

    # ────────────────────── State Integration ─────────────────────
    with Cluster("ADK Integration"):
        large_context_state = Python("LargeContextState\n(Enhanced State)")
        adk_state = Python("ADK Base State\n(Existing)")

    [lru, lfu, ttl, memory_pressure] >> large_context_state
    context_store >> large_context_state
    large_context_state >> Edge(label="extends") >> adk_state

    # ────────────────────── Performance Results ─────────────────────
    with Cluster("Performance Achievements"):
        perf_memory = StartEnd("49x Memory\nReduction")
        perf_serial = StartEnd("625x Serialization\nSpeedup")
        perf_storage = StartEnd("99.55% Storage\nReduction (Multimodal)")
        perf_quality = StartEnd("Zero Quality\nDegradation")

    large_context_state >> [perf_memory, perf_serial, perf_storage, perf_quality]

    # ────────────────────── Usage Patterns ─────────────────────
    with Cluster("Usage Scenarios"):
        multi_agent = Python("Multi-Agent\nScenarios")
        long_sessions = Python("Long-Running\nSessions")
        multimodal_ai = Python("Multimodal\nAI Apps")

    adk_state >> [multi_agent, long_sessions, multimodal_ai]
