"""
Define types.
"""

from collections.abc import Mapping, Sequence

type QubitIdx = int
type QubitPair = tuple[QubitIdx, QubitIdx]
type QubitPairSeq = Sequence[QubitPair]

type Corr1ptMap = Mapping[QubitIdx, float]
type Corr2ptMap = Mapping[QubitPair, float]

type BitstringMap = Mapping[str, int]

type Metric = float
type MetricMap = Mapping[int, float]

type SystemSize = int
type SystemSizeSeq = Sequence[SystemSize]
